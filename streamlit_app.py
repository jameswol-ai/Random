# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# V14 — ARC STUDIO SIMULATION CORE
# Multi-Agent Evolution + Structural Intelligence Layer
# =========================================================

import streamlit as st
import json
import uuid
import random
import copy
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Arc Studio V14",
    page_icon="🏗",
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

.arc-card {
    background: #0b1220;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 14px;
    border-radius: 14px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "logs": [],
    "sessions": [],
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
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except:
        pass

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# =========================================================
# INIT
# =========================================================

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if "history" not in st.session_state:
    st.session_state.history = []

mem = st.session_state.memory

# =========================================================
# CORE ENGINE
# =========================================================

def planner(goal):
    area = random.randint(150, 1000)

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "goal": goal,
        "area": area,
        "cost": area * random.randint(900, 2500),
        "structure": {
            "columns": random.randint(10, 60),
            "beams": random.randint(20, 120)
        },
        "rooms": ["Living", "Kitchen", "Bath"] + ["Module"] * random.randint(2, 7)
    }

def critic(d):
    issues = []

    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    cost_per_m2 = d["cost"] / max(1, d["area"])

    if ratio < 1.6:
        issues.append("Weak structural beam-column ratio")

    if cost_per_m2 > 2100:
        issues.append("High cost efficiency risk")

    if len(d["rooms"]) < 5:
        issues.append("Low spatial complexity")

    return issues

def mutator(d):
    d = copy.deepcopy(d)

    d["structure"]["columns"] += random.randint(-3, 4)
    d["structure"]["beams"] += random.randint(-5, 6)

    if random.random() > 0.6:
        d["rooms"].append("Adaptive Spatial Pod")
        d["area"] += 20

    d["cost"] = int(d["area"] * random.randint(900, 2500))

    return d

def scorer(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    cost_pressure = d["cost"] / max(1, d["area"])

    return (
        d["area"] * 0.15 +
        d["structure"]["columns"] * 1.5 +
        d["structure"]["beams"] * 1.3 -
        cost_pressure * 0.9 -
        abs(ratio - 2.0) * 20
    )

# =========================================================
# MULTI-AGENT EVOLUTION LOOP
# =========================================================

def evolve(goal, generations=6, pop_size=8):
    population = [planner(goal) for _ in range(pop_size)]
    history = []

    for _ in range(generations):

        evaluated = []
        for d in population:
            d = mutator(d)
            d["issues"] = critic(d)
            d["score"] = scorer(d)
            evaluated.append(d)

        evaluated.sort(key=lambda x: x["score"], reverse=True)

        best = evaluated[0]
        history.append(best["score"])

        survivors = evaluated[:max(2, pop_size // 2)]

        new_population = []
        for s in survivors:
            new_population.append(s)
            new_population.append(mutator(s))

        population = new_population[:pop_size]

    return best, history

# =========================================================
# FLOOR PLAN
# =========================================================

def floor_plan(d):
    return [
        {"room": r, "area": random.randint(25, 95)}
        for r in d["rooms"]
    ]

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏗 Arc Studio V14")

page = st.sidebar.radio(
    "Workspace",
    ["Dashboard", "Design Lab", "AI Architect", "Analytics", "Memory"]
)

goal = st.sidebar.text_input("Design Goal", "Eco Smart Tower")
run = st.sidebar.button("Run Evolution Engine")

# =========================================================
# EXECUTION
# =========================================================

if run:
    best, hist = evolve(goal)

    best["plan"] = floor_plan(best)

    mem["designs"].append(best)
    st.session_state.active_design = best
    st.session_state.history = hist

    mem["sessions"].append({
        "id": str(uuid.uuid4())[:6],
        "goal": goal,
        "time": datetime.now().isoformat()
    })

    log(f"Generated design {best['id']}")

# =========================================================
# ACTIVE DESIGN
# =========================================================

d = st.session_state.active_design

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏗 Arc Studio V14 Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Sessions", len(mem["sessions"]))
    c3.metric("Logs", len(mem["logs"]))

    st.markdown("### System Activity Log")
    for l in mem["logs"][-6:]:
        st.write(l)

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "Design Lab":
    st.title("📐 Design Lab")

    if d:
        st.subheader(f"Design {d['id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Area", f"{d['area']} m²")
        c2.metric("Cost", f"${d['cost']:,}")
        c3.metric("Score", round(d["score"], 2))

        st.markdown("### AI Critic Findings")
        st.write(d["issues"])

        st.markdown("### Structure")
        st.json(d["structure"])

        st.markdown("### Floor Plan")
        st.json(d["plan"])

        st.markdown("### Evolution Curve")
        st.line_chart(st.session_state.history)

    else:
        st.info("Run the evolution engine to generate a design.")

# =========================================================
# AI ARCHITECT
# =========================================================

elif page == "AI Architect":
    st.title("🧠 AI Architect Layer")

    if d:
        st.json({
            "structural_ratio": d["structure"]["beams"] / max(1, d["structure"]["columns"]),
            "complexity": len(d["rooms"]) * 10,
            "cost_pressure": d["cost"] / max(1, d["area"])
        })

# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":
    st.title("📊 Evolution Analytics")

    if d:
        st.line_chart([random.randint(60, 100) for _ in range(15)])

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Arc Memory Core")

    st.json(mem)

    if st.button("Reset System"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        st.session_state.history = []
        save_memory()
        st.rerun()
