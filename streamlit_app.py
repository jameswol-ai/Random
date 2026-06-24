# =========================================================
# ⚙️ OMEGA RANDOM V5 — SELF-REWRITING OPERATING SYSTEM
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="OMEGA RANDOM V5", layout="wide")

# =========================================================
# 🧠 META MEMORY CORE (SELF-EXPANDING SUBSTRATE)
# =========================================================

MEMORY_FILE = Path("omega_memory.json")

DEFAULT_MEMORY = {
    "projects": [],
    "designs": [],
    "cities": [],
    "knowledge": [],
    "engines": [],
    "modules": {}   # 🧠 dynamic system registry
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            data = json.loads(MEMORY_FILE.read_text())
            for k in DEFAULT_MEMORY:
                if k not in data:
                    data[k] = DEFAULT_MEMORY[k]
            return data
        except:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

memory = load_memory()

# =========================================================
# 🧬 ENGINE BIRTH SYSTEM (META GENERATION CORE)
# =========================================================

def spawn_engine(name=None):
    return {
        "id": str(uuid.uuid4())[:8],
        "name": name or f"Engine-{random.randint(100,999)}",
        "power": random.uniform(0.3, 1.0),
        "adaptation": random.uniform(0.3, 1.0),
        "stability": random.uniform(0.3, 1.0),
        "created": datetime.now().isoformat()
    }

def evolve_engine(e):
    e["power"] = min(1.0, e["power"] + random.uniform(-0.05, 0.08))
    e["adaptation"] = min(1.0, e["adaptation"] + random.uniform(-0.05, 0.1))
    e["stability"] = min(1.0, e["stability"] + random.uniform(-0.03, 0.06))
    return e

# =========================================================
# 🧠 SELF-EXPANDING MODULE SYSTEM
# =========================================================

def register_module(name, function_type):
    memory["modules"][name] = {
        "type": function_type,
        "created": datetime.now().isoformat()
    }

def get_dynamic_modules():
    return list(memory["modules"].keys())

# =========================================================
# 🏗 CORE GENERATION FUNCTIONS
# =========================================================

def generate_rooms():
    base = ["Living", "Kitchen", "Core"]
    extras = [f"Room-{i}" for i in range(random.randint(0, 3))]
    return base + extras + ["Bath"]

def score_design():
    base = random.randint(60, 100)
    return {
        "circulation": base,
        "efficiency": random.randint(60, 100),
        "adaptation": random.randint(60, 100),
        "structure": random.randint(60, 100),
        "meta_index": round(random.random(), 3)
    }

# =========================================================
# 🌱 SYSTEM EVOLUTION STEP
# =========================================================

# auto-grow engines
if len(memory["engines"]) < 3:
    memory["engines"].append(spawn_engine())

# auto-register modules based on system state
if random.random() > 0.6:
    register_module(
        f"module_{random.randint(1000,9999)}",
        "auto_generated"
    )

# evolve engines
memory["engines"] = [evolve_engine(e) for e in memory["engines"]]

save_memory(memory)

# =========================================================
# 🧭 SIDEBAR (SELF-GENERATED UI TREE)
# =========================================================

base_pages = [
    "Dashboard",
    "Design Studio",
    "City Simulator",
    "Knowledge Base",
    "Engine Lab"
]

dynamic_pages = base_pages + get_dynamic_modules()

page = st.sidebar.selectbox("OMEGA CORE", dynamic_pages)

# =========================================================
# 🧠 DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("⚙ OMEGA RANDOM V5 — CORE SYSTEM")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Projects", len(memory["projects"]))
    col2.metric("Designs", len(memory["designs"]))
    col3.metric("Engines", len(memory["engines"]))
    col4.metric("Modules", len(memory["modules"]))

# =========================================================
# 🏗 DESIGN STUDIO
# =========================================================

elif page == "Design Studio":
    st.title("🏗 Self-Generating Design Engine")

    if st.button("Generate Design"):
        design = {
            "rooms": generate_rooms(),
            "score": score_design(),
            "created": datetime.now().isoformat()
        }
        memory["designs"].append(design)
        save_memory(memory)

    st.json(memory["designs"])

# =========================================================
# 🌆 CITY SIMULATOR
# =========================================================

elif page == "City Simulator":
    st.title("🌆 Adaptive Civilization Node")

    if st.button("Spawn City"):
        memory["cities"].append({
            "id": str(uuid.uuid4())[:8],
            "population": random.randint(1000, 200000),
            "growth": random.random(),
            "created": datetime.now().isoformat()
        })
        save_memory(memory)

    st.json(memory["cities"])

# =========================================================
# 📚 KNOWLEDGE CORE
# =========================================================

elif page == "Knowledge Base":
    st.title("📚 Memory Substrate")

    txt = st.text_input("Add Knowledge")

    if st.button("Store") and txt:
        memory["knowledge"].append({
            "text": txt,
            "created": datetime.now().isoformat()
        })
        save_memory(memory)

    st.json(memory["knowledge"])

# =========================================================
# ⚙ ENGINE LAB
# =========================================================

elif page == "Engine Lab":
    st.title("🧬 Engine Evolution Lab")

    if st.button("Breed Engine"):
        memory["engines"].append(spawn_engine())
        save_memory(memory)

    st.json(memory["engines"])

# =========================================================
# 🧠 DYNAMIC MODULE VIEW (SELF-GENERATED NODES)
# =========================================================

elif page in memory["modules"]:
    st.title(f"🧬 Dynamic Module: {page}")

    st.write("Type:", memory["modules"][page]["type"])
    st.json(memory["modules"][page])
