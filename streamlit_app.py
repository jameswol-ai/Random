# =========================================================
# 🌌 RANDOM V4.5 — GALAXY CIVILIZATION ENGINE
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="GALAXY RANDOM V4.5", layout="wide")

# =========================================================
# 🌌 GALAXY MEMORY CORE
# =========================================================

MEMORY_FILE = Path("random_galaxy.json")

DEFAULT_MEMORY = {
    "planets": [],
    "routes": [],
    "events": []
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
# 🪐 PLANET MODEL (FULL CIVILIZATION SYSTEM)
# =========================================================

def spawn_planet():
    return {
        "id": str(uuid.uuid4())[:8],
        "name": f"Planet-{random.randint(1000,9999)}",
        "civilizations": random.randint(1, 5),
        "innovation_field": random.uniform(0.5, 2.0),
        "stability_gravity": random.uniform(0.5, 2.0),
        "trade_friction": random.uniform(0.1, 1.5),
        "created": datetime.now().isoformat()
    }

def evolve_planet(p):
    p["civilizations"] = max(1, p["civilizations"] + random.choice([-1, 0, 1]))
    p["innovation_field"] = max(0.1, p["innovation_field"] + random.uniform(-0.1, 0.2))
    p["stability_gravity"] = max(0.1, p["stability_gravity"] + random.uniform(-0.1, 0.2))
    return p

# =========================================================
# 🚀 INTERPLANETARY TRAVEL
# =========================================================

def travel(a, b):
    success = random.random() > (b["trade_friction"] * 0.5)

    return {
        "from": a["id"],
        "to": b["id"],
        "success": success,
        "mutation": random.uniform(0.0, 1.0),
        "time": datetime.now().isoformat()
    }

# =========================================================
# 🌌 GALAXY EVOLUTION STEP
# =========================================================

def step_galaxy():
    # evolve planets
    for p in memory["planets"]:
        evolve_planet(p)

    # spawn planets
    if len(memory["planets"]) < 3 or random.random() > 0.7:
        memory["planets"].append(spawn_planet())

    # interplanetary travel events
    if len(memory["planets"]) >= 2 and random.random() > 0.4:
        a, b = random.sample(memory["planets"], 2)
        memory["routes"].append(travel(a, b))

    # supernova event
    if random.random() > 0.9:
        memory["events"].append({
            "type": random.choice([
                "supernova knowledge burst",
                "civilization extinction wave",
                "galactic innovation bloom",
                "planetary alignment shift"
            ]),
            "intensity": random.randint(50, 100),
            "time": datetime.now().isoformat()
        })

# =========================================================
# 🌌 GALACTIC ENTROPY INDEX
# =========================================================

def gei():
    p = len(memory["planets"])
    r = len(memory["routes"])
    e = len(memory["events"])
    return round((p * 0.6) + (r * 0.3) + (e * 0.4), 2)

# =========================================================
# INITIALIZATION
# =========================================================

step_galaxy()
save_memory(memory)

# =========================================================
# 🌌 UI — GALAXY VIEW
# =========================================================

st.title("🌌 GALAXY RANDOM V4.5")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Planets", len(memory["planets"]))
col2.metric("Travel Routes", len(memory["routes"]))
col3.metric("Events", len(memory["events"]))
col4.metric("GEI", gei())

st.divider()

# =========================================================
# 🪐 PLANETS
# =========================================================

st.subheader("🪐 Planetary Systems")
st.json(memory["planets"])

# =========================================================
# 🚀 ROUTES
# =========================================================

st.subheader("🚀 Interplanetary Travel")
st.json(memory["routes"])

# =========================================================
# 🌌 EVENTS
# =========================================================

st.subheader("🌠 Galactic Events")
st.json(memory["events"])
