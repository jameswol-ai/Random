# =========================================================
# RANDOM V2 - AUTONOMOUS ARCHITECTURE & CIVILIZATION OS
# Unified Streamlit Edition
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
# MEMORY
# =========================================================

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass

    return {
        "projects": [],
        "cities": [],
        "history": []
    }

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

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
# FLOOR PLAN ENGINE
# =========================================================

def generate_floorplan(width, length, bedrooms):

    rooms = []

    rooms.append(("Living Room", width * 0.4))
    rooms.append(("Kitchen", width * 0.15))

    for i in range(bedrooms):
        rooms.append((f"Bedroom {i+1}", width * 0.15))

    rooms.append(("Bathroom", width * 0.10))

    return rooms

# =========================================================
# STRUCTURAL GRID ENGINE
# =========================================================

def create_grid(width, length, spacing=4):

    x = np.arange(0, width + spacing, spacing)
    y = np.arange(0, length + spacing, spacing)

    return x, y

# =========================================================
# EUROCODE ENGINE
# =========================================================

def eurocode_check(span):

    if span <= 8:
        return "PASS"

    return "REVIEW REQUIRED"

# =========================================================
# CIVILIZATION ENGINE
# =========================================================

def evolve_city():

    return {
        "population": random.randint(1000, 100000),
        "infrastructure": random.randint(1, 100),
        "happiness": random.randint(1, 100)
    }

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("RANDOM V2")

section = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Architecture AI",
        "Structural AI",
        "Eurocode",
        "Civilization",
        "Memory"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if section == "Dashboard":

    st.title("🏗️ RANDOM V2")

    col1, col2, col3 = st.columns(3)

    col1.metric("Engines", len(ENGINES))
    col2.metric("Projects", len(memory["projects"]))
    col3.metric("Cities", len(memory["cities"]))

    st.subheader("System Status")

    st.json(ENGINES)

# =========================================================
# ARCHITECTURE AI
# =========================================================

elif section == "Architecture AI":

    st.header("Floor Plan Generator")

    width = st.number_input("Width (m)", 10)
    length = st.number_input("Length (m)", 15)
    bedrooms = st.slider("Bedrooms", 1, 10, 3)

    if st.button("Generate Floor Plan"):

        rooms = generate_floorplan(width, length, bedrooms)

        st.success("Floor Plan Generated")

        for room in rooms:
            st.write(room)

# =========================================================
# STRUCTURAL AI
# =========================================================

elif section == "Structural AI":

    st.header("Structural Grid Generator")

    width = st.number_input("Building Width", 20)
    length = st.number_input("Building Length", 20)

    if st.button("Generate Grid"):

        x, y = create_grid(width, length)

        fig, ax = plt.subplots()

        for gx in x:
            ax.axvline(gx)

        for gy in y:
            ax.axhline(gy)

        ax.set_title("Structural Grid")

        st.pyplot(fig)

# =========================================================
# EUROCODE
# =========================================================

elif section == "Eurocode":

    st.header("Eurocode Span Check")

    span = st.number_input("Span (m)", 5.0)

    if st.button("Run Check"):

        result = eurocode_check(span)

        st.success(result)

# =========================================================
# CIVILIZATION
# =========================================================

elif section == "Civilization":

    st.header("City Evolution")

    if st.button("Evolve City"):

        city = evolve_city()

        memory["cities"].append(city)

        save_memory(memory)

        st.json(city)

# =========================================================
# MEMORY
# =========================================================

elif section == "Memory":

    st.header("Memory Core")

    st.json(memory)
