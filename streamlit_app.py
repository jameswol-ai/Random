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
# CONFIG & GLOBAL STUDIO STYLING
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
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    transition: all 0.25s ease;
}

.arc-room-module:hover {
    transform: translateY(-3px);
    border-color: rgba(255, 255, 255, 0.3);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
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
# SYSTEM MEMORY
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
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except Exception:
        pass

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
    "Commercial": ["Boutique Office", "Corporate Hub", "Hotel Resort", "Medical Clinic"],
    "Industrial": ["Distribution Warehouse", "Advanced Manufacturing Plant"]
}

def get_domain(btype):
    for domain, types in ARCH_DOMAINS.items():
        if btype in types:
            return domain
    return "Unknown"

def generate_base_design(btype, bedrooms):
    core_rooms = ["Living Room", "Kitchen", "Bathroom"] + ["Flex Space"] * random.randint(1, 3)
    est_area = 65 + 44 + (bedrooms * 18)

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": get_domain(btype),
        "bedrooms": bedrooms,
        "rooms": core_rooms,
        "area_sqm": est_area,
        "structure": {
            "columns": random.randint(14, 36),
            "beams": random.randint(28, 72)
        },
        "cost": int(est_area * random.randint(1400, 2600))
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
    struct_score = max(0, 100 - int(abs(ratio - 2.1) * 22))

    cost_per_sqm = d["cost"] / max(1, d["area_sqm"])
    cost_score = max(0, 100 - int(abs(cost_per_sqm - 1650) * 0.04))

    complexity = min(100, len(d["rooms"]) * 9)

    return {
        "structural": struct_score,
        "cost": cost_score,
        "complexity": complexity
    }

def score(fit):
    return int(sum(fit.values()) / len(fit))

def run_evolution(btype, bedrooms, gens, pop):
    population = [generate_base_design(btype, bedrooms) for _ in range(pop)]
    history = []

    for _ in range(gens):
        scored = []

        for d in population:
            fit = calculate_fitness(d)
            d["fitness"] = fit
            d["score"] = score(fit)
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

def log(msg):
    log_event(msg)

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

        log(f"Generated design {best['id']}")

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
