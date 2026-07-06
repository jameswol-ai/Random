# =========================================================
# RANDOM V16
# Autonomous Architecture Intelligence System
# Evolutionary Spatial + Agentic Design Engine
# Single-File Streamlit Edition
# =========================================================

import streamlit as st
import json
import uuid
import random
from datetime import datetime
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V16",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# MEMORY CORE
# =========================================================

MEMORY_FILE = Path("random_memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"projects": [], "logs": [], "agents": []}

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

memory = load_memory()

# =========================================================
# UTILS
# =========================================================

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
# AGENT SYSTEM
# =========================================================

AGENT_LIBRARY = {
    "planner": "Breaks design into modular subsystems",
    "critic": "Detects structural inefficiencies",
    "evolver": "Mutates architecture configurations",
    "visualizer": "Generates spatial representations",
    "optimizer": "Improves system coherence score"
}

def run_agent(agent, context):
    if agent == "planner":
        return {
            "modules": ["core", "data_layer", "ui_layer", "ai_layer", "storage"],
            "strategy": "modular decomposition"
        }

    if agent == "critic":
        issues = ["tight coupling risk", "missing abstraction layer"]
        return {"issues": issues, "score": random.randint(60, 85)}

    if agent == "evolver":
        return {
            "mutation": random.choice(["add_cache", "split_module", "introduce_event_bus"]),
            "generation": random.randint(1, 10)
        }

    if agent == "visualizer":
        return {
            "nodes": random.randint(5, 12),
            "edges": random.randint(6, 18),
            "layout": "force-directed-simulated"
        }

    if agent == "optimizer":
        return {
            "improvements": ["reduced coupling", "enhanced modularity"],
            "efficiency_gain": f"{random.randint(5, 35)}%"
        }

    return {"error": "unknown agent"}

# =========================================================
# ARCHITECTURE ENGINE
# =========================================================

def generate_architecture(name):
    base = {
        "id": uid(),
        "name": name,
        "timestamp": datetime.utcnow().isoformat(),
        "modules": [],
        "score": 0,
        "evolution": []
    }

    planner = run_agent("planner", base)
    critic = run_agent("critic", planner)
    evolver = run_agent("evolver", critic)
    optimizer = run_agent("optimizer", evolver)

    base["modules"] = planner["modules"]
    base["score"] = critic["score"]
    base["evolution"].append(evolver)
    base["optimization"] = optimizer

    return base

# =========================================================
# UI HEADER
# =========================================================

st.title("🧠 RANDOM V16 — Architecture Intelligence Engine")
st.caption("Evolutionary spatial synthesis + multi-agent reasoning core")

# =========================================================
# SIDEBAR CONTROL PANEL
# =========================================================

st.sidebar.header("⚙️ Control Panel")

project_name = st.sidebar.text_input("Project Name", "Neural Tower")

if st.sidebar.button("🚀 Generate Architecture"):
    arch = generate_architecture(project_name)
    memory["projects"].append(arch)
    log(f"Generated architecture: {project_name}")
    save_memory(memory)
    st.session_state["latest"] = arch

if st.sidebar.button("🧬 Run Evolution Cycle"):
    if memory["projects"]:
        target = memory["projects"][-1]
        mutation = run_agent("evolver", target)
        target["evolution"].append(mutation)
        log("Evolution cycle executed")
        save_memory(memory)
        st.session_state["latest"] = target

if st.sidebar.button("📊 Run Diagnostics"):
    log("Diagnostics executed")

# =========================================================
# MAIN VIEW
# =========================================================

tab1, tab2, tab3 = st.tabs(["🏗 Architecture", "🧠 Agents", "📜 Memory Log"])

# ---------------------------------------------------------
# ARCHITECTURE VIEW
# ---------------------------------------------------------

with tab1:
    st.subheader("Generated Architecture")

    if "latest" in st.session_state:
        arch = st.session_state["latest"]

        st.json(arch)

        st.markdown("### Modules")
        for m in arch["modules"]:
            st.write("•", m)

        st.markdown("### System Score")
        st.metric("Coherence Score", arch["score"])

        st.markdown("### Evolution Trace")
        st.json(arch.get("evolution", []))

    else:
        st.info("Generate an architecture to begin the simulation.")

# ---------------------------------------------------------
# AGENTS VIEW
# ---------------------------------------------------------

with tab2:
    st.subheader("Agent Registry")

    for k, v in AGENT_LIBRARY.items():
        st.markdown(f"**{k.upper()}**")
        st.caption(v)

    st.markdown("### Live Agent Test")

    selected = st.selectbox("Select Agent", list(AGENT_LIBRARY.keys()))
    if st.button("Run Agent"):
        result = run_agent(selected, {})
        st.json(result)

# ---------------------------------------------------------
# MEMORY VIEW
# ---------------------------------------------------------

with tab3:
    st.subheader("System Memory")

    st.write("Projects stored:", len(memory["projects"]))
    st.write("Events logged:", len(memory["logs"]))

    st.markdown("### Recent Logs")
    st.json(memory["logs"][-10:])

# =========================================================
# FOOTER STATUS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.caption("RANDOM V16 running in autonomous simulation mode")
