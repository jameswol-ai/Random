# =========================================================
# RANDOM V14
# Self-Writing Architecture Intelligence OS
# Kernel + Plugin Evolution System
# =========================================================

import streamlit as st
import uuid
import json
import random
from datetime import datetime
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random AIOS V14",
    page_icon="🧠",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")
KERNEL_FILE = Path("arc_kernel.json")

# =========================================================
# CORE STATE
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "plugins": [],
    "logs": [],
    "evolution": [],
    "self_writes": []
}

DEFAULT_KERNEL = {
    "modules": {
        "Dashboard": True,
        "Design Studio": True,
        "AI Architect": True,
        "Plugins": True
    },
    "generated_modules": []
}

# =========================================================
# MEMORY SYSTEM
# =========================================================

def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default.copy()
    return default.copy()

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

memory = load_json(MEMORY_FILE, DEFAULT_STATE)
kernel = load_json(KERNEL_FILE, DEFAULT_KERNEL)

# =========================================================
# LOGGING
# =========================================================

def log(msg):
    memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_json(MEMORY_FILE, memory)

# =========================================================
# SELF-WRITING ENGINE (CORE IDEA)
# =========================================================

def ai_propose_module():
    """AI generates a new system module idea"""
    ideas = [
        "Seismic Simulation Engine",
        "Carbon Impact Analyzer",
        "Structural Load Predictor",
        "Urban Density Optimizer",
        "Material Supply Chain AI",
        "Auto-BIM Generator",
        "Climate Adaptive Facade Designer"
    ]

    name = random.choice(ideas)

    return {
        "id": str(uuid.uuid4())[:6],
        "name": name,
        "type": "auto_generated_module",
        "created": datetime.now().isoformat(),
        "status": "proposed"
    }

def register_module(module):
    kernel["generated_modules"].append(module)
    save_json(KERNEL_FILE, kernel)
    log(f"Module registered: {module['name']}")

# =========================================================
# EVOLUTION ENGINE (SYSTEM SELF-IMPROVEMENT)
# =========================================================

def evolve_system():
    new_module = ai_propose_module()

    # probabilistic acceptance (governance gate)
    if random.random() > 0.35:
        new_module["status"] = "accepted"
        register_module(new_module)
        return new_module, True
    else:
        new_module["status"] = "rejected"
        return new_module, False

# =========================================================
# STREAMLIT UI
# =========================================================

st.sidebar.title("🧠 Random AIOS V14")
page = st.sidebar.radio(
    "System Core",
    [
        "🏠 Dashboard",
        "🧪 Design Studio",
        "🧠 AI Architect",
        "🔌 Plugin Engine",
        "🧬 Self-Writing Kernel",
        "📜 System Memory"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("V14 • Self-Writing Architecture Kernel")

# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":
    st.title("🧠 Self-Writing Architecture OS")

    c1, c2, c3 = st.columns(3)

    c1.metric("Projects", len(memory["projects"]))
    c2.metric("Plugins", len(memory["plugins"]))
    c3.metric("Generated Modules", len(kernel["generated_modules"]))

    st.subheader("Recent System Activity")

    for log_entry in memory["logs"][-8:][::-1]:
        st.write(f"⏱ {log_entry['time'][11:19]} → {log_entry['msg']}")

# =========================================================
# DESIGN STUDIO
# =========================================================

elif page == "🧪 Design Studio":
    st.title("🧪 Generative Architecture Studio")

    if st.button("Generate Design"):
        design = {
            "id": str(uuid.uuid4())[:8],
            "area": random.randint(120, 700),
            "score": random.randint(60, 100),
            "structure": {
                "columns": random.randint(10, 50),
                "beams": random.randint(20, 90)
            }
        }

        memory["designs"].append(design)
        log(f"Design generated {design['id']}")

        st.success("Design generated")
        st.json(design)

# =========================================================
# AI ARCHITECT CORE
# =========================================================

elif page == "🧠 AI Architect":
    st.title("🧠 AI Architecture Brain")

    st.info("This layer will eventually generate architecture logic, zoning plans, and structural reasoning.")

    if st.button("Run Cognitive Simulation"):
        thought = random.choice([
            "Optimizing beam-to-column ratio",
            "Simulating urban density flow",
            "Evaluating thermal efficiency",
            "Rebalancing structural load paths"
        ])

        st.success(f"AI Thought: {thought}")
        log(thought)

# =========================================================
# PLUGIN ENGINE
# =========================================================

elif page == "🔌 Plugin Engine":
    st.title("🔌 Plugin Registry")

    name = st.text_input("New Plugin Name")

    if st.button("Register Plugin"):
        plugin = {
            "id": str(uuid.uuid4())[:6],
            "name": name,
            "created": datetime.now().isoformat()
        }

        memory["plugins"].append(plugin)
        log(f"Plugin registered: {name}")

        st.success("Plugin added")

    st.json(memory["plugins"])

# =========================================================
# SELF-WRITING KERNEL
# =========================================================

elif page == "🧬 Self-Writing Kernel":
    st.title("🧬 Self-Writing System Kernel")

    st.write("System can now propose and evolve its own modules.")

    if st.button("Evolve System"):
        module, accepted = evolve_system()

        if accepted:
            st.success(f"Accepted Module: {module['name']}")
        else:
            st.warning(f"Rejected Module: {module['name']}")

        st.json(module)

    st.subheader("Generated Modules")
    st.json(kernel["generated_modules"])

# =========================================================
# SYSTEM MEMORY
# =========================================================

elif page == "📜 System Memory":
    st.title("📜 Memory Core")

    st.json(memory)

    if st.button("Reset System"):
        memory = DEFAULT_STATE.copy()
        kernel = DEFAULT_KERNEL.copy()

        save_json(MEMORY_FILE, memory)
        save_json(KERNEL_FILE, kernel)

        st.rerun()