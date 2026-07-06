# =========================================================
# RANDOM ARC HYBRID ENGINE
# Seed Kernel + Evolutionary Architect + Chaos Mutator
# Single-File Streamlit System
# =========================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random Arc Hybrid Engine",
    page_icon="🌐",
    layout="wide"
)

MEMORY_FILE = Path("random_arc_memory.json")

# =========================================================
# MEMORY
# =========================================================

DEFAULT_STATE = {
    "seeds": [],
    "cities": [],
    "chaos_events": [],
    "lineage": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        MEMORY_FILE.write_text(json.dumps(st.session_state.memory, indent=2))
    except:
        pass

def log(event):
    st.session_state.memory["chaos_events"].append({
        "time": datetime.now().isoformat(),
        "event": event
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_city" not in st.session_state:
    st.session_state.active_city = None

mem = st.session_state.memory

# =========================================================
# ARCHETYPE CORE
# =========================================================

BUILD_TYPES = [
    "Sky Tower", "Arcology Block", "Floating Habitat",
    "Subterranean Nexus", "Coastal Stack", "Modular Hive"
]

ROOM_MUTATIONS = [
    "Gravity Neutral Chamber",
    "Light Fold Atrium",
    "Bio Adaptive Garden",
    "Quantum Corridor",
    "Reactive Wall Grid",
    "Memory Storage Room"
]

def generate_seed():
    btype = random.choice(BUILD_TYPES)

    base = {
        "id": str(uuid.uuid4())[:8],
        "type": btype,
        "floors": random.randint(3, 80),
        "modules": random.randint(5, 25),
        "instability": random.random(),
        "rooms": ["Core Hub", "Energy Spine", "Access Loop"],
        "mass_index": random.randint(50, 500)
    }

    return base

def mutate(city):
    c = json.loads(json.dumps(city))

    # structural drift
    c["floors"] = max(1, c["floors"] + random.randint(-5, 10))
    c["modules"] += random.randint(-2, 5)

    # chaos injection
    if random.random() > 0.6:
        c["rooms"].append(random.choice(ROOM_MUTATIONS))
        c["instability"] = min(1.0, c["instability"] + random.random() * 0.2)

    c["mass_index"] += random.randint(-20, 40)

    return c

def fitness(city):
    stability = max(0, 100 - city["instability"] * 120)
    density = min(100, city["modules"] * 4)
    scale = min(100, city["floors"])

    return int((stability + density + scale) / 3)

def evolve(seed, generations=5):
    population = [seed]
    history = []

    for _ in range(generations):
        next_gen = []

        for p in population:
            child = mutate(p)
            child["score"] = fitness(child)
            next_gen.append(child)

        best = max(next_gen, key=lambda x: x["score"])
        history.append(best["score"])

        population = [best, mutate(best)]

    return best, history

# =========================================================
# CITY VIEW
# =========================================================

def render(city):
    st.subheader(f"🌆 {city['type']} :: {city['id']}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Floors", city["floors"])
    col2.metric("Modules", city["modules"])
    col3.metric("Instability", round(city["instability"], 2))

    st.markdown("### 🧠 Spatial Composition")

    for r in city["rooms"]:
        st.markdown(f"- {r}")

# =========================================================
# CHAOS ENGINE
# =========================================================

def chaos_event(city):
    event = random.choice([
        "Structural resonance shift detected",
        "Module duplication anomaly",
        "Temporal layout drift",
        "Gravity redistribution spike",
        "Memory corridor collapse"
    ])

    city["instability"] = min(1.0, city["instability"] + 0.15)
    log(event)
    return event

# =========================================================
# UI
# =========================================================

st.title("🌐 RANDOM ARC HYBRID ENGINE")
st.caption("Seed + Evolution + Chaos Unified Architecture System")

mode = st.sidebar.radio("Mode", ["Seed Generator", "Evolution Lab", "Chaos Simulator", "Memory Vault"])

# =========================================================
# SEED
# =========================================================

if mode == "Seed Generator":
    st.subheader("🧬 Generate Architectural Seed")

    if st.button("Generate Seed"):
        seed = generate_seed()
        mem["seeds"].append(seed)
        st.session_state.active_city = seed
        save_memory()

    if st.session_state.active_city:
        render(st.session_state.active_city)

# =========================================================
# EVOLUTION
# =========================================================

elif mode == "Evolution Lab":
    st.subheader("🏗️ Evolution Engine")

    if st.button("Evolve Latest Seed"):
        if mem["seeds"]:
            seed = mem["seeds"][-1]
            best, history = evolve(seed)

            best["score"] = fitness(best)

            mem["cities"].append(best)
            st.session_state.active_city = best
            save_memory()

            st.line_chart(history)
        else:
            st.warning("No seed available")

    if st.session_state.active_city:
        render(st.session_state.active_city)

# =========================================================
# CHAOS
# =========================================================

elif mode == "Chaos Simulator":
    st.subheader("🌪️ Chaos Mutation Field")

    if st.button("Trigger Chaos Event"):
        if st.session_state.active_city:
            event = chaos_event(st.session_state.active_city)
            st.warning(event)
            save_memory()

    if st.session_state.active_city:
        render(st.session_state.active_city)
    else:
        st.info("No active city loaded")

# =========================================================
# MEMORY
# =========================================================

elif mode == "Memory Vault":
    st.subheader("🧠 System Memory")

    st.json(mem)

    if st.button("Reset System"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_city = None
        save_memory()
        st.success("System reset complete")
        st.rerun()
