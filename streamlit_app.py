# =========================================================
# RANDOM V5 — SELF-WRITING AI ARCHITECTURE GENERATOR OS
# Single-file Streamlit Kernel (Evolving System)
# =========================================================

import streamlit as st
import json
import uuid
from pathlib import Path
from datetime import datetime
import random

# ---------------------------------------------------------
# APP CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="RANDOM V5", layout="wide")
st.title("🧠 RANDOM V5 — Self-Writing Architecture Generator")

# ---------------------------------------------------------
# MEMORY + ARCHITECTURE STORE
# ---------------------------------------------------------
MEMORY_FILE = Path("random_memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {
        "projects": [],
        "logs": [],
        "agents": [],
        "modules": []   # NEW: generated architecture modules
    }

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

memory = load_memory()

# ---------------------------------------------------------
# SELF-WRITING CODE ENGINE (ARCHITECTURE GENERATOR)
# ---------------------------------------------------------
class ArchitectureGenerator:
    """
    This system does NOT overwrite itself.
    It generates new conceptual modules (like AI-written plugins).
    """

    MODULE_TEMPLATES = [
        {
            "name": "Memory Compression Unit",
            "purpose": "Compress long-term memory logs into semantic summaries",
            "logic": "cluster + summarize + prune low-signal events"
        },
        {
            "name": "Agent Evolution Engine",
            "purpose": "Mutate agent roles based on system performance",
            "logic": "reward successful behaviors and rewrite roles"
        },
        {
            "name": "Architecture Synthesizer",
            "purpose": "Generate new system modules from system gaps",
            "logic": "detect missing capabilities and propose modules"
        },
        {
            "name": "Simulation Drift Controller",
            "purpose": "Stabilize chaotic simulation outputs",
            "logic": "apply equilibrium balancing across logs"
        },
        {
            "name": "Knowledge Node Expander",
            "purpose": "Grow graph-like memory structure",
            "logic": "convert logs into connected knowledge nodes"
        }
    ]

    def generate_module(self):
        base = random.choice(self.MODULE_TEMPLATES)

        module = {
            "id": str(uuid.uuid4())[:8],
            "name": base["name"],
            "purpose": base["purpose"],
            "logic": base["logic"],
            "created_at": str(datetime.now()),
            "status": "dormant"
        }

        return module

# ---------------------------------------------------------
# AGENT CORE
# ---------------------------------------------------------
class Agent:
    def __init__(self, name, role):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.role = role
        self.energy = random.randint(50, 100)

    def act(self):
        return random.choice([
            "mapping system topology",
            "rewriting internal heuristics",
            "stabilizing memory drift",
            "collaborating with modules",
            "observing architecture evolution"
        ])

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
st.sidebar.header("⚙️ Control Panel")

gen = ArchitectureGenerator()

if st.sidebar.button("➕ Spawn Agent"):
    agent = Agent(f"Agent-{len(memory['agents'])+1}", "builder")
    memory["agents"].append(agent.__dict__)
    save_memory(memory)
    st.sidebar.success("Agent created")

if st.sidebar.button("🧬 Generate New Module"):
    module = gen.generate_module()
    memory["modules"].append(module)
    save_memory(memory)
    st.sidebar.success(f"Module generated: {module['name']}")

if st.sidebar.button("🧹 Reset System"):
    memory = {"projects": [], "logs": [], "agents": [], "modules": []}
    save_memory(memory)
    st.sidebar.warning("System reset")

# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Agents", len(memory["agents"]))
col2.metric("Modules", len(memory["modules"]))
col3.metric("Logs", len(memory["logs"]))
col4.metric("Projects", len(memory["projects"]))

# ---------------------------------------------------------
# MODULE VIEW (SELF-WRITTEN ARCHITECTURE)
# ---------------------------------------------------------
st.subheader("🧬 Generated Architecture Modules")

if memory["modules"]:
    for m in memory["modules"]:
        with st.expander(f"{m['name']} [{m['status']}]"):
            st.write("**Purpose:**", m["purpose"])
            st.write("**Logic Kernel:**", m["logic"])
            st.write("**Created:**", m["created_at"])
else:
    st.info("No modules generated yet. The system has not begun evolving its architecture.")

# ---------------------------------------------------------
# AGENTS VIEW
# ---------------------------------------------------------
st.subheader("🤖 Agents")

for a in memory["agents"]:
    st.write(f"**{a['name']}** ({a['role']}) energy={a['energy']}")

# ---------------------------------------------------------
# SIMULATION ENGINE
# ---------------------------------------------------------
st.subheader("🌐 Evolution Simulation")

if st.button("Run Evolution Tick"):
    event = random.choice([
        "architecture drift detected",
        "module synergy increased",
        "agent specialization shift",
        "memory restructuring occurred",
        "system self-stabilized"
    ])

    memory["logs"].append({
        "id": str(uuid.uuid4())[:8],
        "time": str(datetime.now()),
        "event": event
    })

    # Occasionally auto-generate a module (self-writing behavior)
    if random.random() > 0.6:
        auto_module = gen.generate_module()
        memory["modules"].append(auto_module)
        event += " + auto-module spawned"

    save_memory(memory)
    st.success(event)

# ---------------------------------------------------------
# LOG STREAM
# ---------------------------------------------------------
st.subheader("📜 System Logs")

for log in reversed(memory["logs"][-10:]):
    st.text(f"{log['time']} → {log['event']}")

# ---------------------------------------------------------
# SYSTEM INTROSPECTION
# ---------------------------------------------------------
st.markdown("---")
st.caption("RANDOM V5 — architecture grows through emitted module structures, not self-editing code")
