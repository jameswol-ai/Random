# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# 2D + 3D EVOLUTIONARY SPATIAL SIMULATION OS
# SINGLE FILE STREAMLIT IMPLEMENTATION
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
    page_title="Random Studio Engine",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLING
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

.arc-blueprint-canvas {
    display:flex;
    flex-wrap:wrap;
    gap:16px;
    background:#0b0f1a;
    padding:20px;
    border-radius:12px;
}

.arc-room-module {
    flex:1 1 220px;
    padding:16px;
    border-radius:10px;
    color:white;
    border:1px solid rgba(255,255,255,0.1);
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
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        json.dump(st.session_state.memory, open(MEMORY_FILE, "w"), indent=2)
    except:
        pass

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

if "history" not in st.session_state:
    st.session_state.history = []

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE ENGINE (2D)
# =========================================================

ARCH = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel Resort", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}

def domain(t):
    for k,v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

def generate_base_design(btype, beds):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": domain(btype),
        "bedrooms": beds,
        "area": 120 + beds * 18,
        "structure": {
            "columns": random.randint(14, 36),
            "beams": random.randint(28, 72)
        }
    }

def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-4, 5)
    return d

def fitness(d):
    r = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    return max(0, 100 - abs(r - 2.1) * 20)

def run_evo(btype, beds, gens, pop):
    popu = [generate_base_design(btype, beds) for _ in range(pop)]
    hist = []

    for _ in range(gens):
        scored = []
        for d in popu:
            d["score"] = fitness(d)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        hist.append(scored[0]["score"])

        survivors = scored[:max(2, pop//2)]
        popu = survivors + [mutate(random.choice(survivors)) for _ in survivors]
        popu = popu[:pop]

    return scored[0], hist

def floor(d):
    return [
        {"name":"Living","w":6,"h":5,"color":"#1e3a8a"},
        {"name":"Kitchen","w":4,"h":4,"color":"#065f46"},
    ] + [
        {"name":f"Bedroom {i+1}","w":4,"h":4,"color":"#4c1d95"}
        for i in range(d["bedrooms"])
    ]

# =========================================================
# 🌍 3D VOXEL WORLD ENGINE
# =========================================================

WORLD_SIZE = (20, 10, 20)

def voxelize(d):
    world = np.zeros(WORLD_SIZE, dtype=int)

    cx, cz = 10, 10

    for _ in range(d["structure"]["columns"]):
        x = (cx + random.randint(-6, 6)) % WORLD_SIZE[0]
        z = (cz + random.randint(-6, 6)) % WORLD_SIZE[2]
        h = random.randint(2, 7)
        for y in range(h):
            world[x, y, z] = 1

    for _ in range(d["structure"]["beams"]):
        x = random.randint(0, 19)
        z = random.randint(0, 19)
        y = random.randint(2, 5)
        for i in range(3):
            world[min(19, x+i), y, z] = 2

    for _ in range(len(d["structure"])):
        x = random.randint(2, 17)
        z = random.randint(2, 17)
        world[x, 0, z] = 3

    return world

def analyze_world(w):
    return {
        "solid": int(np.sum(w == 1)),
        "beams": int(np.sum(w == 2)),
        "anchors": int(np.sum(w == 3)),
        "density": float(np.sum(w > 0) / w.size)
    }

def render_slice(world, y):
    grid = world[:, y, :]
    out = ""

    for z in range(grid.shape[1]):
        row = ""
        for x in range(grid.shape[0]):
            v = grid[x, z]
            row += "⬛" if v == 0 else "🟦" if v == 1 else "🟨" if v == 2 else "🟩"
        out += row + "\n"

    st.code(out)

# =========================================================
# UI
# =========================================================

st.sidebar.title("📐 ARC OS")

page = st.sidebar.radio("Mode", ["Dashboard", "Lab", "Memory"])

btype = st.sidebar.selectbox("Type", sum(ARCH.values(), []))
beds = st.sidebar.slider("Beds", 1, 8, 3)
gens = st.sidebar.slider("Generations", 2, 15, 5)
pop = st.sidebar.slider("Population", 4, 20, 8)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("📐 ARCH CONTROL CORE")

    c1,c2,c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

# =========================================================
# LAB (2D + 3D)
# =========================================================

elif page == "Lab":
    st.title("🌍 2D + 3D ARCHITECTURE ENGINE")

    if st.button("Run Engine"):
        best, hist = run_evo(btype, beds, gens, pop)

        best["plan"] = floor(best)
        best["world"] = voxelize(best)
        best["world_metrics"] = analyze_world(best["world"])

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best": best["id"],
            "score": best["score"]
        })

        st.session_state.active_design = best
        st.session_state.history = hist

        log_event(f"Generated {best['id']}")

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.subheader(f"Design {d['id']}")

        a,b,c = st.columns(3)
        a.metric("Score", d["score"])
        b.metric("Area", d["area"])
        c.metric("Density", round(d["world_metrics"]["density"], 3))

        tab1, tab2, tab3 = st.tabs([
            "2D Blueprint",
            "Diagnostics",
            "3D World"
        ])

        with tab1:
            html = '<div class="arc-blueprint-canvas">'
            for r in d["plan"]:
                html += f"<div class='arc-room-module' style='background:{r['color']}'>{r['name']}<br>{r['w']}×{r['h']}</div>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        with tab2:
            st.json(d)

        with tab3:
            y = st.slider("Layer", 0, WORLD_SIZE[1]-1, 0)
            render_slice(d["world"], y)
            st.json(d["world_metrics"])

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 MEMORY CORE")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        st.session_state.history = []
        save_memory()
        st.rerun()