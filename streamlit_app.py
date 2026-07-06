# =============================
# ARC STUDIO V15
# AEC + BIM + EVOLUTION ENGINE CORE
# =============================

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
    page_title="Arc Studio V15 - AEC Engine",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "bim_models": [],
    "logs": [],
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(st.session_state.memory, f, indent=2)

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory

# =========================================================
# AEC BIM DATA MODEL (NEW CORE ADDITION)
# =========================================================

def create_bim_model(design):
    """Turns raw design into BIM-like structured object"""

    floors = design.get("floors", 1)
    bedrooms = design.get("bedrooms", 1)

    bim = {
        "project_id": design["id"],
        "architecture": {
            "floors": floors,
            "rooms": design.get("rooms", []),
            "typology": design.get("type", "Unknown")
        },
        "structure": {
            "columns": random.randint(20, 80),
            "beams": random.randint(40, 160),
            "slabs": floors,
            "foundation": "Raft Foundation"
        },
        "mep": {
            "water_system": "Pressurized Network",
            "electrical": "3-phase distribution",
            "fire_system": "Sprinkler + Hydrant",
            "drainage": "Gravity + Pump Assist"
        },
        "hvac": {
            "system": "VRF / Central Chiller Hybrid",
            "air_handling_units": random.randint(1, floors),
            "cooling_load_kw": random.randint(50, 500),
            "zones": floors * 2
        },
        "cost_model": {
            "structure_cost": 0,
            "mep_cost": 0,
            "hvac_cost": 0,
            "total": 0
        }
    }

    return bim

# =========================================================
# AEC COST ENGINE (NEW)
# =========================================================

def calculate_costs(bim):
    base_structure = bim["structure"]["columns"] * 1200
    base_mep = bim["architecture"]["floors"] * 15000
    base_hvac = bim["hvac"]["cooling_load_kw"] * 300

    total = base_structure + base_mep + base_hvac

    bim["cost_model"] = {
        "structure_cost": base_structure,
        "mep_cost": base_mep,
        "hvac_cost": base_hvac,
        "total": total
    }

    return bim

# =========================================================
# GENETIC ENGINE (SIMPLIFIED V15 CORE)
# =========================================================

def generate_design():
    return {
        "id": str(uuid.uuid4())[:8],
        "type": random.choice(["Residential", "Commercial", "Industrial"]),
        "floors": random.randint(1, 20),
        "bedrooms": random.randint(1, 6),
        "rooms": ["Living", "Kitchen", "Bath", "Flex"],
        "area": random.randint(80, 2000)
    }

def evolve_design(d):
    d = json.loads(json.dumps(d))
    d["floors"] = max(1, d["floors"] + random.randint(-1, 3))
    d["area"] += random.randint(-50, 120)
    return d

def run_evolution(n=10):
    population = [generate_design() for _ in range(n)]
    best = population[0]

    for p in population:
        if p["area"] > best["area"]:
            best = p

    return best

# =========================================================
# BIM PIPELINE (NEW CORE FEATURE)
# =========================================================

def build_full_bim(design):
    bim = create_bim_model(design)
    bim = calculate_costs(bim)
    return bim
