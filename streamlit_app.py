# =========================================================
# RANDOM V41 — FULL SYSTEM
# AI Architecture + City Generator + BIM-lite Engine
# Plotly 3D + BOQ + Timeline + Cost Simulation (EA Region)
# =========================================================

import streamlit as st
import uuid
import random
import json
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objects as go

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(page_title="RANDOM V41", layout="wide")

# =========================================================
# MEMORY CORE
# =========================================================

MEMORY_FILE = Path("v41_memory.json")

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
# 🌍 EAST AFRICA COST + MARKET SIMULATION
# =========================================================

BASE_COSTS = {
    "cement": 42000,
    "steel": 3800,
    "sand": 60000,
    "brick": 900,
    "tile": 85000,
    "paint": 28000
}

INFLATION = random.uniform(0.95, 1.25)

def market_price(material):
    return int(BASE_COSTS[material] * INFLATION)

# =========================================================
# 🏗 BUILDING ENGINE
# =========================================================

SPACE_TYPES = ["Living", "Kitchen", "Bedroom", "Office", "Bath", "Lobby", "Shop"]

def generate_building(name, floors):
    spaces = []
    for f in range(floors):
        for _ in range(random.randint(3, 6)):
            spaces.append({
                "floor": f+1,
                "type": random.choice(SPACE_TYPES),
                "area": random.randint(12, 80),
                "height": random.choice([2.7, 3.0, 3.5])
            })

    return {
        "id": uid(),
        "name": name,
        "floors": floors,
        "spaces": spaces,
        "created": datetime.utcnow().isoformat()
    }

# =========================================================
# 🏙 CITY GENERATOR
# =========================================================

def generate_city(name, building_count=5):
    city = {
        "id": uid(),
        "name": name,
        "buildings": []
    }

    for i in range(building_count):
        city["buildings"].append(
            generate_building(f"Bldg-{i+1}", random.randint(1, 8))
        )

    return city

# =========================================================
# 🧠 AI CHIEF ARCHITECT AGENTS
# =========================================================

def planner(city):
    return {
        "zones": ["residential", "commercial", "mixed"],
        "logic": "zoning optimized for density flow"
    }

def engineer(building):
    return {
        "structure": "reinforced concrete frame",
        "stability_score": random.randint(70, 95)
    }

def quantity_surveyor(building):
    area = sum(s["area"] for s in building["spaces"])
    return {
        "cement_bags": int(area * 0.9),
        "steel_kg": int(area * 11),
        "sand_m3": int(area * 0.6),
        "bricks": int(area * 40)
    }

def inspector():
    return {
        "violations": random.choice([
            "none",
            "minor ventilation issue",
            "structural spacing warning"
        ])
    }

# =========================================================
# 💰 COST ENGINE
# =========================================================

def compute_cost(boq):
    total = 0
    for k, v in boq.items():
        if k == "cement_bags":
            total += v * market_price("cement")
        if k == "steel_kg":
            total += v * market_price("steel")
        if k == "sand_m3":
            total += v * market_price("sand")
        if k == "bricks":
            total += v * market_price("brick")
    return total

# =========================================================
# 📊 TIMELINE ENGINE (GANTT SIMULATION)
# =========================================================

def timeline():
    base = datetime.today()
    phases = [
        ("Excavation", 7),
        ("Foundation", 14),
        ("Structure", 30),
        ("Masonry", 25),
        ("Finishing", 20)
    ]

    return [
        {
            "phase": p,
            "start": (base + timedelta(days=sum(d for _, d in phases[:i]))).strftime("%Y-%m-%d"),
            "duration": d
        }
        for i, (p, d) in enumerate(phases)
    ]

# =========================================================
# 🧊 3D CITY VISUALIZATION (PLOTLY ORBIT STYLE)
# =========================================================

def plot_city(city):
    fig = go.Figure()

    x, y = 0, 0

    for b in city["buildings"]:
        height = b["floors"] * 10

        fig.add_trace(go.Scatter3d(
            x=[x],
            y=[y],
            z=[height],
            mode='markers+text',
            text=[b["name"]],
            marker=dict(size=8)
        ))

        x += random.randint(10, 25)
        y += random.randint(10, 25)

    fig.update_layout(
        title="🏙 V41 City Orbit Model",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Height"
        )
    )

    return fig

# =========================================================
# UI HEADER
# =========================================================

st.title("🧠 RANDOM V41 — AI Architecture + City BIM OS")
st.caption("City-scale construction intelligence • BOQ • AI engineers • 3D orbit model")

# =========================================================
# SIDEBAR CONTROL
# =========================================================

st.sidebar.header("🎛 Control Center")

mode = st.sidebar.selectbox("Mode", ["Building", "City"])

name = st.sidebar.text_input("Name", "Neo-Kampala Core")

floors = st.sidebar.slider("Floors", 1, 10, 3)

if st.sidebar.button("🚀 Generate"):
    
    if mode == "Building":
        project = generate_building(name, floors)
        memory["projects"].append(project)
        st.session_state["building"] = project

    else:
        city = generate_city(name)
        memory["cities"].append(city)
        st.session_state["city"] = city

    save_memory(memory)

# =========================================================
# MAIN DASHBOARD
# =========================================================

if "building" in st.session_state:

    b = st.session_state["building"]

    st.subheader("🏗 Building Engine Output")

    st.json(b)

    qs = quantity_surveyor(b)
    eng = engineer(b)
    insp = inspector()

    st.markdown("### 🧱 BOQ")
    st.json(qs)

    st.markdown("### 🧠 Engineering Analysis")
    st.json(eng)

    st.markdown("### ⚠ Inspector Report")
    st.json(insp)

    st.markdown("### 💰 Cost Estimate (UGX)")
    st.success(f"{compute_cost(qs):,}")

    st.markdown("### 📊 Construction Timeline")
    st.json(timeline())

elif "city" in st.session_state:

    c = st.session_state["city"]

    st.subheader("🏙 City Engine Output")

    st.json(c)

    st.markdown("### 🧠 AI Planner")
    st.json(planner(c))

    st.markdown("### 🧊 3D City Orbit View")
    st.plotly_chart(plot_city(c), use_container_width=True)

else:
    st.info("Generate a building or city to activate V41 system.")

# =========================================================
# MEMORY DEBUG PANEL
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Memory")
st.sidebar.write("Buildings:", len(memory["projects"]))
st.sidebar.write("Cities:", len(memory["cities"]))
