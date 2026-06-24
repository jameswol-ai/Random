# =========================================================
# 🧠 RANDOM V5 — UNIVERSE ENGINE CORE (MULTI-USER READY)
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="RANDOM V5 UNIVERSE", layout="wide")

# =========================================================
# 🌐 REMOTE WORLD SUPPORT (MULTI-USER MODE)
# =========================================================

API_URL = st.sidebar.text_input("🌍 World Server URL (optional)", "")
REMOTE_MODE = len(API_URL.strip()) > 0

def api(path, method="GET", data=None):
    if not REMOTE_MODE:
        return None
    try:
        if method == "GET":
            return requests.get(API_URL + path, timeout=3).json()
        else:
            return requests.post(API_URL + path, json=data, timeout=3).json()
    except:
        return None

# =========================================================
# MEMORY CORE (LOCAL FALLBACK WORLD STATE)
# =========================================================

MEMORY_FILE = Path("random_memory.json")

DEFAULT_MEMORY = {
    "projects": [],
    "designs": [],
    "cities": [],
    "knowledge": [],
    "engines": [],
    "agents": [],
    "economy": {
        "gold": 1000,
        "market": {}
    },
    "rules": {
        "growth": 1.0,
        "innovation": 1.0
    }
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
# 🧠 WORLD RULE ENGINE (SELF-EVOLVING)
# =========================================================

def evolve_rules():
    pressure = len(memory["cities"]) + len(memory["designs"])
    memory["rules"]["growth"] = 1.0 + pressure * 0.001
    memory["rules"]["innovation"] = 1.0 + len(memory["engines"]) * 0.01

# =========================================================
# 🏙 CITY AI (AUTONOMOUS EVOLUTION)
# =========================================================

def spawn_city():
    return {
        "id": str(uuid.uuid4())[:8],
        "population": random.randint(5000, 200000),
        "efficiency": random.randint(50, 100),
        "innovation": random.randint(50, 100),
        "wealth": random.randint(1000, 10000),
        "created": datetime.now().isoformat()
    }

def evolve_city(city):
    city["population"] = int(city["population"] * random.uniform(0.98, 1.05))
    city["wealth"] += random.randint(-50, 200)
    city["efficiency"] = min(100, city["efficiency"] + random.randint(-1, 3))
    return city

# =========================================================
# 🧬 DESIGN GENERATION
# =========================================================

def generate_design():
    return {
        "id": str(uuid.uuid4())[:8],
        "complexity": random.random(),
        "efficiency": random.randint(60, 100),
        "innovation": random.random(),
        "created": datetime.now().isoformat()
    }

# =========================================================
# ⚙ ENGINE EVOLUTION
# =========================================================

def spawn_engine():
    return {
        "id": str(uuid.uuid4())[:8],
        "power": random.uniform(0.2, 1.0),
        "adaptation": random.uniform(0.2, 1.0),
        "stability": random.uniform(0.2, 1.0),
        "created": datetime.now().isoformat()
    }

# =========================================================
# 🤖 AI AGENTS (NEW LAYER)
# =========================================================

def spawn_agent():
    return {
        "id": str(uuid.uuid4())[:8],
        "role": random.choice(["builder", "trader", "engineer", "observer"]),
        "energy": random.randint(50, 100),
        "intelligence": random.randint(50, 100),
        "wealth": random.randint(100, 1000),
    }

def step_agents():
    for a in memory["agents"]:
        a["energy"] = max(0, a["energy"] + random.randint(-3, 5))
        a["wealth"] += random.randint(-10, 20)

# =========================================================
# 💰 ECONOMY SIMULATION
# =========================================================

def step_economy():
    market = memory["economy"]["market"]

    for city in memory["cities"]:
        city["wealth"] += random.randint(-100, 300)

    for k in ["food", "tech", "energy"]:
        market[k] = market.get(k, random.randint(50, 150))
        market[k] += random.randint(-5, 5)

# =========================================================
# 🌍 WORLD TICK (SIMULATION LOOP)
# =========================================================

def world_tick():
    evolve_rules()

    memory["cities"] = [evolve_city(c) for c in memory["cities"]]
    memory["agents"] = memory["agents"][:20]

    step_agents()
    step_economy()

# =========================================================
# INITIALIZATION
# =========================================================

if len(memory["cities"]) < 2:
    memory["cities"].append(spawn_city())

if len(memory["engines"]) < 2:
    memory["engines"].append(spawn_engine())

if len(memory["agents"]) < 3:
    memory["agents"].append(spawn_agent())

world_tick()
save_memory(memory)

# =========================================================
# UI
# =========================================================

st.title("🧠 RANDOM V5 — UNIVERSE ENGINE")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌆 Cities", len(memory["cities"]))
col2.metric("🤖 Agents", len(memory["agents"]))
col3.metric("⚙ Engines", len(memory["engines"]))
col4.metric("💰 Economy Size", sum(memory["economy"]["market"].values()) if memory["economy"]["market"] else 0)

st.divider()

# =========================================================
# CITY VIEW
# =========================================================

st.subheader("🌆 Cities")
st.json(memory["cities"])

# =========================================================
# AGENTS VIEW
# =========================================================

st.subheader("🤖 AI Agents")
st.json(memory["agents"])

# =========================================================
# ECONOMY VIEW
# =========================================================

st.subheader("💰 Economy")
st.json(memory["economy"])

# =========================================================
# ENGINE VIEW
# =========================================================

st.subheader("⚙ Engines")
st.json(memory["engines"])

# =========================================================
# CONTROL PANEL
# =========================================================

st.sidebar.subheader("⚙ Controls")

if st.sidebar.button("Spawn City"):
    memory["cities"].append(spawn_city())
    save_memory(memory)

if st.sidebar.button("Spawn Agent"):
    memory["agents"].append(spawn_agent())
    save_memory(memory)

if st.sidebar.button("Spawn Engine"):
    memory["engines"].append(spawn_engine())
    save_memory(memory)

if st.sidebar.button("Reset Economy"):
    memory["economy"] = {"gold": 1000, "market": {}}
    save_memory(memory)

if st.sidebar.button("Force World Tick"):
    world_tick()
    save_memory(memory)
