# =========================================================
# RANDOM V9 (CLEAN MERGED BUILD)
# Evolutionary Architecture Intelligence System
# + Procedural 2D Floor Plans
# + 3D Massing Model
# + AI Design Review + Cost + Materials
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
    page_title="RANDOM V9",
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
# BASE DESIGN
# =========================================================

def base_design(btype, bedrooms):
    return {
        "id": str(uuid.uuid4())[:8],
        "type": btype,
        "domain": domain_of(btype),
        "bedrooms": bedrooms,
        "rooms": ["Core"] * random.randint(3, 7),
        "structure": {
            "columns": random.randint(12, 30),
            "beams": random.randint(20, 60)
        },
        "cost": random.randint(300000, 2500000)
    }

# =========================================================
# MUTATION ENGINE 🧬 (SAFE)
# =========================================================

def clamp(v, min_v, max_v):
    return max(min_v, min(max_v, v))

def mutate(d):
    d = json.loads(json.dumps(d))  # deep copy

    d["structure"]["columns"] = clamp(
        d["structure"]["columns"] + random.randint(-2, 3),
        8, 60
    )

    d["structure"]["beams"] = clamp(
        d["structure"]["beams"] + random.randint(-5, 5),
        10, 120
    )

    if random.random() > 0.5:
        d["rooms"].append("Module")

    d["cost"] = clamp(
        d["cost"] + random.randint(-100000, 200000),
        100000, 5000000
    )

    return d

# =========================================================
# FITNESS ENGINE
# =========================================================

def fitness(d):
    return {
        "structure": max(0, 100 - abs(d["structure"]["columns"] - 20)),
        "cost": max(0, 100 - (d["cost"] // 50000)),
        "complexity": min(100, len(d["rooms"]) * 10)
    }

def score(f):
    return int(sum(f.values()) / 3)

# =========================================================
# EVOLUTION ENGINE 🌍
# =========================================================

def evolve(btype, bedrooms, gens, pop):
    population = [base_design(btype, bedrooms) for _ in range(pop)]
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

        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate(s))

        population = new_pop[:pop]

    return scored[0], history, scored

# =========================================================
# FLOOR PLAN ENGINE 🏠
# =========================================================

def floor_plan(design):
    bedrooms = design["bedrooms"]

    rooms = [
        {"name": "Living", "x": 0, "y": 0, "w": 6, "h": 5},
        {"name": "Kitchen", "x": 6, "y": 0, "w": 4, "h": 4},
        {"name": "Bath", "x": 6, "y": 4, "w": 2, "h": 2}
    ]

    x = 0
    for i in range(bedrooms):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "x": x,
            "y": 5,
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
        rect = plt.Rectangle((r["x"], r["y"]), r["w"], r["h"], fill=False)
        ax.add_patch(rect)
        ax.text(r["x"] + 0.5, r["y"] + 0.5, r["name"], fontsize=8)

    ax.set_xlim(0, 16)
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
# AI REVIEW ENGINE 🤖
# =========================================================

def review(d):
    r = []

    if d["bedrooms"] >= 4:
        r.append("Good for family housing scale")

    if d["cost"] > 1500000:
        r.append("High cost warning detected")

    if d["structure"]["columns"] < 15:
        r.append("Structural reinforcement recommended")

    if not r:
        r.append("Balanced architectural design")

    return r

# =========================================================
# MATERIALS + SUSTAINABILITY
# =========================================================

def materials(d):
    return {
        "Concrete (m³)": d["structure"]["columns"] * 2,
        "Steel (tons)": d["structure"]["beams"] * 0.5,
        "Bricks": len(d["rooms"]) * 2000
    }

def sustainability(d):
    return max(40, 100 - d["structure"]["columns"])

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🧬 RANDOM V9")
page = st.sidebar.radio("Navigation", ["Dashboard", "Evolution", "Memory"])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🧬 RANDOM V9 Core")

    c1, c2, c3 = st.columns(3)

    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Evolution Runs", len(mem["evolution"]))

# =========================================================
# EVOLUTION LAB
# =========================================================

elif page == "Evolution":

    st.title("🧬 Evolution Lab V9")

    btype = st.selectbox("Building Type", sum(ARCH.values(), []))
    bedrooms = st.slider("Bedrooms", 1, 10, 3)
    gens = st.slider("Generations", 1, 8, 3)
    pop = st.slider("Population", 3, 12, 6)

    if st.button("Run Evolution"):

        best, history, _ = evolve(btype, bedrooms, gens, pop)

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
        log("Evolution completed")

        st.success("Evolution Complete")

        st.subheader("Best Design")
        st.json(best)

        st.subheader("Evolution Curve")
        st.line_chart(history)

        st.subheader("AI Review")
        for r in review(best):
            st.write("✔", r)

        st.subheader("Sustainability Score")
        st.metric("Score", sustainability(best))

        st.subheader("Material Estimate")
        st.json(materials(best))

        st.subheader("2D Floor Plan")
        draw_2d(plan)

        st.subheader("3D Massing Model")
        draw_3d(plan)

# =========================================================
# MEMORY VIEW
# =========================================================

elif page == "Memory":

    st.title("🧠 Memory Archive")
    st.json(mem)