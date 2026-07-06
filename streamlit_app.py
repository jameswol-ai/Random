# =========================================================
# ARCHITECTURE INTELLIGENCE OS V38
# Architectural + Structural AI + BOQ + 2D + 3D SYSTEM
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
    page_title="Architecture Intelligence OS V38",
    page_icon="🏛️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# SAFE MEMORY CORE
# =========================================================

DEFAULT = {
    "projects": [],
    "designs": [],
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

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.mem

# =========================================================
# ARCHITECTURAL TAXONOMY ENGINE
# =========================================================

ARCH_PROGRAM = {
    "Residential": {
        "spaces": ["Living Room", "Kitchen", "Master Bedroom", "Bathroom", "Dining"],
        "struct_factor": 1.0,
        "cost_factor": 1.0
    },
    "Commercial": {
        "spaces": ["Lobby", "Office Floor", "Meeting Room", "Server Room", "Reception"],
        "struct_factor": 1.3,
        "cost_factor": 1.5
    },
    "Industrial": {
        "spaces": ["Production Hall", "Storage Bay", "Loading Dock", "Control Room"],
        "struct_factor": 1.8,
        "cost_factor": 2.0
    }
}

# =========================================================
# STRUCTURAL ENGINE
# =========================================================

def structural_system(area, typology):
    f = ARCH_PROGRAM[typology]["struct_factor"]

    columns = int((area / 25) * f)
    beams = int(columns * random.uniform(1.8, 2.6))

    return {
        "columns": max(8, columns),
        "beams": max(12, beams)
    }

def structural_score(struct):
    ratio = struct["beams"] / max(1, struct["columns"])
    return max(0, 100 - abs(ratio - 2.2) * 20)

# =========================================================
# ARCHITECTURAL AI (PROGRAM GENERATOR)
# =========================================================

def generate_program(typology, floors):
    base = ARCH_PROGRAM[typology]["spaces"]
    program = []

    for f in range(floors):
        for s in base:
            program.append({
                "name": f"{s} - L{f+1}",
                "floor": f+1,
                "area": random.randint(20, 80)
            })

    return program

# =========================================================
# COST + BOQ ENGINE
# =========================================================

def boq(struct, area, typology):
    steel_rate = 3.2
    concrete_rate = 2.6
    block_rate = 42

    return {
        "Concrete (m³)": round(struct["columns"] * 2.5 * ARCH_PROGRAM[typology]["struct_factor"], 2),
        "Steel (tons)": round(struct["beams"] * 0.48, 2),
        "Blocks (units)": int(area * block_rate),
        "Estimated Cost ($)": int(area * 1500 * ARCH_PROGRAM[typology]["cost_factor"])
    }

# =========================================================
# 3D VOXEL ENGINE
# =========================================================

WORLD = (20, 12, 20)

def voxel(struct):
    w = np.zeros(WORLD)

    for _ in range(struct["columns"]):
        x, z = random.randint(0, 19), random.randint(0, 19)
        h = random.randint(2, 7)
        w[x, :h, z] = 1

    for _ in range(struct["beams"]):
        x, z = random.randint(0, 19), random.randint(0, 19)
        y = random.randint(2, 6)
        w[x, y, z] = 2

    return w

def slice_view(w, y):
    grid = w[:, y, :]
    out = ""

    for z in range(20):
        row = ""
        for x in range(20):
            v = grid[x, z]
            row += "⬛" if v == 0 else "🟦" if v == 1 else "🟨"
        out += row + "\n"

    st.code(out)

# =========================================================
# DESIGN ENGINE
# =========================================================

def generate_design(typology, floors, area):
    struct = structural_system(area, typology)

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "typology": typology,
        "floors": floors,
        "area": area,
        "structure": struct,
        "program": generate_program(typology, floors),
        "boq": boq(struct, area, typology),
        "score": structural_score(struct)
    }

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏛️ ARCH AI V38")

typology = st.sidebar.selectbox(
    "Project Type",
    ["Residential", "Commercial", "Industrial"]
)

floors = st.sidebar.slider("Floors", 1, 10, 3)
area = st.sidebar.slider("Total Area (sqm)", 100, 2000, 500)

page = st.sidebar.radio(
    "Mode",
    ["Dashboard", "Design Lab", "BOQ", "Memory"]
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏛️ Architectural Intelligence OS V38")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Projects", len(mem["projects"]))
    c3.metric("Logs", len(mem["logs"]))

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "Design Lab":
    st.title("🧠 AI Architectural Generator")

    if st.button("Generate Design"):
        d = generate_design(typology, floors, area)

        d["world"] = voxel(d["structure"])

        mem["designs"].append(d)
        st.session_state.active = d

        log(mem, f"Generated {d['id']}")

    if st.session_state.active:
        d = st.session_state.active

        st.subheader(f"Design {d['id']}")

        a, b, c = st.columns(3)
        a.metric("Structural Score", round(d["score"], 2))
        b.metric("Area", d["area"])
        c.metric("Floors", d["floors"])

        tab1, tab2, tab3 = st.tabs(["Program", "Structure", "3D"])

        with tab1:
            st.subheader("Space Program")
            st.json(d["program"])

        with tab2:
            st.subheader("Structural System")
            st.json(d["structure"])

        with tab3:
            y = st.slider("Section Cut", 0, 11, 0)
            slice_view(d["world"], y)

# =========================================================
# BOQ MODULE
# =========================================================

elif page == "BOQ":
    st.title("📊 Bill of Quantities (BOQ)")

    if st.session_state.active:
        st.json(st.session_state.active["boq"])
    else:
        st.info("Generate a design first.")

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory Core")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.mem = DEFAULT.copy()
        st.session_state.active = None
        save(mem)
        st.rerun()