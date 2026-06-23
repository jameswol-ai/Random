# =========================================================
# 🏗️ RANDOM V2 — AUTONOMOUS CIVILIZATION OPERATING SYSTEM
# Unified Core (Brain + Architecture + Eurocode + Evolution)
# =========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import json
import time
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="RANDOM V2 OS", layout="wide")

st.title("🏗️ RANDOM V2 — Civilization Operating System")
st.caption("A self-evolving architecture + city intelligence engine")

# =========================================================
# MEMORY (PERSISTENT)
# =========================================================
MEMORY_FILE = Path("random_memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except:
            return []
    return []

def save_memory(data):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

# =========================================================
# 🧠 BRAIN
# =========================================================
class RandomBrain:
    def __init__(self):
        self.awareness = random.random()
        self.intelligence = random.random()

    def think(self, text):
        return {
            "intent": text,
            "complexity": len(text.split()),
            "domain": random.choice(["housing", "industry", "transport", "mixed-use"])
        }

    def evolve(self):
        self.awareness = min(1, max(0, self.awareness + random.uniform(-0.05, 0.05)))
        self.intelligence = min(1, max(0, self.intelligence + random.uniform(-0.05, 0.05)))

brain = RandomBrain()

# =========================================================
# 🏗️ ARCHITECTURE ENGINE
# =========================================================
class ArchitectureEngine:
    def generate_floor_plan(self, w, h, rooms):
        grid = np.zeros((h, w))

        for r in range(1, rooms + 1):
            x = random.randint(0, w - 2)
            y = random.randint(0, h - 2)
            rw = random.randint(2, 4)
            rh = random.randint(2, 4)
            grid[y:y+rh, x:x+rw] = r

        return grid

arch = ArchitectureEngine()

# =========================================================
# ⚖️ EUROCODE-INSPIRED ENGINE
# =========================================================
class EurocodeEngine:
    def analyze(self, grid):
        void = np.sum(grid == 0) / grid.size
        density = np.count_nonzero(grid) / grid.size

        coords = np.argwhere(grid > 0)
        balance = 1 - np.linalg.norm(np.mean(coords, axis=0) - np.array(grid.shape)/2) / np.linalg.norm(grid.shape)

        aspect = max(grid.shape) / min(grid.shape)

        score = 100
        issues = []

        if void > 0.65:
            issues.append("Excessive void ratio")
            score -= 25

        if density < 0.2:
            issues.append("Low structural density")
            score -= 20

        if balance < 0.45:
            issues.append("Poor structural balance")
            score -= 20

        if aspect > 3.5:
            issues.append("Extreme aspect ratio")
            score -= 15

        return {
            "score": max(0, score),
            "void": round(float(void), 3),
            "density": round(float(density), 3),
            "balance": round(float(balance), 3),
            "issues": issues
        }

euro = EurocodeEngine()

# =========================================================
# 🔁 CRITIC + REPAIR
# =========================================================
class RepairEngine:
    def repair(self, grid):
        g = grid.copy()
        h, w = g.shape

        for _ in range(int(h * w * 0.1)):
            x = random.randint(0, h-1)
            y = random.randint(0, w-1)
            g[x, y] = random.randint(1, 3)

        return g

repair = RepairEngine()

def evolve_structure(grid, steps=3):
    history = []
    current = grid

    for _ in range(steps):
        report = euro.analyze(current)

        if report["score"] < 70:
            current = repair.repair(current)

        history.append((current.copy(), report))

    return history

# =========================================================
# 🌆 CITY ENGINE
# =========================================================
class CityEngine:
    def generate(self, size):
        city = np.zeros((size, size))
        city[:, size//2] = 1
        city[size//2, :] = 1

        for _ in range(size * 2):
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            city[x, y] = random.randint(2, 5)

        return city

city_engine = CityEngine()

# =========================================================
# UI MODE
# =========================================================
mode = st.sidebar.radio(
    "🧭 RANDOM OS MODE",
    [
        "🧠 Brain",
        "🏗️ Architecture Evolution",
        "🌆 City Generator",
        "🧠 Memory"
    ]
)

# =========================================================
# 🧠 BRAIN MODE
# =========================================================
if mode == "🧠 Brain":
    txt = st.text_area("Enter Intent")

    if st.button("Think"):
        brain.evolve()
        st.json(brain.think(txt))

    st.metric("Awareness", round(brain.awareness, 3))
    st.metric("Intelligence", round(brain.intelligence, 3))

# =========================================================
# 🏗️ ARCHITECTURE + EVOLUTION + EUROCODE
# =========================================================
elif mode == "🏗️ Architecture Evolution":
    w = st.slider("Width", 5, 30, 12)
    h = st.slider("Height", 5, 30, 12)
    r = st.slider("Rooms", 1, 10, 5)

    if st.button("Generate & Evolve Structure"):
        grid = arch.generate_floor_plan(w, h, r)
        history = evolve_structure(grid, steps=5)

        for i, (state, report) in enumerate(history):
            st.markdown(f"### Step {i+1}")

            fig, ax = plt.subplots()
            ax.imshow(state, cmap="viridis")
            st.pyplot(fig)

            st.metric("Score", report["score"])

            if report["issues"]:
                for issue in report["issues"]:
                    st.warning(issue)
            else:
                st.success("Structurally stable")

# =========================================================
# 🌆 CITY MODE
# =========================================================
elif mode == "🌆 City Generator":
    size = st.slider("City Size", 10, 50, 20)

    if st.button("Generate City"):
        city = city_engine.generate(size)

        fig, ax = plt.subplots()
        ax.imshow(city, cmap="coolwarm")
        st.pyplot(fig)

        st.success("City generated")

        st.session_state.memory.append({
            "type": "city",
            "size": size
        })
        save_memory(st.session_state.memory)

# =========================================================
# 🧠 MEMORY MODE
# =========================================================
elif mode == "🧠 Memory":
    st.json(st.session_state.memory)

    entry = st.text_input("Add Memory")

    if st.button("Save"):
        st.session_state.memory.append(entry)
        save_memory(st.session_state.memory)
        st.success("Saved")
