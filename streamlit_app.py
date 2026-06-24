# =========================================================
# 🧠 RANDOM V4.6 — UNIVERSE ENGINE (MULTI-REALITY LAYER)
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="RANDOM V4.6 UNIVERSE ENGINE", layout="wide")

# =========================================================
# 🌌 UNIVERSE MEMORY CORE
# =========================================================

MEMORY_FILE = Path("random_universe.json")

DEFAULT_MEMORY = {
    "universes": [],
    "cross_links": [],
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
# 🌠 UNIVERSE MODEL
# =========================================================

def spawn_universe():
    return {
        "id": str(uuid.uuid4())[:8],
        "laws": {
            "growth_rate": random.uniform(0.5, 2.0),
            "innovation_bias": random.uniform(0.5, 2.0),
            "stability_field": random.uniform(0.5, 2.0),
            "connectivity": random.uniform(0.5, 2.0)
        },
        "civilizations": random.randint(1, 5),
        "entropy": random.uniform(0.1, 1.0),
        "created": datetime.now().isoformat()
    }

def evolve_universe(u):
    # LAW MUTATION (THE BIG IDEA)
    for k in u["laws"]:
        drift = random.uniform(-0.05, 0.08)
        u["laws"][k] = max(0.1, u["laws"][k] + drift)

    # civilization drift influenced by laws
    u["civilizations"] += random.choice([-1, 0, 1]) * u["laws"]["growth_rate"]
    u["civilizations"] = max(1, int(u["civilizations"]))

    # entropy rises unless stability suppresses it
    u["entropy"] += random.uniform(-0.05, 0.1) / u["laws"]["stability_field"]
    u["entropy"] = min(1.0, max(0.0, u["entropy"]))

    return u

# =========================================================
# 🕳 CROSS-UNIVERSE INTERACTION
# =========================================================

def cross_link(a, b):
    return {
        "from": a["id"],
        "to": b["id"],
        "type": random.choice(["drift", "knowledge bleed", "law echo"]),
        "strength": random.uniform(0.1, 1.0),
        "time": datetime.now().isoformat()
    }

# =========================================================
# 🌠 COSMIC STEP FUNCTION
# =========================================================

def step_universe():
    # evolve universes
    for u in memory["universes"]:
        evolve_universe(u)

    # spawn universes
    if len(memory["universes"]) < 2 or random.random() > 0.6:
        memory["universes"].append(spawn_universe())

    # cross-universe interaction
    if len(memory["universes"]) >= 2 and random.random() > 0.5:
        a, b = random.sample(memory["universes"], 2)
        memory["cross_links"].append(cross_link(a, b))

    # rare cosmic event
    if random.random() > 0.9:
        memory["events"].append({
            "type": random.choice([
                "universe split",
                "law mutation cascade",
                "entropy collapse bloom",
                "civilization rebirth wave"
            ]),
            "impact": random.randint(10, 100),
            "time": datetime.now().isoformat()
        })

# =========================================================
# 🌌 UNIVERSAL COHERENCE INDEX
# =========================================================

def uci():
    u = len(memory["universes"])
    c = len(memory["cross_links"])
    e = len(memory["events"])
    return round((u * 0.5) + (c * 0.4) + (e * 0.6), 2)

# =========================================================
# INITIALIZATION
# =========================================================

step_universe()
save_memory(memory)

# =========================================================
# 🌌 UI — UNIVERSE VIEW
# =========================================================

st.title("🧠 RANDOM V4.6 — UNIVERSE ENGINE")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Universes", len(memory["universes"]))
col2.metric("Cross Links", len(memory["cross_links"]))
col3.metric("Cosmic Events", len(memory["events"]))
col4.metric("UCI", uci())

st.divider()

st.subheader("🌠 Universes")
st.json(memory["universes"])

st.subheader("🕳 Cross-Universe Links")
st.json(memory["cross_links"])

st.subheader("🌌 Cosmic Events")
st.json(memory["events"])
