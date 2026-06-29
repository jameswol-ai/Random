# =========================================================
# RANDOM V5
# Autonomous Architecture Operating System
# Single-File Streamlit Edition
# =========================================================

import streamlit as st
import json
import uuid
import random
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V5",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# THEME
# =========================================================

st.markdown("""
<style>
body {
    background-color: #0b1220;
}
.main {
    background: linear-gradient(180deg,#0b1220,#0f172a);
}
h1,h2,h3 {
    color: #38bdf8;
}
.stMetric {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1f2937;
}
.stButton>button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

DEFAULT = {
    "projects": [],
    "designs": [],
    "logs": [],
    "knowledge": [],
    "agents": [],
    "settings": {}
}

def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            for k in DEFAULT:
                data.setdefault(k, DEFAULT[k])
            return data
    return DEFAULT.copy()

def save():
    with open(MEMORY_FILE, "w") as f:
        json.dump(st.session_state.memory, f, indent=2)

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory

# =========================================================
# ENGINE SYSTEM
# =========================================================

class Engine:
    def __init__(self, name):
        self.name = name

    def run(self, data):
        return {}

class RoomEngine(Engine):
    def run(self, data):
        t = data["type"]
        b = data.get("bedrooms", 1)

        base = ["Living", "Kitchen", "Dining"]

        if t == "House":
            rooms = base + [f"Bedroom {i+1}" for i in range(b)] + ["Bath"]
        elif t == "School":
            rooms = ["Classroom", "Lab", "Library", "Admin"]
        elif t == "Hospital":
            rooms = ["Ward", "ER", "Surgery", "Pharmacy"]
        else:
            rooms = ["Workspace", "Meeting", "Open Area"]

        return {"rooms": rooms}

class GridEngine(Engine):
    def run(self, data):
        return {
            "grid": {
                "x": list("ABCDE"),
                "y": [1,2,3,4,5],
                "spacing": "6m x 6m"
            }
        }

class StructureEngine(Engine):
    def run(self, data):
        return {
            "structure": {
                "columns": random.randint(10, 30),
                "beams": random.randint(20, 60),
                "slabs": random.randint(5, 15),
                "foundation": "Strip"
            }
        }

class CostEngine(Engine):
    def run(self, data):
        return {
            "cost": {
                "estimate": random.randint(200000, 3000000),
                "currency": "USD"
            }
        }

ENGINES = [
    RoomEngine("Room"),
    GridEngine("Grid"),
    StructureEngine("Structure"),
    CostEngine("Cost")
]

# =========================================================
# AGENTS
# =========================================================

AGENTS = [
    "Chief Architect",
    "Structural Engineer",
    "Civil Engineer",
    "Project Manager",
    "Quantity Surveyor"
]

# =========================================================
# PIPELINE
# =========================================================

def generate_design(btype, bedrooms):
    data = {"type": btype, "bedrooms": bedrooms}
    result = {}

    for e in ENGINES:
        result.update(e.run(data))

    return result

# =========================================================
# PROJECTS
# =========================================================

def new_project(name, ptype):
    p = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "type": ptype,
        "created": datetime.now().isoformat()
    }
    mem["projects"].append(p)
    save()
    log(f"Project created {name}")
    return p

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏗 RANDOM V5")
page = st.sidebar.radio("Navigate", [
    "Dashboard",
    "Projects",
    "Design Studio",
    "Agents",
    "Engines",
    "Memory"
])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🏗 RANDOM V5 Control Center")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Logs", len(mem["logs"]))
    c4.metric("Agents", len(AGENTS))

    st.divider()
    st.subheader("Activity Log")

    for l in mem["logs"][-8:]:
        st.write(f"{l['time']} → {l['msg']}")

    st.success("System Operational")

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":

    st.title("📁 Projects")

    name = st.text_input("Project Name")
    ptype = st.selectbox("Type", ["House","School","Hospital","Office"])

    if st.button("Create Project"):
        new_project(name, ptype)
        st.success("Created")

    st.divider()

    for p in mem["projects"]:
        with st.expander(f"📁 {p['name']}"):
            st.write(p)

# =========================================================
# DESIGN STUDIO
# =========================================================

elif page == "Design Studio":

    st.title("🏠 AI Design Studio")

    left,right = st.columns([1,2])

    with left:
        btype = st.selectbox("Building", ["House","School","Hospital","Office"])
        bedrooms = st.slider("Bedrooms",1,10,3)
        go = st.button("Generate Design")

    with right:
        st.info("AI engines generate architectural systems automatically.")

    if go:

        design = generate_design(btype, bedrooms)

        entry = {
            "id": str(uuid.uuid4())[:8],
            "type": btype,
            "bedrooms": bedrooms,
            "data": design,
            "created": datetime.now().isoformat()
        }

        mem["designs"].append(entry)
        save()
        log("Design generated")

        st.success("Design Created")

        tab1,tab2,tab3,tab4 = st.tabs([
            "Rooms","Grid","Structure","Cost"
        ])

        with tab1:
            st.write(design.get("rooms"))

        with tab2:
            st.json(design.get("grid"))

        with tab3:
            st.json(design.get("structure"))

        with tab4:
            st.json(design.get("cost"))

# =========================================================
# AGENTS
# =========================================================

elif page == "Agents":

    st.title("🤖 AI Agents")

    for a in AGENTS:
        st.success(f"🟢 {a}")

# =========================================================
# ENGINES
# =========================================================

elif page == "Engines":

    st.title("⚙ Engine Registry")

    for e in ENGINES:
        st.info(e.name)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.title("🧠 System Memory")

    tab1,tab2,tab3 = st.tabs(["Projects","Designs","Logs"])

    with tab1:
        st.json(mem["projects"])

    with tab2:
        st.json(mem["designs"])

    with tab3:
        st.json(mem["logs"])
