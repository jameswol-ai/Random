# =========================================================
# RANDOM V24
# Architecture Intelligence OS (Multi-Domain Studio Engine)
# =========================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random Studio Engine V24",
    page_icon="🏛️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1,h2,h3 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.03em;
}

.arc {
    background: #0b1020;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #243042;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "logs": [],
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.memory, f, indent=2)

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active" not in st.session_state:
    st.session_state.active = None

if "trend" not in st.session_state:
    st.session_state.trend = []

mem = st.session_state.memory

# =========================================================
# ENGINE CORE
# =========================================================

def generate_design(goal):
    return {
        "id": str(uuid.uuid4())[:8],
        "goal": goal,
        "area": random.randint(120, 800),
        "cost": random.randint(120000, 900000),
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(25, 90)
        },
        "rooms": ["Living", "Kitchen", "Bath"] + ["Room"] * random.randint(2, 6)
    }

def fitness(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    structural = max(0, 100 - int(abs(ratio - 2.0) * 20))
    cost_eff = max(0, 100 - int(d["cost"] / max(1, d["area"]) / 25))
    complexity = min(100, len(d["rooms"]) * 10)

    return {
        "structural": structural,
        "cost": cost_eff,
        "complexity": complexity
    }

def aggregate(f):
    return int(sum(f.values()) / len(f))

# =========================================================
# EXTRA SYSTEMS (V24)
# =========================================================

def sustainability_score(d):
    efficiency = d["area"] / max(1, d["structure"]["columns"])
    carbon_proxy = 100 - min(100, efficiency * 2)
    return max(0, int(carbon_proxy))

def compliance_score(d):
    score = 100
    if d["structure"]["columns"] < 14:
        score -= 20
    if d["structure"]["beams"] < 30:
        score -= 15
    if len(d["rooms"]) < 4:
        score -= 10
    return max(0, score)

def cost_breakdown(d):
    base = d["cost"]
    return {
        "Structural": int(base * 0.45),
        "Finishes": int(base * 0.25),
        "Systems": int(base * 0.20),
        "Contingency": int(base * 0.10)
    }

# =========================================================
# EVOLUTION
# =========================================================

def evolve(goal, gens=6):
    pop = [generate_design(goal) for _ in range(10)]
    history = []

    for _ in range(gens):
        scored = []
        for d in pop:
            f = fitness(d)
            d["score"] = aggregate(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:5]
        pop = survivors + [generate_design(goal) for _ in range(5)]

    return scored[0], history

# =========================================================
# FLOOR PLAN
# =========================================================

def floor_plan(d):
    rooms = [{"name":"Living","w":6,"h":5,"c":"#1e3a8a"},
             {"name":"Kitchen","w":4,"h":4,"c":"#065f46"}]

    for i in range(random.randint(2,5)):
        rooms.append({
            "name": f"Room {i+1}",
            "w":4,"h":4,
            "c":"#4c1d95"
        })
    return rooms

def render_plan(plan):
    html = '<div class="arc">'
    for r in plan:
        html += f"<div style='margin:6px;padding:10px;background:{r['c']};color:white;border-radius:8px'>{r['name']} {r['w']}x{r['h']}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏛 V24 Studio")

goal = st.sidebar.text_input("Design Goal", "Eco smart villa")
gens = st.sidebar.slider("Evolution Cycles", 2, 15, 6)

page = st.sidebar.radio("Navigation", [
    "🏠 Project Overview",
    "📐 Floor Plan",
    "🏗 Structural Model",
    "💰 Cost Estimate",
    "🌍 Sustainability",
    "📋 Code Compliance",
    "📊 AI Evolution",
    "🧠 Memory",
    "⚙ Settings"
])

if st.sidebar.button("🚀 Run Generation"):
    best, trend = evolve(goal, gens)
    best["plan"] = floor_plan(best)

    st.session_state.active = best
    st.session_state.trend = trend

    mem["designs"].append(best)
    mem["evolution"].append({
        "id": str(uuid.uuid4())[:6],
        "best": best["id"],
        "score": best["score"]
    })

    log(f"Generated {best['id']}")

# =========================================================
# PAGES
# =========================================================

d = st.session_state.active

# -------------------------
if page == "🏠 Project Overview":
    st.title("🏠 Project Overview")

    st.metric("Active Designs", len(mem["designs"]))

    if d:
        st.success(f"Active Design: {d['id']}")
        st.write("Goal:", d["goal"])
        st.metric("Score", d.get("score", 0))
    else:
        st.info("Run generation to begin.")

    st.write("Logs")
    for l in reversed(mem["logs"][-5:]):
        st.caption(l["msg"])

# -------------------------
elif page == "📐 Floor Plan":
    st.title("📐 Floor Plan")
    if d:
        render_plan(d["plan"])
    else:
        st.info("No design loaded.")

# -------------------------
elif page == "🏗 Structural Model":
    st.title("🏗 Structural Model")
    if d:
        st.json(d["structure"])
    else:
        st.info("No design loaded.")

# -------------------------
elif page == "💰 Cost Estimate":
    st.title("💰 Cost Estimate")
    if d:
        breakdown = cost_breakdown(d)
        st.json(breakdown)
    else:
        st.info("No design loaded.")

# -------------------------
elif page == "🌍 Sustainability":
    st.title("🌍 Sustainability")
    if d:
        st.metric("Green Score", sustainability_score(d))
    else:
        st.info("No design loaded.")

# -------------------------
elif page == "📋 Code Compliance":
    st.title("📋 Code Compliance")
    if d:
        st.metric("Compliance Score", compliance_score(d))
    else:
        st.info("No design loaded.")

# -------------------------
elif page == "📊 AI Evolution":
    st.title("📊 AI Evolution")
    if st.session_state.trend:
        st.line_chart(st.session_state.trend)
    else:
        st.info("No evolution data.")

# -------------------------
elif page == "🧠 Memory":
    st.title("🧠 Memory")
    st.json(mem)

# -------------------------
elif page == "⚙ Settings":
    st.title("⚙ Settings")
    st.write("Engine parameters are controlled in sidebar.")