# =============================
# ARC STUDIO ENGINE v13.1
# BEAUTIFIED BIM + AI UI REVAMP
# =============================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Arc Studio BIM",
    page_icon="🏗️",
    layout="wide"
)

# =========================================================
# GLOBAL STYLE (CLEAN STUDIO UI)
# =========================================================

st.markdown("""
<style>
body {
    background-color: #0b1220;
    color: #e5e7eb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #ffffff;
}

.stMetric {
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
}

.card {
    background: rgba(255,255,255,0.06);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 10px;
}

.badge {
    display:inline-block;
    padding:4px 10px;
    border-radius:20px;
    background:#1f2937;
    font-size:12px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

MEMORY_FILE = Path("arc_memory.json")

DEFAULT = {"models": [], "logs": []}

def load():
    if MEMORY_FILE.exists():
        return json.load(open(MEMORY_FILE))
    return DEFAULT.copy()

def save(mem):
    json.dump(mem, open(MEMORY_FILE, "w"), indent=2)

if "mem" not in st.session_state:
    st.session_state.mem = load()

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.mem

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏗 Arc Studio BIM")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "🏢 BIM Studio", "📊 Analytics"]
)

st.sidebar.markdown("---")

building_type = st.sidebar.selectbox(
    "Building Type",
    ["Residential", "Commercial", "Industrial"]
)

floors = st.sidebar.slider("Floors", 1, 60, 10)
rooms_pf = st.sidebar.slider("Rooms per Floor", 1, 12, 5)

# =========================================================
# BIM GENERATOR
# =========================================================

def generate_model():
    floors_data = []

    for f in range(floors):
        floors_data.append({
            "level": f,
            "spaces": [
                {
                    "name": f"Room_{f}_{r}",
                    "area": random.randint(20, 80)
                }
                for r in range(rooms_pf)
            ]
        })

    return {
        "id": str(uuid.uuid4())[:8],
        "type": building_type,
        "floors": floors_data
    }

# =========================================================
# AI ENGINE
# =========================================================

def ai_review(model):
    total_area = sum(s["area"] for f in model["floors"] for s in f["spaces"])

    issues = []
    suggestions = []

    if total_area < 2000:
        issues.append("Low total spatial capacity")
        suggestions.append("Increase floor area or room density")

    return issues, suggestions

# =========================================================
# COST + MEP
# =========================================================

def boq(model):
    area = sum(s["area"] for f in model["floors"] for s in f["spaces"])
    return {
        "Concrete": area * 130 * 0.35,
        "Steel": area * 950 * 0.08,
        "Finishes": area * 120
    }

def mep(model):
    area = sum(s["area"] for f in model["floors"] for s in f["spaces"])
    return {
        "Power (kW)": area * 0.1,
        "Water (L/day)": area * 18,
        "Cooling (kW)": area * 0.08
    }

# =========================================================
# VISUALS
# =========================================================

def render_2d(model):
    fig = go.Figure()
    y = 0

    for f in model["floors"]:
        x = 0
        for s in f["spaces"]:
            size = s["area"] ** 0.5

            fig.add_shape(
                type="rect",
                x0=x, y0=y,
                x1=x+size, y1=y+size,
                fillcolor="rgba(99,102,241,0.4)",
                line=dict(color="white")
            )

            x += size + 1
        y += 10

    fig.update_layout(
        paper_bgcolor="#0b1220",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

def render_3d(model):
    fig = go.Figure()

    for f in model["floors"]:
        z = f["level"] * 3

        fig.add_trace(go.Mesh3d(
            x=[0,10,10,0],
            y=[0,0,10,10],
            z=[z,z,z,z],
            opacity=0.4
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# DASHBOARD UI
# =========================================================

st.title("🏗 Arc Studio BIM Engine")

if page == "🏠 Dashboard":

    st.markdown("### System Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Models", len(mem["models"]))
    c2.metric("Active Type", building_type)
    c3.metric("Floors", floors)

    st.markdown("---")

    if st.button("🚀 Generate BIM Model"):
        model = generate_model()
        st.session_state.active = model
        mem["models"].append(model)
        save(mem)

    if st.session_state.active:

        model = st.session_state.active

        st.markdown("## 🏢 Active BIM Model")

        issues, suggestions = ai_review(model)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ⚠ Issues")
            for i in issues:
                st.error(i)

        with col2:
            st.markdown("### 💡 Suggestions")
            for s in suggestions:
                st.info(s)

        tab1, tab2 = st.tabs(["🗺 2D Plan", "🏢 3D Model"])

        with tab1:
            render_2d(model)

        with tab2:
            render_3d(model)

elif page == "🏢 BIM Studio":
    st.markdown("### BIM Data Viewer")
    st.json(st.session_state.active)

elif page == "📊 Analytics":

    if st.session_state.active:
        model = st.session_state.active

        st.markdown("### 💰 Cost Estimate")
        st.json(boq(model))

        st.markdown("### 🌬 MEP Systems")
        st.json(mep(model))

        st.markdown("### 📊 Insights")

        st.line_chart([random.randint(60, 100) for _ in range(10)])

    else:
        st.info("Generate a model first")
