# =========================================================
# RANDOM V11 — FIXED UNIFIED BUILD
# Evolutionary Architecture Intelligence System
# + ARC Structural Engine (Integrated Cleanly)
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
    page_title="RANDOM V11",
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
# MEMORY
# =========================================================

DEFAULT = {"designs": [], "logs": [], "evolution": []}

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
# ARCH TYPES
# =========================================================

ARCH = {
    "Residential": ["House", "Apartment", "Villa"],
    "Commercial": ["Office", "School", "Hospital", "Hotel"],
    "Industrial": ["Warehouse", "Factory", "Plant"]
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
        "rooms": ["Core"] * random.randint(3, 6),
        "structure": {
            "columns": random.randint(10, 30),
            "beams": random.randint(20, 60)
        },
        "cost": random.randint(300000, 2000000)
    }

# =========================================================
# MUTATION ENGINE
# =========================================================

def mutate(d):
    d = json.loads(json.dumps(d))

    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-5, 5)

    if random.random() > 0.5:
        d["rooms"].append("Module")

    d["cost"] += random.randint(-100000, 150000)

    return d

# =========================================================
# FITNESS
# =========================================================

def fitness(d):
    structure = max(0, 100 - abs(d["structure"]["columns"] - 20))
    cost = max(0, 100 - d["cost"] // 50000)
    complexity = min(100, len(d["rooms"]) * 10)

    return {"structure": structure, "cost": cost, "complexity": complexity}

def score(f):
    return int((f["structure"] + f["cost"] + f["complexity"]) / 3)

# =========================================================
# EVOLUTION ENGINE
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

        population = []
        for s in survivors:
            population.append(s)
            population.append(mutate(s))

        population = population[:pop]

    return scored[0], history

# =========================================================
# FLOOR PLAN
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
# VISUALS
# =========================================================

def draw_2d(plan):
    fig, ax = plt.subplots()
    for r in plan:
        ax.add_patch(plt.Rectangle((r["x"], r["y"]), r["w"], r["h"], fill=False))
        ax.text(r["x"]+0.5, r["y"]+0.5, r["name"])
    st.pyplot(fig)

def draw_3d(plan):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    for r in plan:
        ax.bar3d(r["x"], r["y"], 0, r["w"], r["h"], 3)
    st.pyplot(fig)

# =========================================================
# MATERIALS
# =========================================================

def materials(d):
    return {
        "Concrete": d["structure"]["columns"] * 2,
        "Steel": d["structure"]["beams"] * 0.5,
        "Bricks": len(d["rooms"]) * 2000
    }

# =========================================================
# EUROCODE FIXED ENGINE
# =========================================================

def eurocode(d):

    span = 6.0
    gk = 5.5
    qk = 2.0

    design_load = (1.35 * gk) + (1.5 * qk)
    w_ed = design_load * 4.5

    m_ed = (w_ed * span ** 2) / 8
    v_ed = (w_ed * span) / 2

    b = 300
    d_eff = 450
    f_ck = 30

    m_rd = (0.167 * f_ck * b * (d_eff ** 2)) / 1e6

    return {
        "m_ed": m_ed,
        "m_rd": m_rd,
        "v_ed": v_ed,
        "status": "PASS" if m_rd > m_ed else "FAIL"
    }

# =========================================================
# UI
# =========================================================

st.sidebar.title("🧬 RANDOM V11")
page = st.sidebar.radio("Menu", ["Dashboard", "Evolution"])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🧬 RANDOM V11 Core")

    c1,c2,c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution Runs", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

# =========================================================
# EVOLUTION
# =========================================================

elif page == "Evolution":

    st.title("🧬 Evolution Engine")

    btype = st.selectbox("Type", sum(ARCH.values(), []))
    bedrooms = st.slider("Bedrooms", 1, 8, 3)
    gens = st.slider("Generations", 1, 6, 3)
    pop = st.slider("Population", 3, 10, 5)

    if st.button("Run Evolution"):

        best, history = evolve(btype, bedrooms, gens, pop)

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

        st.success("Done")

        st.json(best)

        st.line_chart(history)

        st.subheader("Materials")
        st.json(materials(best))

        st.subheader("2D")
        draw_2d(plan)

        st.subheader("3D")
        draw_3d(plan)

        st.subheader("Eurocode")
        st.json(eurocode(best))