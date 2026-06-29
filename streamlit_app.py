# =========================================================
# RANDOM V10
# Evolutionary Architecture Intelligence System
# + Constraint-Based Design Evolution
# + Procedural 2D Floor Plans
# + 3D Massing Model
# + Weighted AI Review + Materials + Sustainability
# Single-File Streamlit Edition
# =========================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V10",
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
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return DEFAULT.copy()
    return DEFAULT.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(st.session_state.memory, f, indent=2)
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
# ARCHITECTURE TYPES
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
# BASE DESIGN (INTENT-AWARE)
# =========================================================

def base_design(btype, bedrooms, budget_level):
    base_cost = {
        "low": (200000, 800000),
        "mid": (800000, 1500000),
        "high": (1500000, 3000000)
    }[budget_level]

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
        "cost": random.randint(*base_cost),
        "intent": budget_level
    }

# =========================================================
# MUTATION ENGINE 🧬 (CONTROLLED)
# =========================================================

def clamp(v, a, b):
    return max(a, min(b, v))

def mutate(d):
    d = json.loads(json.dumps(d))

    strength = 1.0 if d["intent"] == "high" else 0.7 if d["intent"] == "mid" else 0.4

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
        d["cost"] + int(random.randint(-120000, 180000) * strength),
        100000, 5000000
    )

    return d

# =========================================================
# FITNESS ENGINE (WEIGHTED INTELLIGENCE)
# =========================================================

def fitness(d):
    structure_score = max(0, 100 - abs(d["structure"]["columns"] - 20))

    cost_target = {
        "low": 600000,
        "mid": 1200000,
        "high": 2200000
    }[d["intent"]]

    cost_score = max(0, 100 - abs(d["cost"] - cost_target) / 20000)

    complexity_score = min(100, len(d["rooms"]) * 12)

    return {
        "structure": structure_score,
        "cost": cost_score,
        "complexity": complexity_score
    }

def score(f):
    return round(
        f["structure"] * 0.4 +
        f["cost"] * 0.4 +
        f["complexity"] * 0.2
    )

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
# FLOOR PLAN ENGINE 🏠 (IMPROVED LAYOUT LOGIC)
# =========================================================

def floor_plan(d):
    rooms = [
        {"name": "Living", "x": 0, "y": 0, "w": 6, "h": 5},
        {"name": "Kitchen", "x": 6, "y": 0, "w": 4, "h": 4},
        {"name": "Bath", "x": 6, "y": 4, "w": 2, "h": 2}
    ]

    spacing_x = 4
    x = 0

    for i in range(d["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "x": x,
            "y": 6,
            "w": 4,
            "h": 4
        })
        x += spacing_x

    return rooms

# =========================================================
# VISUALIZATION
# =========================================================

def draw_2d(plan):
    fig, ax = plt.subplots()

    for r in plan:
        ax.add_patch(plt.Rectangle(
            (r["x"], r["y"]),
            r["w"], r["h"],
            fill=False
        ))
        ax.text(r["x"] + 0.5, r["y"] + 0.5, r["name"], fontsize=8)

    ax.set_xlim(0, 18)
    ax.set_ylim(0, 16)
    ax.set_title("2D Floor Plan")

    st.pyplot(fig)

def draw_3d(plan):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for r in plan:
        ax.bar3d(r["x"], r["y"], 0, r["w"], r["h"], 3)

    ax.set_title("3D Massing Model")

    st.pyplot(fig)

# =========================================================
# AI REVIEW ENGINE 🤖 (WEIGHTED INSIGHT)
# =========================================================

def review(d):
    notes = []

    if d["bedrooms"] >= 4:
        notes.append("High occupancy residential suitability")

    if d["cost"] > 2000000:
        notes.append("Premium cost envelope detected")

    if d["structure"]["columns"] < 15:
        notes.append("Structural reinforcement recommended")

    if len(d["rooms"]) > 8:
        notes.append("High spatial complexity")

    if not notes:
        notes.append("Balanced optimized design")

    return notes

# =========================================================
# MATERIALS + SUSTAINABILITY
# =========================================================

def materials(d):
    return {
        "Concrete (m³)": d["structure"]["columns"] * 2.2,
        "Steel (tons)": d["structure"]["beams"] * 0.55,
        "Bricks": len(d["rooms"]) * 1800
    }

def sustainability(d):
    return clamp(100 - d["structure"]["columns"], 40, 100)

# =========================================================
# UI
# =========================================================

st.sidebar.title("🧬 RANDOM V10")
page = st.sidebar.radio("Navigation", ["Dashboard", "Evolution", "Memory"])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🧬 RANDOM V10 Core")

    c1, c2, c3 = st.columns(3)

    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Evolution Runs", len(mem["evolution"]))

# =========================================================
# EVOLUTION
# =========================================================

elif page == "Evolution":

    st.title("🧬 Evolution Engine V10")

    btype = st.selectbox("Type", sum(ARCH.values(), []))
    bedrooms = st.slider("Bedrooms", 1, 10, 3)
    gens = st.slider("Generations", 1, 8, 4)
    pop = st.slider("Population", 3, 12, 6)
    budget = st.selectbox("Budget", ["low", "mid", "high"])

    if st.button("Run Evolution"):

        best, history = evolve(btype, bedrooms, gens, pop, budget)

        plan = floor_plan(best)
        best["plan"] = plan

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:8],
            "best": best,
            "history": history,
            "time": datetime.now().isoformat()
        })

        save_memory()
        log("Evolution run completed")

        st.success("Evolution Complete")

        st.subheader("Best Design")
        st.json(best)

        st.subheader("Evolution Curve")
        st.line_chart(history)

        st.subheader("AI Review")
        for r in review(best):
            st.write("✔", r)

        st.subheader("Sustainability")
        st.metric("Score", sustainability(best))

        st.subheader("Materials Estimate")
        st.json(materials(best))

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