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

st.markdown(
"""
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
""",
unsafe_allow_html=True
)

# =========================================================
# SYSTEM MEMORY MANAGEMENT
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


# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if "active_history" not in st.session_state:
    st.session_state.active_history = []

mem = st.session_state.memory

# =========================================================
# ARCHITECTURAL GENETICS ENGINE
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
    core_rooms = (
        ["Living Room", "Gourmet Kitchen", "Primary Bathroom"]
        + ["Flex Space"] * random.randint(1, 3)
    )

    est_area = 65 + 44 + (3 * 3) + (bedrooms * 18)

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


def mutate_design(design):
    d = json.loads(json.dumps(design))

    d["structure"]["columns"] = max(
        10, d["structure"]["columns"] + random.randint(-2, 4)
    )
    d["structure"]["beams"] = max(
        16, d["structure"]["beams"] + random.randint(-4, 6)
    )

    if random.random() > 0.5:
        d["rooms"].append("Adaptive Modular Terracing")
        d["area_sqm"] += 20

    d["cost"] = int(
        d["area_sqm"] * random.randint(1300, 2500)
        + d["structure"]["columns"] * 600
    )

    return d


def calculate_fitness(d):
    structural_ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    struct_score = max(0, 100 - int(abs(structural_ratio - 2.1) * 22))

    cost_per_sqm = d["cost"] / max(1, d["area_sqm"])
    cost_score = max(0, 100 - int(abs(cost_per_sqm - 1650) * 0.04))

    complexity_score = min(100, len(d["rooms"]) * 9)

    return {
        "structural_integrity": struct_score,
        "cost_efficiency": cost_score,
        "spatial_complexity": complexity_score
    }


def aggregate_score(fit):
    return int(sum(fit.values()) / len(fit))


def run_evolutionary_loop(btype, bedrooms, generations, pop_size):
    population = [
        generate_base_design(btype, bedrooms)
        for _ in range(pop_size)
    ]

    history = []

    for _ in range(generations):
        scored_pop = []

        for d in population:
            fit = calculate_fitness(d)
            d["fitness"] = fit
            d["score"] = aggregate_score(fit)
            scored_pop.append(d)

        scored_pop.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored_pop[0]["score"])

        survivors = scored_pop[:max(2, pop_size // 2)]

        new_generation = []
        for parent in survivors:
            new_generation.append(parent)
            new_generation.append(mutate_design(parent))

        population = new_generation[:pop_size]

    return scored_pop[0], history


def generate_floor_plan(design):
    rooms = [
        {"name": "Grand Living Lounge", "w": 6.5, "h": 5.0, "color": "#1e3a8a"},
        {"name": "Culinary Kitchen", "w": 4.5, "h": 4.0, "color": "#064e3b"},
        {"name": "Central Powder Room", "w": 3.0, "h": 2.5, "color": "#78350f"},
    ]

    for i in range(design["bedrooms"]):
        rooms.append({
            "name": f"{'Master Suite' if i == 0 else 'Bedroom'} {i+1}",
            "w": 4.5 if i == 0 else 4.0,
            "h": 4.0,
            "color": "#4c1d95"
        })

    return rooms

# =========================================================
# UI LAYOUT + VIEWPORTS (structure preserved, cleaned)
# =========================================================

st.sidebar.title("📐 Arc Studio")
st.sidebar.caption("v10.2 • Generative Structural Design Loop")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Studio Workspace",
    ["Dashboard Control", "Design Synthesis Lab", "Memory Repositories"]
)

st.sidebar.markdown("---")

with st.sidebar.expander("🛠️ Configure Arc Engine", expanded=False):
    st.subheader("Synthesis Directives")

    all_typologies = []
    for sub_list in ARCH_DOMAINS.values():
        all_typologies.extend(sub_list)

    input_type = st.selectbox("Design Typology Target", all_typologies)
    input_bedrooms = st.slider("Target Spatial Modules", 1, 8, 3)
    input_generations = st.slider("Genetic Epoch Cycles", 2, 20, 6)
    input_pop = st.slider("Population Bounds", 4, 30, 10)

# =========================================================
# DASHBOARD VIEW
# =========================================================

if page == "Dashboard Control":
    st.title("📐 Studio Control Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Tracked Space Profiles", len(mem["projects"]))
    col2.metric("Evolved Blueprint Seeds", len(mem["designs"]))
    col3.metric("Total Parametric Compute Loops", len(mem["evolution"]))

    st.markdown("---")
    st.subheader("Engine Logs")

    if mem["logs"]:
        for log in reversed(mem["logs"][-6:]):
            st.caption(f"⏱️ `{log['time'][11:19]}` — {log['msg']}")
    else:
        st.info("No logs yet.")

# =========================================================
# SYNTHESIS LAB VIEW
# =========================================================

elif page == "Design Synthesis Lab":
    st.title("🌍 Algorithmic Design Lab")

    generate_now = st.button(
        "Run Generative Architectural Evolution Pipeline",
        use_container_width=True
    )

    if generate_now:
        with st.spinner("Evolving architectural population..."):
            best, trend = run_evolutionary_loop(
                input_type,
                input_bedrooms,
                input_generations,
                input_pop
            )

            best["plan"] = generate_floor_plan(best)

            mem["designs"].append(best)
            mem["evolution"].append({
                "id": str(uuid.uuid4())[:6].upper(),
                "best_id": best["id"],
                "peak_score": best["score"],
                "timestamp": datetime.now().isoformat()
            })

            st.session_state.active_design = best
            st.session_state.active_history = trend

            log_event(f"Evolved Design {best['id']}")

    if st.session_state.active_design:
        design = st.session_state.active_design

        st.subheader(f"Design {design['id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{design['score']} / 100")
        c2.metric("Area", f"{design['area_sqm']} m²")
        c3.metric("Cost", f"${design['cost']:,}")

# =========================================================
# MEMORY VIEW
# =========================================================

elif page == "Memory Repositories":
    st.title("🧠 System Memory")

    st.json(mem)

    if st.button("Reset Memory", use_container_width=True):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        st.session_state.active_history = []
        save_memory()
        st.rerun()
