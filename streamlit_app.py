# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE — V32
# 2D + 3D EVOLUTIONARY SPATIAL SIMULATION OS
# Unified Streamlit Architecture Kernel
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
    page_title="Random Studio Engine V32",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLING CORE
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background:#0b0f1a;
    color:white;
}

h1,h2,h3 {
    font-family:'Space Grotesk',sans-serif;
    letter-spacing:-0.03em;
}

.arc-canvas {
    display:flex;
    flex-wrap:wrap;
    gap:14px;
    padding:18px;
    border-radius:12px;
    background:#0f172a;
    border:1px solid rgba(255,255,255,0.08);
}

.arc-room {
    flex:1 1 200px;
    padding:14px;
    border-radius:10px;
    border:1px solid rgba(255,255,255,0.12);
}

.voxel {
    font-size:12px;
    line-height:12px;
    white-space:pre;
    background:#05070d;
    padding:12px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY ENGINE
# =========================================================

DEFAULT = {"designs": [], "logs": [], "evolution": []}

def load():
    if MEMORY_FILE.exists():
        return json.load(open(MEMORY_FILE))
    return DEFAULT.copy()

def save():
    json.dump(st.session_state.mem, open(MEMORY_FILE, "w"), indent=2)

def log(msg):
    st.session_state.mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save()

if "mem" not in st.session_state:
    st.session_state.mem = load()

mem = st.session_state.mem

if "active" not in st.session_state:
    st.session_state.active = None

# =========================================================
# ARCHITECTURE ENGINE (GENETIC CORE)
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

def base(btype, beds):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": domain(btype),
        "beds": beds,
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

def evo(btype, beds, gens, pop):
    p = [base(btype, beds) for _ in range(pop)]
    hist = []

    for _ in range(gens):
        for d in p:
            d["score"] = fitness(d)

        p.sort(key=lambda x: x["score"], reverse=True)
        hist.append(p[0]["score"])

        survivors = p[:max(2, pop//2)]
        p = survivors + [mutate(random.choice(survivors)) for _ in survivors]
        p = p[:pop]

    return p[0], hist

# =========================================================
# 2D FLOOR SYSTEM
# =========================================================

def floor(d):
    rooms = [
        {"name":"Living","w":6,"h":5,"c":"#1e3a8a"},
        {"name":"Kitchen","w":4,"h":4,"c":"#065f46"},
    ]
    for i in range(d["beds"]):
        rooms.append({"name":f"Bedroom {i+1}","w":4,"h":4,"c":"#4c1d95"})
    return rooms

def render_2d(plan):
    html = '<div class="arc-canvas">'
    for r in plan:
        html += f"""
        <div class="arc-room" style="background:{r['c']}">
        <b>{r['name']}</b><br>{r['w']} × {r['h']}
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# 🌐 3D VOXEL WORLD ENGINE
# =========================================================

WORLD = (20,10,20)

def voxel(d):
    w = np.zeros(WORLD)

    for _ in range(d["structure"]["columns"]):
        x,z = random.randint(0,19), random.randint(0,19)
        h = random.randint(2,6)
        for y in range(h):
            w[x,y,z] = 1

    for _ in range(d["structure"]["beams"]):
        x,z,y = random.randint(0,19), random.randint(0,19), random.randint(2,5)
        for i in range(3):
            w[min(19,x+i), y, z] = 2

    return w

def slice_view(w, y):
    grid = w[:,y,:]
    out=""
    for z in range(20):
        for x in range(20):
            v = grid[x,z]
            out += "⬛" if v==0 else "🟦" if v==1 else "🟨"
        out += "\n"
    st.code(out)

# =========================================================
# UI
# =========================================================

st.sidebar.title("ARC V32")
page = st.sidebar.radio("Mode", ["Dashboard","Lab","Memory"])

btype = st.sidebar.selectbox("Type", sum(ARCH.values(), []))
beds = st.sidebar.slider("Beds",1,8,3)
gens = st.sidebar.slider("Generations",2,15,5)
pop = st.sidebar.slider("Population",4,20,8)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("📐 ARC OS CORE V32")
    c1,c2,c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

# =========================================================
# LAB (2D + 3D)
# =========================================================

elif page == "Lab":
    st.title("🌍 2D + 3D ENGINE CORE")

    if st.button("Generate Universe"):
        best, hist = evo(btype,beds,gens,pop)

        best["plan"] = floor(best)
        best["world"] = voxel(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "score": best["score"]
        })

        st.session_state.active = best
        log("Generated design")

    if st.session_state.active:
        d = st.session_state.active

        st.subheader(d["id"])
        st.metric("Score", d["score"])

        tab1, tab2, tab3 = st.tabs(["2D","Diagnostics","3D"])

        with tab1:
            render_2d(d["plan"])

        with tab2:
            st.json(d)

        with tab3:
            y = st.slider("Layer",0,9,0)
            slice_view(d["world"], y)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 MEMORY CORE")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.mem = DEFAULT.copy()
        st.session_state.active = None
        save()
        st.rerun()