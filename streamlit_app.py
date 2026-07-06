# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# V27 — Neural Architecture Simulation Layer
# Evolutionary + Council + Neural Spatial Intelligence OS
# Extended Module Navigation Edition
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
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": [],
    "plugins": [],
    "analytics": []
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
# CORE ENGINE
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
    debate = []

    for agent in COUNCIL:
        score = random.randint(60, 98)
        votes.append(score)
        debate.append({"agent": agent, "vote": score})

    return debate, sum(votes)/len(votes)

# =========================================================
# NEURAL MODEL
# =========================================================

def neural_score(d):
    v = [
        d["area"]/1000,
        d["structure"]["columns"]/50,
        d["structure"]["beams"]/100,
        len(d["rooms"])/10,
        d["cost"]/1_000_000
    ]
    raw = sum(v)
    return 100/(1+math.exp(-5*(raw-0.5)))

# =========================================================
# FLOOR SYSTEM
# =========================================================

def floor_plan(d):
    return [{"room": r, "size": random.randint(20, 60)} for r in d["rooms"]]

# =========================================================
# SIDEBAR NAVIGATION (EXPANDED MODULES)
# =========================================================

st.sidebar.title("🧠 Neural Architecture OS")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📂 Projects",
        "📐 Design Studio",
        "🧠 AI Architect",
        "🏗 Structural Analysis",
        "💰 Cost Estimation",
        "🌱 Sustainability",
        "📋 Code Compliance",
        "🏢 BIM Manager",
        "📊 Analytics",
        "🧠 Memory",
        "🔌 Plugins",
        "⚙ Settings"
    ]
)

goal = st.sidebar.text_input("Design Goal", "Futuristic eco villa")

run = st.sidebar.button("Generate Architecture")

# =========================================================
# GENERATION TRIGGER
# =========================================================

if run:
    design = generate_design(goal)
    debate, score = council_debate(goal)

    design["council_score"] = score
    design["neural_score"] = neural_score(design)

    mem["designs"].append(design)
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": f"Generated {design['id']} score {score:.1f}"
    })

    st.session_state.active = design
    st.session_state.debate = debate
    save_memory()

design = st.session_state.get("active", None)

# =========================================================
# MODULE PAGES
# =========================================================

if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.write("Neural architecture system active.")

    st.metric("Designs", len(mem["designs"]))
    st.metric("Evolution Logs", len(mem["logs"]))

# ----------------------------

elif page == "📂 Projects":
    st.title("📂 Projects")

    st.json(mem["designs"])

# ----------------------------

elif page == "📐 Design Studio":
    st.title("📐 Design Studio")

    if design:
        st.json(design)
    else:
        st.info("Generate a design first.")

# ----------------------------

elif page == "🧠 AI Architect":
    st.title("🧠 AI Architect (Council View)")

    if st.session_state.get("debate"):
        st.json(st.session_state.debate)

# ----------------------------

elif page == "🏗 Structural Analysis":
    st.title("🏗 Structural Analysis")

    if design:
        st.json(design["structure"])

# ----------------------------

elif page == "💰 Cost Estimation":
    st.title("💰 Cost Estimation")

    if design:
        st.metric("Cost", f"${design['cost']:,}")

# ----------------------------

elif page == "🌱 Sustainability":
    st.title("🌱 Sustainability")

    if design:
        score = max(0, 100 - design["structure"]["columns"] * 1.1)
        st.metric("Sustainability Score", f"{score:.1f}/100")

# ----------------------------

elif page == "📋 Code Compliance":
    st.title("📋 Code Compliance")

    st.success("Simulated compliance check passed.")

# ----------------------------

elif page == "🏢 BIM Manager":
    st.title("🏢 BIM Manager")

    st.info("Future BIM integration layer (placeholder module)")

# ----------------------------

elif page == "📊 Analytics":
    st.title("📊 Analytics")

    st.json({
        "avg_columns": sum(d["structure"]["columns"] for d in mem["designs"]) / max(1, len(mem["designs"])),
        "avg_cost": sum(d["cost"] for d in mem["designs"]) / max(1, len(mem["designs"]))
    })

# ----------------------------

elif page == "🧠 Memory":
    st.title("🧠 Memory")

    st.json(mem)

# ----------------------------

elif page == "🔌 Plugins":
    st.title("🔌 Plugins")

    st.info("Plugin registry system ready for extension.")
    st.json(mem.get("plugins", []))

# ----------------------------

elif page == "⚙ Settings":
    st.title("⚙ Settings")

    if st.button("Reset System"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active = None
        save_memory()
        st.success("System reset complete")
        st.rerun()