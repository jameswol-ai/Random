# =========================================================
# RANDOM OS — V1 REBORN (Unified Architecture Core)
# From V1 → V41 compressed into stable foundation
# =========================================================

import streamlit as st
import uuid
import random
import json
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go

# =========================================================
# APP CONFIG
# =========================================================

st.set_page_config(page_title="RANDOM OS V1", layout="wide")

st.title("🧠 RANDOM OS — Unified Architecture Core (V1 Reborn)")
st.caption("BIM • AI Agents • City Generator • BOQ • Cost Engine")

# =========================================================
# MEMORY LAYER
# =========================================================

MEMORY_FILE = Path("random_os_memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"projects": [], "cities": []}

def save_memory(m):
    MEMORY_FILE.write_text(json.dumps(m, indent=2))

memory = load_memory()

def uid():
    return str(uuid.uuid4())[:8]

# =========================================================
# 🧠 AI AGENTS (MERGED FROM V1–V41)
# =========================================================

def agent_planner(project):
    return {
        "modules": ["structure", "spaces", "circulation", "services"],
        "logic": "modular decomposition applied"
    }

def agent_engineer(project):
    return {
        "structural_system": "reinforced concrete frame",
        "stability_score": random.randint(65, 95)
    }

def agent_qs(project):
    total_area = sum(s["area"] for s in project["spaces"])
    return {
        "cement_bags": int(total_area * 0.9),
        "steel_kg": int(total_area * 12),
        "sand_m3": int(total_area * 0.6),
        "bricks": int(total_area * 40)
    }

def agent_critic():
    return {
        "issues": random.choice([
            "none",
            "minor structural imbalance",
            "overdesigned slab system"
        ])
    }

# =========================================================
# 🏗 BUILDING ENGINE (UNIFIED CORE)
# =========================================================

SPACE_TYPES = ["Living", "Kitchen", "Bedroom", "Office", "Bath", "Lobby", "Shop"]

def generate_building(name, floors):
    spaces = []

    for f in range(floors):
        for _ in range(random.randint(3, 6)):
            spaces.append({
                "floor": f + 1,
                "type": random.choice(SPACE_TYPES),
                "area": random.randint(12, 80)
            })

    return {
        "id": uid(),
        "name": name,
        "floors": floors,
        "spaces": spaces,
        "created": datetime.utcnow().isoformat()
    }

# =========================================================
# 🏙 CITY ENGINE (LIGHTWEIGHT MERGE)
# =========================================================

def generate_city(name):
    return {
        "id": uid(),
        "name": name,
        "buildings": [
            generate_building(f"B-{i+1}", random.randint(2, 8))
            for i in range(random.randint(3, 6))
        ]
    }

# =========================================================
# 💰 COST ENGINE (EA REGION SIMPLIFIED)
# =========================================================

BASE_COSTS = {
    "cement": 42000,
    "steel": 3800,
    "sand": 60000,
    "brick": 900
}

def compute_cost(boq):
    total = 0
    total += boq["cement_bags"] * BASE_COSTS["cement"]
    total += boq["steel_kg"] * BASE_COSTS["steel"]
    total += boq["sand_m3"] * BASE_COSTS["sand"]
    total += boq["bricks"] * BASE_COSTS["brick"]
    return total

# =========================================================
# 📦 BOQ ENGINE
# =========================================================

def boq(project):
    area = sum(s["area"] for s in project["spaces"])
    return {
        "cement_bags": int(area * 0.9),
        "steel_kg": int(area * 12),
        "sand_m3": int(area * 0.6),
        "bricks": int(area * 40)
    }

# =========================================================
# 🧠 AI BRAIN (MERGED V41 LOGIC)
# =========================================================

def ai_brain(project):
    area = sum(s["area"] for s in project["spaces"])
    risk = random.randint(10, 45)

    return {
        "total_area": area,
        "risk_index": risk,
        "efficiency": 100 - risk,
        "recommendations": [
            "Optimize beam spacing",
            "Improve ventilation layout" if area > 300 else "Layout is stable",
            "Consider vertical circulation core"
        ]
    }

# =========================================================
# 🧊 3D VIEW (SIMPLE STABLE VERSION)
# =========================================================

def plot_building(project):
    fig = go.Figure()

    x, y = 0, 0

    for s in project["spaces"]:
        z = s["floor"] * 5

        fig.add_trace(go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode="markers",
            marker=dict(size=5),
            text=[s["type"]]
        ))

        x += random.uniform(1, 3)
        y += random.uniform(1, 3)

    fig.update_layout(
        title="🧊 BIM 3D Model (Unified Core)",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Height"
        )
    )

    return fig

# =========================================================
# SIDEBAR CONTROLS
# =========================================================

st.sidebar.header("🎛 Control Panel")

mode = st.sidebar.selectbox("Mode", ["Building", "City"])
name = st.sidebar.text_input("Project Name", "Neo Core")
floors = st.sidebar.slider("Floors", 1, 10, 3)

if st.sidebar.button("🚀 Generate"):

    if mode == "Building":
        project = generate_building(name, floors)

        st.session_state["project"] = project
        st.session_state["analysis"] = ai_brain(project)

        memory["projects"].append(project)

    else:
        city = generate_city(name)

        st.session_state["city"] = city

        memory["cities"].append(city)

    save_memory(memory)

# =========================================================
# MAIN UI
# =========================================================

if "project" in st.session_state:

    p = st.session_state["project"]
    a = st.session_state["analysis"]

    st.subheader("🏗 Building System")

    st.json(p)

    st.markdown("## 🧠 AI Brain Analysis")

    col1, col2 = st.columns(2)

    col1.metric("Risk Index", a["risk_index"])
    col2.metric("Efficiency", a["efficiency"])

    st.write("### Recommendations")
    st.write(a["recommendations"])

    b = boq(p)

    st.markdown("## 📦 BOQ")
    st.json(b)

    st.markdown("## 💰 Cost Estimate (UGX)")
    st.success(f"{compute_cost(b):,}")

    st.markdown("## 🧊 3D Model")
    st.plotly_chart(plot_building(p), use_container_width=True)

elif "city" in st.session_state:

    c = st.session_state["city"]

    st.subheader("🏙 City System")

    st.json(c)

    st.info("City engine active — buildings generated inside system.")

else:
    st.info("Generate a building or city to start RANDOM OS")

# =========================================================
# MEMORY PANEL
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Memory")
st.sidebar.write("Projects:", len(memory["projects"]))
st.sidebar.write("Cities:", len(memory["cities"]))
