# =========================================================
# RANDOM V2
# Autonomous Architecture & Civilization OS
# Stable Unified Edition
# =========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import json
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V2",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# MEMORY CORE
# =========================================================

DEFAULT_MEMORY = {
    "projects": [],
    "cities": [],
    "history": []
}


def load_memory():

    if not MEMORY_FILE.exists():
        return DEFAULT_MEMORY.copy()

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return DEFAULT_MEMORY.copy()

        data.setdefault("projects", [])
        data.setdefault("cities", [])
        data.setdefault("history", [])

        return data

    except Exception:
        return DEFAULT_MEMORY.copy()


def save_memory(data):

    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Memory save error: {e}")


memory = load_memory()

# =========================================================
# ENGINE REGISTRY
# =========================================================

ENGINES = {
    "Architecture AI": "ACTIVE",
    "Structural AI": "ACTIVE",
    "Eurocode Engine": "ACTIVE",
    "Civilization Engine": "ACTIVE",
    "Memory Core": "ACTIVE"
}

# =========================================================
# ARCHITECTURE ENGINE
# =========================================================

def generate_floorplan(width, length, bedrooms):

    total_area = width * length

    rooms = [
        {
            "room": "Living Room",
            "area": round(total_area * 0.30, 2)
        },
        {
            "room": "Kitchen",
            "area": round(total_area * 0.15, 2)
        },
        {
            "room": "Bathroom",
            "area": round(total_area * 0.10, 2)
        }
    ]

    remaining = total_area - sum(r["area"] for r in rooms)

    bedroom_area = round(remaining / bedrooms, 2)

    for i in range(bedrooms):
        rooms.append({
            "room": f"Bedroom {i+1}",
            "area": bedroom_area
        })

    return rooms

# =========================================================
# STRUCTURAL GRID ENGINE
# =========================================================

def create_grid(width, length, spacing):

    x = np.arange(0, width + spacing, spacing)
    y = np.arange(0, length + spacing, spacing)

    return x, y

# =========================================================
# EUROCODE PLACEHOLDER
# =========================================================

def eurocode_check(span):

    if span <= 8:
        return {
            "status": "PASS",
            "message": "Span is within preliminary limits."
        }

    if span <= 12:
        return {
            "status": "WARNING",
            "message": "Detailed structural design recommended."
        }

    return {
        "status": "FAIL",
        "message": "Span exceeds preliminary limits."
    }

# =========================================================
# CIVILIZATION ENGINE
# =========================================================

def evolve_city():

    return {
        "population": random.randint(1000, 1000000),
        "infrastructure": random.randint(1, 100),
        "economy": random.randint(1, 100),
        "happiness": random.randint(1, 100)
    }

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏗️ RANDOM V2")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Architecture AI",
        "Structural AI",
        "Eurocode",
        "Civilization",
        "Projects",
        "Memory",
        "System Health"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🏗️ RANDOM V2")

    c1, c2, c3 = st.columns(3)

    c1.metric("Engines", len(ENGINES))
    c2.metric("Projects", len(memory.get("projects", [])))
    c3.metric("Cities", len(memory.get("cities", [])))

    st.subheader("Engine Registry")
    st.json(ENGINES)

# =========================================================
# ARCHITECTURE AI
# =========================================================

elif page == "Architecture AI":

    st.header("Floor Plan Generator")

    width = st.number_input(
        "Building Width (m)",
        min_value=5.0,
        value=12.0
    )

    length = st.number_input(
        "Building Length (m)",
        min_value=5.0,
        value=18.0
    )

    bedrooms = st.slider(
        "Bedrooms",
        1,
        10,
        3
    )

    if st.button("Generate Floor Plan"):

        rooms = generate_floorplan(
            width,
            length,
            bedrooms
        )

        st.success("Floor Plan Generated")

        total_area = width * length

        st.write(f"Total Area: {total_area:.2f} m²")

        for room in rooms:
            st.write(
                f"{room['room']} : {room['area']} m²"
            )

# =========================================================
# STRUCTURAL AI
# =========================================================

elif page == "Structural AI":

    st.header("Structural Grid Generator")

    width = st.number_input(
        "Grid Width",
        min_value=5.0,
        value=20.0
    )

    length = st.number_input(
        "Grid Length",
        min_value=5.0,
        value=20.0
    )

    spacing = st.number_input(
        "Grid Spacing",
        min_value=2.0,
        value=4.0
    )

    if st.button("Generate Grid"):

        x, y = create_grid(
            width,
            length,
            spacing
        )

        fig, ax = plt.subplots(figsize=(6, 6))

        for gx in x:
            ax.axvline(gx)

        for gy in y:
            ax.axhline(gy)

        ax.set_title("Structural Grid")
        ax.set_aspect("equal")

        st.pyplot(fig)

# =========================================================
# EUROCODE
# =========================================================

elif page == "Eurocode":

    st.header("Eurocode Span Checker")

    span = st.number_input(
        "Span (m)",
        min_value=1.0,
        value=6.0
    )

    if st.button("Run Check"):

        result = eurocode_check(span)

        st.subheader(result["status"])
        st.write(result["message"])

# =========================================================
# CIVILIZATION
# =========================================================

elif page == "Civilization":

    st.header("Civilization Simulator")

    if st.button("Evolve City"):

        city = evolve_city()

        memory["cities"].append(city)

        save_memory(memory)

        st.success("City Evolved")

        st.json(city)

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":

    st.header("Project Manager")

    project_name = st.text_input(
        "Project Name"
    )

    if st.button("Save Project"):

        if project_name.strip():

            memory["projects"].append({
                "name": project_name
            })

            save_memory(memory)

            st.success("Project Saved")

    st.subheader("Stored Projects")

    st.json(memory["projects"])

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.header("Memory Core")

    st.json(memory)

    if st.button("Reset Memory"):

        memory = DEFAULT_MEMORY.copy()

        save_memory(memory)

        st.success("Memory Reset")

# =========================================================
# SYSTEM HEALTH
# =========================================================

elif page == "System Health":

    st.header("System Health")

    st.write("Memory File Exists:")
    st.write(MEMORY_FILE.exists())

    st.write("Memory Type:")
    st.code(str(type(memory)))

    st.write("Projects:")
    st.code(str(len(memory.get("projects", []))))

    st.write("Cities:")
    st.code(str(len(memory.get("cities", []))))

    st.subheader("Loaded Memory")

    st.json(memory)

# =========================================================
# FOOTER
# =========================================================

st.sidebar.markdown("---")
st.sidebar.caption("RANDOM V2 Unified Stable Edition")
