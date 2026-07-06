# =============================
# ARC STUDIO V16 (ROBUST BUILD)
# BIM + AI + EVOLUTION ENGINE
# Dependency-safe Streamlit Architecture
# =============================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# =========================================================
# SAFE IMPORT LAYER (CRITICAL FIX)
# =========================================================

# Plotly (required for 2D/3D)
try:
    import plotly.graph_objects as go
except:
    go = None

# Pandas (optional fallback-safe)
try:
    import pandas as pd
except:
    pd = None

# NetworkX (optional MEP graph)
try:
    import networkx as nx
except:
    nx = None

# Matplotlib (optional)
try:
    import matplotlib.pyplot as plt
except:
    plt = None

# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="Arc Studio V16 - Stable BIM Engine",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# MEMORY SYSTEM (SAFE)
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "logs": []
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

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

# =========================================================
# CORE DESIGN ENGINE
# =========================================================

def generate_design():
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": random.choice(["Residential", "Commercial", "Industrial"]),
        "floors": random.randint(1, 8),
        "rooms": ["Living", "Kitchen", "Bath"],
        "area": random.randint(80, 1200)
    }

# =========================================================
# BIM ENGINE
# =========================================================

def build_bim(design):
    floors = design["floors"]

    bim = {
        "id": design["id"],
        "architecture": {"floors": floors},
        "structure": {
            "columns": random.randint(20, 70),
            "beams": random.randint(40, 140)
        },
        "hvac": {
            "cooling_load_kw": random.randint(60, 350)
        },
        "cost_model": {}
    }

    bim["cost_model"] = {
        "structure_cost": bim["structure"]["columns"] * 1200,
        "mep_cost": floors * 15000,
        "hvac_cost": bim["hvac"]["cooling_load_kw"] * 300,
    }

    bim["cost_model"]["total"] = sum(bim["cost_model"].values())

    return bim

# =========================================================
# 2D PLAN (SAFE PLOTLY CHECK)
# =========================================================

def draw_2d(design):
    if go is None:
        st.warning("Plotly not installed — 2D view disabled")
        return

    fig = go.Figure()
    x, y = 0, 0

    for room in design["rooms"]:
        w, h = random.randint(2, 5), random.randint(2, 5)

        fig.add_shape(
            type="rect",
            x0=x, y0=y,
            x1=x + w, y1=y + h
        )

        fig.add_annotation(
            x=x + w/2,
            y=y + h/2,
            text=room,
            showarrow=False
        )

        x += w + 1

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 3D MODEL (SAFE)
# =========================================================

def draw_3d(design):
    if go is None:
        st.warning("Plotly not installed — 3D view disabled")
        return

    floors = design["floors"]
    x, y, z = [], [], []

    for f in range(floors):
        x += [0, 10, 10, 0, 0]
        y += [0, 0, 10, 10, 0]
        z += [f]*5

    fig = go.Figure(
        data=[go.Scatter3d(x=x, y=y, z=z, mode="lines")]
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# OPTIONAL MEP GRAPH
# =========================================================

def draw_mep():
    if nx is None or plt is None:
        st.warning("NetworkX not installed — MEP graph disabled")
        return

    G = nx.Graph()
    G.add_edges_from([
        ("Water", "Drainage"),
        ("Power", "HVAC"),
        ("Fire", "Water")
    ])

    plt.figure()
    nx.draw(G, with_labels=True)
    st.pyplot(plt)

# =========================================================
# AI COPILOT
# =========================================================

def ai(cmd, bim):
    cmd = cmd.lower()

    if "cost" in cmd:
        return f"Total cost: {bim['cost_model']['total']:,}"
    if "hvac" in cmd:
        return f"Cooling load: {bim['hvac']['cooling_load_kw']} kW"
    if "optimize" in cmd:
        return "Reduce floors or HVAC load for efficiency gain"
    return "Try: cost, hvac, optimize"

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏗 Arc Studio V16")

if st.sidebar.button("Generate Design"):
    st.session_state.active_design = generate_design()
    log("Design generated")

design = st.session_state.active_design

if design:
    bim = build_bim(design)

    tab1, tab2, tab3, tab4 = st.tabs([
        "BIM", "2D", "3D", "MEP"
    ])

    with tab1:
        st.json(bim)

    with tab2:
        draw_2d(design)

    with tab3:
        draw_3d(design)

    with tab4:
        draw_mep()

    st.markdown("---")
    st.subheader("🧠 Arc AI Copilot")

    cmd = st.text_input("Ask Arc")
    if cmd:
        st.success(ai(cmd, bim))
