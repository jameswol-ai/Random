# =========================================================
# 🪐 RANDOM V4.4 — PLANETARY CIVILIZATION SIMULATION
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="PLANET RANDOM V4.4", layout="wide")

# =========================================================
# 🌍 PLANETARY MEMORY CORE
# =========================================================

MEMORY_FILE = Path("random_planet.json")

DEFAULT_MEMORY = {
    "civilizations": [],
    "transactions": [],
    "global_events": []
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
# 🏛 CIVILIZATION MODEL
# =========================================================

def spawn_civilization():
    return {
        "id": str(uuid.uuid4())[:8],
        "name": f"Civ-{random.randint(100,999)}",
        "wealth": random.randint(50, 200),
        "knowledge": random.randint(50, 200),
        "innovation": random.randint(50, 200),
        "stability": random.randint(50, 200),
        "created": datetime.now().isoformat()
    }

def evolve_civilization(c):
    drift = random.uniform(-10, 15)

    c["wealth"] = max(0, c["wealth"] + int(drift))
    c["knowledge"] = max(0, c["knowledge"] + random.randint(-5, 10))
    c["innovation"] = max(0, c["innovation"] + random.randint(-8, 12))
    c["stability"] = max(0, c["stability"] + random.randint(-6, 8))

    return c

# =========================================================
# 💱 INTERACTION SYSTEM (ECONOMY + EXCHANGE)
# =========================================================

def trade(a, b):
    transfer = random.randint(5, 20)

    a["wealth"] += transfer
    b["knowledge"] += transfer

    return {
        "from": a["id"],
        "to": b["id"],
        "value": transfer,
        "type": "knowledge-wealth-exchange",
        "time": datetime.now().isoformat()
    }

# =========================================================
# 🌐 GLOBAL EVOLUTION STEP
# =========================================================

def step_world():
    # evolve civs
    for c in memory["civilizations"]:
        evolve_civilization(c)

    # spontaneous civilization birth
    if len(memory["civilizations"]) < 3 or random.random() > 0.7:
        memory["civilizations"].append(spawn_civilization())

    # spontaneous trade event
    if len(memory["civilizations"]) >= 2 and random.random() > 0.5:
        a, b = random.sample(memory["civilizations"], 2)
        memory["transactions"].append(trade(a, b))

    # occasional global event
    if random.random() > 0.85:
        memory["global_events"].append({
            "event": random.choice([
                "knowledge bloom",
                "resource imbalance",
                "innovation surge",
                "civilization drift"
            ]),
            "impact": random.randint(10, 40),
            "time": datetime.now().isoformat()
        })

# =========================================================
# 🌡 PLANETARY COHERENCE INDEX
# =========================================================

def pci():
    civs = len(memory["civilizations"])
    trades = len(memory["transactions"])
    events = len(memory["global_events"])

    return round((civs * 0.5) + (trades * 0.3) + (events * 0.2), 2)

# =========================================================
# INITIALIZATION
# =========================================================

step_world()
save_memory(memory)

# =========================================================
# 🌍 UI — PLANET VIEW
# =========================================================

st.title("🪐 PLANET RANDOM V4.4")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Civilizations", len(memory["civilizations"]))
col2.metric("Trades", len(memory["transactions"]))
col3.metric("Events", len(memory["global_events"]))
col4.metric("PCI", pci())

st.divider()

# =========================================================
# 🏛 CIVILIZATIONS
# =========================================================

st.subheader("🏛 Civilizations")

st.json(memory["civilizations"])

# =========================================================
# 💱 ECONOMY LAYER
# =========================================================

st.subheader("💱 Transactions")

st.json(memory["transactions"])

# =========================================================
# 🌐 GLOBAL EVENTS
# =========================================================

st.subheader("🌐 Planetary Events")

st.json(memory["global_events"])
