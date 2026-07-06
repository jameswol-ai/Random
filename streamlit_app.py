
# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE — V33 SAFE CORE
# 2D + 3D EVOLUTIONARY ARCHITECTURE OS (CRASH-PROOF)
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
    page_title="Random Studio Engine V33",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# SAFE MEMORY LOADER (FIXES YOUR JSON ERROR)
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "evolution": [],
    "logs": []
}

def safe_load_memory():
    """Never crash even if file is empty/corrupt"""
    if not MEMORY_FILE.exists():
        return DEFAULT_STATE.copy()

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # 🔥 FIX: empty file protection
            if not content:
                return DEFAULT_STATE.copy()

            return json.loads(content)

    except (json.JSONDecodeError, Exception):
        # backup broken file instead of crashing
        try:
            MEMORY_FILE.rename(MEMORY_FILE.with_suffix(".broken.json"))
        except:
            pass

        return DEFAULT_STATE.copy()


def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.mem, f, indent=2)
    except:
        pass


def log(msg):
    st.session_state.mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()


# =========================================================
# INIT STATE
# =========================================================

if "mem" not in st.session_state:
    st.session_state.mem = safe_load_memory()

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.mem

# =========================================================
# ARCH ENGINE (GENETIC CORE)
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


def base_design(btype, beds):
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
    d["structure"]["columns"] = max(10, d["structure"]["columns"] + random.randint(-2, 3))
    d["structure"]["beams"] = max(10, d["structure"]["beams"] + random.randint(-4, 5))
    return d


def fitness(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    return max(0, 100 - abs(ratio - 2.1) * 20)


def evolve(btype, beds, gens, pop):
    population = [base_design(btype, beds) for _ in range(pop)]
    history = []

    for _ in range(gens):
        for d in population:
            d["score"] = fitness(d)

        population.sort(key=lambda x: x["score"], reverse=True)
        history.append(population[0]["score"])

        survivors = population[:max(2, pop // 2)]
        population = survivors + [mutate(random.choice(survivors)) for _ in survivors]
        population = population[:pop]

    return population[0], history


# =========================================================
# 2D FLOOR SYSTEM
# =========================================================

def floor_plan(d):
    rooms = [
        {"name": "Living", "w": 6, "h": 5, "c": "#1e3a8a"},
        {"name": "Kitchen", "w": 4, "h": 4, "c": "#065f46"},
    ]

    for i in range(d["beds"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4,
            "h": 4,
            "c": "#4c1d95"
        })

    return rooms


def render_2d(plan):
    html = '<div style="display:flex;flex-wrap:wrap;gap:12px;padding:12px;">'
    for r in plan:
        html += f"""
        <div style="
            background:{r['c']};
            padding:12px;
            border-radius:10px;
            color:white;
            min-width:160px;
        ">
            <b>{r['name']}</b><br>
            {r['w']} × {r['h']}
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# =========================================================
# 🌐 3D VOXEL ENGINE (SAFE)
# =========================================================

WORLD = (20, 10, 20)

def voxelize(d):
    w = np.zeros(WORLD)

    for _ in range(d["structure"]["columns"]):
        x, z = random.randint(0, 19), random.randint(0, 19)
        h = random.randint(2, 6)
        for y in range(h):
            w[x, y, z] = 1

    for _ in range(d["structure"]["beams"]):
        x, z, y = random.randint(0, 19), random.randint(0, 19), random.randint(2, 5)
        for i in range(3):
            w[min(19, x + i), y, z] = 2

    return w


def render_slice(w, y):
    grid = w[:, y, :]
    out = ""

    for z in range(20):
        for x in range(20):
            v = grid[x, z]
            out += "⬛" if v == 0 else "🟦" if v == 1 else "🟨"
        out += "\n"

    st.code(out)


# =========================================================
# UI
# =========================================================

st.sidebar.title("ARC V33 SAFE CORE")

page = st.sidebar.radio("Mode", ["Dashboard", "Lab", "Memory"])

btype = st.sidebar.selectbox("Type", sum(ARCH.values(), []))
beds = st.sidebar.slider("Beds", 1, 8, 3)
gens = st.sidebar.slider("Generations", 2, 15, 5)
pop = st.sidebar.slider("Population", 4, 20, 8)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("📐 ARC ENGINE V33 (STABLE)")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))


# =========================================================
# LAB
# =========================================================

elif page == "Lab":
    st.title("🌍 2D + 3D SIMULATION CORE")

    if st.button("Generate Design Universe"):
        best, hist = evolve(btype, beds, gens, pop)

        best["plan"] = floor_plan(best)
        best["world"] = voxelize(best)

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

        tab1, tab2, tab3 = st.tabs(["2D", "Diagnostics", "3D"])

        with tab1:
            render_2d(d["plan"])

        with tab2:
            st.json(d)

        with tab3:
            y = st.slider("Voxel Layer", 0, 9, 0)
            render_slice(d["world"], y)


# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 MEMORY CORE SAFE MODE")
    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.mem = DEFAULT_STATE.copy()
        st.session_state.active = None
        save_memory()
        st.rerun()