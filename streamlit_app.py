# =============================
# ARC STUDIO V15 (FIXED BUILD)
# AEC + BIM + EVOLUTION ENGINE CORE
# =============================

import streamlit as st
import json
import uuid
import random
import re
from pathlib import Path
from datetime import datetime, timedelta

import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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
            return json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except:
        pass

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# Initialize session
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

# =========================================================
# BIM CORE
# =========================================================

def create_bim_model(design):
    floors = design.get("floors", 1)

    return {
        "id": design["id"],
        "architecture": {
            "floors": floors,
            "rooms": design.get("rooms", []),
            "typology": design.get("type", "Unknown")
        },
        "structure": {
            "columns": random.randint(20, 80),
            "beams": random.randint(40, 160),
            "slabs": floors
        },
        "hvac": {
            "system": "VRF Hybrid",
            "cooling_load_kw": random.randint(50, 400),
            "zones": floors * 2
        },
        "cost_model": {}
    }

def calculate_costs(bim):
    floors = bim["architecture"]["floors"]

    structure = bim["structure"]["columns"] * 1200
    mep = floors * 15000
    hvac = bim["hvac"]["cooling_load_kw"] * 300

    bim["cost_model"] = {
        "structure_cost": structure,
        "mep_cost": mep,
        "hvac_cost": hvac,
        "total": structure + mep + hvac
    }

    return bim

def build_full_bim(design):
    return calculate_costs(create_bim_model(design))

# =========================================================
# DESIGN GENERATION
# =========================================================

def generate_design():
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": random.choice(["Residential", "Commercial", "Industrial"]),
        "floors": random.randint(1, 10),
        "bedrooms": random.randint(1, 5),
        "rooms": ["Living", "Kitchen", "Bath"],
        "area": random.randint(80, 1200)
    }

# =========================================================
# 2D + 3D ENGINE
# =========================================================

def generate_2d_plan(design):
    layout = []
    x, y = 0, 0

    for room in design.get("rooms", []):
        w, h = random.randint(3, 6), random.randint(3, 6)

        layout.append({"name": room, "x": x, "y": y, "w": w, "h": h})

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
            x0=r["x"], y0=r["y"],
            x1=r["x"] + r["w"],
            y1=r["y"] + r["h"]
        )
        fig.add_annotation(
            x=r["x"] + r["w"]/2,
            y=r["y"] + r["h"]/2,
            text=r["name"],
            showarrow=False
        )

    fig.update_layout(height=500, title="2D Floor Plan")
    return fig

def generate_3d_model(design):
    floors = design.get("floors", 1)

    x, y, z = [], [], []
    for f in range(floors):
        x += [0, 10, 10, 0, 0]
        y += [0, 0, 10, 10, 0]
        z += [f]*5

    return x, y, z

def draw_3d_model(design):
    x, y, z = generate_3d_model(design)

    fig = go.Figure(
        data=[go.Scatter3d(x=x, y=y, z=z, mode="lines")]
    )

    fig.update_layout(height=500, title="3D Massing Model")
    return fig

# =========================================================
# ENGINEERING LAYERS
# =========================================================

def structural_engine(bim):
    return {
        "load_per_column": random.uniform(120, 450),
        "efficiency": random.uniform(65, 95)
    }

def hvac_zoning(bim):
    return [
        {
            "floor": i + 1,
            "zone": random.choice(["Cooling", "Heating", "Mixed"])
        }
        for i in range(bim["architecture"]["floors"])
    ]

def generate_mep_graph():
    G = nx.Graph()
    nodes = ["Water", "Power", "HVAC", "Drainage", "Fire"]

    for n in nodes:
        G.add_node(n)

    G.add_edges_from([
        ("Water", "Drainage"),
        ("Power", "HVAC"),
        ("Fire", "Water")
    ])

    return G

def draw_mep_graph(G):
    plt.figure()
    nx.draw(G, with_labels=True)
    st.pyplot(plt)

# =========================================================
# AI COPILOT
# =========================================================

def ai_copilot(cmd, bim):
    cmd = cmd.lower()

    if "cost" in cmd:
        return f"Total cost: {bim['cost_model']['total']:,}"
    if "hvac" in cmd:
        return f"HVAC load: {bim['hvac']['cooling_load_kw']} kW"
    if "optimize" in cmd:
        return "Reduce floors or HVAC load for efficiency"
    return "Try: cost, hvac, optimize"

# =========================================================
# UI
# =========================================================

st.sidebar.title("Arc Studio V15")
if st.sidebar.button("Generate Design"):
    design = generate_design()
    st.session_state.active_design = design
    log("Design generated")

if st.session_state.active_design:
    design = st.session_state.active_design
    bim = build_full_bim(design)

    tab1, tab2, tab3, tab4 = st.tabs([
        "BIM", "2D", "3D", "Copilot"
    ])

    with tab1:
        st.json(bim)

    with tab2:
        st.plotly_chart(draw_2d_plan(generate_2d_plan(design)))

    with tab3:
        st.plotly_chart(draw_3d_model(design))

    with tab4:
        cmd = st.text_input("Ask Arc AI")
        if cmd:
            st.success(ai_copilot(cmd, bim))
