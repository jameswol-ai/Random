# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# V28 — Neural World Engine (Streamlit Control Core)
# =========================================================

import streamlit as st
import json
import uuid
import random
import math
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random Neural World Engine V28",
    page_icon="🌍",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# UI STYLE
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
}

.world-card {
    background: #0b1220;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "worlds": [],
    "designs": [],
    "simulation": [],
    "plugins": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(st.session_state.memory, f, indent=2)

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory

# =========================================================
# NEURAL WORLD CORE
# =========================================================

def generate_world(name):
    return {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "terrain": {
            "type": random.choice(["flat", "hilly", "coastal", "urban"]),
            "roughness": random.uniform(0.1, 1.0)
        },
        "lighting": {
            "sun_angle": random.randint(0, 360),
            "intensity": random.uniform(0.5, 1.2)
        },
        "weather": random.choice(["clear", "rain", "wind", "storm"]),
        "time": random.randint(0, 24)
    }

# =========================================================
# AI COUNCIL
# =========================================================

COUNCIL = [
    "Architect AI",
    "Structural AI",
    "Cost AI",
    "Sustainability AI",
    "Simulation AI",
    "Chaos AI"
]

def council_vote(world):
    votes = []
    report = []

    for agent in COUNCIL:
        score = random.randint(60, 99)
        votes.append(score)
        report.append({
            "agent": agent,
            "score": score,
            "comment": f"{agent} evaluates world stability."
        })

    return report, sum(votes) / len(votes)

# =========================================================
# OCCUPANCY SIMULATION
# =========================================================

def simulate_people(world, steps=10):
    people = [{"id": i, "x": random.random(), "y": random.random()} for i in range(5)]
    history = []

    for t in range(steps):
        for p in people:
            p["x"] += random.uniform(-0.05, 0.05)
            p["y"] += random.uniform(-0.05, 0.05)

        congestion = sum(abs(p["x"]) + abs(p["y"]) for p in people)

        history.append({
            "tick": t,
            "congestion": congestion,
            "comfort": max(0, 100 - congestion * 10)
        })

    return history

# =========================================================
# STRUCTURAL ENGINE (ABSTRACT)
# =========================================================

def structural_health(world):
    base = 100
    penalty = world["terrain"]["roughness"] * 20
    return max(0, base - penalty)

# =========================================================
# SUSTAINABILITY ENGINE
# =========================================================

def sustainability_score(world):
    weather_factor = {"clear": 1, "rain": 0.9, "wind": 0.85, "storm": 0.7}
    return round(
        100 * weather_factor[world["weather"]] * (1 - world["terrain"]["roughness"] * 0.3),
        2
    )

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🌍 Neural World Engine V28")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🌍 World Generator",
        "🏗 Structural Physics",
        "🌱 Sustainability",
        "🚶 Occupancy Simulation",
        "🏢 BIM Manager",
        "📊 Digital Twin",
        "🔌 Plugins",
        "🧠 Memory",
        "⚙ Settings"
    ]
)

world_name = st.sidebar.text_input("World Name", "Neo Architecture Zone")

if st.sidebar.button("Generate World"):
    world = generate_world(world_name)

    report, score = council_vote(world)
    world["council_score"] = score

    mem["worlds"].append(world)
    st.session_state.active_world = world
    st.session_state.council = report

    save_memory()

world = st.session_state.get("active_world", None)

# =========================================================
# PAGES
# =========================================================

if page == "🏠 Dashboard":
    st.title("🏠 Neural World Dashboard")

    st.metric("Worlds Created", len(mem["worlds"]))
    st.metric("Simulation Runs", len(mem["simulation"]))

    if world:
        st.markdown("### Active World")
        st.json(world)

# ---------------------------------------------------------

elif page == "🌍 World Generator":
    st.title("🌍 World Generator")

    if world:
        st.json(world)
    else:
        st.info("Generate a world first.")

# ---------------------------------------------------------

elif page == "🏗 Structural Physics":
    st.title("🏗 Structural Physics")

    if world:
        st.metric("Structural Health", f"{structural_health(world):.1f}/100")

# ---------------------------------------------------------

elif page == "🌱 Sustainability":
    st.title("🌱 Sustainability Engine")

    if world:
        st.metric("Sustainability Score", f"{sustainability_score(world):.1f}/100")

# ---------------------------------------------------------

elif page == "🚶 Occupancy Simulation":
    st.title("🚶 Occupancy Simulation")

    if world:
        sim = simulate_people(world)
        st.line_chart([s["comfort"] for s in sim])
        st.json(sim[-1])

# ---------------------------------------------------------

elif page == "🏢 BIM Manager":
    st.title("🏢 BIM Manager")

    if world:
        bim = {
            "project": world["name"],
            "site": world["terrain"],
            "lighting": world["lighting"]
        }
        st.json(bim)

# ---------------------------------------------------------

elif page == "📊 Digital Twin":
    st.title("📊 Digital Twin")

    if world:
        twin = {
            "structural_health": structural_health(world),
            "sustainability": sustainability_score(world),
            "time": world["time"],
            "weather": world["weather"]
        }
        st.json(twin)

# ---------------------------------------------------------

elif page == "🔌 Plugins":
    st.title("🔌 Plugin System")

    st.info("Future module registry for CFD, GIS, VR, IFC, robotics.")
    st.json(mem.get("plugins", []))

# ---------------------------------------------------------

elif page == "🧠 Memory":
    st.title("🧠 Memory Core")

    st.json(mem)

# ---------------------------------------------------------

elif page == "⚙ Settings":
    st.title("⚙ Settings")

    if st.button("Reset Engine"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_world = None
        save_memory()
        st.success("System reset complete")
        st.rerun()