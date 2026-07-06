# =========================================================
# RANDOM V9
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
h2,h3 { color: #7dd3fc; }

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

def load():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE))
        except:
            return DEFAULT.copy()
    return DEFAULT.copy()

def save():
    try:
        json.dump(st.session_state.memory, open(MEMORY_FILE, "w"), indent=2)
    except:
        pass

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save()

if "memory" not in st.session_state:
    st.session_state.memory = load()

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE TYPES
# =========================================================

ARCH = {
    "Residential": ["House","Apartment","Villa"],
    "Commercial": ["Office","School","Hospital","Hotel"],
    "Industrial": ["Warehouse","Factory","Plant"]
}

def domain_of(t):
    for k,v in ARCH.items():
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
# MUTATION ENGINE 🧬
# =========================================================

def mutate(d):
    d = json.loads(json.dumps(d))

    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-5, 5)

    if random.random() > 0.5:
        d["rooms"].append("Module")

    d["cost"] += random.randint(-100000, 200000)

    return d

# =========================================================
# FITNESS FUNCTION
# =========================================================

def fitness(d):
    return {
        "structure": max(0, 100 - abs(d["structure"]["columns"] - 20)),
        "cost": max(0, 100 - d["cost"] // 50000),
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

    for g in range(gens):

        scored = []
        for d in population:
            f = fitness(d)
            d["fitness"] = f
            d["score"] = score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)

        best = scored[0]
        history.append(best["score"])

        survivors = scored[:max(2, pop // 2)]

        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate(s))

        population = new_pop[:pop]

    return scored[0], history, scored

# =========================================================
# 🏠 FLOOR PLAN ENGINE
# =========================================================

def floor_plan(design):
    bedrooms = design["bedrooms"]

    rooms = [
        {"name":"Living", "x":0, "y":0, "w":6, "h":5},
        {"name":"Kitchen", "x":6, "y":0, "w":4, "h":4},
        {"name":"Bath", "x":6, "y":4, "w":2, "h":2}
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
# 🏠 2D DRAW
# =========================================================

def draw_2d(plan):

    fig, ax = plt.subplots()

    for r in plan:
        rect = plt.Rectangle(
            (r["x"], r["y"]),
            r["w"], r["h"],
            fill=False
        )
        ax.add_patch(rect)
        ax.text(r["x"]+1, r["y"]+1, r["name"])

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 15)
    ax.set_title("2D Floor Plan")

    st.pyplot(fig)

# =========================================================
# 🏗️ 3D BUILDING MODEL
# =========================================================

def draw_3d(plan):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for r in plan:
        ax.bar3d(r["x"], r["y"], 0, r["w"], r["h"], 3)

    ax.set_title("3D Building Massing")

    st.pyplot(fig)

# =========================================================
# 🤖 AI REVIEW ENGINE
# =========================================================

def review(d):

    r = []

    if d["bedrooms"] >= 4:
        r.append("Good for family housing")

    if d["cost"] > 1500000:
        r.append("High cost warning")

    if d["structure"]["columns"] < 15:
        r.append("Increase structural support")

    if not r:
        r.append("Balanced design")

    return r

# =========================================================
# 📐 MATERIAL ESTIMATION
# =========================================================

def materials(d):

    return {
        "Concrete (m³)": d["structure"]["columns"] * 2,
        "Steel (tons)": d["structure"]["beams"] * 0.5,
        "Bricks": len(d["rooms"]) * 2000
    }

# =========================================================
# 🌱 SUSTAINABILITY
# =========================================================

def sustainability(d):
    return max(40, 100 - d["structure"]["columns"])

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧬 RANDOM V9")
page = st.sidebar.radio("Navigation", ["Dashboard","Evolution","Memory"])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🧬 RANDOM V9 Core")

    c1,c2,c3 = st.columns(3)

    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Evolutions", len(mem["evolution"]))

# =========================================================
# EVOLUTION LAB
# =========================================================

elif page == "Evolution":

    st.title("🧬 Evolution Lab V9")

    btype = st.selectbox("Type", sum(ARCH.values(), []))
    bedrooms = st.slider("Bedrooms", 1, 10, 3)
    gens = st.slider("Generations", 1, 6, 3)
    pop = st.slider("Population", 3, 10, 5)

    if st.button("Run Evolution"):

        best, history, pop_final = evolve(btype, bedrooms, gens, pop)

        plan = floor_plan(best)

        best["plan"] = plan

        mem["designs"].append(best)

        mem["evolution"].append({
            "id": str(uuid.uuid4())[:8],
            "best": best,
            "history": history,
            "time": datetime.now().isoformat()
        })

        save()
        log("Evolution completed")

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

        st.subheader("Materials")
        st.json(materials(best))

        st.subheader("2D Floor Plan")
        draw_2d(plan)

        st.subheader("3D Model")
        draw_3d(plan)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.title("🧠 Memory")

    st.json(mem)
