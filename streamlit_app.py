# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# V27 — Neural Architecture Simulation OS
# Evolutionary + Council + Neural Spatial Intelligence Layer
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
    page_title="Neural Architecture OS V27",
    page_icon="🧠",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLE LAYER
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.03em;
}

.card {
    background: #0b1220;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY ENGINE
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
# CORE DESIGN ENGINE
# =========================================================

def generate_design(goal):
    return {
        "id": str(uuid.uuid4())[:8],
        "goal": goal,
        "area": random.randint(120, 900),
        "cost": random.randint(80_000, 1_000_000),
        "structure": {
            "columns": random.randint(12, 55),
            "beams": random.randint(20, 100)
        },
        "rooms": ["Living", "Kitchen", "Bath"] + ["Room"] * random.randint(2, 6)
    }

# =========================================================
# COUNCIL ENGINE
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
    votes = []
    log = []

    for agent in COUNCIL:
        score = random.randint(60, 99)
        votes.append(score)

        log.append({
            "agent": agent,
            "vote": score,
            "statement": f"{agent} evaluates architectural feasibility of '{goal}'"
        })

    return log, sum(votes) / len(votes)

# =========================================================
# NEURAL ENGINE
# =========================================================

def encode(d):
    return [
        d["area"] / 1000,
        d["structure"]["columns"] / 50,
        d["structure"]["beams"] / 100,
        len(d["rooms"]) / 10,
        d["cost"] / 1_000_000
    ]

def neural_score(d):
    v = encode(d)
    raw = v[0]*0.25 + v[1]*0.2 + v[2]*0.2 + v[3]*0.2 + (1 - min(v[4], 1)) * 0.15
    return round(100 / (1 + math.exp(-5 * (raw - 0.5))), 2)

def mood(d):
    density = d["structure"]["columns"] / max(1, d["area"] / 60)
    flow = len(d["rooms"]) / max(1, d["structure"]["columns"])

    return {
        "comfort": round(100 - abs(density - 0.8) * 60, 2),
        "flow": round(100 - abs(flow - 0.6) * 70, 2)
    }

def neural_simulation(d, ticks=8):
    history = []
    sim = json.loads(json.dumps(d))

    for t in range(ticks):
        if random.random() > 0.5:
            sim["structure"]["columns"] += random.randint(-1, 2)
            sim["structure"]["beams"] += random.randint(-2, 3)

        history.append({
            "tick": t,
            "score": neural_score(sim),
            "mood": mood(sim)
        })

    return history

# =========================================================
# FLOOR PLAN ENGINE
# =========================================================

def floor_plan(d):
    return [{"room": r, "size": random.randint(20, 70)} for r in d["rooms"]]

# =========================================================
# SIDEBAR
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

goal = st.sidebar.text_input("Design Goal", "Eco smart vertical villa")

run = st.sidebar.button("Generate Architecture")

# =========================================================
# GENERATE
# =========================================================

if run:
    design = generate_design(goal)

    debate, score = council_debate(goal)
    design["council_score"] = score

    mem["designs"].append(design)
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": f"Generated {design['id']} | Council Score {score:.1f}"
    })

    st.session_state.active = design
    st.session_state.debate = debate

    save_memory()

design = st.session_state.get("active", None)

# =========================================================
# PAGE: PROJECT OVERVIEW
# =========================================================

if page == "🏠 Project Overview":
    st.title("🏠 Project Overview")

    if design:
        st.markdown(f"### Design ID: {design['id']}")
        st.write(design)
        st.metric("Council Score", f"{design['council_score']:.1f}")
        st.metric("Neural Score", neural_score(design))
    else:
        st.info("Generate a design to begin simulation.")

# =========================================================
# PAGE: FLOOR PLAN
# =========================================================

elif page == "📐 Floor Plan":
    st.title("📐 Floor Plan")

    if design:
        st.json(floor_plan(design))

# =========================================================
# STRUCTURAL MODEL
# =========================================================

elif page == "🏗 Structural Model":
    st.title("🏗 Structural Model")

    if design:
        st.json(design["structure"])

# =========================================================
# COST
# =========================================================

elif page == "💰 Cost Estimate":
    st.title("💰 Cost Estimate")

    if design:
        st.metric("Total Cost", f"${design['cost']:,}")
        st.metric("Cost per m²", f"${design['cost']/design['area']:.2f}")

# =========================================================
# SUSTAINABILITY
# =========================================================

elif page == "🌍 Sustainability":
    st.title("🌍 Sustainability Layer")

    if design:
        score = max(0, 100 - design["structure"]["columns"] * 1.1)
        st.metric("Sustainability Score", f"{score:.1f}/100")

# =========================================================
# COMPLIANCE
# =========================================================

elif page == "📋 Code Compliance":
    st.title("📋 Code Compliance Engine")

    if design:
        ok = design["structure"]["columns"] > 15 and design["structure"]["beams"] > 25
        if ok:
            st.success("Design passes structural compliance thresholds")
        else:
            st.warning("Design requires structural optimization review")

# =========================================================
# AI EVOLUTION
# =========================================================

elif page == "📊 AI Evolution":
    st.title("📊 Neural Evolution Simulation")

    if design:
        history = neural_simulation(design)

        st.line_chart([h["score"] for h in history])
        st.json(history[-1]["mood"])

# =========================================================
# MEMORY
# =========================================================

elif page == "🧠 Memory":
    st.title("🧠 System Memory")

    st.json(mem)

# =========================================================
# SETTINGS
# =========================================================

elif page == "⚙ Settings":
    st.title("⚙ System Settings")

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active = None
        save_memory()
        st.success("Memory reset complete")
        st.rerun()