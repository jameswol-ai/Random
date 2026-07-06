# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE v11
# BIM + AI MULTI-AGENT + IFC EXPORT CORE
# =========================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random Studio Engine v11",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": []
}


def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()


def save_memory():
    MEMORY_FILE.write_text(json.dumps(st.session_state.memory, indent=2))


def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()


if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE GENERATOR
# =========================================================

ARCH_TYPES = ["Villa", "Office", "Apartment", "Warehouse"]


def generate_design():
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": random.choice(ARCH_TYPES),
        "area": random.randint(120, 800),
        "bedrooms": random.randint(1, 6),
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(20, 90)
        },
        "cost": random.randint(100000, 900000),
        "rooms": ["Living", "Kitchen", "Bath"]
    }


def floor_plan(design):
    rooms = [
        {"name": "Living", "w": 6, "h": 5},
        {"name": "Kitchen", "w": 4, "h": 4},
        {"name": "Bath", "w": 3, "h": 2}
    ]

    for i in range(design["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4,
            "h": 4
        })

    return rooms

# =========================================================
# BIM GRAPH ENGINE
# =========================================================

def build_bim(design):
    nodes = []
    edges = []

    for i in range(design["structure"]["columns"]):
        nodes.append({
            "id": f"C{i}",
            "type": "column",
            "x": random.uniform(0, 20),
            "y": random.uniform(0, 20),
            "z": 0
        })

    for i in range(design["structure"]["beams"]):
        a, b = random.sample(nodes, 2)
        edges.append({
            "id": f"B{i}",
            "from": a["id"],
            "to": b["id"]
        })

    return {"nodes": nodes, "edges": edges}

# =========================================================
# MULTI-AGENT SYSTEM
# =========================================================

def structural_agent(d):
    return {
        "score": max(0, 100 - d["structure"]["columns"] * 2),
        "status": "stable"
    }


def cost_agent(d):
    cps = d["cost"] / max(1, d["area"])
    return {
        "efficiency": max(0, 100 - abs(cps - 1000) * 0.01),
        "status": "ok"
    }


def spatial_agent(d):
    return {
        "utilization": min(100, len(d["rooms"]) * 10),
        "status": "balanced"
    }


def ai_board(d):
    return {
        "structural": structural_agent(d),
        "cost": cost_agent(d),
        "spatial": spatial_agent(d)
    }

# =========================================================
# IFC EXPORT (SIMPLIFIED)
# =========================================================

def export_ifc(design, bim):
    return {
        "IFCProject": {"id": design["id"]},
        "IFCBuilding": {
            "type": design["type"],
            "area": design["area"]
        },
        "IFCStructure": {
            "columns": len(bim["nodes"]),
            "beams": len(bim["edges"])
        },
        "IFCMeta": {
            "engine": "v11",
            "time": datetime.now().isoformat()
        }
    }

# =========================================================
# PIPELINE
# =========================================================

def run_pipeline():
    d = generate_design()
    plan = floor_plan(d)
    bim = build_bim(d)
    ai = ai_board(d)
    ifc = export_ifc(d, bim)

    d["plan"] = plan
    d["bim"] = bim
    d["ai"] = ai
    d["ifc"] = ifc

    return d

# =========================================================
# UI
# =========================================================

st.title("📐 Random Architecture Intelligence Engine v11")

if st.button("Generate Architecture System", use_container_width=True):
    result = run_pipeline()
    st.session_state.active = result

    mem["designs"].append(result)
    log(f"Generated {result['id']}")

if st.session_state.active:
    d = st.session_state.active

    st.subheader(f"Design {d['id']}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Area", d["area"])
    c2.metric("Cost", d["cost"])
    c3.metric("Columns", d["structure"]["columns"])

    tab1, tab2, tab3, tab4 = st.tabs([
        "Plan", "BIM", "AI Agents", "IFC Export"
    ])

    with tab1:
        st.json(d["plan"])

    with tab2:
        st.json(d["bim"])

    with tab3:
        st.json(d["ai"])

    with tab4:
        st.json(d["ifc"])

# =========================================================
# MEMORY VIEW
# =========================================================

st.sidebar.title("Memory")

if st.sidebar.button("View Memory"):
    st.sidebar.json(mem)

if st.sidebar.button("Reset"):
    st.session_state.memory = DEFAULT_STATE.copy()
    st.session_state.active = None
    save_memory()
    st.rerun()
