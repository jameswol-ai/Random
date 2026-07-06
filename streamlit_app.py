# =========================================================
# RANDOM V25
# NEURAL CITY ENGINE (Walkable Architecture Civilization Simulator)
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
    page_title="Neural City Engine V25",
    page_icon="🏙️",
    layout="wide"
)

MEMORY_FILE = Path("city_memory.json")

# =========================================================
# UI: CITY GLOW ENGINE
# =========================================================

st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #070a12, #02040a);
    color: white;
}

.city-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
}

.cell {
    height: 80px;
    border-radius: 6px;
    background: linear-gradient(145deg, #101828, #0a0f1d);
    border: 1px solid rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
}

.agent {
    position: absolute;
    width: 10px;
    height: 10px;
    background: cyan;
    border-radius: 50%;
    box-shadow: 0 0 12px cyan;
    animation: pulse 1.5s infinite;
}

.building {
    position: absolute;
    inset: 10px;
    border-radius: 6px;
    background: linear-gradient(145deg, #1a2238, #0d1324);
    border: 1px solid rgba(255,255,255,0.08);
}

@keyframes pulse {
    0% { transform: scale(0.8); opacity: 0.6; }
    50% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(0.8); opacity: 0.6; }
}

.walk-ui {
    background: rgba(0,255,255,0.06);
    padding: 12px;
    border-radius: 10px;
    border: 1px solid rgba(0,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

def load():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"cities": [], "agents": [], "logs": []}

def save(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

if "mem" not in st.session_state:
    st.session_state.mem = load()

mem = st.session_state.mem

# =========================================================
# CITY GENERATION ENGINE
# =========================================================

def generate_city(size=6):
    city = []
    for y in range(size):
        for x in range(size):
            cell_type = random.choice(["empty", "building", "park", "road"])
            city.append({
                "x": x,
                "y": y,
                "type": cell_type,
                "height": random.randint(1, 5) if cell_type == "building" else 0,
                "light": random.uniform(0.2, 1.0)
            })
    return city

def spawn_agents(n=5):
    return [{
        "id": str(uuid.uuid4())[:6],
        "x": random.randint(0, 5),
        "y": random.randint(0, 5),
        "mood": random.choice(["calm", "curious", "analytical", "restless"]),
        "energy": random.randint(40, 100)
    } for _ in range(n)]

def move_agent(agent):
    agent["x"] = max(0, min(5, agent["x"] + random.choice([-1, 0, 1])))
    agent["y"] = max(0, min(5, agent["y"] + random.choice([-1, 0, 1])))
    agent["energy"] -= random.uniform(0.1, 1.5)
    return agent

# =========================================================
# WALKABLE SIMULATION ENGINE
# =========================================================

def simulate_step():
    for a in mem["agents"]:
        move_agent(a)

# =========================================================
# LIGHTING ENGINE (NEURAL SUN MODEL)
# =========================================================

def compute_light(cell):
    base = cell["light"]
    time_bias = math.sin(datetime.now().second / 60 * math.pi * 2)
    return max(0.1, min(1.0, base + time_bias))

# =========================================================
# RENDER CITY
# =========================================================

def render_city(city, agents):
    grid = '<div class="city-grid">'

    for cell in city:
        light = compute_light(cell)

        glow = f"rgba(0,255,255,{light*0.5})"

        grid += f"""
        <div class="cell" style="box-shadow: 0 0 10px {glow}">
        """

        if cell["type"] == "building":
            grid += '<div class="building"></div>'

        for a in agents:
            if a["x"] == cell["x"] and a["y"] == cell["y"]:
                grid += '<div class="agent"></div>'

        grid += "</div>"

    grid += "</div>"
    st.markdown(grid, unsafe_allow_html=True)

# =========================================================
# UI NAV
# =========================================================

page = st.sidebar.radio(
    "🏙️ Neural City",
    [
        "🏠 Project Overview",
        "📐 Floor Plan",
        "🏗 Structural Model",
        "🚶 Walk Mode",
        "🌍 City Simulation",
        "🧠 Memory"
    ]
)

# =========================================================
# INIT WORLD
# =========================================================

if "city" not in st.session_state:
    st.session_state.city = generate_city()

if "agents" not in st.session_state:
    st.session_state.agents = spawn_agents()

# =========================================================
# PAGES
# =========================================================

if page == "🏠 Project Overview":
    st.title("🏙️ Neural City Engine V25")
    st.write("A living architecture civilization simulator.")

    render_city(st.session_state.city, st.session_state.agents)

elif page == "📐 Floor Plan":
    st.title("📐 Procedural Building Layouts")
    st.json(random.choice(st.session_state.city))

elif page == "🏗 Structural Model":
    st.title("🏗 Load Simulation Field")

    load_map = sum([c["height"] for c in st.session_state.city])
    st.metric("Total Structural Load", load_map)

elif page == "🚶 Walk Mode":
    st.title("🚶 First-Person Navigation (Simulated)")

    col1, col2, col3 = st.columns(3)

    if col1.button("⬆ Move"):
        for a in st.session_state.agents:
            a["y"] = max(0, a["y"] - 1)

    if col2.button("⬇ Move"):
        for a in st.session_state.agents:
            a["y"] = min(5, a["y"] + 1)

    if col3.button("🔄 Step AI"):
        simulate_step()

    render_city(st.session_state.city, st.session_state.agents)

elif page == "🌍 City Simulation":
    st.title("🌍 Autonomous City Evolution")

    if st.button("Evolve City"):
        st.session_state.city = generate_city()
        st.session_state.agents = spawn_agents()

    render_city(st.session_state.city, st.session_state.agents)

elif page == "🧠 Memory":
    st.title("🧠 Neural Memory")

    mem["cities"].append(st.session_state.city)
    mem["agents"].append(st.session_state.agents)

    save(mem)
    st.json(mem)