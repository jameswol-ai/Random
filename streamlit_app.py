# =============================
# ARC STUDIO V15
# AEC + BIM + EVOLUTION ENGINE CORE
# =============================

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
    page_title="Arc Studio V15 - AEC Engine",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "bim_models": [],
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

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory

# =========================================================
# AEC BIM DATA MODEL (NEW CORE ADDITION)
# =========================================================

def create_bim_model(design):
    """Turns raw design into BIM-like structured object"""

    floors = design.get("floors", 1)
    bedrooms = design.get("bedrooms", 1)

    bim = {
        "project_id": design["id"],
        "architecture": {
            "floors": floors,
            "rooms": design.get("rooms", []),
            "typology": design.get("type", "Unknown")
        },
        "structure": {
            "columns": random.randint(20, 80),
            "beams": random.randint(40, 160),
            "slabs": floors,
            "foundation": "Raft Foundation"
        },
        "mep": {
            "water_system": "Pressurized Network",
            "electrical": "3-phase distribution",
            "fire_system": "Sprinkler + Hydrant",
            "drainage": "Gravity + Pump Assist"
        },
        "hvac": {
            "system": "VRF / Central Chiller Hybrid",
            "air_handling_units": random.randint(1, floors),
            "cooling_load_kw": random.randint(50, 500),
            "zones": floors * 2
        },
        "cost_model": {
            "structure_cost": 0,
            "mep_cost": 0,
            "hvac_cost": 0,
            "total": 0
        }
    }

    return bim

# =========================================================
# AEC COST ENGINE (NEW)
# =========================================================

def calculate_costs(bim):
    base_structure = bim["structure"]["columns"] * 1200
    base_mep = bim["architecture"]["floors"] * 15000
    base_hvac = bim["hvac"]["cooling_load_kw"] * 300

    total = base_structure + base_mep + base_hvac

    bim["cost_model"] = {
        "structure_cost": base_structure,
        "mep_cost": base_mep,
        "hvac_cost": base_hvac,
        "total": total
    }

    return bim

# =========================================================
# GENETIC ENGINE (SIMPLIFIED V15 CORE)
# =========================================================

def generate_design():
    return {
        "id": str(uuid.uuid4())[:8],
        "type": random.choice(["Residential", "Commercial", "Industrial"]),
        "floors": random.randint(1, 20),
        "bedrooms": random.randint(1, 6),
        "rooms": ["Living", "Kitchen", "Bath", "Flex"],
        "area": random.randint(80, 2000)
    }

def evolve_design(d):
    d = json.loads(json.dumps(d))
    d["floors"] = max(1, d["floors"] + random.randint(-1, 3))
    d["area"] += random.randint(-50, 120)
    return d

def run_evolution(n=10):
    population = [generate_design() for _ in range(n)]
    best = population[0]

    for p in population:
        if p["area"] > best["area"]:
            best = p

    return best

# =========================================================
# BIM PIPELINE (NEW CORE FEATURE)
# =========================================================

def build_full_bim(design):
    bim = create_bim_model(design)
    bim = calculate_costs(bim)
    return bim

import plotly.graph_objects as go

# =========================================================
# 2D FLOOR PLAN ENGINE (SIMPLIFIED BIM DRAWING LAYER)
# =========================================================

def generate_2d_plan(design):
    rooms = design.get("rooms", ["Living", "Kitchen", "Bath", "Bedroom"])

    layout = []
    x, y = 0, 0

    for i, room in enumerate(rooms):
        w = random.randint(3, 6)
        h = random.randint(3, 6)

        layout.append({
            "name": room,
            "x": x,
            "y": y,
            "w": w,
            "h": h
        })

        x += w + 1
        if x > 10:
            x = 0
            y += h + 1

    return layout


def draw_2d_plan(layout):
    fig = go.Figure()

    for r in layout:
        fig.add_shape(
            type="rect",
            x0=r["x"],
            y0=r["y"],
            x1=r["x"] + r["w"],
            y1=r["y"] + r["h"],
            line=dict(color="white"),
            fillcolor="rgba(0,150,255,0.3)"
        )

        fig.add_annotation(
            x=r["x"] + r["w"]/2,
            y=r["y"] + r["h"]/2,
            text=r["name"],
            showarrow=False,
            font=dict(color="white", size=10)
        )

    fig.update_layout(
        title="2D BIM Floor Plan",
        paper_bgcolor="black",
        plot_bgcolor="black",
        height=600
    )

    return fig


# =========================================================
# 3D BUILDING ENGINE (BIM MASSING MODEL)
# =========================================================

def generate_3d_model(design):
    floors = design.get("floors", 1)

    x, y, z = [], [], []

    for f in range(floors):
        x.extend([0, 10, 10, 0, 0])
        y.extend([0, 0, 10, 10, 0])
        z.extend([f, f, f, f, f])

    return x, y, z


def draw_3d_model(design):
    x, y, z = generate_3d_model(design)

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=dict(color="cyan", width=5)
            )
        ]
    )

    fig.update_layout(
        title="3D BIM Building Massing",
        scene=dict(
            xaxis=dict(title="X"),
            yaxis=dict(title="Y"),
            zaxis=dict(title="Floors")
        ),
        paper_bgcolor="black",
        height=600
    )

    return fig


# =========================================================
# AI COPILOT (RULE-BASED ENGINE V1)
# =========================================================

def ai_copilot(command, design, bim):
    cmd = command.lower()

    if "cost" in cmd:
        return f"💰 Total cost is {bim['cost_model']['total']:,}. Reduce floors or MEP systems to optimize."

    if "reduce cost" in cmd:
        return "⚡ Suggestion: reduce HVAC load and structural columns by 10–15%."

    if "increase floors" in cmd:
        return "🏗️ Structural check: safe to increase up to +3 floors with current system."

    if "hvac" in cmd:
        return f"🌬 HVAC system uses {bim['hvac']['system']} with {bim['hvac']['cooling_load_kw']} kW load."

    if "optimize" in cmd:
        return "🧠 Optimization: balance structural density and HVAC zoning for efficiency gain."

    return "🤖 Command not recognized. Try: cost, hvac, optimize, reduce cost, increase floors"


# =========================================================
# STREAMLIT UI EXTENSION
# =========================================================

st.sidebar.markdown("## 🧠 AI Copilot")
user_prompt = st.sidebar.text_input("Ask Arc AI (cost, hvac, optimize...)")

# =========================================================
# MAIN UI TABS EXTENSION
# =========================================================

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if st.session_state.active_design:

    design = st.session_state.active_design
    bim = build_full_bim(design)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏗 BIM Dashboard",
        "📐 2D Floor Plan",
        "🏙 3D Model",
        "🤖 AI Copilot"
    ])

    # -------------------------
    # BIM DASHBOARD
    # -------------------------
    with tab1:
        st.subheader("BIM Model Overview")
        st.json(bim)

    # -------------------------
    # 2D FLOOR PLAN
    # -------------------------
    with tab2:
        layout = generate_2d_plan(design)
        fig = draw_2d_plan(layout)
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # 3D MODEL
    # -------------------------
    with tab3:
        fig3d = draw_3d_model(design)
        st.plotly_chart(fig3d, use_container_width=True)

    # -------------------------
    # AI COPILOT
    # -------------------------
    with tab4:
        st.subheader("Arc AI Copilot Response")

        if user_prompt:
            response = ai_copilot(user_prompt, design, bim)
            st.success(response)
        else:
            st.info("Ask something like: 'reduce cost' or 'optimize hvac'")
