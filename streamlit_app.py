# =========================================================
# 🏗️ RANDOM V2 — AUTONOMOUS ARCHITECTURE & CIVILIZATION OS
# Clean Core (No Forex, No SAI, No External Plugins)
# =========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="RANDOM V2 - Civilization OS",
    layout="wide"
)

st.title("🏗️ RANDOM V2 — Autonomous Architecture & Civilization OS")
st.caption("A self-growing system for cities, structures, and simulated worlds")

# =========================================================
# MEMORY CORE (Lightweight In-Memory Store)
# =========================================================
class MemoryCore:
    def __init__(self):
        if "memory" not in st.session_state:
            st.session_state.memory = []

    def save(self, item):
        st.session_state.memory.append({
            "timestamp": time.time(),
            "data": item
        })

    def load(self):
        return st.session_state.memory


memory = MemoryCore()

# =========================================================
# ARCHITECTURE ENGINE
# =========================================================
class ArchitectureEngine:
    def generate_floor_plan(self, width=10, height=10, rooms=5):
        grid = np.zeros((height, width))

        for r in range(1, rooms + 1):
            x = random.randint(0, width - 2)
            y = random.randint(0, height - 2)

            w = random.randint(2, 4)
            h = random.randint(2, 4)

            grid[y:y+h, x:x+w] = r

        return grid

    def structural_score(self, grid):
        density = np.count_nonzero(grid) / grid.size
        balance = 1 - abs(np.mean(grid) - np.median(grid)) / (np.max(grid) + 1)

        score = (density * 0.6 + balance * 0.4) * 100
        return round(score, 2)


arch = ArchitectureEngine()

# =========================================================
# CIVILIZATION ENGINE
# =========================================================
class CivilizationEngine:
    def generate_city(self, size=20):
        city = np.zeros((size, size))

        # roads
        city[:, size // 2] = 1
        city[size // 2, :] = 1

        # buildings
        for _ in range(size * 2):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            if city[y, x] == 0:
                city[y, x] = random.randint(2, 5)

        return city

    def population_estimate(self, city):
        return int(np.count_nonzero(city) * random.randint(10, 50))


city_engine = CivilizationEngine()

# =========================================================
# SIMULATION ENGINE
# =========================================================
class SimulationEngine:
    def evolve(self, city, steps=5):
        history = [city.copy()]

        for _ in range(steps):
            new_city = city.copy()

            x, y = random.randint(0, city.shape[0]-1), random.randint(0, city.shape[1]-1)
            new_city[x, y] = random.randint(1, 5)

            history.append(new_city)
            city = new_city

        return history


sim_engine = SimulationEngine()

# =========================================================
# UI SIDEBAR CONTROL PANEL
# =========================================================
mode = st.sidebar.radio(
    "🧭 System Mode",
    [
        "🏗️ Architecture Generator",
        "🌆 City Generator",
        "🌍 Civilization Simulation",
        "🧠 Memory Archive"
    ]
)

# =========================================================
# ARCHITECTURE MODE
# =========================================================
if mode == "🏗️ Architecture Generator":
    st.subheader("🏗️ Floor Plan Generator")

    w = st.slider("Width", 5, 30, 10)
    h = st.slider("Height", 5, 30, 10)
    r = st.slider("Rooms", 1, 10, 5)

    if st.button("Generate Floor Plan"):
        grid = arch.generate_floor_plan(w, h, r)
        score = arch.structural_score(grid)

        fig, ax = plt.subplots()
        ax.imshow(grid, cmap="viridis")
        st.pyplot(fig)

        st.success(f"Structural Integrity Score: {score}")

        memory.save({
            "type": "floor_plan",
            "score": score
        })

# =========================================================
# CITY MODE
# =========================================================
elif mode == "🌆 City Generator":
    st.subheader("🌆 Procedural City Generator")

    size = st.slider("City Size", 10, 60, 20)

    if st.button("Generate City"):
        city = city_engine.generate_city(size)
        pop = city_engine.population_estimate(city)

        fig, ax = plt.subplots()
        ax.imshow(city, cmap="coolwarm")
        st.pyplot(fig)

        st.info(f"Estimated Population: {pop}")

        memory.save({
            "type": "city",
            "population": pop
        })

# =========================================================
# SIMULATION MODE
# =========================================================
elif mode == "🌍 Civilization Simulation":
    st.subheader("🌍 City Evolution Simulator")

    size = st.slider("Base City Size", 10, 40, 20)
    steps = st.slider("Evolution Steps", 1, 15, 5)

    if st.button("Run Simulation"):
        city = city_engine.generate_city(size)
        history = sim_engine.evolve(city, steps)

        fig, ax = plt.subplots()

        for i, state in enumerate(history):
            ax.clear()
            ax.imshow(state, cmap="plasma")
            ax.set_title(f"Step {i}")
            st.pyplot(fig)
            time.sleep(0.3)

        memory.save({
            "type": "simulation",
            "steps": steps
        })

# =========================================================
# MEMORY MODE
# =========================================================
elif mode == "🧠 Memory Archive":
    st.subheader("🧠 System Memory")

    data = memory.load()

    if not data:
        st.warning("Memory is empty.")
    else:
        for i, item in enumerate(data[::-1]):
            st.write(f"{i+1}. {item}")
