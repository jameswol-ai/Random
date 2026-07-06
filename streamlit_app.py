# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# Evolutionary Spatial Layout Synthesis & Diagnostics
# Zero-Dependency Single-File Streamlit Implementation
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
    page_title="Random Studio Engine",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.03em;
}

.arc-blueprint-canvas {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    background: #090d16;
    padding: 24px;
    border-radius: 12px;
    border: 1px dashed #334155;
}

.arc-room-module {
    flex: 1 1 calc(33.333% - 16px);
    min-width: 220px;
    padding: 20px;
    border-radius: 8px;
    color: #fff;
    border: 1px solid rgba(255,255,255,0.12);
    transition: 0.2s;
}

.arc-room-module:hover {
    transform: translateY(-3px);
}

.room-meta {
    font-size: 0.85rem;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(st.session_state.memory, f, indent=2)

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

# =========================================================
# ENGINE CORE
# =========================================================

def generate_design(goal):
    return {
        "id": str(uuid.uuid4())[:8],
        "goal": goal,
        "area": random.randint(120, 900),
        "cost": random.randint(80_000, 950_000),
        "structure": {
            "columns": random.randint(12, 55),
            "beams": random.randint(20, 110)
        },
        "rooms": ["Living", "Kitchen", "Bath"] + ["Room"] * random.randint(2, 6)
    }

def fitness(d):
    return (
        d["area"] * 0.2 +
        d["structure"]["columns"] * 1.5 +
        d["structure"]["beams"] * 1.2 -
        d["cost"] * 0.0001
    )

def evolve(goal, generations=6):
    pop = [generate_design(goal) for _ in range(8)]
    history = []

    for _ in range(generations):
        pop.sort(key=fitness, reverse=True)
        history.append(fitness(pop[0]))

        survivors = pop[:4]
        new_pop = []

        for s in survivors:
            new_pop.append(s)
            mutated = json.loads(json.dumps(s))
            mutated["structure"]["columns"] += random.randint(-2, 3)
            mutated["structure"]["beams"] += random.randint(-3, 4)
            mutated["cost"] += random.randint(-5000, 5000)
            new_pop.append(mutated)

        pop = new_pop[:8]

    return pop[0], history

def floor_plan(d):
    rooms = [
        {"name": "Living Lounge", "w": 6, "h": 5, "color": "#1e3a8a"},
        {"name": "Kitchen Core", "w": 4, "h": 4, "color": "#065f46"},
        {"name": "Bath Node", "w": 3, "h": 2, "color": "#78350f"}
    ]

    for i in range(len(d["rooms"])):
        rooms.append({
            "name": f"Room {i+1}",
            "w": 4,
            "h": 4,
            "color": "#4c1d95"
        })

    return rooms

def render_blueprint(plan):
    st.markdown("### 🗺️ Spatial Blueprint")

    html = '<div class="arc-blueprint-canvas">'
    for r in plan:
        html += f"""
        <div class="arc-room-module" style="background:{r['color']}">
            <div style="font-weight:700">{r['name']}</div>
            <div class="room-meta">{r['w']}m × {r['h']}m</div>
        </div>
        """
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📐 Arc Studio V10")

page = st.sidebar.radio(
    "Workspace",
    ["Dashboard", "Design Studio", "AI Architect", "Memory"]
)

goal = st.sidebar.text_input("Goal", "Eco Smart Tower")

if st.sidebar.button("Generate"):
    design, hist = evolve(goal)
    design["plan"] = floor_plan(design)

    mem["designs"].append(design)
    st.session_state.active_design = design

    log_event(f"Generated {design['id']}")

d = st.session_state.active_design

# =========================================================
# PAGES
# =========================================================

if page == "Dashboard":
    st.title("🏠 Dashboard")
    st.metric("Designs", len(mem["designs"]))
    st.metric("Logs", len(mem["logs"]))

elif page == "Design Studio":
    st.title("📐 Design Studio")

    if d:
        st.json(d)
        render_blueprint(d["plan"])
    else:
        st.info("Generate a design first.")

elif page == "AI Architect":
    st.title("🧠 AI Architect")

    if d:
        st.json({
            "complexity": len(d["rooms"]) * 10,
            "efficiency": 100 - (d["cost"] / 10000)
        })

elif page == "Memory":
    st.title("🧠 Memory")
    st.json(mem)
