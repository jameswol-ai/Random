# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE v9
# Evolutionary Spatial Layout Synthesis & Diagnostics
# Core Generative Streamlit System (No BIM / No IFC / No AI agents)
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
    page_title="Random Studio Engine v9",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
}

.arc-blueprint {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    padding: 20px;
    background: #0b1020;
    border-radius: 12px;
    border: 1px dashed #334155;
}

.arc-room {
    flex: 1 1 calc(33% - 10px);
    min-width: 200px;
    padding: 16px;
    border-radius: 10px;
    color: white;
    box-shadow: 0 10px 20px rgba(0,0,0,0.25);
}

.meta {
    font-size: 0.8rem;
    opacity: 0.8;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM (v9 simple)
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "logs": [],
    "evolution": []
}


def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()


def save_memory():
    MEMORY_FILE.write_text(json.dumps(st.session_state.memory, indent=2))


def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()


if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.memory

# =========================================================
# CORE GENERATIVE ENGINE
# =========================================================

ARCH_TYPES = [
    "Luxury Villa",
    "Modern Apartment",
    "Townhouse",
    "Boutique Office",
    "Warehouse"
]


def generate_design():
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": random.choice(ARCH_TYPES),
        "bedrooms": random.randint(1, 6),
        "area": random.randint(120, 600),
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(20, 80)
        },
        "cost": random.randint(120000, 800000),
        "rooms": ["Living Room", "Kitchen", "Bathroom"]
    }


def mutate(d):
    d = json.loads(json.dumps(d))

    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-3, 5)

    if random.random() > 0.6:
        d["rooms"].append("Flex Space")
        d["area"] += 15

    d["cost"] = d["area"] * random.randint(1200, 2600)

    return d


def fitness(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    structural = max(0, 100 - abs(ratio - 2.0) * 20)

    cost_sqm = d["cost"] / max(1, d["area"])
    cost = max(0, 100 - abs(cost_sqm - 1500) * 0.05)

    space = min(100, len(d["rooms"]) * 12)

    return {
        "structural": structural,
        "cost": cost,
        "space": space
    }


def score(f):
    return int(sum(f.values()) / len(f))


def evolve(bedrooms, gens, pop):
    population = []

    for _ in range(pop):
        d = generate_design()
        d["bedrooms"] = bedrooms
        population.append(d)

    history = []

    for _ in range(gens):
        scored = []

        for d in population:
            f = fitness(d)
            d["fitness"] = f
            d["score"] = score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop // 2)]

        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate(s))

        population = new_pop[:pop]

    return scored[0], history


def floor_plan(d):
    rooms = [
        {"name": "Living Room", "w": 6, "h": 5, "color": "#1e3a8a"},
        {"name": "Kitchen", "w": 4, "h": 4, "color": "#064e3b"},
        {"name": "Bathroom", "w": 3, "h": 2, "color": "#78350f"}
    ]

    for i in range(d["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4,
            "h": 4,
            "color": "#4c1d95"
        })

    return rooms

# =========================================================
# UI
# =========================================================

st.sidebar.title("📐 Arc Studio")

page = st.sidebar.radio(
    "Workspace",
    ["Dashboard", "Synthesis Lab", "Memory"]
)

with st.sidebar.expander("Engine Config"):
    bedrooms = st.slider("Bedrooms", 1, 6, 3)
    gens = st.slider("Generations", 2, 15, 6)
    pop = st.slider("Population", 4, 20, 10)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("📐 Control Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution Runs", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

    st.subheader("Recent Logs")

    for log_entry in mem["logs"][-6:]:
        st.caption(f"{log_entry['time'][11:19]} — {log_entry['msg']}")

# =========================================================
# SYNTHESIS LAB
# =========================================================

elif page == "Synthesis Lab":
    st.title("🌍 Evolution Engine v9")

    if st.button("Generate Design"):
        best, history = evolve(bedrooms, gens, pop)

        best["plan"] = floor_plan(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6].upper(),
            "best": best["id"],
            "score": best["score"],
            "time": datetime.now().isoformat()
        })

        st.session_state.active = best
        st.session_state.history = history

        log(f"Generated {best['id']}")

    if st.session_state.active:
        d = st.session_state.active

        st.subheader(f"Design {d['id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", d["score"])
        c2.metric("Area", d["area"])
        c3.metric("Cost", d["cost"])

        st.markdown("### Floor Plan")

        canvas = '<div class="arc-blueprint">'
        for r in d["plan"]:
            canvas += f"""
            <div class="arc-room" style="background:{r['color']}">
                <b>{r['name']}</b>
                <div class="meta">{r['w']}m × {r['h']}m</div>
            </div>
            """
        canvas += "</div>"

        st.markdown(canvas, unsafe_allow_html=True)

        st.line_chart(st.session_state.history)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory Store")

    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active = None
        save_memory()
        st.rerun()
