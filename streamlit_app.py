# =========================================================
# RANDOM V2
# Autonomous Architecture Operating System
# =========================================================

import streamlit as st
import json
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V2",
    layout="wide"
)

# =========================================================
# SAFE IMPORTS
# =========================================================

try:
    from engines.room_engine import RoomEngine
except:
    RoomEngine = None

try:
    from engines.adjacency_engine import AdjacencyEngine
except:
    AdjacencyEngine = None

try:
    from engines.grid_engine import GridEngine
except:
    GridEngine = None

try:
    from engines.layout_engine import LayoutEngine
except:
    LayoutEngine = None

try:
    from engines.structural_grid_engine import StructuralGridEngine
except:
    StructuralGridEngine = None

# =========================================================
# MEMORY
# =========================================================

MEMORY_FILE = Path("random_memory.json")

def load_memory():

    if MEMORY_FILE.exists():

        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    return {}

memory = load_memory()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏗 RANDOM V2")

module = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Room Programming",
        "Adjacency",
        "Grid Generator",
        "Floor Plan",
        "Structural Grid",
        "Memory"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if module == "Dashboard":

    st.title("🏗 RANDOM V2")

    st.markdown("""
    ### Autonomous Architecture Operating System

    Current Development Phase

    ✅ Room Programming Engine

    ✅ Adjacency Engine

    ✅ Grid Generator

    ⏳ Floor Plan Renderer

    ⏳ Structural Grid Generator

    ⏳ Eurocode Engine

    ⏳ BIM Export
    """)

# =========================================================
# ROOM PROGRAMMING
# =========================================================

elif module == "Room Programming":

    st.header("Room Programming Engine")

    building_type = st.selectbox(
        "Building Type",
        [
            "School",
            "Hospital",
            "Office",
            "Residential"
        ]
    )

    occupants = st.number_input(
        "Occupants",
        min_value=10,
        value=500
    )

    if st.button("Generate Program"):

        if RoomEngine:

            engine = RoomEngine()

            rooms = engine.generate(
                building_type,
                occupants
            )

            st.json(rooms)

        else:

            st.warning(
                "room_engine.py not found"
            )

# =========================================================
# ADJACENCY
# =========================================================

elif module == "Adjacency":

    st.header("Adjacency Engine")

    if st.button("Generate Adjacency"):

        if AdjacencyEngine:

            engine = AdjacencyEngine()

            data = engine.generate()

            st.json(data)

        else:

            st.warning(
                "adjacency_engine.py not found"
            )

# =========================================================
# GRID GENERATOR
# =========================================================

elif module == "Grid Generator":

    st.header("Grid Generator")

    width = st.number_input(
        "Width (m)",
        value=60
    )

    length = st.number_input(
        "Length (m)",
        value=90
    )

    spacing = st.number_input(
        "Grid Spacing",
        value=8
    )

    if st.button("Generate Grid"):

        if GridEngine:

            engine = GridEngine()

            grid = engine.generate(
                width,
                length,
                spacing
            )

            st.json(grid)

        else:

            st.warning(
                "grid_engine.py not found"
            )

# =========================================================
# FLOOR PLAN
# =========================================================

elif module == "Floor Plan":

    st.header("Floor Plan Generator")

    if st.button("Generate Floor Plan"):

        if LayoutEngine:

            engine = LayoutEngine()

            fig = engine.generate()

            st.pyplot(fig)

        else:

            st.warning(
                "layout_engine.py not found"
            )

# =========================================================
# STRUCTURAL GRID
# =========================================================

elif module == "Structural Grid":

    st.header("Structural Grid Generator")

    if st.button("Generate Structure"):

        if StructuralGridEngine:

            engine = StructuralGridEngine()

            structure = engine.generate()

            st.json(structure)

        else:

            st.warning(
                "structural_grid_engine.py not found"
            )

# =========================================================
# MEMORY
# =========================================================

elif module == "Memory":

    st.header("Memory")

    st.json(memory)

# =========================================================
# FOOTER
# =========================================================

st.sidebar.markdown("---")
st.sidebar.caption(
    "RANDOM V2 • Autonomous Architecture OS"
    )
