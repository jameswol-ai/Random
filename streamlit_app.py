# =========================================================
# RANDOM V40
# Architectural Intelligence + Engineering + BOQ System
# East Africa Cost Estimation Engine
# 2D/3D Spatial Generator (Matplotlib)
# Single File Streamlit BIM-like Simulator
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
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V40",
    layout="wide"
)

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
# EAST AFRICA COST ENGINE
# =========================================================

CURRENCY = {
    "UGX": 1,
    "KES": 0.032,
    "TZS": 0.029,
    "RWF": 0.31
}

MATERIALS = {
    "cement_bag": {"ugx": 42000},
    "steel_kg": {"ugx": 3800},
    "sand_m3": {"ugx": 60000},
    "brick": {"ugx": 900},
    "glass_m2": {"ugx": 120000},
    "tile_m2": {"ugx": 85000},
    "paint_litre": {"ugx": 28000},
    "timber_m3": {"ugx": 950000}
}

def convert(ugx, currency):
    return ugx * CURRENCY[currency]

# =========================================================
# ARCHITECTURE GENERATOR
# =========================================================

SPACE_LIBRARY = [
    "Living Room",
    "Kitchen",
    "Bedroom",
    "Bathroom",
    "Office",
    "Lobby",
    "Storage",
    "Balcony"
]

def generate_architecture(name, floors=2):
    spaces = []
    for f in range(floors):
        for _ in range(random.randint(3, 6)):
            space = {
                "floor": f+1,
                "type": random.choice(SPACE_LIBRARY),
                "area_sqm": random.randint(10, 60),
                "height_m": random.choice([2.7, 3.0, 3.3])
            }
            spaces.append(space)

    return {
        "id": uid(),
        "name": name,
        "floors": floors,
        "spaces": spaces,
        "created": datetime.utcnow().isoformat()
    }

# =========================================================
# ENGINEERING + BOQ ENGINE
# =========================================================

def compute_boq(project):
    boq = {
        "cement_bags": 0,
        "steel_kg": 0,
        "sand_m3": 0,
        "bricks": 0,
        "tiles_m2": 0,
        "paint_l": 0
    }

    total_area = sum(s["area_sqm"] for s in project["spaces"])

    boq["cement_bags"] = int(total_area * 0.8)
    boq["steel_kg"] = int(total_area * 12)
    boq["sand_m3"] = int(total_area * 0.5)
    boq["bricks"] = int(total_area * 45)
    boq["tiles_m2"] = int(total_area * 0.6)
    boq["paint_l"] = int(total_area * 0.3)

    return boq

# =========================================================
# COST ENGINE
# =========================================================

def estimate_cost(boq, currency="UGX"):
    total = 0

    total += boq["cement_bags"] * MATERIALS["cement_bag"]["ugx"]
    total += boq["steel_kg"] * MATERIALS["steel_kg"]["ugx"]
    total += boq["sand_m3"] * MATERIALS["sand_m3"]["ugx"]
    total += boq["bricks"] * MATERIALS["brick"]["ugx"]
    total += boq["tiles_m2"] * MATERIALS["tile_m2"]["ugx"]
    total += boq["paint_l"] * MATERIALS["paint_litre"]["ugx"]

    converted = convert(total, currency)

    return total, converted

# =========================================================
# 2D PLAN VISUALIZER
# =========================================================

def plot_2d(project):
    fig, ax = plt.subplots()

    x, y = 0, 0
    for i, s in enumerate(project["spaces"]):
        w = s["area_sqm"] ** 0.5
        h = w

        ax.add_patch(plt.Rectangle((x, y), w, h, fill=None))
        ax.text(x, y, s["type"], fontsize=6)

        x += w * 0.5
        y += h * 0.2

    ax.set_title("2D Spatial Layout")
    return fig

# =========================================================
# 3D MASSING MODEL
# =========================================================

def plot_3d(project):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x, y = 0, 0
    for s in project["spaces"]:
        z = s["floor"] * 3
        size = s["area_sqm"] ** 0.5

        ax.scatter(x, y, z, s=size * 10)

        x += random.uniform(1, 3)
        y += random.uniform(1, 3)

    ax.set_title("3D Massing Model")
    return fig

# =========================================================
# UI
# =========================================================

st.title("🧠 RANDOM V40 — Architecture + Engineering Intelligence Engine")
st.caption("BOQ • Cost Estimation • 2D/3D Design • East Africa Construction Economics")

# SIDEBAR
st.sidebar.header("Control Panel")

name = st.sidebar.text_input("Project Name", "Neural Complex")
floors = st.sidebar.slider("Floors", 1, 10, 3)
currency = st.sidebar.selectbox("Currency", ["UGX", "KES", "TZS", "RWF"])

if st.sidebar.button("🏗 Generate Project"):
    proj = generate_architecture(name, floors)
    memory["projects"].append(proj)
    save_memory(memory)
    st.session_state["project"] = proj
    log("Project generated")

# =========================================================
# MAIN VIEW
# =========================================================

if "project" in st.session_state:
    project = st.session_state["project"]

    st.subheader("📦 Project Overview")
    st.json(project)

    # BOQ
    boq = compute_boq(project)
    st.subheader("🧱 Bill of Quantities (BOQ)")
    st.json(boq)

    # COST
    total_ugx, converted = estimate_cost(boq, currency)

    st.subheader("💰 Cost Estimation")
    st.metric("Total (UGX)", f"{total_ugx:,}")
    st.metric(f"Total ({currency})", f"{converted:,.2f}")

    # 2D
    st.subheader("📐 2D Layout")
    st.pyplot(plot_2d(project))

    # 3D
    st.subheader("🧊 3D Massing Model")
    st.pyplot(plot_3d(project))

else:
    st.info("Generate a project to activate engineering simulation.")

# =========================================================
# MATERIAL COST PANEL
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🧱 Material Prices (UGX)")

for k, v in MATERIALS.items():
    st.sidebar.write(f"{k}: {v['ugx']:,}")

# =========================================================
# LOG VIEW
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📜 Logs")
st.sidebar.json(memory["logs"][-5:])
