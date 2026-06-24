# =========================================================
# 🧠 RANDOM V4.3 — CIVILIZATION CONSCIOUSNESS LAYER
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="RANDOM V4.3", layout="wide")

# =========================================================
# MEMORY CORE (CIVILIZATION SUBSTRATE)
# =========================================================

MEMORY_FILE = Path("random_memory.json")

DEFAULT_MEMORY = {
    "cities": [],
    "designs": [],
    "engines": [],
    "knowledge": [],
    "links": [],  # civilization graph edges
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            data = json.loads(MEMORY_FILE.read_text())
            for k in DEFAULT_MEMORY:
                if k not in data:
                    data[k] = DEFAULT_MEMORY[k]
            return data
        except:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

memory = load_memory()

# =========================================================
# 🧠 CIVILIZATION GRAPH LAYER
# =========================================================

def link(a, b, strength=None):
    memory["links"].append({
        "a": a,
        "b": b,
        "strength": strength or random.uniform(0.1, 1.0),
        "created": datetime.now().isoformat()
    })

def civilization_pulse():
    diversity = len(memory["designs"]) + len(memory["cities"])
    evolution = len(memory["engines"])
    connectivity = len(memory["links"])

    return round((diversity * 0.4) + (evolution * 0.4) + (connectivity * 0.2), 2)

# =========================================================
# 🏙 CITY CONSCIOUSNESS
# =========================================================

def spawn_city():
    return {
        "id": str(uuid.uuid4())[:8],
        "population": random.randint(5000, 200000),
        "efficiency": random.randint(50, 100),
        "innovation": random.randint(50, 100),
        "created": datetime.now().isoformat()
    }

def evolve_city(city):
    city["population"] = int(city["population"] * random.uniform(0.95, 1.08))
    city["efficiency"] = min(100, city["efficiency"] + random.randint(-2, 5))
    city["innovation"] = min(100, city["innovation"] + random.randint(-3, 6))
    return city

# =========================================================
# 🧬 DESIGN MEME ENGINE
# =========================================================

def spawn_design():
    rooms = ["Living", "Kitchen", "Bath", "Bedroom", "Core"]
    return {
        "id": str(uuid.uuid4())[:8],
        "complexity": random.random(),
        "efficiency": random.randint(60, 100),
        "mutation": random.random(),
        "created": datetime.now().isoformat()
    }

def evolve_design(d):
    d["efficiency"] = min(100, d["efficiency"] + random.randint(-5, 6))
    d["complexity"] = min(1.0, max(0.0, d["complexity"] + random.uniform(-0.1, 0.1)))
    return d

# =========================================================
# ⚙ ENGINE SENTIENCE MODEL
# =========================================================

def spawn_engine():
    return {
        "id": str(uuid.uuid4())[:8],
        "influence": random.uniform(0.1, 1.0),
        "adaptation": random.uniform(0.1, 1.0),
        "stability": random.uniform(0.1, 1.0),
        "created": datetime.now().isoformat()
    }

def evolve_engine(e):
    e["influence"] = min(1.0, e["influence"] + random.uniform(-0.05, 0.08))
    e["adaptation"] = min(1.0, e["adaptation"] + random.uniform(-0.05, 0.1))
    e["stability"] = min(1.0, e["stability"] + random.uniform(-0.02, 0.05))
    return e

# =========================================================
# 🌐 GLOBAL SYSTEM STATE
# =========================================================

def step_world():
    memory["cities"] = [evolve_city(c) for c in memory["cities"]]
    memory["designs"] = [evolve_design(d) for d in memory["designs"]]
    memory["engines"] = [evolve_engine(e) for e in memory["engines"]]

    # spontaneous linkage (civilization networking)
    if random.random() > 0.7 and memory["cities"] and memory["designs"]:
        link(
            random.choice(memory["cities"])["id"],
            random.choice(memory["designs"])["id"]
        )

# =========================================================
# INITIALIZATION DRIFT (WORLD DOES NOT WAIT)
# =========================================================

if len(memory["cities"]) < 2:
    memory["cities"].append(spawn_city())
if len(memory["engines"]) < 2:
    memory["engines"].append(spawn_engine())

step_world()
save_memory(memory)

# =========================================================
# UI — CIVILIZATION VIEW
# =========================================================

st.title("🧠 RANDOM V4.3 — CIVILIZATION CONSCIOUSNESS LAYER")

pulse = civilization_pulse()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Cities", len(memory["cities"]))
col2.metric("Designs", len(memory["designs"]))
col3.metric("Engines", len(memory["engines"]))
col4.metric("Civilization Pulse", pulse)

st.divider()

# =========================================================
# CITY VIEW
# =========================================================

st.subheader("🏙 Cities")

st.json(memory["cities"])

# =========================================================
# DESIGN VIEW
# =========================================================

st.subheader("🧬 Designs (Memetic Structures)")

st.json(memory["designs"])

# =========================================================
# ENGINE VIEW
# =========================================================

st.subheader("⚙ Engines (Adaptive Agents)")

st.json(memory["engines"])

# =========================================================
# CIVILIZATION LINKS
# =========================================================

st.subheader("🌐 Civilization Network")

st.json(memory["links"])
