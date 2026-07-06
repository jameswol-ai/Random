# =========================================================
# V33 SIMULATION OS — STREAMLIT ENTRYPOINT
# Thin UI Layer (Orchestrates Modular Engine)
# =========================================================

import streamlit as st
import numpy as np

from world.voxel import VoxelWorld
from world.terrain import generate_terrain
from world.fluids import apply_gravity

from architecture.generator import generate_design
from evolution.evolutionary_loop import evolve_population

from meta.rule_engine import evolve_rules
from meta.observation import collect_stats

from memory.logger import log_event


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="V33 Simulation OS",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 V33 — Simulation Operating System")

# =========================================================
# SESSION INIT
# =========================================================

if "world" not in st.session_state:
    st.session_state.world = VoxelWorld(size=30)

if "agents" not in st.session_state:
    st.session_state.agents = [{"x": 15, "y": 15, "z": 10}]

if "design" not in st.session_state:
    st.session_state.design = None

if "history" not in st.session_state:
    st.session_state.history = []

world = st.session_state.world


# =========================================================
# SIDEBAR CONTROL PANEL
# =========================================================

st.sidebar.title("🧠 Control Panel")

if st.sidebar.button("🌍 Generate World"):
    world.grid = generate_terrain(world.size)
    log_event("World generated")

if st.sidebar.button("🌊 Simulate Step"):
    apply_gravity(world)
    stats = collect_stats(world, st.session_state.agents)

    evolve_rules(stats)
    log_event("Simulation step executed")

if st.sidebar.button("🏗 Evolve Architecture"):
    population = [generate_design() for _ in range(10)]
    best, history = evolve_population(population)

    st.session_state.design = best
    st.session_state.history = history

    log_event(f"Architecture evolved: {best['id']}")


# =========================================================
# WORLD VIEW
# =========================================================

st.subheader("🌐 World State")

voxel_count = np.count_nonzero(world.grid)

st.metric("Active Voxels", voxel_count)
st.metric("World Size", world.size)

st.text("Voxel Preview (compressed)")

preview = ""

for x in range(world.size):
    for y in range(world.size):
        z = int(np.argmax(world.grid[x, y]))
        val = world.grid[x, y, z]

        if val == 0:
            preview += "⬛"
        elif val == 1:
            preview += "🟩"
        elif val == 2:
            preview += "🟥"
        else:
            preview += "🟦"

st.text(preview[:1500])


# =========================================================
# ARCHITECTURE VIEW
# =========================================================

st.subheader("🏗 Latest Design Output")

if st.session_state.design:
    d = st.session_state.design

    col1, col2, col3 = st.columns(3)
    col1.metric("Fitness", round(d["fitness"], 2))
    col2.metric("Area", d["area"])
    col3.metric("Columns", d["columns"])

    st.json(d)
else:
    st.info("No design generated yet.")


# =========================================================
# SYSTEM ANALYTICS
# =========================================================

st.subheader("🧠 System Diagnostics")

stats = collect_stats(world, st.session_state.agents)

st.json({
    "voxels": voxel_count,
    "agents": len(st.session_state.agents),
    "rules": "adaptive",
    "simulation_health": "stable",
    "stats": stats
})


# =========================================================
# LIVE LOG OUTPUT
# =========================================================

st.subheader("📜 Event Log")

try:
    from memory.store import load_logs
    logs = load_logs()
    for l in logs[-10:]:
        st.caption(f"{l['time']} — {l['msg']}")
except:
    st.caption("Logging system initializing...")