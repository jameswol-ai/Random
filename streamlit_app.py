# =========================================================
# RANDOM ARC HYBRID ENGINE V2
# Multi-Agent City Intelligence + Evolution + Chaos System
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
    page_title="Random Arc Council Engine",
    page_icon="🏙️",
    layout="wide"
)

MEMORY_FILE = Path("arc_council_memory.json")

# =========================================================
# MEMORY
# =========================================================

DEFAULT_STATE = {
    "cities": [],
    "agents": [],
    "votes": [],
    "chaos_log": []
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

def log(msg):
    st.session_state.memory["chaos_log"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_city" not in st.session_state:
    st.session_state.active_city = None

mem = st.session_state.memory

# =========================================================
# AGENTS (THE ARCHITECT COUNCIL)
# =========================================================

AGENTS = [
    {"name": "Structural Purist", "bias": "stability"},
    {"name": "Chaos Architect", "bias": "innovation"},
    {"name": "Cost Guardian", "bias": "efficiency"},
    {"name": "Skyline Poet", "bias": "scale"},
    {"name": "Urban Systems Analyst", "bias": "balance"}
]

BUILDINGS = [
    "Arc Tower", "Neon Habitat", "Floating Stack",
    "Deep Core Block", "Spiral Megastructure", "Bio Dome Cluster"
]

DISTRICTS = [
    "Commercial Core", "Residential Ring", "Industrial Belt",
    "Greenbelt Sector", "Transit Spine", "Innovation Quarter"
]

# =========================================================
# CITY GENERATION
# =========================================================

def generate_city():
    city = {
        "id": str(uuid.uuid4())[:8],
        "name": f"City-{random.randint(100,999)}",
        "districts": [],
        "scale": random.randint(5, 50),
        "stability": random.random(),
        "innovation": random.random(),
        "density": random.random()
    }

    for d in DISTRICTS:
        city["districts"].append({
            "name": d,
            "buildings": random.randint(3, 15),
            "signature": random.choice(BUILDINGS),
            "energy_flow": random.random()
        })

    return city

# =========================================================
# AGENT EVALUATION SYSTEM
# =========================================================

def agent_score(agent, city):
    if agent["bias"] == "stability":
        return 100 - city["stability"] * 120
    if agent["bias"] == "innovation":
        return city["innovation"] * 120
    if agent["bias"] == "efficiency":
        return (1 - city["density"]) * 100
    if agent["bias"] == "scale":
        return city["scale"] * 2
    if agent["bias"] == "balance":
        return 100 - abs(city["stability"] - city["innovation"]) * 120

    return random.randint(0, 100)

def council_vote(city):
    votes = []
    total = 0

    for agent in AGENTS:
        score = agent_score(agent, city)
        votes.append({
            "agent": agent["name"],
            "score": round(score, 2)
        })
        total += score

    city["council_score"] = total / len(AGENTS)
    return votes

# =========================================================
# EVOLUTION ENGINE
# =========================================================

def mutate_city(city):
    c = json.loads(json.dumps(city))

    c["scale"] = max(1, c["scale"] + random.randint(-3, 5))
    c["stability"] = min(1, max(0, c["stability"] + random.uniform(-0.1, 0.1)))
    c["innovation"] = min(1, max(0, c["innovation"] + random.uniform(-0.1, 0.15)))
    c["density"] = min(1, max(0, c["density"] + random.uniform(-0.1, 0.1)))

    # chaos injection
    if random.random() > 0.7:
        d = random.choice(c["districts"])
        d["energy_flow"] += random.random() * 0.2
        log("Chaos spike in district: " + d["name"])

    return c

def evolve_city(city, steps=5):
    current = city
    history = []

    for _ in range(steps):
        current = mutate_city(current)
        votes = council_vote(current)
        current["votes"] = votes

        score = current["council_score"]
        history.append(score)

    return current, history

# =========================================================
# RENDERING
# =========================================================

def render_city(city):
    st.subheader(f"🏙️ {city['name']} :: {city['id']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Scale", city["scale"])
    col2.metric("Stability", round(city["stability"], 2))
    col3.metric("Innovation", round(city["innovation"], 2))
    col4.metric("Council Score", round(city.get("council_score", 0), 2))

    st.markdown("### 🧭 District Composition")

    for d in city["districts"]:
        st.markdown(
            f"- **{d['name']}** → {d['signature']} "
            f"(Buildings: {d['buildings']}, Flow: {round(d['energy_flow'],2)})"
        )

# =========================================================
# UI
# =========================================================

st.title("🏙️ RANDOM ARC HYBRID ENGINE V2")
st.caption("Multi-Agent Council • Evolutionary Cities • Chaos Injection Layer")

mode = st.sidebar.radio(
    "System Mode",
    ["City Seed", "Council Evolution", "Agent Court", "Memory Vault"]
)

# =========================================================
# SEED
# =========================================================

if mode == "City Seed":
    st.subheader("🧬 Generate City Seed")

    if st.button("Spawn City"):
        city = generate_city()
        mem["cities"].append(city)
        st.session_state.active_city = city
        save_memory()

    if st.session_state.active_city:
        render_city(st.session_state.active_city)

# =========================================================
# EVOLUTION
# =========================================================

elif mode == "Council Evolution":
    st.subheader("⚖️ Council Evolution Engine")

    if st.button("Evolve City Through Council"):
        if mem["cities"]:
            city = mem["cities"][-1]
            evolved, history = evolve_city(city)

            mem["cities"].append(evolved)
            st.session_state.active_city = evolved

            st.line_chart(history)
            save_memory()
        else:
            st.warning("No city exists yet")

    if st.session_state.active_city:
        render_city(st.session_state.active_city)

# =========================================================
# AGENT COURT
# =========================================================

elif mode == "Agent Court":
    st.subheader("🧠 Architect Council Voting Panel")

    if st.session_state.active_city:
        votes = council_vote(st.session_state.active_city)

        for v in votes:
            st.write(f"🧾 {v['agent']} → {round(v['score'],2)}")

        save_memory()
    else:
        st.info("No active city loaded")

# =========================================================
# MEMORY
# =========================================================

elif mode == "Memory Vault":
    st.subheader("🧠 System Memory Archive")

    st.json(mem)

    if st.button("Reset Universe"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_city = None
        save_memory()
        st.success("System reset complete")
        st.rerun()
