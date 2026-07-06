# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE + V23 COUNCIL CORE
# Evolutionary Spatial Layout + AI Debate System
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
    page_title="Random Studio Engine V23",
    page_icon="🏛️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>
    html, body {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .arc-room-module {
        padding: 16px;
        border-radius: 12px;
        background: #111827;
        color: white;
        margin: 6px;
    }

    .arc-blueprint-canvas {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        background: #0b1220;
        padding: 20px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": [],
    "debates": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    MEMORY_FILE.write_text(json.dumps(st.session_state.memory, indent=2))

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# init
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

# =========================================================
# ARCH ENGINE
# =========================================================

ARCH_DOMAINS = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"]
}

def generate_base_design(goal):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "goal": goal,
        "area": random.randint(120, 600),
        "cost": random.randint(100000, 900000),
        "rooms": ["Living", "Kitchen"] + ["Room"] * random.randint(2, 5),
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(20, 80)
        }
    }

# =========================================================
# 🏛️ V23 COUNCIL SYSTEM (CORE ADDITION)
# =========================================================

COUNCIL = [
    "🏗 Architect",
    "🧠 Structural",
    "💰 Cost",
    "🌱 Sustainability",
    "📋 Compliance",
    "⚡ Chaos"
]

def agent_opinion(goal):
    return {
        "🏗 Architect": f"Spatial coherence strong for '{goal}'.",
        "🧠 Structural": "Check beam-column stability.",
        "💰 Cost": "Budget optimization needed.",
        "🌱 Sustainability": "Reduce carbon footprint materials.",
        "📋 Compliance": "Ensure regulation alignment.",
        "⚡ Chaos": "Introduce asymmetry for innovation."
    }

def vote():
    return random.randint(55, 99)

def run_council(goal):
    opinions = agent_opinion(goal)
    debate = []
    votes = []

    for agent in COUNCIL:
        v = vote()
        votes.append(v)

        debate.append({
            "agent": agent,
            "statement": opinions[agent],
            "vote": v
        })

    return debate, sum(votes) / len(votes)

# =========================================================
# DESIGN + EVOLUTION
# =========================================================

def evolve_design(goal):
    return generate_base_design(goal)

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏛️ V23 Engine")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Design Lab (Council)", "Memory"]
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏛️ Random Studio V23")

    c1, c2 = st.columns(2)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Debates", len(mem["debates"]))

    st.markdown("### Logs")
    for l in mem["logs"][-5:]:
        st.write(l["time"][11:19], "→", l["msg"])

# =========================================================
# 🧪 COUNCIL MODE
# =========================================================

elif page == "Design Lab (Council)":
    st.title("🏛️ AI Council Architecture Engine")

    goal = st.text_input("Architectural Goal", "Futuristic eco city tower")

    if st.button("Run Council Debate", use_container_width=True):

        debate, score = run_council(goal)

        st.markdown("## 🧠 Debate Log")

        for d in debate:
            st.write(f"**{d['agent']}** → {d['statement']} (Vote: {d['vote']})")

        st.success(f"Council Score: {score:.2f}")

        design = evolve_design(goal)
        design["council_score"] = score

        st.session_state.active_design = design

        mem["designs"].append(design)
        mem["debates"].append(debate)

        log_event(f"Council created design {design['id']}")

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.markdown("## 🏗 Final Design")

        st.metric("Score", d["council_score"])
        st.metric("Area", f"{d['area']} m²")
        st.metric("Cost", f"${d['cost']:,}")

        st.json(d["structure"])
        st.write(d["rooms"])

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 System Memory")

    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.rerun()