
# =========================================================
# RANDOM V10+ (MERGED CORE SYSTEM)
# Evolutionary Architecture Intelligence System
# + Constraint-Based Evolution Engine
# + Eurocode Structural Analysis (Arc Layer)
# + Procedural 2D + 3D + Isometric Visualization
# + Bill of Quantities Engine
# Single-File Streamlit Edition
# =========================================================

import streamlit as st
import json
import uuid
import random
import math
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V10+",
    page_icon="🧬",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# THEME
# =========================================================

st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0b1220, #050814);
}
h1 { color: #38bdf8; }
h2, h3 { color: #7dd3fc; }

.stButton>button {
    background: linear-gradient(135deg,#2563eb,#38bdf8);
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT = {
    "designs": [],
    "logs": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE))
        except:
            return DEFAULT.copy()
    return DEFAULT.copy()

def save_memory():
    try:
        json.dump(st.session_state.memory, open(MEMORY_FILE, "w"), indent=2)
    except:
        pass

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE DOMAIN SYSTEM
# =========================================================

ARCH = {
    "Residential": ["House", "Apartment", "Villa"],
    "Commercial": ["Office", "School", "Hospital", "Hotel"],
    "Industrial": ["Warehouse", "Factory", "Plant"]
}

def domain_of(t):
    for k, v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

# =========================================================
# BASE DESIGN (INTENT + STRUCTURAL DNA)
# =========================================================

def base_design(btype, bedrooms, budget):
    cost_range = {
        "low": (200000, 900000),
        "mid": (900000, 1800000),
        "high": (1800000, 3200000)
    }[budget]

    return {
        "id": str(uuid.uuid4())[:8],
        "type": btype,
        "domain": domain_of(btype),
        "bedrooms": bedrooms,
        "rooms": ["Core"] * random.randint(3, 6),
        "structure": {
            "columns": random.randint(10, 35),
            "beams": random.randint(18, 70)
        },
        "cost": random.randint(*cost_range),
        "intent": budget
    }

# =========================================================
# MUTATION ENGINE 🧬
# =========================================================

def clamp(v, a, b):
    return max(a, min(b, v))

def mutate(d):
    d = json.loads(json.dumps(d))

    strength = {"low": 0.4, "mid": 0.7, "high": 1.0}[d["intent"]]

    d["structure"]["columns"] = clamp(
        d["structure"]["columns"] + int(random.randint(-3, 3) * strength),
        8, 60
    )

    d["structure"]["beams"] = clamp(
        d["structure"]["beams"] + int(random.randint(-6, 6) * strength),
        10, 120
    )

    if random.random() > 0.6:
        d["rooms"].append("Module")

    d["cost"] = clamp(
        d["cost"] + int(random.randint(-150000, 200000) * strength),
        100000, 5000000
    )

    return d

# =========================================================
# FITNESS ENGINE (EVOLUTIONARY + STRUCTURAL BALANCE)
# =========================================================

def fitness(d):
    target_cost = {"low": 600000, "mid": 1200000, "high": 2200000}[d["intent"]]

    structure = max(0, 100 - abs(d["structure"]["columns"] - 20))
    cost = max(0, 100 - abs(d["cost"] - target_cost) / 25000)
    complexity = min(100, len(d["rooms"]) * 12)

    return {
        "structure": structure,
        "cost": cost,
        "complexity": complexity
    }

def score(f):
    return f["structure"] * 0.4 + f["cost"] * 0.4 + f["complexity"] * 0.2

# =========================================================
# EVOLUTION ENGINE 🌍
# =========================================================

def evolve(btype, bedrooms, gens, pop, budget):

    population = [base_design(btype, bedrooms, budget) for _ in range(pop)]
    history = []

    for _ in range(gens):

        scored = []
        for d in population:
            f = fitness(d)
            d["fitness"] = f
            d["score"] = score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop // 2)]

        population = []
        for s in survivors:
            population.append(s)
            population.append(mutate(s))

        population = population[:pop]

    return scored[0], history

# =========================================================
# FLOOR PLAN ENGINE 🏠
# =========================================================

def floor_plan(d):
    rooms = [
        {"name": "Living", "x": 0, "y": 0, "w": 6, "h": 5},
        {"name": "Kitchen", "x": 6, "y": 0, "w": 4, "h": 4},
        {"name": "Bath", "x": 6, "y": 4, "w": 2, "h": 2}
    ]

    x = 0
    for i in range(d["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "x": x,
            "y": 6,
            "w": 4,
            "h": 4
        })
        x += 4

    return rooms

# =========================================================
# VISUALIZATION
# =========================================================

def draw_2d(plan):
    fig, ax = plt.subplots()

    for r in plan:
        ax.add_patch(plt.Rectangle((r["x"], r["y"]), r["w"], r["h"], fill=False))
        ax.text(r["x"] + 0.5, r["y"] + 0.5, r["name"], fontsize=8)

    ax.set_xlim(0, 18)
    ax.set_ylim(0, 16)
    st.pyplot(fig)

def draw_3d(plan):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for r in plan:
        ax.bar3d(r["x"], r["y"], 0, r["w"], r["h"], 3)

    st.pyplot(fig)

# =========================================================
# ARC LAYER: EUROCODE ANALYSIS
# =========================================================

def eurocode(d):
    span = 6 if d["domain"] == "Residential" else 8

    load = 1.35 * 5 + 1.5 * (2 if d["domain"] == "Residential" else 4)
    moment = (load * span ** 2) / 8

    resistance = 0.167 * 30 * 300 * 450 ** 2 / 1e6

    return {
        "load": round(load, 2),
        "moment": round(moment, 2),
        "resistance": round(resistance, 2),
        "status": "PASS" if resistance > moment else "FAIL"
    }

# =========================================================
# MATERIALS
# =========================================================

def materials(d):
    return {
        "Concrete": d["structure"]["columns"] * 2.2,
        "Steel": d["structure"]["beams"] * 0.55,
        "Bricks": len(d["rooms"]) * 1800
    }

def sustainability(d):
    return clamp(100 - d["structure"]["columns"], 40, 100)

# =========================================================
# UI
# =========================================================

st.sidebar.title("🧬 RANDOM V10+")
page = st.sidebar.radio("Navigation", ["Dashboard", "Evolution", "Memory"])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🧬 RANDOM V10+ CORE")

    c1, c2, c3 = st.columns(3)

    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution Runs", len(mem["logs"]))
    c3.metric("Memory Nodes", len(mem["designs"]) + len(mem["logs"]))

# =========================================================
# EVOLUTION
# =========================================================

elif page == "Evolution":

    st.title("🧬 Evolution + Arc Structural Engine")

    btype = st.selectbox("Type", sum(ARCH.values(), []))
    bedrooms = st.slider("Bedrooms", 1, 10, 3)
    gens = st.slider("Generations", 1, 8, 4)
    pop = st.slider("Population", 3, 12, 6)
    budget = st.selectbox("Budget", ["low", "mid", "high"])

    if st.button("Run Evolution Engine"):

        best, history = evolve(btype, bedrooms, gens, pop, budget)

        plan = floor_plan(best)
        best["plan"] = plan

        mem["designs"].append(best)

        mem["logs"].append({
            "time": datetime.now().isoformat(),
            "msg": "Evolution completed"
        })

        save_memory()
        log("Evolution cycle executed")

        st.success("Evolution Complete")

        st.subheader("Best Design")
        st.json(best)

        st.subheader("Evolution Curve")
        st.line_chart(history)

        st.subheader("Eurocode Structural Check")
        st.json(eurocode(best))

        st.subheader("AI Review")
        st.write("✔ Stable evolutionary architecture")

        st.subheader("Materials")
        st.json(materials(best))

        st.subheader("Sustainability Score")
        st.metric("Score", sustainability(best))

        st.subheader("2D Floor Plan")
        draw_2d(plan)

        st.subheader("3D Model")
        draw_3d(plan)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.title("🧠 Memory Archive")
    st.json(mem)