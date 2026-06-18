# =========================================================
# 🏗️ RANDOM AI — AUTONOMOUS CIVILIZATION OPERATING SYSTEM
# RL Cities + Architecture + Eurocodes + Agents + Memory
# =========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import os
import sys
import traceback
from mpl_toolkits.mplot3d import Axes3D

# =========================================================
# PATH SETUP
# =========================================================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# =========================================================
# CORE BOOTSTRAP
# =========================================================
from core.bootstrap import bootstrap
bootstrap()

from core.registry import run_pipeline, REGISTRIES
from core.event_bus import event_bus
from core.safe_execution import safe_execute

# =========================================================
# APP CONFIG
# =========================================================
st.set_page_config(
    page_title="Random AI Civilization OS",
    layout="wide"
)

st.title("🏗️ RANDOM AI — Civilization Operating System")

# =========================================================
# SESSION STATE
# =========================================================
DEFAULTS = {
    "result": None,
    "intent_text": "",
    "site_area": 1000.0,
    "brain_logs": [],
    "city_memory": [],
    "events": [],
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def log(msg):
    st.session_state.brain_logs.append(msg)

# =========================================================
# 🧠 RANDOM BRAIN
# =========================================================
class RandomBrain:
    def __init__(self):
        self.state = {
            "awareness": random.random(),
            "stability": 1.0,
            "intelligence": random.random(),
            "adaptation": random.random(),
        }

    def think(self, text):
        log(f"Brain analyzing intent: {text}")
        return {
            "intent": text,
            "complexity": len(text.split()),
            "priority": random.choice(["housing", "industry", "transport", "mixed_use"])
        }

    def evolve(self):
        self.state["awareness"] = np.clip(self.state["awareness"] + random.uniform(-0.05, 0.05), 0, 1)
        self.state["intelligence"] = np.clip(self.state["intelligence"] + random.uniform(-0.05, 0.05), 0, 1)

    def summary(self):
        return self.state

brain = RandomBrain()

# =========================================================
# MEMORY
# =========================================================
class MemoryEngine:
    def remember(self, item):
        st.session_state.city_memory.append(item)

    def recall(self):
        return st.session_state.city_memory[-10:]

memory = MemoryEngine()

# =========================================================
# EVENT BUS
# =========================================================
class EventBus:
    def emit(self, event, data=None):
        st.session_state.events.append({"event": event, "data": str(data)})

event_bus = EventBus()

# =========================================================
# RL CITY SYSTEM
# =========================================================
class CityPolicy:
    def __init__(self):
        self.risk_map = {}
        self.lr = 0.2

    def choose_location(self):
        x, y = random.randint(0, 25), random.randint(0, 25)
        if self.risk_map.get((x, y), 0) > 2:
            return self.choose_location()
        return x, y

    def update(self, failed_nodes):
        for n in failed_nodes:
            x, y, z = n
            self.risk_map[(x, y)] = self.risk_map.get((x, y), 0) + self.lr


class RLBuildingEngine:
    def generate(self, policy):
        return [{
            "x": policy.choose_location()[0],
            "y": policy.choose_location()[1],
            "floors": random.randint(3, 20),
            "grid": random.choice([6, 8, 10, 12]),
            "usage": random.choice(["Residential", "Commercial", "Industrial"])
        } for _ in range(5)]


class RLPhysics:
    def build_nodes(self, buildings):
        nodes = []
        for b in buildings:
            for z in range(b["floors"]):
                for x in range(0, b["grid"], 2):
                    for y in range(0, b["grid"], 2):
                        nodes.append((x + b["x"], y + b["y"], z))
        return nodes

    def compute_loads(self, nodes):
        loads = {n: 0.0 for n in nodes}
        if not nodes:
            return loads

        max_z = max(n[2] for n in nodes)

        for n in nodes:
            if n[2] == max_z:
                loads[n] += 1.0

        for _ in range(3):
            for (x, y, z), l in list(loads.items()):
                below = (x, y, z - 1)
                if below in loads:
                    loads[below] += l * 0.7

        return loads

    def collapse(self, loads):
        return {n for n, l in loads.items() if l > 2.0}


class RLCityEngine:
    def __init__(self):
        self.policy = CityPolicy()
        self.builder = RLBuildingEngine()
        self.physics = RLPhysics()
        self.history = []

    def step(self):
        buildings = self.builder.generate(self.policy)
        nodes = self.physics.build_nodes(buildings)
        loads = self.physics.compute_loads(nodes)
        failed = self.physics.collapse(loads)

        self.policy.update(failed)

        stability = max(0, 1 - len(failed) / max(1, len(nodes)))
        reward = stability - 0.3 * len(failed)

        self.history.append(reward)

        memory.remember({
            "reward": reward,
            "stability": stability,
            "failures": len(failed)
        })

        event_bus.emit("city_step", {"reward": reward})

        return buildings, nodes, loads, failed, stability, reward


rl_engine = RLCityEngine()

# =========================================================
# AGENTS
# =========================================================
class PlannerAgent:
    def act(self): return "Planning expansion"

class DiplomacyAgent:
    def act(self): return random.choice(["Alliance formed", "Trade agreement", "Tension"])

class WarAgent:
    def act(self): return random.choice(["Peace", "Conflict", "Defense"])

AGENTS = {
    "planner": PlannerAgent(),
    "diplomacy": DiplomacyAgent(),
    "war": WarAgent()
}

# =========================================================
# SIDEBAR
# =========================================================
mode = st.sidebar.selectbox("SYSTEM MODULE", [
    "🧠 AI Brain",
    "🏛️ Architecture Generator",
    "🏗️ Structure Engine",
    "💰 Cost Engine",
    "🧊 Rendering",
    "🚀 Full Pipeline",
    "🏙️ RL City",
    "🌆 City Learning",
    "🤝 Diplomacy Network",
    "⚔️ War System",
    "📚 Memory System",
    "📡 Event Bus",
    "🤖 Agent Network",
    "🛰️ Registry"
])

# =========================================================
# MODULES
# =========================================================

if mode == "🧠 AI Brain":
    st.header("Brain")
    st.session_state.intent_text = st.text_area("Intent", st.session_state.intent_text)

    if st.button("Run"):
        analysis = brain.think(st.session_state.intent_text)
        result = safe_execute(run_pipeline, "main", analysis)
        st.session_state.result = result
        brain.evolve()

    st.json(brain.summary())
    if st.session_state.result:
        st.json(st.session_state.result)

elif mode == "🏛️ Architecture Generator":
    floors = st.slider("Floors", 1, 100, 10)
    if st.button("Generate"):
        st.json([{
            "floor": i,
            "rooms": random.randint(4, 20)
        } for i in range(floors)])

elif mode == "🏗️ Structure Engine":
    span = st.slider("Span", 3, 20, 8)
    load = st.slider("Load", 1, 20, 5)
    st.metric("Moment", load * span**2 / 8)

elif mode == "💰 Cost Engine":
    area = st.number_input("Area", 500.0)
    st.metric("Cost", f"${area * random.randint(400,1200):,.0f}")

elif mode == "🧊 Rendering":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(np.random.rand(100), np.random.rand(100), np.random.rand(100))
    st.pyplot(fig)

elif mode == "🚀 Full Pipeline":
    stages = ["Intent", "Arch", "Struct", "MEP", "Sim", "Render"]
    p = st.progress(0)
    for i, s in enumerate(stages):
        time.sleep(0.2)
        p.progress((i+1)/len(stages))
    st.success("Done")

elif mode == "🏙️ RL City":
    if st.button("Step"):
        b, n, l, f, s, r = rl_engine.step()
        st.metric("Stability", round(s,3))
        st.metric("Failures", len(f))
        st.metric("Reward", round(r,3))
        st.json(b)

elif mode == "🌆 City Learning":
    st.line_chart(rl_engine.history if rl_engine.history else [0])

elif mode == "🤝 Diplomacy Network":
    st.success(AGENTS["diplomacy"].act())

elif mode == "⚔️ War System":
    st.warning(AGENTS["war"].act())

elif mode == "📚 Memory System":
    st.json(memory.recall())

elif mode == "📡 Event Bus":
    st.json(st.session_state.events[-20:])

elif mode == "🤖 Agent Network":
    for k, a in AGENTS.items():
        st.subheader(k)
        st.write(a.act())

elif mode == "🛰️ Registry":
    st.json(REGISTRIES)
