# =========================================================
# V39 — CITY ARCHITECTURE SIMULATION ENGINE
# Multi-Building Urban Intelligence System
# =========================================================

import streamlit as st
import json
import uuid
import random
import numpy as np
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="City Architecture Engine V39",
    page_icon="🌆",
    layout="wide"
)

MEMORY_FILE = Path("city_memory.json")

# =========================================================
# SAFE MEMORY
# =========================================================

DEFAULT = {
    "cities": [],
    "logs": []
}

def load():
    if not MEMORY_FILE.exists():
        return DEFAULT.copy()
    try:
        return json.loads(MEMORY_FILE.read_text())
    except:
        return DEFAULT.copy()

def save(mem):
    try:
        MEMORY_FILE.write_text(json.dumps(mem, indent=2))
    except:
        pass

def log(mem, msg):
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save(mem)

if "mem" not in st.session_state:
    st.session_state.mem = load()

if "active_city" not in st.session_state:
    st.session_state.active_city = None

mem = st.session_state.mem

# =========================================================
# CITY TAXONOMY
# =========================================================

BUILDING_TYPES = {
    "Residential": {"color": 1, "pop": 3},
    "Commercial": {"color": 2, "pop": 1},
    "Industrial": {"color": 3, "pop": 0}
}

# =========================================================
# CITY GENERATION ENGINE
# =========================================================

CITY_SIZE = (30, 12, 30)

def create_building(btype):
    return {
        "id": str(uuid.uuid4())[:6],
        "type": btype,
        "height": random.randint(2, 8),
        "size": random.randint(2, 5)
    }

def generate_city(n_buildings=25):
    city = np.zeros(CITY_SIZE)

    buildings = []

    for _ in range(n_buildings):
        btype = random.choice(list(BUILDING_TYPES.keys()))
        b = create_building(btype)

        x = random.randint(2, 27)
        z = random.randint(2, 27)

        h = b["height"]

        city[x:x+2, :h, z:z+2] = BUILDING_TYPES[btype]["color"]

        buildings.append({
            **b,
            "x": x,
            "z": z
        })

    return city, buildings

# =========================================================
# ROAD NETWORK ENGINE
# =========================================================

def generate_roads(buildings):
    roads = []

    for i in range(len(buildings)-1):
        a = buildings[i]
        b = buildings[i+1]

        roads.append(((a["x"], a["z"]), (b["x"], b["z"])))

    return roads

# =========================================================
# CITY AI BRAIN
# =========================================================

def city_brain(buildings):
    res = sum(1 for b in buildings if b["type"] == "Residential")
    com = sum(1 for b in buildings if b["type"] == "Commercial")
    ind = sum(1 for b in buildings if b["type"] == "Industrial")

    advice = []

    if res < com:
        advice.append("Housing shortage detected.")
    if ind > res:
        advice.append("Over-industrialized city risk.")
    if com == 0:
        advice.append("No economic core detected.")

    if not advice:
        advice.append("City balance is stable.")

    return {
        "residential": res,
        "commercial": com,
        "industrial": ind,
        "advice": advice
    }

# =========================================================
# ECONOMY ENGINE
# =========================================================

def economy(buildings):
    income = sum(
        200 if b["type"] == "Commercial" else
        100 if b["type"] == "Residential" else
        300
        for b in buildings
    )

    maintenance = len(buildings) * 40

    return {
        "income": income,
        "maintenance": maintenance,
        "net": income - maintenance
    }

# =========================================================
# 3D CITY VIEW
# =========================================================

def render_slice(city, y):
    grid = city[:, y, :]

    for z in range(30):
        row = ""
        for x in range(30):
            v = grid[x, z]
            row += "⬛" if v == 0 else "🟦" if v == 1 else "🟨" if v == 2 else "🟩"
        st.code(row)

# =========================================================
# UI
# =========================================================

st.sidebar.title("🌆 CITY V39")

page = st.sidebar.radio("Mode", ["Dashboard", "City Lab", "Analytics"])

n = st.sidebar.slider("Buildings", 10, 60, 25)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🌆 City Simulation Engine V39")

    c1, c2 = st.columns(2)
    c1.metric("Cities Generated", len(mem["cities"]))
    c2.metric("Logs", len(mem["logs"]))

# =========================================================
# CITY LAB
# =========================================================

elif page == "City Lab":
    st.title("🏙️ Urban Simulation Lab")

    if st.button("Generate City"):
        city, buildings = generate_city(n)
        roads = generate_roads(buildings)

        mem["cities"].append({
            "id": str(uuid.uuid4())[:6],
            "buildings": buildings,
            "roads": roads
        })

        st.session_state.active_city = {
            "city": city,
            "buildings": buildings,
            "roads": roads
        }

        log(mem, "City generated")

    if st.session_state.active_city:
        c = st.session_state.active_city

        st.subheader("City Slice View")
        y = st.slider("Height Layer", 0, 11, 0)
        render_slice(c["city"], y)

# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":
    st.title("📊 City Intelligence Layer")

    if st.session_state.active_city:
        b = st.session_state.active_city["buildings"]

        brain = city_brain(b)
        econ = economy(b)

        st.subheader("City Balance AI")
        st.json(brain)

        st.subheader("Economy")
        st.json(econ)
    else:
        st.info("Generate a city first.")

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory Core")
    st.json(mem)