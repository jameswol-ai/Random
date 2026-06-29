# =========================================================
# RANDOM V4
# Autonomous Architecture Operating System
# Improved Single-File Streamlit Edition
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
    page_title="RANDOM V4",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_MEMORY = {
    "projects": [],
    "designs": [],
    "logs": [],
    "knowledge": [],
    "agents": [],
    "engines": []
}


def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                for k in DEFAULT_MEMORY:
                    if k not in data:
                        data[k] = DEFAULT_MEMORY[k]
                return data
        except:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()


def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(st.session_state.memory, f, indent=4)


def log(message):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "message": message
    })
    save_memory()

# =========================================================
# INITIALIZE STATE
# =========================================================

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

memory = st.session_state.memory

# =========================================================
# ENGINE SYSTEM
# =========================================================

class Engine:
    def __init__(self, name):
        self.name = name

    def run(self, data):
        return data


class RoomEngine(Engine):
    def run(self, data):
        btype = data["type"]
        bedrooms = data.get("bedrooms", 1)

        if btype == "House":
            rooms = ["Living Room", "Kitchen", "Dining Room"]
            rooms += [f"Bedroom {i+1}" for i in range(bedrooms)]
            rooms.append("Bathroom")

        elif btype == "School":
            rooms = ["Classroom", "Library", "Lab", "Admin", "Hall"]

        else:
            rooms = ["Open Office", "Meeting Room", "Workspace"]

        return {"rooms": rooms}


class GridEngine(Engine):
    def run(self, data):
        return {
            "grid": {
                "x": ["A", "B", "C", "D"],
                "y": ["1", "2", "3", "4"],
                "spacing": "6m x 6m"
            }
        }


class StructureEngine(Engine):
    def run(self, data):
        return {
            "structure": {
                "columns": random.randint(12, 24),
                "beams": random.randint(20, 40),
                "slabs": random.randint(6, 12),
                "foundation": "Strip Foundation"
            }
        }


class CostEngine(Engine):
    def run(self, data):
        return {
            "cost": {
                "estimate": random.randint(500000, 2500000),
                "currency": "USD"
            }
        }


ENGINES = [
    RoomEngine("Room Engine"),
    GridEngine("Grid Engine"),
    StructureEngine("Structure Engine"),
    CostEngine("Cost Engine")
]

# =========================================================
# AGENTS
# =========================================================

AGENTS = [
    "Architect Agent",
    "Engineer Agent",
    "Planner Agent",
    "Supervisor Agent"
]

# =========================================================
# CORE GENERATOR
# =========================================================

def run_engine_pipeline(project_type, bedrooms):
    data = {"type": project_type, "bedrooms": bedrooms}
    result = {}

    for engine in ENGINES:
        output = engine.run(data)
        result.update(output)

    return result


# =========================================================
# PROJECTS
# =========================================================

def create_project(name, ptype):
    project = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "type": ptype,
        "created": datetime.now().isoformat(),
        "designs": 0
    }

    memory["projects"].append(project)
    save_memory()
    log(f"Project created: {name}")

    return project


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏗 RANDOM V4")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Projects", "Design Studio", "Agents", "Engines", "Memory"]
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🏗 RANDOM V4 Core System")

    c1, c2, c3 = st.columns(3)

    c1.metric("Projects", len(memory["projects"]))
    c2.metric("Designs", len(memory["designs"]))
    c3.metric("Logs", len(memory["logs"]))

    st.markdown("---")

    st.subheader("Recent Activity")

    for log_item in memory["logs"][-5:]:
        st.write(f"🕒 {log_item['time']} → {log_item['message']}")

    st.success("System Online")

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":

    st.title("📁 Projects")

    with st.form("project_form"):
        name = st.text_input("Project Name")
        ptype = st.selectbox("Type", ["House", "School", "Office"])
        submit = st.form_submit_button("Create")

    if submit and name:
        create_project(name, ptype)
        st.success("Project Created")

    st.markdown("---")

    for p in memory["projects"]:
        st.write(p)

# =========================================================
# DESIGN STUDIO
# =========================================================

elif page == "Design Studio":

    st.title("🏠 Design Studio")

    building = st.selectbox("Building Type", ["House", "School", "Office"])
    bedrooms = st.slider("Bedrooms", 1, 10, 3)

    if st.button("Generate Design"):

        result = run_engine_pipeline(building, bedrooms)

        design = {
            "id": str(uuid.uuid4())[:8],
            "type": building,
            "bedrooms": bedrooms,
            "rooms": result.get("rooms", []),
            "grid": result.get("grid", {}),
            "structure": result.get("structure", {}),
            "cost": result.get("cost", {}),
            "created": datetime.now().isoformat()
        }

        memory["designs"].append(design)
        save_memory()

        log("Design generated")

        st.success("Design Generated")

        st.subheader("Rooms")
        st.write(design["rooms"])

        st.subheader("Grid")
        st.json(design["grid"])

        st.subheader("Structure")
        st.json(design["structure"])

        st.subheader("Cost")
        st.json(design["cost"])

# =========================================================
# AGENTS
# =========================================================

elif page == "Agents":

    st.title("🤖 Agents")

    for a in AGENTS:
        st.info(a)

# =========================================================
# ENGINES
# =========================================================

elif page == "Engines":

    st.title("⚙ Engines")

    for e in ENGINES:
        st.success(e.name)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.title("🧠 Memory System")

    st.json(memory)
