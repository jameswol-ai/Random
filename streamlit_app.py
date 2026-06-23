# =========================================================
# RANDOM AI — AUTONOMOUS CIVILIZATION OPERATING SYSTEM
# Single-file Streamlit Edition
# =========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import json
from pathlib import Path

st.set_page_config(page_title="RANDOM AI OS", layout="wide")

MEMORY_FILE = Path("random_memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except Exception:
            return []
    return []

def save_memory(data):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))

DEFAULTS = {
    "brain_logs": [],
    "memory": load_memory(),
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

class RandomBrain:
    def __init__(self):
        self.awareness = random.random()
        self.intelligence = random.random()

    def think(self, text):
        return {
            "intent": text,
            "complexity": len(text.split()),
            "priority": random.choice(["housing","industry","transport"])
        }

    def evolve(self):
        self.awareness = min(1, max(0, self.awareness + random.uniform(-0.05,0.05)))
        self.intelligence = min(1, max(0, self.intelligence + random.uniform(-0.05,0.05)))

class EvolutionEngine:
    def __init__(self):
        self.generation = 1

    def evolve(self):
        self.generation += 1
        return {
            "generation": self.generation,
            "capabilities": random.randint(1,5)
        }

class AutoArchitectureForge:
    def __init__(self):
        self.engines = {}

    def create_engine(self, name, purpose):
        self.engines[name] = {
            "purpose": purpose,
            "version": 1.0
        }

    def run_engine(self, name, data):
        if name not in self.engines:
            return {"error":"engine_not_found"}
        return {
            "engine": name,
            "input": data,
            "status": "active"
        }

if "brain" not in st.session_state:
    st.session_state.brain = RandomBrain()

if "evolution" not in st.session_state:
    st.session_state.evolution = EvolutionEngine()

if "forge" not in st.session_state:
    st.session_state.forge = AutoArchitectureForge()

brain = st.session_state.brain
evolution = st.session_state.evolution
forge = st.session_state.forge

st.title("🏗️ RANDOM AI OS")

mode = st.sidebar.selectbox(
    "Module",
    [
        "Brain",
        "Architecture",
        "City",
        "Agents",
        "Memory",
        "Evolution",
        "Forge"
    ]
)

if mode == "Brain":
    txt = st.text_area("Intent")
    if st.button("Think"):
        result = brain.think(txt)
        brain.evolve()
        st.json(result)
    st.json({
        "awareness": brain.awareness,
        "intelligence": brain.intelligence
    })

elif mode == "Architecture":
    area = st.number_input("Site Area", 100.0, 100000.0, 1000.0)
    floors = st.slider("Floors", 1, 100, 10)

    if st.button("Generate Building"):
        rooms = []
        for i in range(max(4, int(area / 100))):
            rooms.append({
                "room": i + 1,
                "size": random.randint(10, 40)
            })

        st.json({
            "site_area": area,
            "floors": floors,
            "rooms": rooms
        })

    if st.button("Generate Structural Grid"):
        width = int(np.sqrt(area))
        cols = []
        for x in range(0, width, 6):
            for y in range(0, width, 6):
                cols.append({"x": x, "y": y})

        st.json({
            "column_count": len(cols),
            "columns": cols[:50]
        })

elif mode == "City":
    if st.button("Run City Step"):
        stability = random.random()
        reward = random.random()

        fig = plt.figure()
        plt.bar(["stability", "reward"], [stability, reward])
        st.pyplot(fig)

        st.json({
            "stability": stability,
            "reward": reward
        })

elif mode == "Agents":
    st.json({
        "planner": random.choice(["housing","industry","transport"]),
        "diplomacy": random.choice(["alliance","trade","negotiation"]),
        "war": random.choice(["peace","defense","conflict"])
    })

elif mode == "Memory":
    st.json(st.session_state.memory)

    entry = st.text_input("Add Memory")
    if st.button("Save Memory"):
        st.session_state.memory.append(entry)
        save_memory(st.session_state.memory)
        st.success("Saved")

elif mode == "Evolution":
    if st.button("Evolve"):
        result = evolution.evolve()
        st.session_state.memory.append(result)
        save_memory(st.session_state.memory)
        st.json(result)

elif mode == "Forge":
    name = st.text_input("Engine Name", "VisionEngine")
    purpose = st.text_input("Purpose", "analysis")

    if st.button("Forge"):
        forge.create_engine(name, purpose)
        st.success("Engine Created")

    st.json(forge.engines)

    data = st.text_area("Input Data", "test")

    if st.button("Run Engine"):
        st.json(forge.run_engine(name, data))
