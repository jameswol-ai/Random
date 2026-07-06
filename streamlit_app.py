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
# CONFIG & GLOBAL STYLING
# =========================================================

st.set_page_config(
    page_title="Random Studio Engine",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
}

.arc-blueprint-canvas {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    background: #0b0f1a;
    padding: 24px;
    border-radius: 12px;
    border: 1px dashed #334155;
}

.arc-room-module {
    flex: 1 1 calc(33.333% - 16px);
    min-width: 220px;
    padding: 18px;
    border-radius: 10px;
    color: white;
    border: 1px solid rgba(255,255,255,0.12);
    transition: 0.2s ease;
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
# MEMORY SYSTEM
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
            return json.loads(MEMORY_FILE.read_text())
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()


def save_memory():
    MEMORY_FILE.write_text(json.dumps(st.session_state.memory, indent=2))


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

if "active_history" not in st.session_state:
    st.session_state.active_history = []

mem = st.session_state.memory

# =========================================================
# ARCHITECTURAL ENGINE
# =========================================================

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse"],
    "Commercial": ["Boutique Office", "Corporate Hub", "Hotel Resort"],
    "Industrial": ["Warehouse", "Manufacturing Plant"]
}


def get_domain(t):
    for k, v in ARCH_DOMAINS.items():
        if t in v:
            return k
    return "Unknown"


def generate_base_design(btype, bedrooms):
    rooms = ["Living Room", "Kitchen", "Bathroom"] + ["Flex Space"] * random.randint(1, 3)

    area = 80 + (bedrooms * 20)

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": get_domain(btype),
        "bedrooms": bedrooms,
        "rooms": rooms,
        "area_sqm": area,
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(20, 80)
        },
        "cost": area * random.randint(1200, 2500)
    }


def mutate_design(d):
    d = json.loads(json.dumps(d))

    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-3, 5)

    if random.random() > 0.6:
        d["rooms"].append("Extended Living Deck")
        d["area_sqm"] += 15

    d["cost"] = d["area_sqm"] * random.randint(1200, 2600)

    return d


def fitness(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    structural = max(0, 100 - abs(ratio - 2.0) * 25)

    cost_sqm = d["cost"] / max(1, d["area_sqm"])
    cost = max(0, 100 - abs(cost_sqm - 1600) * 0.05)

    space = min(100, len(d["rooms"]) * 10)

    return {
        "structural": structural,
        "cost": cost,
        "space": space
    }


def score(f):
    return int(sum(f.values()) / len(f))


def evolve(btype, bedrooms, gens, pop):
    population = [generate_base_design(btype, bedrooms) for _ in range(pop)]
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
            new_pop.append(mutate_design(s))

        population = new_pop[:pop]

    return scored[0], history


def generate_floor_plan(d):
    rooms = [
        {"name": "Living Lounge", "w": 6, "h": 5, "color": "#1e3a8a"},
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
    typology = st.selectbox(
        "Type",
        sum(ARCH_DOMAINS.values(), [])
    )
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
    c2.metric("Evolutions", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

    st.subheader("Logs")

    for log in mem["logs"][-5:]:
        st.caption(f"{log['time'][11:19]} — {log['msg']}")

# =========================================================
# SYNTHESIS
# =========================================================

elif page == "Synthesis Lab":
    st.title("🌍 Evolution Engine")

    if st.button("Generate Architecture"):
        best, history = evolve(typology, bedrooms, gens, pop)

        best["plan"] = generate_floor_plan(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6].upper(),
            "best": best["id"],
            "score": best["score"],
            "time": datetime.now().isoformat()
        })

        st.session_state.active_design = best
        st.session_state.active_history = history

        log_event(f"Generated {best['id']}")

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.subheader(f"Design {d['id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", d["score"])
        c2.metric("Area", d["area_sqm"])
        c3.metric("Cost", d["cost"])

        st.markdown("### Floor Plan")

        canvas = '<div class="arc-blueprint-canvas">'
        for r in d["plan"]:
            canvas += f"""
            <div class="arc-room-module" style="background:{r['color']}">
                <b>{r['name']}</b>
                <div class="room-meta">{r['w']}m × {r['h']}m</div>
            </div>
            """
        canvas += "</div>"

        st.markdown(canvas, unsafe_allow_html=True)

        st.line_chart(st.session_state.active_history)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory Bank")

    st.json(mem)

    if st.button("Reset"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        st.session_state.active_history = []
        save_memory()
        st.rerun()
