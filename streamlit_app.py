# =========================================================
# RANDOM V6
# Autonomous Architecture Operating System
# Single-File Streamlit Edition
# =========================================================

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
    page_title="RANDOM V6",
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
# MEMORY SYSTEM (ROBUST)
# =========================================================

DEFAULT = {
    "projects": [],
    "designs": [],
    "logs": [],
    "knowledge": [],
    "agents": [],
    "settings": {}
}

def safe_load():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                for k in DEFAULT:
                    data.setdefault(k, DEFAULT[k])
                return data
        except:
            return DEFAULT.copy()
    return DEFAULT.copy()

def save():
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except:
        pass

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save()

if "memory" not in st.session_state:
    st.session_state.memory = safe_load()

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE DOMAINS (NEW IN V6)
# =========================================================

ARCHITECTURE_DOMAINS = {
    "Residential": ["House", "Apartment", "Villa"],
    "Commercial": ["Office", "School", "Hospital", "Hotel"],
    "Industrial": ["Warehouse", "Factory", "Plant"]
}

def get_domain(btype):
    for d, items in ARCHITECTURE_DOMAINS.items():
        if btype in items:
            return d
    return "Unknown"

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

        btype = data.get("type")
        domain = data.get("domain")
        bedrooms = data.get("bedrooms", 1)

        if domain == "Residential":
            rooms = ["Living Room", "Kitchen", "Dining Room"]
            rooms += [f"Bedroom {i+1}" for i in range(bedrooms)]
            rooms.append("Bathroom")

        elif domain == "Commercial":
            rooms = ["Reception", "Office Area", "Meeting Room", "Storage"]

        elif domain == "Industrial":
            rooms = ["Production Floor", "Storage Zone", "Loading Bay", "Control Room"]

        else:
            rooms = ["Generic Space"]

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
                "foundation": "Strip Foundation"
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

    domain = get_domain(btype)

    data = {
        "type": btype,
        "domain": domain,
        "bedrooms": bedrooms
    }

    result = {}

    for e in ENGINES:
        try:
            result.update(e.run(data))
        except:
            continue

    result["domain"] = domain
    return result

# =========================================================
# PROJECT SYSTEM
# =========================================================

def new_project(name, ptype):

    if not name:
        return None

    p = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "type": ptype,
        "created": datetime.now().isoformat()
    }

    mem["projects"].append(p)
    save()
    log(f"Project created: {name}")

    return p

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏗 RANDOM V6")

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

    st.title("🏗 RANDOM V6 Control Center")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Logs", len(mem["logs"]))
    c4.metric("Agents", len(AGENTS))

    st.divider()
    st.subheader("Activity Log")

    for l in mem["logs"][-8:]:
        msg = l.get("msg", "")
        time = l.get("time", "")
        st.write(f"{time} → {msg}")

    st.success("System Operational")

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":

    st.title("📁 Projects")

    name = st.text_input("Project Name")
    ptype = st.selectbox("Type", sum(ARCHITECTURE_DOMAINS.values(), []))

    if st.button("Create Project"):
        new_project(name, ptype)
        st.success("Created")

    st.divider()

    for p in mem["projects"]:
        with st.expander(f"📁 {p.get('name','Unnamed')}"):
            st.json(p)

# =========================================================
# DESIGN STUDIO
# =========================================================

elif page == "Design Studio":

    st.title("🏠 AI Design Studio")

    left, right = st.columns([1,2])

    with left:
        btype = st.selectbox("Building Type", sum(ARCHITECTURE_DOMAINS.values(), []))
        bedrooms = st.slider("Bedrooms", 1, 10, 3)
        go = st.button("Generate Design")

    with right:
        st.info("AI engines simulate architectural systems across domains.")

    if go:

        design = generate_design(btype, bedrooms)

        entry = {
            "id": str(uuid.uuid4())[:8],
            "type": btype,
            "domain": design["domain"],
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
