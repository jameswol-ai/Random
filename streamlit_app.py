# =========================================================
# RANDOM V40 — BEAUTIFIED STUDIO EDITION
# Architecture + Engineering + BOQ + Cost Intelligence
# Streamlit Glass Dashboard UI Upgrade
# =========================================================

import streamlit as st
import json
import uuid
import random
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =========================================================
# PAGE CONFIG + THEME
# =========================================================

st.set_page_config(
    page_title="RANDOM V40 Studio",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Main background */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0b1020, #05070f);
    color: #e6edf3;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #020617);
}

/* Cards */
.block-container {
    padding-top: 2rem;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 12px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

/* Titles */
h1, h2, h3 {
    color: #7dd3fc;
    letter-spacing: 0.5px;
}

/* JSON box */
pre {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

MEMORY_FILE = Path("random_v40_memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"projects": [], "logs": []}

def save_memory(m):
    MEMORY_FILE.write_text(json.dumps(m, indent=2))

memory = load_memory()

def uid():
    return str(uuid.uuid4())[:8]

def log(event):
    memory["logs"].append({
        "id": uid(),
        "event": event,
        "time": datetime.utcnow().isoformat()
    })
    save_memory(memory)

# =========================================================
# COST + MATERIALS
# =========================================================

MATERIALS = {
    "cement_bag": 42000,
    "steel_kg": 3800,
    "sand_m3": 60000,
    "brick": 900,
    "tile_m2": 85000,
    "paint_l": 28000
}

# =========================================================
# ARCHITECTURE GENERATOR
# =========================================================

SPACE_LIBRARY = ["Living", "Kitchen", "Bedroom", "Bath", "Office", "Lobby", "Storage"]

def generate_project(name, floors):
    spaces = []
    for f in range(floors):
        for _ in range(random.randint(3, 6)):
            spaces.append({
                "floor": f + 1,
                "type": random.choice(SPACE_LIBRARY),
                "area": random.randint(12, 65)
            })

    return {
        "id": uid(),
        "name": name,
        "floors": floors,
        "spaces": spaces,
        "created": datetime.utcnow().isoformat()
    }

# =========================================================
# BOQ ENGINE
# =========================================================

def boq(project):
    total_area = sum(s["area"] for s in project["spaces"])

    return {
        "cement": int(total_area * 0.8),
        "steel": int(total_area * 12),
        "sand": int(total_area * 0.5),
        "brick": int(total_area * 45),
        "tile": int(total_area * 0.6),
        "paint": int(total_area * 0.3)
    }

# =========================================================
# COST ENGINE
# =========================================================

def cost(boq):
    total = 0
    total += boq["cement"] * MATERIALS["cement_bag"]
    total += boq["steel"] * MATERIALS["steel_kg"]
    total += boq["sand"] * MATERIALS["sand_m3"]
    total += boq["brick"] * MATERIALS["brick"]
    total += boq["tile"] * MATERIALS["tile_m2"]
    total += boq["paint"] * MATERIALS["paint_l"]

    return total

# =========================================================
# VISUALS
# =========================================================

def plot_2d(project):
    fig, ax = plt.subplots()
    x, y = 0, 0

    for s in project["spaces"]:
        size = s["area"] ** 0.5
        rect = plt.Rectangle((x, y), size, size, fill=False)
        ax.add_patch(rect)
        ax.text(x, y, s["type"], fontsize=7)
        x += size * 0.6
        y += size * 0.3

    ax.set_title("2D Architectural Layout")
    ax.axis("equal")
    return fig

def plot_3d(project):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    x, y = 0, 0
    for s in project["spaces"]:
        z = s["floor"] * 3
        ax.scatter(x, y, z, s=s["area"] * 5)

        x += random.uniform(1, 3)
        y += random.uniform(1, 3)

    ax.set_title("3D Massing Model")
    return fig

# =========================================================
# UI HEADER
# =========================================================

st.title("🏗 RANDOM V40 — Architecture Intelligence Studio")
st.caption("BOQ • Engineering • Costing • 2D/3D Visualization • East Africa Build Engine")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("🎛 Control Panel")

name = st.sidebar.text_input("Project Name", "Neural Complex")
floors = st.sidebar.slider("Floors", 1, 10, 3)

if st.sidebar.button("🚀 Generate Project"):
    proj = generate_project(name, floors)
    memory["projects"].append(proj)
    save_memory(memory)
    st.session_state["project"] = proj
    log("Project generated")

# =========================================================
# DASHBOARD
# =========================================================

if "project" in st.session_state:
    project = st.session_state["project"]

    st.subheader("📦 Project Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Floors", project["floors"])

    with col2:
        st.metric("Spaces", len(project["spaces"]))

    with col3:
        total_area = sum(s["area"] for s in project["spaces"])
        st.metric("Total Area (m²)", total_area)

    # BOQ
    b = boq(project)

    st.markdown("## 🧱 Bill of Quantities (BOQ)")

    c1, c2, c3 = st.columns(3)
    c1.metric("Cement Bags", b["cement"])
    c2.metric("Steel Kg", b["steel"])
    c3.metric("Sand m³", b["sand"])

    c4, c5, c6 = st.columns(3)
    c4.metric("Bricks", b["brick"])
    c5.metric("Tiles m²", b["tile"])
    c6.metric("Paint L", b["paint"])

    # COST
    total_cost = cost(b)

    st.markdown("## 💰 Cost Estimation")

    st.success(f"Estimated Total Cost: UGX {total_cost:,.0f}")

    # VISUALS
    st.markdown("## 📐 2D Layout")
    st.pyplot(plot_2d(project))

    st.markdown("## 🧊 3D Massing")
    st.pyplot(plot_3d(project))

else:
    st.info("Generate a project to activate the architecture studio.")
