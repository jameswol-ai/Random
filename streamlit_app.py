# =========================================================
# RANDOM ARCHITECTURE OS V37
# Full Simulation + AI Architect Brain
# 2D + 3D + Evolution + Diagnostics + Memory Safe Layer
# =========================================================

import streamlit as st
import json
import uuid
import random
import numpy as np
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random Architecture OS V37",
    page_icon="🏛️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# SAFE MEMORY LAYER (NO MORE JSON CRASHES)
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "evolution": [],
    "logs": []
}

def safe_load_json(path, default):
    if not path.exists():
        return default.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default.copy()

def safe_save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

# =========================================================
# SESSION STATE INIT
# =========================================================

if "memory" not in st.session_state:
    st.session_state.memory = safe_load_json(MEMORY_FILE, DEFAULT_STATE)

if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

def log(msg):
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    safe_save_json(MEMORY_FILE, mem)

# =========================================================
# ARCHITECTURAL DOMAINS
# =========================================================

ARCH = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}

def domain(t):
    for k, v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

# =========================================================
# AI ARCHITECT BRAIN (RULE SYSTEM)
# =========================================================

def architect_brain(design):
    advice = []

    ratio = design["structure"]["beams"] / max(1, design["structure"]["columns"])

    if ratio < 1.8:
        advice.append("Increase beam density for structural stability.")

    if ratio > 3.0:
        advice.append("Over-engineered beam system detected.")

    if design["area"] > 400:
        advice.append("Large spatial volume — optimize circulation flow.")

    if design["cost"] / design["area"] > 2000:
        advice.append("Cost inefficiency detected per sqm.")

    if not advice:
        advice.append("Design is structurally and economically balanced.")

    return advice

# =========================================================
# GENERATION ENGINE
# =========================================================

def generate_base(btype, beds):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": domain(btype),
        "beds": beds,
        "area": 100 + beds * 22,
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(25, 80)
        }
    }

def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-5, 6)
    if random.random() > 0.6:
        d["area"] += 15
    return d

def fitness(d):
    r = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    cost_penalty = abs(r - 2.2) * 15
    return max(0, 100 - cost_penalty)

def evolve(btype, beds, gens, pop):
    population = [generate_base(btype, beds) for _ in range(pop)]
    history = []

    for _ in range(gens):
        scored = []
        for d in population:
            d["score"] = fitness(d)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop // 2)]
        population = survivors + [mutate(random.choice(survivors)) for _ in survivors]
        population = population[:pop]

    return scored[0], history

# =========================================================
# 2D FLOOR ENGINE
# =========================================================

def floor_plan(d):
    rooms = [
        {"name": "Living Core", "w": 6, "h": 5, "color": "#1e3a8a"},
        {"name": "Kitchen Node", "w": 4, "h": 4, "color": "#065f46"},
    ]

    for i in range(d["beds"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4,
            "h": 4,
            "color": "#4c1d95"
        })

    return rooms

def render_2d(plan):
    html = '<div style="display:flex;flex-wrap:wrap;gap:10px;">'
    for r in plan:
        html += f"""
        <div style="
            background:{r['color']};
            padding:12px;
            border-radius:10px;
            color:white;
            min-width:160px;">
            <b>{r['name']}</b><br>
            {r['w']}m × {r['h']}m
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# 3D VOXEL WORLD ENGINE
# =========================================================

WORLD = (20, 10, 20)

def voxel_world(d):
    w = np.zeros(WORLD)

    cx, cz = 10, 10

    for _ in range(d["structure"]["columns"]):
        x = cx + random.randint(-6, 6)
        z = cz + random.randint(-6, 6)
        h = random.randint(2, 6)
        w[x % 20, :h, z % 20] = 1

    for _ in range(d["structure"]["beams"]):
        x = random.randint(0, 19)
        z = random.randint(0, 19)
        y = random.randint(2, 5)
        w[x, y, z] = 2

    return w

def slice_view(world, y):
    grid = world[:, y, :]
    out = ""

    for z in range(grid.shape[1]):
        row = ""
        for x in range(grid.shape[0]):
            v = grid[x, z]
            row += "⬛" if v == 0 else "🟦" if v == 1 else "🟨"
        out += row + "\n"

    st.code(out)

def analyze_world(w):
    return {
        "solid": int(np.sum(w == 1)),
        "beams": int(np.sum(w == 2)),
        "density": float(np.sum(w > 0) / w.size)
    }

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏛️ V37 ARCH OS")

page = st.sidebar.radio("Mode", ["Dashboard", "Lab", "Memory", "AI Brain"])

btype = st.sidebar.selectbox("Building", sum(ARCH.values(), []))
beds = st.sidebar.slider("Beds", 1, 8, 3)
gens = st.sidebar.slider("Generations", 2, 15, 6)
pop = st.sidebar.slider("Population", 4, 20, 10)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏛️ Architecture OS V37")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution Runs", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

# =========================================================
# LAB
# =========================================================

elif page == "Lab":
    st.title("🧬 Evolutionary Architecture Lab")

    if st.button("Run Evolution"):
        best, hist = evolve(btype, beds, gens, pop)

        best["plan"] = floor_plan(best)
        best["world"] = voxel_world(best)
        best["analysis"] = analyze_world(best["world"])

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best": best["id"],
            "score": best["score"]
        })

        st.session_state.active_design = best
        log(f"Generated {best['id']}")

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.subheader(f"Design {d['id']}")

        a, b, c = st.columns(3)
        a.metric("Score", d["score"])
        b.metric("Area", d["area"])
        c.metric("Density", round(d["analysis"]["density"], 3))

        tab1, tab2, tab3 = st.tabs(["2D", "AI Brain", "3D"])

        with tab1:
            render_2d(d["plan"])

        with tab2:
            for a in architect_brain(d):
                st.write("🧠", a)

        with tab3:
            y = st.slider("Slice", 0, 9, 0)
            slice_view(d["world"], y)
            st.json(d["analysis"])

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory Core")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        safe_save_json(MEMORY_FILE, st.session_state.memory)
        st.rerun()

# =========================================================
# AI BRAIN VIEW
# =========================================================

elif page == "AI Brain":
    st.title("🧠 Architect Intelligence Layer")

    if st.session_state.active_design:
        for a in architect_brain(st.session_state.active_design):
            st.write("🔹", a)
    else:
        st.info("Run a design first to activate the brain.")