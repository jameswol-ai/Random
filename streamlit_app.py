# =============================
# ARC STUDIO ENGINE v13
# BIM CORE + AI MULTI-AGENT SYSTEM
# =============================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Arc Studio BIM v13",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_bim_memory.json")

# =========================================================
# MEMORY LAYER
# =========================================================

DEFAULT = {
    "projects": [],
    "bim_models": [],
    "logs": [],
    "runs": []
}

def load():
    if MEMORY_FILE.exists():
        return json.load(open(MEMORY_FILE, "r"))
    return DEFAULT.copy()

def save():
    json.dump(st.session_state.mem, open(MEMORY_FILE, "w"), indent=2)

def log(msg):
    st.session_state.mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save()

if "mem" not in st.session_state:
    st.session_state.mem = load()

if "active_model" not in st.session_state:
    st.session_state.active_model = None

if "history" not in st.session_state:
    st.session_state.history = []

mem = st.session_state.mem

# =========================================================
# SIDEBAR BIM CONFIG
# =========================================================

st.sidebar.title("🏗️ Arc BIM Engine v13")

page = st.sidebar.radio("Navigation", ["Dashboard", "BIM Model", "Memory"])

project_name = st.sidebar.text_input("Project Name", "Arc Tower")

building_type = st.sidebar.selectbox(
    "Building Type",
    ["Residential", "Commercial", "Industrial"]
)

floors = st.sidebar.slider("Floors", 1, 100, 12)
rooms_pf = st.sidebar.slider("Rooms per Floor", 1, 20, 6)
population = st.sidebar.slider("Occupancy Load", 0, 8000, 400)

# =========================================================
# BIM DATA STRUCTURE (CORE)
# =========================================================

def generate_bim():
    building_id = str(uuid.uuid4())[:8]

    floors_data = []

    for f in range(floors):
        floor = {
            "level": f,
            "spaces": []
        }

        for r in range(rooms_pf):
            space = {
                "id": str(uuid.uuid4())[:6],
                "name": f"Room_{f}_{r}",
                "area": random.randint(20, 80),
                "type": random.choice(["Room", "Core", "Service"]),
                "elements": {
                    "walls": random.randint(4, 12),
                    "doors": random.randint(1, 4),
                    "windows": random.randint(1, 6)
                }
            }
            floor["spaces"].append(space)

        floors_data.append(floor)

    return {
        "id": building_id,
        "name": project_name,
        "type": building_type,
        "floors": floors_data,
        "meta": {
            "total_floors": floors,
            "total_spaces": floors * rooms_pf,
            "population": population
        }
    }

# =========================================================
# AI AGENT COUNCIL
# =========================================================

def ai_council(bim):
    issues = []
    suggestions = []

    total_area = sum(
        s["area"]
        for f in bim["floors"]
        for s in f["spaces"]
    )

    # Architect AI
    if total_area / len(bim["floors"]) < 300:
        issues.append("Low spatial efficiency per floor.")
        suggestions.append("Increase floor plate utilization.")

    # Structural AI
    avg_walls = sum(
        s["elements"]["walls"]
        for f in bim["floors"]
        for s in f["spaces"]
    ) / bim["meta"]["total_spaces"]

    if avg_walls < 6:
        issues.append("Low structural enclosure density.")
        suggestions.append("Increase structural partitions.")

    # Cost AI (simplified)
    cost = total_area * 1500
    if cost > 500000:
        issues.append("High projected construction cost.")
        suggestions.append("Optimize material usage and finishes.")

    # Sustainability AI
    if population > 3000:
        issues.append("High occupancy load stress.")
        suggestions.append("Improve ventilation and zoning strategy.")

    return {
        "issues": issues if issues else ["BIM model is stable."],
        "suggestions": suggestions if suggestions else ["Design is optimized."]
    }

# =========================================================
# BOQ ENGINE
# =========================================================

def boq(bim):
    area = sum(s["area"] for f in bim["floors"] for s in f["spaces"])

    return {
        "Concrete": area * 0.4 * 130,
        "Steel": area * 0.09 * 950,
        "Finishes": area * 120,
        "Doors": area * 0.8 * 120,
        "Windows": area * 0.6 * 200
    }

# =========================================================
# MEP SYSTEM (BIM LAYER)
# =========================================================

def mep(bim):
    area = sum(s["area"] for f in bim["floors"] for s in f["spaces"])

    return {
        "Electrical Load kW": area * 0.11,
        "Water Demand L/day": area * 20,
        "Cooling Load kW": area * 0.085,
        "Ventilation m3/hr": area * 5.5
    }

# =========================================================
# 2D BIM VIEW
# =========================================================

def render_2d(bim):
    fig = go.Figure()

    y_offset = 0

    for f in bim["floors"]:
        x = 0

        for s in f["spaces"]:
            w = s["area"] ** 0.5
            h = w

            fig.add_shape(
                type="rect",
                x0=x,
                y0=y_offset,
                x1=x + w,
                y1=y_offset + h,
                line=dict(color="white"),
                fillcolor="rgba(100,150,255,0.4)"
            )

            x += w + 1

        y_offset += 10

    fig.update_layout(
        height=500,
        paper_bgcolor="#0b1220"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 3D BIM VIEW
# =========================================================

def render_3d(bim):
    fig = go.Figure()

    for f in bim["floors"]:
        z = f["level"] * 3

        for s in f["spaces"]:
            size = s["area"] ** 0.5

            fig.add_trace(go.Mesh3d(
                x=[0, size, size, 0],
                y=[0, 0, size, size],
                z=[z, z, z, z],
                opacity=0.4
            ))

    fig.update_layout(scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False)
    ))

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# DASHBOARD UI
# =========================================================

st.title("🏗️ Arc Studio BIM Engine v13")

if page == "Dashboard":

    if st.button("🧠 Generate BIM Model"):
        bim = generate_bim()

        review = ai_council(bim)
        boq_data = boq(bim)
        mep_data = mep(bim)

        st.session_state.active_model = {
            "bim": bim,
            "review": review,
            "boq": boq_data,
            "mep": mep_data
        }

        mem["bim_models"].append(bim)
        log("Generated BIM model")

    if st.session_state.active_model:

        model = st.session_state.active_model

        st.subheader("📊 AI BIM Analysis")

        st.json(model["review"])

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("💰 BoQ")
            st.json(model["boq"])

        with col2:
            st.subheader("🌬 MEP")
            st.json(model["mep"])

        tab1, tab2 = st.tabs(["🗺 2D BIM", "🏢 3D BIM"])

        with tab1:
            render_2d(model["bim"])

        with tab2:
            render_3d(model["bim"])

elif page == "BIM Model":
    st.json(st.session_state.active_model)

elif page == "Memory":
    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.mem = DEFAULT.copy()
        st.rerun()
