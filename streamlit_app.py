# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# V30 — FINAL NEURAL ARCHITECTURE OS (MERGED BUILD)
# Evolutionary + BIM + AI Studio + Blueprint Visualization
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
    page_title="Random Neural Architecture OS V30",
    page_icon="🏗",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLE LAYER (Merged Arc Studio + V30)
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

.card {
    background: #0b1220;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 12px;
    margin: 10px 0;
}

/* Blueprint Canvas */
.arc-blueprint-canvas {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    background: #090d16;
    padding: 24px;
    border-radius: 12px;
    border: 1px dashed #334155;
    margin-top: 15px;
}

.arc-room-module {
    flex: 1 1 calc(33.333% - 16px);
    min-width: 220px;
    padding: 20px;
    border-radius: 10px;
    color: white;
    border: 1px solid rgba(255,255,255,0.12);
    transition: 0.25s;
}

.arc-room-module:hover {
    transform: translateY(-3px);
    border-color: rgba(255,255,255,0.3);
}

.room-meta {
    font-size: 0.85rem;
    opacity: 0.8;
    margin-top: 8px;
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
    "evolution": [],
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
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.memory, f, indent=2)

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# Init
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.memory

# =========================================================
# CORE ENGINE
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

# =========================================================
# FLOOR + BLUEPRINT VISUAL ENGINE
# =========================================================

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
    st.markdown("### 🗺️ Spatial Blueprint Simulation")

    html = '<div class="arc-blueprint-canvas">'
    for r in plan:
        html += f"""
        <div class="arc-room-module" style="background:{r['color']}">
            <div style="font-weight:700">{r['name']}</div>
            <div class="room-meta">{r['w']}m × {r['h']}m module</div>
        </div>
        """
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# EVOLUTION ENGINE
# =========================================================

def run(goal):
    return evolve(goal)

# =========================================================
# SIDEBAR NAV
# =========================================================

st.sidebar.title("🏗 Neural Architecture OS V30")

page = st.sidebar.radio(
    "Workspace",
    [
        "🏠 Dashboard",
        "📂 Projects",
        "📐 Design Studio",
        "🧠 AI Architect",
        "🏗 Structural Analysis",
        "💰 Cost Estimation",
        "🌱 Sustainability",
        "📋 Code Compliance",
        "🏢 BIM Manager",
        "📊 Analytics",
        "🧠 Memory",
        "🔌 Plugins",
        "⚙ Settings"
    ]
)

goal = st.sidebar.text_input("Design Goal", "Neo Eco Tower")
run_btn = st.sidebar.button("Generate Architecture")

# =========================================================
# GENERATION
# =========================================================

if run_btn:
    design, history = run(goal)
    design["plan"] = floor_plan(design)

    mem["designs"].append(design)
    st.session_state.active = design

    log(f"Generated design {design['id']}")

# =========================================================
# ACTIVE DESIGN
# =========================================================

d = st.session_state.get("active", None)

# =========================================================
# PAGES
# =========================================================

if page == "🏠 Dashboard":
    st.title("🏠 System Dashboard")

    st.metric("Designs", len(mem["designs"]))
    st.metric("Logs", len(mem["logs"]))
    st.metric("Plugins Loaded", len(mem["plugins"]))

    st.markdown("---")
    for l in mem["logs"][-6:]:
        st.write(l)

elif page == "📂 Projects":
    st.title("📂 Projects")
    st.json(mem["projects"])

elif page == "📐 Design Studio":
    st.title("📐 Design Studio")

    if d:
        st.json(d)
        render_blueprint(d["plan"])
    else:
        st.info("Generate a design first.")

elif page == "🧠 AI Architect":
    st.title("🧠 AI Architect")

    if d:
        st.json({
            "complexity": len(d["rooms"]) * 10,
            "efficiency": 100 - (d["cost"] / 10000)
        })

elif page == "🏗 Structural Analysis":
    st.title("🏗 Structural Analysis")

    if d:
        st.json(d["structure"])

elif page == "💰 Cost Estimation":
    st.title("💰 Cost Estimation")

    if d:
        st.metric("Cost", f"${d['cost']:,}")

elif page == "🌱 Sustainability":
    st.title("🌱 Sustainability")

    if d:
        score = max(0, 100 - d["structure"]["columns"])
        st.metric("Score", f"{score}/100")

elif page == "📋 Code Compliance":
    st.success("Simulated BIM compliance PASSED")

elif page == "🏢 BIM Manager":
    st.title("🏢 BIM Manager")

    if d:
        st.json({"materials": ["Concrete", "Steel", "Glass"], "structure": d["structure"]})

elif page == "📊 Analytics":
    st.title("📊 Analytics")

    if d:
        st.line_chart([random.randint(60, 100) for _ in range(10)])

elif page == "🧠 Memory":
    st.title("🧠 Memory")
    st.json(mem)

elif page == "🔌 Plugins":
    st.title("🔌 Plugins")

    if "BIM_CORE_V30" not in mem["plugins"]:
        mem["plugins"].append("BIM_CORE_V30")

    st.json(mem["plugins"])

elif page == "⚙ Settings":
    st.title("⚙ Settings")

    if st.button("Reset System"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active = None
        save_memory()
        st.success("Reset complete")