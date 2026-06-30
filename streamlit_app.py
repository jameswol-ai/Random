# =========================================================
# ARC BIM CORE — LEVEL 5 (REVIT-STYLE DIGITAL TWIN ENGINE)
# Parametric BIM Graph + Structural Intelligence + Versioning
# =========================================================

import streamlit as st
import json
import uuid
import random
import math
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="ARC BIM CORE L5",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_bim_core_l5.json")

# =========================================================
# STYLE (REVIT-LIKE DARK UI)
# =========================================================

st.markdown("""
<style>
body {
    background-color: #0b0f1a;
    color: #e5e7eb;
    font-family: Inter, sans-serif;
}

h1, h2, h3 {
    color: #60a5fa;
}

.bim-canvas {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
    padding: 15px;
}

.bim-element {
    background: #111827;
    border: 1px solid #1f2937;
    padding: 12px;
    border-radius: 10px;
}

.tag {
    font-size: 11px;
    color: #93c5fd;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM (REVIT PROJECT FILES)
# =========================================================

DEFAULT = {
    "projects": [],
    "active_project": None,
    "logs": []
}

def load():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE))
        except:
            return DEFAULT.copy()
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

# =========================================================
# BIM OBJECT MODEL (REVIT-LIKE FAMILY SYSTEM)
# =========================================================

def nid(prefix):
    return f"{prefix}-{str(uuid.uuid4())[:8]}"

def create_level(i):
    return {
        "id": nid("LVL"),
        "type": "Level",
        "elevation": i * 3.2,
        "index": i
    }

def create_wall(level_id):
    return {
        "id": nid("WAL"),
        "type": "Wall",
        "level": level_id,
        "height": 3.2,
        "material": random.choice(["Concrete", "Glass", "Brick"]),
        "length": random.randint(4, 12)
    }

def create_column(level_id):
    return {
        "id": nid("COL"),
        "type": "Column",
        "level": level_id,
        "load_capacity": random.randint(500, 2500),
        "stress": random.randint(100, 1800)
    }

def create_room(level_id, name):
    return {
        "id": nid("RM"),
        "type": "Room",
        "level": level_id,
        "area": random.randint(12, 80),
        "occupancy": random.randint(1, 6),
        "lighting": random.uniform(0.3, 1.0),
        "heat_gain": random.uniform(0.2, 1.0),
        "name": name
    }

# =========================================================
# BIM PROJECT GENERATOR (REVIT PROJECT FILE SIMULATION)
# =========================================================

def generate_project(levels=3, rooms_per_level=4):

    nodes = []
    relations = []

    level_ids = []

    for i in range(levels):
        lvl = create_level(i)
        nodes.append(lvl)
        level_ids.append(lvl["id"])

        # structural system
        for _ in range(random.randint(6, 10)):
            col = create_column(lvl["id"])
            nodes.append(col)
            relations.append((lvl["id"], col["id"], "supports"))

        for _ in range(random.randint(4, 8)):
            wall = create_wall(lvl["id"])
            nodes.append(wall)
            relations.append((lvl["id"], wall["id"], "hosts"))

        # rooms
        for r in range(rooms_per_level):
            room = create_room(lvl["id"], f"Room {i}-{r}")
            nodes.append(room)
            relations.append((lvl["id"], room["id"], "contains"))

    return {
        "id": nid("PRJ"),
        "created": datetime.now().isoformat(),
        "nodes": nodes,
        "relations": relations,
        "levels": levels
    }

# =========================================================
# STRUCTURAL ANALYSIS ENGINE (REVIT ANALYTICAL MODEL)
# =========================================================

def structural_analysis(project):

    stress_values = []
    overload = 0

    for n in project["nodes"]:
        if n["type"] == "Column":
            stress_values.append(n["stress"])
            if n["stress"] > n["load_capacity"] * 0.75:
                overload += 1

    return {
        "avg_stress": round(sum(stress_values) / max(1, len(stress_values)), 2),
        "max_stress": max(stress_values) if stress_values else 0,
        "overloaded_elements": overload
    }

# =========================================================
# ENVIRONMENT SIMULATION (LIGHT BIM TWIN LAYER)
# =========================================================

def env_analysis(project):

    heat = []
    light = []

    for n in project["nodes"]:
        if n["type"] == "Room":
            heat.append(n["heat_gain"])
            light.append(n["lighting"])

    return {
        "avg_heat": round(sum(heat) / max(1, len(heat)), 3),
        "avg_light": round(sum(light) / max(1, len(light)), 3),
        "comfort_index": round((sum(light) - sum(heat)) * 10, 2)
    }

# =========================================================
# BIM SELF-HEALING ENGINE (REVIT OPTIMIZATION LOOP)
# =========================================================

def optimize(project):

    for n in project["nodes"]:
        if n["type"] == "Column" and n["stress"] > n["load_capacity"]:
            n["load_capacity"] += 200

        if n["type"] == "Room" and n["heat_gain"] > 0.8:
            n["lighting"] += 0.1

    return project

# =========================================================
# REVIT-STYLE VISUALIZER
# =========================================================

def render_project(project):

    st.markdown("### 🏗️ BIM Model Explorer")

    for n in project["nodes"][:80]:
        st.markdown(
            f"""
            <div class="bim-element">
                <div><b>{n['type']}</b></div>
                <div class="tag">{n['id']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# UI (REVIT PROJECT BROWSER)
# =========================================================

st.sidebar.title("ARC BIM CORE L5")
page = st.sidebar.radio("Workspace", [
    "Project Browser",
    "Model Generator",
    "Digital Twin"
])

# =========================================================
# PROJECT BROWSER
# =========================================================

if page == "Project Browser":

    st.title("📁 BIM Project Browser")

    st.metric("Total Projects", len(mem["projects"]))

    for p in reversed(mem["projects"][-5:]):
        st.markdown(f"**{p['id']}** | Levels: {p['levels']} | Nodes: {len(p['nodes'])}")

    if st.button("Load Latest Project"):
        mem["active_project"] = mem["projects"][-1]
        log("Loaded project")

# =========================================================
# MODEL GENERATOR
# =========================================================

elif page == "Model Generator":

    st.title("🏗️ Parametric BIM Generator")

    levels = st.slider("Levels", 1, 10, 3)
    rooms = st.slider("Rooms per Level", 1, 8, 3)

    if st.button("Generate BIM Model"):

        project = generate_project(levels, rooms)
        project = optimize(project)

        mem["projects"].append(project)
        mem["active_project"] = project

        log("Generated BIM model")

        st.success("BIM Model Generated")

        st.json(project)

# =========================================================
# DIGITAL TWIN VIEW
# =========================================================

elif page == "Digital Twin":

    st.title("🧠 BIM Digital Twin")

    project = mem.get("active_project")

    if not project:
        st.warning("No active model loaded.")
    else:

        st.subheader("Structural Analysis")
        st.json(structural_analysis(project))

        st.subheader("Environmental Analysis")
        st.json(env_analysis(project))

        st.subheader("Model Explorer")
        render_project(project)

        if st.button("Run Self-Optimization Loop"):
            mem["active_project"] = optimize(project)
            log("Self-optimization executed")
            st.rerun()
