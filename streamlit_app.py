# =========================================================
# V37-OS — HARDENED STREAMLIT ARCHITECTURE ENGINE
# Production-grade Single File System
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
    page_title="Architecture OS V37",
    page_icon="🏛️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# 🧯 SAFETY LAYER (CRASH PROOF MEMORY)
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "evolution": [],
    "logs": []
}

def safe_load():
    if not MEMORY_FILE.exists():
        return DEFAULT_STATE.copy()
    try:
        return json.loads(MEMORY_FILE.read_text())
    except Exception:
        return DEFAULT_STATE.copy()

def safe_save(state):
    try:
        MEMORY_FILE.write_text(json.dumps(state, indent=2))
    except Exception:
        pass

def log(state, msg):
    state["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    safe_save(state)

# init
if "state" not in st.session_state:
    st.session_state.state = safe_load()

if "active" not in st.session_state:
    st.session_state.active = None

S = st.session_state.state

# =========================================================
# 🧠 CORE ENGINE
# =========================================================

ARCH = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}

def domain(t):
    return next((k for k,v in ARCH.items() if t in v), "Unknown")

def create_design(btype, beds, seed=None):
    if seed:
        random.seed(seed)

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": domain(btype),
        "beds": beds,
        "area": 100 + beds * 20,
        "structure": {
            "columns": random.randint(14, 40),
            "beams": random.randint(25, 80)
        },
        "seed": seed or random.randint(1, 999999)
    }

# =========================================================
# 🧬 EVOLUTION ENGINE
# =========================================================

def fitness(d):
    r = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    return max(0, 100 - abs(r - 2.2) * 18)

def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] = max(10, d["structure"]["columns"] + random.randint(-2, 3))
    d["structure"]["beams"] = max(15, d["structure"]["beams"] + random.randint(-4, 5))
    return d

def evolve(btype, beds, gens, pop):
    population = [create_design(btype, beds) for _ in range(pop)]
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
# 🏗️ 2D ENGINE
# =========================================================

def floor(d):
    return [
        {"name": "Living Core", "w": 6, "h": 5, "color": "#1e3a8a"},
        {"name": "Kitchen Node", "w": 4, "h": 4, "color": "#065f46"},
    ] + [
        {"name": f"Bedroom {i+1}", "w": 4, "h": 4, "color": "#4c1d95"}
        for i in range(d["beds"])
    ]

def render_2d(plan):
    html = "<div style='display:flex;flex-wrap:wrap;gap:10px;'>"
    for r in plan:
        html += f"""
        <div style='background:{r["color"]};padding:12px;border-radius:10px;color:white;min-width:160px'>
        <b>{r["name"]}</b><br>{r["w"]}×{r["h"]}
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# 🌐 3D ENGINE (VOXEL WORLD)
# =========================================================

WORLD = (20, 10, 20)

def voxel(d):
    w = np.zeros(WORLD)

    cx, cz = 10, 10

    for _ in range(d["structure"]["columns"]):
        x = (cx + random.randint(-6, 6)) % 20
        z = (cz + random.randint(-6, 6)) % 20
        h = random.randint(2, 6)
        w[x, :h, z] = 1

    for _ in range(d["structure"]["beams"]):
        x, z = random.randint(0, 19), random.randint(0, 19)
        y = random.randint(2, 5)
        w[x, y, z] = 2

    return w

def slice_view(w, y):
    grid = w[:, y, :]
    for z in range(20):
        row = ""
        for x in range(20):
            v = grid[x, z]
            row += "⬛" if v == 0 else "🟦" if v == 1 else "🟨"
        st.code(row)

# =========================================================
# 🧠 AI ARCHITECT BRAIN
# =========================================================

def brain(d):
    r = d["structure"]["beams"] / max(1, d["structure"]["columns"])

    out = []

    if r < 1.8:
        out.append("Increase structural beam density.")
    if r > 3.0:
        out.append("Over-engineering detected.")
    if d["area"] > 350:
        out.append("Optimize spatial circulation.")
    if not out:
        out.append("Design is balanced.")

    return out

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏛️ V37-OS")

page = st.sidebar.radio("Mode", ["Dashboard", "Lab", "Memory", "AI Brain"])

btype = st.sidebar.selectbox("Type", sum(ARCH.values(), []))
beds = st.sidebar.slider("Beds", 1, 8, 3)
gens = st.sidebar.slider("Generations", 2, 15, 6)
pop = st.sidebar.slider("Population", 4, 20, 10)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏛️ Architecture OS V37 (Hardened)")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(S["designs"]))
    c2.metric("Evolution Runs", len(S["evolution"]))
    c3.metric("Logs", len(S["logs"]))

# =========================================================
# LAB
# =========================================================

elif page == "Lab":
    st.title("🧬 Evolution Lab")

    if st.button("Run Simulation"):
        best, hist = evolve(btype, beds, gens, pop)

        best["plan"] = floor(best)
        best["world"] = voxel(best)

        S["designs"].append(best)
        S["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best": best["id"],
            "score": best["score"]
        })

        st.session_state.active = best
        log(S, f"Generated {best['id']}")

    if st.session_state.active:
        d = st.session_state.active

        st.subheader(f"Design {d['id']}")

        a, b, c = st.columns(3)
        a.metric("Score", d["score"])
        b.metric("Area", d["area"])
        c.metric("Seed", d["seed"])

        tab1, tab2, tab3 = st.tabs(["2D", "AI Brain", "3D"])

        with tab1:
            render_2d(d["plan"])

        with tab2:
            for x in brain(d):
                st.write("🧠", x)

        with tab3:
            y = st.slider("Slice", 0, 9, 0)
            slice_view(d["world"], y)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory Core")

    st.json(S)

    if st.button("Reset"):
        st.session_state.state = DEFAULT_STATE.copy()
        safe_save(st.session_state.state)
        st.rerun()

# =========================================================
# AI BRAIN VIEW
# =========================================================

elif page == "AI Brain":
    st.title("🧠 Architect Brain")

    if st.session_state.active:
        for x in brain(st.session_state.active):
            st.write("🔹", x)
    else:
        st.info("Run a simulation first.")