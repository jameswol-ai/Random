# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE — V37
# Architectural + Structural + Cost + 2D + 3D BIM-Lite OS
# Deployment-Grade Streamlit Single File
# =========================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
import numpy as np

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="ARC V37 OS",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# SAFE MEMORY (CRASH-PROOF JSON LOADER)
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "boq": [],
    "logs": [],
    "evolution": []
}

def safe_load():
    if not MEMORY_FILE.exists():
        return DEFAULT_STATE.copy()
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {**DEFAULT_STATE, **data}
    except:
        return DEFAULT_STATE.copy()

def safe_save(mem):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(mem, f, indent=2)
    except:
        pass

def log(mem, msg):
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    safe_save(mem)

# init
if "mem" not in st.session_state:
    st.session_state.mem = safe_load()

mem = st.session_state.mem

# =========================================================
# DOMAIN ENGINE
# =========================================================

ARCH_TYPES = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Mall", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory", "Plant"]
}

def domain(t):
    for k,v in ARCH_TYPES.items():
        if t in v:
            return k
    return "Unknown"

# =========================================================
# EAST AFRICA COST ENGINE (BASE RATES)
# =========================================================
# editable baseline (UGX per unit)
RATES = {
    "foundation_m3": 280000,
    "slab_m2": 120000,
    "wall_m2": 95000,
    "roof_m2": 140000,
    "column_unit": 180000,
    "beam_unit": 220000,
    "door_unit": 350000,
    "window_unit": 280000
}

# =========================================================
# ARCHITECTURAL GENERATION
# =========================================================

def generate_design(btype, floors, rooms):
    return {
        "id": str(uuid.uuid4())[:8],
        "type": btype,
        "domain": domain(btype),
        "floors": floors,
        "rooms": rooms,
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(20, 80)
        }
    }

# =========================================================
# SPACE GENERATION (2D BIM)
# =========================================================

def generate_spaces(design):
    base = [
        {"name": "Living Room", "type": "social", "area": 35},
        {"name": "Kitchen", "type": "service", "area": 18},
        {"name": "Bathroom", "type": "wet", "area": 8}
    ]

    for i in range(design["rooms"]):
        base.append({
            "name": f"Bedroom {i+1}",
            "type": "private",
            "area": 22 if i == 0 else 16
        })

    # doors & windows
    for s in base:
        s["doors"] = random.randint(1, 2)
        s["windows"] = random.randint(1, 4)

    return base

# =========================================================
# 3D VOXEL ENGINE (SIMPLIFIED BIM KERNEL)
# =========================================================

WORLD = (20, 10, 20)

def voxel_world(design):
    w = np.zeros(WORLD)

    for _ in range(design["structure"]["columns"]):
        x, z = random.randint(0,19), random.randint(0,19)
        for y in range(random.randint(2,6)):
            w[x,y,z] = 1

    for _ in range(design["structure"]["beams"]):
        x,z = random.randint(0,19), random.randint(0,19)
        y = random.randint(2,5)
        for i in range(3):
            w[min(19,x+i), y, z] = 2

    return w

def voxel_metrics(w):
    return {
        "solid": int(np.sum(w == 1)),
        "beams": int(np.sum(w == 2)),
        "density": float(np.sum(w > 0) / w.size)
    }

# =========================================================
# BOQ ENGINE (FOUNDATION → ROOF)
# =========================================================

def boq(design, spaces):
    floors = design["floors"]
    area = sum(s["area"] for s in spaces)

    foundation = area * 0.6
    slab = area * floors
    walls = area * 2.8
    roof = area * 1.0

    return [
        ("Foundation Concrete (m3)", foundation, foundation * RATES["foundation_m3"]),
        ("Floor Slab (m2)", slab, slab * RATES["slab_m2"]),
        ("Walling (m2)", walls, walls * RATES["wall_m2"]),
        ("Roofing (m2)", roof, roof * RATES["roof_m2"]),
        ("Columns (units)", design["structure"]["columns"], design["structure"]["column_unit"]),
        ("Beams (units)", design["structure"]["beams"], design["structure"]["beam_unit"]),
        ("Doors (units)", sum(s["doors"] for s in spaces), RATES["door_unit"]),
        ("Windows (units)", sum(s["windows"] for s in spaces), RATES["window_unit"])
    ]

# =========================================================
# COST SUMMARIZER
# =========================================================

def total_cost(items):
    return int(sum(v * c for _, v, c in items))

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏗️ ARC V37 OS")

mode = st.sidebar.radio("Mode", ["Design Lab", "Dashboard", "Memory"])

btype = st.sidebar.selectbox("Building Type", sum(ARCH_TYPES.values(), []))
floors = st.sidebar.slider("Floors", 1, 5, 2)
rooms = st.sidebar.slider("Bedrooms", 1, 8, 3)

# =========================================================
# DASHBOARD
# =========================================================

if mode == "Dashboard":
    st.title("🏗️ ARCH SYSTEM CORE")

    c1,c2,c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("BOQs", len(mem["boq"]))
    c3.metric("Logs", len(mem["logs"]))

    st.line_chart([d.get("structure", {}).get("columns", 0) for d in mem["designs"]])

# =========================================================
# DESIGN LAB
# =========================================================

elif mode == "Design Lab":
    st.title("🧠 ARCHITECT + ENGINEER AI")

    if st.button("Generate Full BIM Model"):
        design = generate_design(btype, floors, rooms)
        spaces = generate_spaces(design)
        world = voxel_world(design)
        metrics = voxel_metrics(world)
        boq_items = boq(design, spaces)

        design["spaces"] = spaces
        design["boq"] = boq_items
        design["total_cost"] = total_cost(boq_items)
        design["voxel"] = metrics

        mem["designs"].append(design)
        mem["boq"].append(boq_items)

        log(mem, f"Generated {design['id']}")

        st.session_state.active = design

    if "active" in st.session_state:
        d = st.session_state.active

        st.subheader(f"Project {d['id']}")

        a,b,c = st.columns(3)
        a.metric("Cost (UGX)", d["total_cost"])
        b.metric("Columns", d["structure"]["columns"])
        c.metric("Density", round(d["voxel"]["density"],3))

        tab1, tab2, tab3 = st.tabs(["Spaces", "BOQ", "3D Voxel"])

        with tab1:
            for s in d["spaces"]:
                st.write(s)

        with tab2:
            st.table([
                {"Item": i, "Qty": q, "Cost": c}
                for i,q,c in d["boq"]
            ])

        with tab3:
            layer = st.slider("Voxel Layer", 0, WORLD[1]-1, 0)
            grid = d["voxel"]

            st.write("Slice View (simplified)")
            st.write(grid)

# =========================================================
# MEMORY
# =========================================================

else:
    st.title("🧠 MEMORY CORE")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.mem = DEFAULT_STATE.copy()
        safe_save(st.session_state.mem)
        st.rerun()