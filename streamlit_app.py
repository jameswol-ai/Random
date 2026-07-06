# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE V35
# 2D + 3D EVOLUTIONARY SPATIAL SIMULATION OS
# Safe Memory + Voxel World + Evolution Core
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
    page_title="Random Studio Engine V35",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# SAFE MEMORY LAYER (FIXES JSON CRASH)
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
            raw = MEMORY_FILE.read_text(encoding="utf-8").strip()
            if not raw:
                return DEFAULT_STATE.copy()
            return json.loads(raw)
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        MEMORY_FILE.write_text(
            json.dumps(st.session_state.memory, indent=2),
            encoding="utf-8"
        )
    except Exception:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# init state
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if "history" not in st.session_state:
    st.session_state.history = []

mem = st.session_state.memory

# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>
html, body { font-family: 'Arial'; }

.canvas {
    display:flex;
    flex-wrap:wrap;
    gap:12px;
    padding:16px;
    background:#0b0f1a;
    border-radius:12px;
}

.room {
    flex:1 1 200px;
    padding:12px;
    border-radius:10px;
    color:white;
    border:1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# ARCH ENGINE (2D)
# =========================================================

ARCH = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}

def domain(t):
    for k,v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

def generate_base(btype, beds):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": domain(btype),
        "bedrooms": beds,
        "area": 100 + beds * 20,
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

def evolve(btype, beds, gens, pop):
    popu = [generate_base(btype, beds) for _ in range(pop)]
    hist = []

    for _ in range(gens):
        for d in popu:
            d["score"] = fitness(d)

        popu.sort(key=lambda x: x["score"], reverse=True)
        hist.append(popu[0]["score"])

        survivors = popu[:max(2, pop//2)]
        popu = survivors + [mutate(random.choice(survivors)) for _ in survivors]
        popu = popu[:pop]

    return popu[0], hist

def floor_plan(d):
    return [
        {"name":"Living","w":6,"h":5,"color":"#1e3a8a"},
        {"name":"Kitchen","w":4,"h":4,"color":"#065f46"},
    ] + [
        {"name":f"Bedroom {i+1}","w":4,"h":4,"color":"#4c1d95"}
        for i in range(d["bedrooms"])
    ]

# =========================================================
# 🌍 3D VOXEL ENGINE
# =========================================================

WORLD = (20, 10, 20)

def voxelize(d):
    w = np.zeros(WORLD, dtype=int)

    for _ in range(d["structure"]["columns"]):
        x = random.randint(0, WORLD[0]-1)
        z = random.randint(0, WORLD[2]-1)
        h = random.randint(2, 6)
        for y in range(h):
            w[x,y,z] = 1

    for _ in range(d["structure"]["beams"]):
        x = random.randint(0, WORLD[0]-2)
        z = random.randint(0, WORLD[2]-1)
        y = random.randint(2, 5)
        w[x,y,z] = 2
        w[x+1,y,z] = 2

    return w

def world_metrics(w):
    return {
        "solid": int(np.sum(w==1)),
        "beams": int(np.sum(w==2)),
        "density": float(np.sum(w>0)/w.size)
    }

def render_slice(w, y):
    grid = w[:,y,:]
    out = ""
    for z in range(grid.shape[1]):
        row = ""
        for x in range(grid.shape[0]):
            v = grid[x,z]
            row += "⬛" if v==0 else "🟦" if v==1 else "🟨"
        out += row + "\n"
    st.code(out)

# =========================================================
# UI
# =========================================================

st.sidebar.title("ARC V35")
page = st.sidebar.radio("Mode", ["Dashboard","Lab","Memory"])

btype = st.sidebar.selectbox("Type", sum(ARCH.values(), []))
beds = st.sidebar.slider("Beds",1,8,3)
gens = st.sidebar.slider("Generations",2,15,6)
pop = st.sidebar.slider("Population",4,20,8)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("ARC V35 CONTROL CORE")
    st.metric("Designs", len(mem["designs"]))
    st.metric("Evolution", len(mem["evolution"]))
    st.metric("Logs", len(mem["logs"]))

# =========================================================
# LAB
# =========================================================

elif page == "Lab":
    st.title("2D + 3D ENGINE")

    if st.button("Run Evolution"):
        best, hist = evolve(btype, beds, gens, pop)

        best["plan"] = floor_plan(best)
        best["world"] = voxelize(best)
        best["metrics"] = world_metrics(best["world"])

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
        st.metric("Score", d["score"])
        st.metric("Density", round(d["metrics"]["density"],3))

        tab1, tab2, tab3 = st.tabs(["2D","Diagnostics","3D"])

        with tab1:
            html = '<div class="canvas">'
            for r in d["plan"]:
                html += f"<div class='room' style='background:{r['color']}'>{r['name']}<br>{r['w']}×{r['h']}</div>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        with tab2:
            st.json(d)

        with tab3:
            y = st.slider("Layer",0,WORLD[1]-1,0)
            render_slice(d["world"], y)
            st.json(d["metrics"])

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("MEMORY CORE")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        st.session_state.history = []
        save_memory()
        st.rerun()