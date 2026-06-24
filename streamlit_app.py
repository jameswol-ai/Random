# =========================================================
# RANDOM V4 — AUTONOMOUS AI CIVILIZATION OS (CORE)
# Single-file Streamlit Kernel
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
st.set_page_config(page_title="RANDOM V4", layout="wide")

st.title("🧠 RANDOM V4 — Autonomous AI OS Kernel")

# ---------------------------------------------------------
# MEMORY LAYER
# ---------------------------------------------------------
MEMORY_FILE = Path("random_memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"projects": [], "logs": [], "agents": []}

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

memory = load_memory()

# ---------------------------------------------------------
# AGENT CORE (minimal autonomous logic unit)
# ---------------------------------------------------------
class Agent:
    def __init__(self, name, role):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.role = role
        self.energy = random.randint(50, 100)

    def act(self):
        actions = [
            "analyzing system patterns",
            "optimizing memory graph",
            "simulating architecture growth",
            "stabilizing workflows",
            "expanding knowledge nodes"
        ]
        return random.choice(actions)

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
st.sidebar.header("⚙️ Control Panel")

if st.sidebar.button("➕ Create Agent"):
    agent = Agent(f"Agent-{len(memory['agents'])+1}", "builder")
    memory["agents"].append(agent.__dict__)
    save_memory(memory)
    st.sidebar.success("Agent spawned")

if st.sidebar.button("🧹 Reset Memory"):
    memory = {"projects": [], "logs": [], "agents": []}
    save_memory(memory)
    st.sidebar.warning("Memory cleared")

# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Projects", len(memory["projects"]))
col2.metric("Agents", len(memory["agents"]))
col3.metric("Logs", len(memory["logs"]))

# ---------------------------------------------------------
# AGENT VIEW
# ---------------------------------------------------------
st.subheader("🤖 Active Agents")

if memory["agents"]:
    for a in memory["agents"]:
        st.write(f"**{a['name']}** ({a['role']}) — energy: {a['energy']}")
else:
    st.info("No agents yet. Spawn one from the sidebar.")

# ---------------------------------------------------------
# SIMULATION ENGINE (lightweight chaos loop)
# ---------------------------------------------------------
st.subheader("🌐 System Simulation")

if st.button("Run Simulation Tick"):
    log_entry = {
        "id": str(uuid.uuid4())[:8],
        "time": str(datetime.now()),
        "event": random.choice([
            "node expansion",
            "memory compression",
            "agent collaboration spike",
            "system equilibrium shift"
        ])
    }
    memory["logs"].append(log_entry)
    save_memory(memory)
    st.success(f"Event: {log_entry['event']}")

# ---------------------------------------------------------
# LOG VIEW
# ---------------------------------------------------------
st.subheader("📜 System Logs")

for log in reversed(memory["logs"][-10:]):
    st.text(f"{log['time']} → {log['event']}")

# ---------------------------------------------------------
# FOOTER INTROSPECTION
# ---------------------------------------------------------
st.markdown("---")
st.caption("Random V4 Kernel — evolving toward autonomous architecture synthesis")
