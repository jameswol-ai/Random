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
# STUDIO VISUAL SYSTEM
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body, [data-testid="stSidebarNav"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
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
    margin: 15px 0;
}

.arc-room-module {
    flex: 1 1 calc(33.333% - 16px);
    min-width: 220px;
    padding: 20px;
    border-radius: 8px;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 10px 15px rgba(0,0,0,0.3);
    transition: 0.25s ease;
}

.arc-room-module:hover {
    transform: translateY(-3px);
    border-color: rgba(255,255,255,0.3);
    box-shadow: 0 20px 25px rgba(0,0,0,0.5);
}

.room-meta {
    font-family: 'Space Grotesk', monospace;
    font-size: 0.85rem;
    opacity: 0.8;
    margin-top: 8px;
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
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        MEMORY_FILE.write_text(
            json.dumps(st.session_state.memory, indent=2),
            encoding="utf-8"
        )
    except Exception:
        pass

def log_event(msg: str):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# session init
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if "active_history" not in st.session_state:
    st.session_state.active_history = []

mem = st.session_state.memory

# =========================================================
# ENGINE CORE
# =========================================================

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse"],
    "Commercial": ["Boutique Office", "Corporate Hub", "Hotel Resort", "Medical Clinic"],
    "Industrial": ["Distribution Warehouse", "Advanced Manufacturing Plant"]
}

def get_domain(btype):
    for domain, items in ARCH_DOMAINS.items():
        if btype in items:
            return domain
    return "Unknown"

def generate_base_design(btype, bedrooms):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": get_domain(btype),
        "bedrooms": bedrooms,
        "rooms": ["Living", "Kitchen", "Bathroom"] + ["Flex"] * random.randint(1, 3),
        "area_sqm": 65 + 44 + bedrooms * 18,
        "structure": {
            "columns": random.randint(14, 36),
            "beams": random.randint(28, 72)
        },
        "cost": 0
    }

def mutate_design(d):
    d = json.loads(json.dumps(d))

    d["structure"]["columns"] = max(10, d["structure"]["columns"] + random.randint(-2, 4))
    d["structure"]["beams"] = max(16, d["structure"]["beams"] + random.randint(-4, 6))

    if random.random() > 0.5:
        d["rooms"].append("Adaptive Terrace")
        d["area_sqm"] += 20

    d["cost"] = int(d["area_sqm"] * random.randint(1300, 2500))
    return d

def calculate_fitness(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])

    return {
        "structural": max(0, 100 - int(abs(ratio - 2.1) * 22)),
        "cost": max(0, 100 - int(abs(d["cost"]/max(1,d["area_sqm"]) - 1650) * 0.04)),
        "complexity": min(100, len(d["rooms"]) * 9)
    }

def score(fit):
    return int(sum(fit.values()) / len(fit))

def run_evolution(btype, bedrooms, gens, pop):
    population = [generate_base_design(btype, bedrooms) for _ in range(pop)]
    history = []

    for _ in range(gens):
        scored = []

        for d in population:
            d["fitness"] = calculate_fitness(d)
            d["score"] = score(d["fitness"])
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop // 2)]

        population = []
        for s in survivors:
            population.append(s)
            population.append(mutate_design(s))

        population = population[:pop]

    return scored[0], history

def generate_floor_plan(design):
    rooms = [
        {"name": "Living Lounge", "w": 6.5, "h": 5.0, "color": "#1e3a8a"},
        {"name": "Kitchen", "w": 4.5, "h": 4.0, "color": "#064e3b"},
        {"name": "Bathroom", "w": 3.0, "h": 2.5, "color": "#78350f"}
    ]

    for i in range(design["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4.5 if i == 0 else 4.0,
            "h": 4.0,
            "color": "#4c1d95"
        })

    return rooms

def render_blueprint(plan):
    html = '<div class="arc-blueprint-canvas">'
    for r in plan:
        html += f"""
        <div class="arc-room-module" style="background:{r['color']}">
            <div style="font-weight:600">{r['name']}</div>
            <div class="room-meta">{r['w']}m × {r['h']}m</div>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# UI
# =========================================================

st.sidebar.title("📐 Arc Studio")

page = st.sidebar.radio(
    "Workspace",
    ["Dashboard", "Design Lab", "Memory"]
)

with st.sidebar.expander("Engine Config"):
    typologies = sum(ARCH_DOMAINS.values(), [])
    btype = st.selectbox("Type", typologies)
    bedrooms = st.slider("Bedrooms", 1, 8, 3)
    gens = st.slider("Generations", 2, 20, 6)
    pop = st.slider("Population", 4, 30, 10)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("📐 Studio Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Evolution Runs", len(mem["evolution"]))

    st.subheader("Logs")
    for l in mem["logs"][-6:]:
        st.caption(f"{l['time'][11:19]} — {l['msg']}")

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "Design Lab":
    st.title("🌍 Generative Design Lab")

    if st.button("Run Evolution", use_container_width=True):
        best, hist = run_evolution(btype, bedrooms, gens, pop)
        best["plan"] = generate_floor_plan(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6].upper(),
            "best": best["id"],
            "score": best["score"],
            "time": datetime.now().isoformat()
        })

        st.session_state.active_design = best
        st.session_state.active_history = hist

        log_event(f"Generated design {best['id']}")

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.subheader(f"Design {d['id']}")

        st.metric("Score", d["score"])
        st.metric("Area", d["area_sqm"])
        st.metric("Cost", d["cost"])

        render_blueprint(d["plan"])

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory")

    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        st.session_state.active_history = []
        save_memory()
        st.rerun()
