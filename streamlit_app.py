# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# Evolutionary Spatial Layout Synthesis & Diagnostics
# Streamlit Modular Implementation (Clean Refactor)
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
# UI STYLING
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
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
}

.arc-room-module {
    flex: 1 1 calc(33.333% - 16px);
    min-width: 220px;
    padding: 20px;
    border-radius: 8px;
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
    try:
        MEMORY_FILE.write_text(json.dumps(st.session_state.memory, indent=2))
    except:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# init
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if "active_history" not in st.session_state:
    st.session_state.active_history = []

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE DOMAIN LOGIC
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

# =========================================================
# GENERATION ENGINE
# =========================================================

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

# =========================================================
# FITNESS FUNCTION
# =========================================================

def calculate_fitness(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    structural = max(0, 100 - int(abs(ratio - 2.1) * 22))

    cost_per_sqm = d["cost"] / max(1, d["area_sqm"])
    cost_eff = max(0, 100 - int(abs(cost_per_sqm - 1650) * 0.04))

    complexity = min(100, len(d["rooms"]) * 9)

    return {
        "structural": structural,
        "cost": cost_eff,
        "complexity": complexity
    }

def score(f):
    return int(sum(f.values()) / len(f))

# =========================================================
# EVOLUTION LOOP
# =========================================================

def run_evolution(btype, bedrooms, generations, pop_size):
    population = [generate_base_design(btype, bedrooms) for _ in range(pop_size)]
    history = []

    for _ in range(generations):
        scored = []

        for d in population:
            fit = calculate_fitness(d)
            d["fitness"] = fit
            d["score"] = score(fit)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop_size // 2)]

        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate_design(s))

        population = new_pop[:pop_size]

    return scored[0], history

# =========================================================
# FLOOR PLAN
# =========================================================

def generate_floor_plan(design):
    rooms = [
        {"name": "Living Lounge", "w": 6.5, "h": 5.0, "color": "#1e3a8a"},
        {"name": "Kitchen", "w": 4.5, "h": 4.0, "color": "#064e3b"}
    ]

    for i in range(design["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4.5 if i == 0 else 4.0,
            "h": 4.0,
            "color": "#4c1d95"
        })

    return rooms

# =========================================================
# VISUAL RENDER
# =========================================================

def render_blueprint(plan):
    st.markdown("### 🗺️ Layout Canvas")

    html = '<div class="arc-blueprint-canvas">'
    for r in plan:
        html += f"""
        <div class="arc-room-module" style="background:{r['color']}">
            <div>{r['name']}</div>
            <div class="room-meta">{r['w']}m × {r['h']}m</div>
        </div>
        """
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# ANALYTICS
# =========================================================

def structural_review(d):
    alerts = []

    if d["structure"]["columns"] < 16:
        alerts.append("🔴 Column density too low for load distribution")

    if d["cost"] / d["area_sqm"] > 2300:
        alerts.append("🟡 Cost efficiency threshold exceeded")

    if d["structure"]["beams"] / d["structure"]["columns"] < 1.9:
        alerts.append("🔵 Beam-column ratio imbalance detected")

    return alerts or ["🟢 Design structurally stable"]

# =========================================================
# UI
# =========================================================

st.sidebar.title("📐 Arc Studio")

page = st.sidebar.radio(
    "Workspace",
    ["Dashboard", "Design Lab", "Memory"]
)

typology = st.sidebar.selectbox(
    "Typology",
    sum(ARCH_DOMAINS.values(), [])
)

bedrooms = st.sidebar.slider("Bedrooms", 1, 8, 3)
gens = st.sidebar.slider("Generations", 2, 20, 6)
pop = st.sidebar.slider("Population", 4, 30, 10)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("📐 Studio Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Projects", len(mem["projects"]))
    col2.metric("Designs", len(mem["designs"]))
    col3.metric("Evolution Runs", len(mem["evolution"]))

    st.subheader("Logs")
    for log in mem["logs"][-6:]:
        st.caption(f"{log['time']} - {log['msg']}")

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "Design Lab":
    st.title("🌍 Generative Design Lab")

    if st.button("Run Evolution Engine"):
        best, history = run_evolution(typology, bedrooms, gens, pop)
        best["plan"] = generate_floor_plan(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best_id": best["id"],
            "score": best["score"],
            "time": datetime.now().isoformat()
        })

        st.session_state.active_design = best
        st.session_state.active_history = history

        log_event(f"Generated design {best['id']}")

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.subheader(f"Design {d['id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", d["score"])
        c2.metric("Area", d["area_sqm"])
        c3.metric("Cost", d["cost"])

        tab1, tab2 = st.tabs(["Blueprint", "Diagnostics"])

        with tab1:
            render_blueprint(d["plan"])

        with tab2:
            for a in structural_review(d):
                st.write(a)

# =========================================================
# MEMORY VIEW
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory Store")

    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        st.session_state.active_history = []
        save_memory()
        st.rerun()