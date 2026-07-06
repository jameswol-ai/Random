# =============================
# ARC STUDIO ENGINE v11
# Evolutionary AEC + MEP + HVAC Generative Architecture System
# =============================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Arc Studio Engine v11",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STUDIO UI SKIN
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

.arc-blueprint {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    background: #0b1220;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
}

.arc-room {
    flex: 1 1 220px;
    padding: 16px;
    border-radius: 10px;
    color: white;
    border: 1px solid rgba(255,255,255,0.12);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
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
            return json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
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

# =========================================================
# INIT STATE
# =========================================================

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if "active_history" not in st.session_state:
    st.session_state.active_history = []

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE CORE (AEC + GENETICS)
# =========================================================

def generate_base_design(typology, floors, rooms_per_floor):
    total_rooms = floors * rooms_per_floor

    base_rooms = [
        "Core Living Zone",
        "Service Core",
        "Circulation Spine"
    ]

    room_list = base_rooms + [f"Module Space {i+1}" for i in range(total_rooms)]

    area = 80 + total_rooms * 14

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "typology": typology,
        "floors": floors,
        "rooms_per_floor": rooms_per_floor,
        "rooms": room_list,
        "area_sqm": area,
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(24, 80)
        },
        "cost": int(area * random.randint(1200, 2400))
    }

def mutate_design(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-3, 5)

    if random.random() > 0.6:
        d["rooms"].append("Adaptive Expansion Module")
        d["area_sqm"] += 18

    d["cost"] = int(d["area_sqm"] * random.randint(1200, 2500))
    return d

def fitness(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    structural = max(0, 100 - abs(ratio - 2.0) * 25)

    cost_eff = max(0, 100 - (d["cost"] / max(1, d["area_sqm"]) - 1500) * 0.05)

    complexity = min(100, len(d["rooms"]) * 3)

    return {
        "structural": structural,
        "cost": cost_eff,
        "complexity": complexity
    }

def score(f):
    return int(sum(f.values()) / len(f))

def evolution_loop(typology, floors, rooms_per_floor, generations, pop_size):
    population = [
        generate_base_design(typology, floors, rooms_per_floor)
        for _ in range(pop_size)
    ]

    history = []

    for _ in range(generations):
        scored = []

        for d in population:
            f = fitness(d)
            d["fitness"] = f
            d["score"] = score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop_size // 2)]

        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate_design(s))

        population = new_pop[:pop_size]

    return scored[0], history

def generate_floor_plan(d):
    plan = [
        {"name": "Living Core", "w": 6, "h": 5, "color": "#1e3a8a"},
        {"name": "Kitchen Node", "w": 4, "h": 4, "color": "#065f46"},
        {"name": "Service Hub", "w": 3, "h": 3, "color": "#78350f"}
    ]

    for i in range(d["rooms_per_floor"]):
        plan.append({
            "name": f"Room Module {i+1}",
            "w": 4,
            "h": 4,
            "color": "#4c1d95"
        })

    return plan

def render(plan):
    html = '<div class="arc-blueprint">'
    for r in plan:
        html += f"""
        <div class="arc-room" style="background:{r['color']}">
            <b>{r['name']}</b><br>
            {r['w']}m × {r['h']}m
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# SIDEBAR CONFIG (AEC + MEP + HVAC)
# =========================================================

st.sidebar.title("📐 Arc Studio Engine")

typology = st.sidebar.selectbox(
    "🏢 Building Typology",
    ["Residential", "Commercial", "Industrial"]
)

floors = st.sidebar.slider("🏗️ Floors", 1, 60, 10)
rooms_per_floor = st.sidebar.slider("🏠 Rooms per Floor", 1, 15, 5)

population = st.sidebar.slider("👥 Population Load", 0, 5000, 300)

st.sidebar.markdown("### 🧬 Genetics")
population_size = st.sidebar.slider("Population Size", 10, 200, 40)
generations = st.sidebar.slider("Epoch Cycles", 2, 40, 10)

st.sidebar.markdown("### 🌬️ MEP + HVAC")

hvac = st.sidebar.selectbox(
    "HVAC Mode",
    ["Natural", "Hybrid", "Full Mechanical"]
)

ventilation = st.sidebar.slider("Ventilation Efficiency", 0, 100, 70)

energy = st.sidebar.selectbox(
    "Energy Model",
    ["Low Energy", "Standard", "Smart Grid"]
)

water = st.sidebar.selectbox(
    "Water System",
    ["Basic", "Greywater", "Closed Loop"]
)

# =========================================================
# ENGINE STATE (NEW AEC CORE)
# =========================================================

arc_engine_state = {
    "aec": {
        "typology": typology,
        "floors": floors,
        "rooms_per_floor": rooms_per_floor,
        "total_rooms": floors * rooms_per_floor,
        "population": population
    },
    "genetics": {
        "population_size": population_size,
        "generations": generations
    },
    "systems": {
        "hvac": hvac,
        "ventilation": ventilation,
        "energy": energy,
        "water": water
    }
}

# =========================================================
# UI
# =========================================================

st.title("📐 Arc Studio Engine v11")
st.caption("AEC + MEP + HVAC Generative Architecture System")

run = st.button("🚀 Run Evolution Engine", use_container_width=True)

if run:
    best, history = evolution_loop(
        typology,
        floors,
        rooms_per_floor,
        generations,
        population_size
    )

    best["plan"] = generate_floor_plan(best)

    st.session_state.active_design = best
    st.session_state.active_history = history

    mem["designs"].append(best)
    mem["evolution"].append({
        "id": str(uuid.uuid4())[:6],
        "score": best["score"],
        "time": datetime.now().isoformat()
    })

    log_event(f"Generated design {best['id']}")

# =========================================================
# OUTPUT
# =========================================================

if st.session_state.active_design:
    d = st.session_state.active_design

    st.subheader(f"🏗️ Design {d['id']}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Score", d["score"])
    c2.metric("Area", f"{d['area_sqm']} m²")
    c3.metric("Cost", f"${d['cost']:,}")

    tab1, tab2 = st.tabs(["Blueprint", "Evolution"])

    with tab1:
        render(d["plan"])

    with tab2:
        st.line_chart(st.session_state.active_history)

else:
    st.info("Run the engine to generate a design.")

# =========================================================
# MEMORY VIEW
# =========================================================

with st.expander("🧠 System Memory"):
    st.json(mem)

if st.button("Reset Memory"):
    st.session_state.memory = DEFAULT_STATE.copy()
    st.session_state.active_design = None
    st.session_state.active_history = []
    save_memory()
    st.rerun()
