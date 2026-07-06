# =========================================================
# V20 PLAYABLE — ARCHITECTURE CIVILIZATION ENGINE
# AI Faction Simulation Game (Streamlit)
# =========================================================

import streamlit as st
import random
import uuid
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="V20 Civilization Engine",
    page_icon="🌍",
    layout="wide"
)

# =========================================================
# WORLD SEED
# =========================================================

DEFAULT_WORLD = {
    "name": "Neo-Arcadia",
    "climate": "tropical",
    "material_cost_index": 1.2,
    "innovation_pressure": 0.7,
    "population_density": 0.6
}

# =========================================================
# INIT STATE
# =========================================================

if "world" not in st.session_state:
    st.session_state.world = DEFAULT_WORLD.copy()

if "factions" not in st.session_state:
    st.session_state.factions = {
        "Structural": 1.0,
        "Economy": 1.0,
        "Innovation": 1.0,
        "Sustainability": 1.0,
        "Compliance": 1.0
    }

if "history" not in st.session_state:
    st.session_state.history = []

# =========================================================
# FACTION EVOLUTION LOGIC
# =========================================================

def evolve_factions(world, factions):
    new = {}

    for name, power in factions.items():

        drift = random.uniform(-0.15, 0.15)

        # world forces bias evolution
        if name == "Innovation":
            drift += world["innovation_pressure"] * 0.1

        if name == "Economy":
            drift -= world["material_cost_index"] * 0.05

        if name == "Sustainability":
            drift += 0.03

        new_power = max(0.1, min(3.0, power + drift))
        new[name] = new_power

    return new

# =========================================================
# CITY STATE GENERATION
# =========================================================

def generate_city_state(factions):
    total = sum(factions.values())

    return {
        "stability": round((factions["Structural"] + factions["Compliance"]) / total * 100, 2),
        "innovation_index": round(factions["Innovation"] / total * 100, 2),
        "economic_pressure": round(factions["Economy"] / total * 100, 2),
        "sustainability": round(factions["Sustainability"] / total * 100, 2),
    }

# =========================================================
# SIMULATION TICK
# =========================================================

def run_tick():
    world = st.session_state.world
    factions = st.session_state.factions

    factions = evolve_factions(world, factions)
    st.session_state.factions = factions

    city = generate_city_state(factions)

    snapshot = {
        "id": str(uuid.uuid4())[:6],
        "time": datetime.now().isoformat(),
        "factions": factions.copy(),
        "city": city
    }

    st.session_state.history.append(snapshot)

# =========================================================
# UI
# =========================================================

st.title("🌍 V20 Civilization Engine — Playable Prototype")
st.caption("AI factions evolve, compete, and shape an architectural world")

# =========================================================
# SIDEBAR WORLD CONTROL
# =========================================================

st.sidebar.header("🌐 World Controls")

st.session_state.world["innovation_pressure"] = st.sidebar.slider(
    "Innovation Pressure",
    0.0, 2.0,
    st.session_state.world["innovation_pressure"]
)

st.session_state.world["material_cost_index"] = st.sidebar.slider(
    "Material Cost Index",
    0.5, 3.0,
    st.session_state.world["material_cost_index"]
)

st.session_state.world["population_density"] = st.sidebar.slider(
    "Population Density",
    0.1, 2.0,
    st.session_state.world["population_density"]
)

# =========================================================
# CONTROL BUTTONS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Run Simulation Tick", use_container_width=True):
        run_tick()

with col2:
    if st.button("⚡ Run 5 Ticks"):
        for _ in range(5):
            run_tick()

with col3:
    if st.button("🧨 Reset Civilization"):
        st.session_state.factions = {
            "Structural": 1.0,
            "Economy": 1.0,
            "Innovation": 1.0,
            "Sustainability": 1.0,
            "Compliance": 1.0
        }
        st.session_state.history = []

# =========================================================
# FACTION STATUS
# =========================================================

st.subheader("🏛 Faction Power Dynamics")

st.json(st.session_state.factions)

# =========================================================
# CITY OUTPUT
# =========================================================

if st.session_state.factions:
    city = generate_city_state(st.session_state.factions)

    st.subheader("🏙 City State Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Stability", f"{city['stability']}%")
    c2.metric("Innovation", f"{city['innovation_index']}%")
    c3.metric("Economy Pressure", f"{city['economic_pressure']}%")
    c4.metric("Sustainability", f"{city['sustainability']}%")

# =========================================================
# EVOLUTION HISTORY
# =========================================================

st.subheader("📈 Civilization Timeline")

if st.session_state.history:
    stability_series = [h["city"]["stability"] for h in st.session_state.history]
    innovation_series = [h["city"]["innovation_index"] for h in st.session_state.history]

    st.line_chart({
        "Stability": stability_series,
        "Innovation": innovation_series
    })
else:
    st.info("Run simulation ticks to evolve the civilization.")

# =========================================================
# LIVE SNAPSHOTS
# =========================================================

st.subheader("🧬 Recent Civilization Events")

for h in reversed(st.session_state.history[-5:]):
    st.write(
        f"🧠 Tick {h['id']} → "
        f"Stability {h['city']['stability']}% | "
        f"Innovation {h['city']['innovation_index']}%"
    )