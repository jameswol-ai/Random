# =========================================================
# RANDOM V3
# Autonomous Architecture Operating System
# Single-File Streamlit Edition
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V3",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# MEMORY
# =========================================================

DEFAULT_MEMORY = {
    "projects": [],
    "agents": [],
    "engines": [],
    "designs": [],
    "cities": [],
    "knowledge": []
}


def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


memory = load_memory()

# =========================================================
# ENGINE REGISTRY
# =========================================================

ENGINE_REGISTRY = [
    "Room Engine",
    "Adjacency Engine",
    "Grid Engine",
    "Layout Engine",
    "Structural Engine",
    "Optimizer Engine"
]

# =========================================================
# AGENT REGISTRY
# =========================================================

AGENTS = [
    "Architect Agent",
    "Engineer Agent",
    "Planner Agent",
    "Optimizer Agent"
]

# =========================================================
# ARCHITECTURE BRAIN
# =========================================================

def generate_rooms(building_type, bedrooms):

    rooms = []

    if building_type == "House":
        rooms = [
            "Living Room",
            "Dining Room",
            "Kitchen"
        ]

        for i in range(bedrooms):
            rooms.append(f"Bedroom {i+1}")

        rooms.append("Bathroom")

    elif building_type == "School":
        rooms = [
            "Classrooms",
            "Library",
            "Laboratory",
            "Administration",
            "Assembly Hall"
        ]

    elif building_type == "Office":
        rooms = [
            "Reception",
            "Meeting Room",
            "Open Office",
            "Director Office",
            "Break Room"
        ]

    return rooms


def generate_adjacency(rooms):

    adjacency = {}

    for i in range(len(rooms)-1):
        adjacency[rooms[i]] = [rooms[i+1]]

    return adjacency


def generate_grid():

    return {
        "x": ["A", "B", "C", "D"],
        "y": ["1", "2", "3", "4"],
        "spacing": "6m x 6m"
    }


# =========================================================
# PROJECTS
# =========================================================

def create_project(name, ptype):

    project = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "type": ptype,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    memory["projects"].append(project)
    save_memory(memory)

    return project

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏗 RANDOM V3")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Projects",
        "Design Studio",
        "Agents",
        "Engines",
        "Memory"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🏗 RANDOM V3")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Projects", len(memory["projects"]))
    c2.metric("Agents", len(AGENTS))
    c3.metric("Engines", len(ENGINE_REGISTRY))
    c4.metric("Designs", len(memory["designs"]))

    st.markdown("---")

    st.subheader("System Status")

    st.success("RANDOM Core Online")

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":

    st.title("📁 Projects")

    with st.form("project_form"):

        pname = st.text_input("Project Name")

        ptype = st.selectbox(
            "Type",
            ["House", "School", "Office"]
        )

        submit = st.form_submit_button("Create Project")

    if submit and pname:

        p = create_project(pname, ptype)

        st.success(
            f"Created Project {p['name']} ({p['id']})"
        )

    st.markdown("---")

    for p in memory["projects"]:
        st.write(p)

# =========================================================
# DESIGN STUDIO
# =========================================================

elif page == "Design Studio":

    st.title("🏠 Design Studio")

    building = st.selectbox(
        "Building Type",
        ["House", "School", "Office"]
    )

    bedrooms = st.slider(
        "Bedrooms",
        1,
        10,
        3
    )

    if st.button("Generate Design"):

        rooms = generate_rooms(
            building,
            bedrooms
        )

        adjacency = generate_adjacency(rooms)

        grid = generate_grid()

        design = {
            "building": building,
            "rooms": rooms,
            "adjacency": adjacency,
            "grid": grid
        }

        memory["designs"].append(design)

        save_memory(memory)

        st.success("Design Generated")

        st.subheader("Rooms")
        st.write(rooms)

        st.subheader("Adjacency")
        st.json(adjacency)

        st.subheader("Grid")
        st.json(grid)

# =========================================================
# AGENTS
# =========================================================

elif page == "Agents":

    st.title("🤖 Agents")

    for agent in AGENTS:
        st.success(agent)

# =========================================================
# ENGINES
# =========================================================

elif page == "Engines":

    st.title("⚙ Engine Registry")

    for engine in ENGINE_REGISTRY:
        st.info(engine)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.title("🧠 Memory")

    st.json(memory)
