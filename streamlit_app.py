# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# V27 — Neural Architecture Simulation Layer
# Evolutionary + Council + Neural Spatial Intelligence OS
# =========================================================

import streamlit as st
import json
import uuid
import random
import math
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random Neural Architecture OS",
    page_icon="🧠",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# UI STYLE
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.03em;
}

.arc-card {
    padding: 16px;
    border-radius: 12px;
    background: #0b1220;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "logs": [],
    "evolution": [],
    "debates": []
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

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory

# =========================================================
# CORE GENERATION ENGINE
# =========================================================

def generate_design(goal):
    return {
        "id": str(uuid.uuid4())[:8],
        "goal": goal,
        "area": random.randint(120, 800),
        "cost": random.randint(80_000, 900_000),
        "structure": {
            "columns": random.randint(12, 50),
            "beams": random.randint(20, 90)
        },
        "rooms": ["Living", "Kitchen", "Bath"] + ["Room"] * random.randint(2, 6)
    }

# =========================================================
# COUNCIL ENGINE (V23)
# =========================================================

COUNCIL = [
    "Chief Architect",
    "Structural Analyst",
    "Cost Engineer",
    "Sustainability Agent",
    "Compliance Officer",
    "Chaos Agent"
]

def council_debate(goal):
    debate = []
    votes = []

    for agent in COUNCIL:
        score = random.randint(60, 98)
        votes.append(score)

        debate.append({
            "agent": agent,
            "statement": f"{agent} evaluates '{goal}' with systemic bias.",
            "vote": score
        })

    return debate, sum(votes)/len(votes)

# =========================================================
# NEURAL ARCHITECTURE MODEL (V27)
# =========================================================

def encode(d):
    return [
        d["area"]/1000,
        d["structure"]["columns"]/50,
        d["structure"]["beams"]/100,
        len(d["rooms"])/10,
        d["cost"]/1_000_000
    ]

def mood(d):
    density = d["structure"]["columns"] / max(1, d["area"]/50)
    flow = len(d["rooms"]) / max(1, d["structure"]["columns"])

    return {
        "comfort": round(100 - abs(density-0.8)*60, 2),
        "flow": round(100 - abs(flow-0.6)*70, 2)
    }

def neural_score(d):
    v = encode(d)
    raw = v[0]*0.25 + v[1]*0.2 + v[2]*0.15 + v[3]*0.2 + (1-min(v[4],1))*0.2
    return 100/(1+math.exp(-5*(raw-0.5)))

def neural_simulation(d, ticks=5):
    history = []
    current = json.loads(json.dumps(d))

    for t in range(ticks):
        if random.random() > 0.6:
            current["structure"]["columns"] += random.randint(-1, 2)
            current["structure"]["beams"] += random.randint(-2, 3)

        score = neural_score(current)
        history.append({
            "tick": t,
            "score": score,
            "mood": mood(current)
        })

    return history

# =========================================================
# FLOOR PLAN VIEW (SIMPLIFIED)
# =========================================================

def floor_plan(d):
    return [{"room": r, "size": random.randint(20, 60)} for r in d["rooms"]]

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🧠 Neural Architecture OS")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Project Overview",
        "📐 Floor Plan",
        "🏗 Structural Model",
        "💰 Cost Estimate",
        "🌍 Sustainability",
        "📋 Code Compliance",
        "📊 AI Evolution",
        "🧠 Memory",
        "⚙ Settings"
    ]
)

goal = st.sidebar.text_input("Design Goal", "Futuristic eco villa")

run = st.sidebar.button("Generate Architecture")

# =========================================================
# GENERATE DESIGN
# =========================================================

if run:
    design = generate_design(goal)

    debate, score = council_debate(goal)
    design["council_score"] = score

    mem["designs"].append(design)
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": f"Generated {design['id']} with council score {score:.1f}"
    })

    st.session_state.active = design
    st.session_state.debate = debate

    save_memory()

# =========================================================
# ACTIVE DESIGN
# =========================================================

design = st.session_state.get("active", None)

# =========================================================
# PAGES
# =========================================================

if page == "🏠 Project Overview":
    st.title("🏠 Project Overview")

    if design:
        st.markdown(f"### ID: {design['id']}")
        st.write(design)
    else:
        st.info("Generate a design to begin.")

# ----------------------------

elif page == "📐 Floor Plan":
    st.title("📐 Floor Plan")

    if design:
        st.json(floor_plan(design))

# ----------------------------

elif page == "🏗 Structural Model":
    st.title("🏗 Structural Model")

    if design:
        st.json(design["structure"])

# ----------------------------

elif page == "💰 Cost Estimate":
    st.title("💰 Cost Estimate")

    if design:
        st.metric("Total Cost", f"${design['cost']:,}")

# ----------------------------

elif page == "🌍 Sustainability":
    st.title("🌍 Sustainability")

    if design:
        score = max(0, 100 - design["structure"]["columns"]*1.2)
        st.metric("Sustainability Score", f"{score:.1f}/100")

# ----------------------------

elif page == "📋 Code Compliance":
    st.title("📋 Code Compliance")

    if design:
        st.success("Structural and zoning constraints passed (simulated)")

# ----------------------------

elif page == "📊 AI Evolution":
    st.title("📊 AI Evolution")

    if design:
        history = neural_simulation(design, 8)

        st.line_chart([h["score"] for h in history])

        st.markdown("### Mood Field")
        st.json(history[-1]["mood"])

# ----------------------------

elif page == "🧠 Memory":
    st.title("🧠 Memory")

    st.json(mem)

# ----------------------------

elif page == "⚙ Settings":
    st.title("⚙ Settings")

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active = None
        save_memory()
        st.success("Reset complete")