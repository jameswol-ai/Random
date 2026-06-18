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
# PATH SETUP (FIXED - STABLE FOR STREAMLIT)
# =========================================================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# =========================================================
# CORE BOOTSTRAP (SAFE)
# =========================================================
try:
    from core.bootstrap import bootstrap
    bootstrap()
except Exception as e:
    st.warning(f"Bootstrap skipped: {e}")

# =========================================================
# CORE IMPORTS (HARDENED)
# =========================================================
try:
    from core.registry import run_pipeline, REGISTRIES
    from core.event_bus import event_bus
    from core.safe_execution import safe_execute
except Exception as e:
    st.error(f"Core system failed to load: {e}")

    run_pipeline = lambda *args, **kwargs: {"error": "core_missing"}
    REGISTRIES = {}

    class DummyBus:
        def emit(self, *args, **kwargs):
            pass

    event_bus = DummyBus()

    def safe_execute(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as ex:
            return {"error": str(ex)}

# =========================================================
# 🧠 APP CONFIG
# =========================================================
st.set_page_config(
    page_title="Random AI Civilization OS",
    layout="wide"
)

st.title("🏗️ RANDOM AI — Civilization Operating System")


# =========================================================
# 🧠 SESSION STATE
# =========================================================
DEFAULTS = {
    "result": None,
    "intent_text": "",
    "site_area": 1000.0,
    "civil_history": [],
    "brain_logs": [],
    "city_memory": [],
    "events": [],
    "active_agents": [],
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# =========================================================
# 🛡️ SAFE LOGGER
# =========================================================
def log(message):
    st.session_state.brain_logs.append(message)


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
# 🌐 EVENT BUS (LOCAL SAFE VERSION)
# =========================================================
class EventBus:
    def __init__(self):
        self.listeners = {}

    def emit(self, event, data=None):
        st.session_state.events.append({"event": event, "data": str(data)})

event_bus = EventBus()


# =========================================================
# 🧬 MEMORY ENGINE
# =========================================================
class MemoryEngine:
    def remember(self, item):
        st.session_state.city_memory.append(item)

    def recall(self):
        return st.session_state.city_memory[-10:]

memory = MemoryEngine()


# =========================================================
# 🏙️ RL CITY POLICY
# =========================================================
class CityPolicy:
    def __init__(self):
        self.risk_map = {}
        self.lr = 0.2

    def choose_location(self):
        x = random.randint(0, 25)
        y = random.randint(0, 25)

        if self.risk_map.get((x, y), 0) > 2:
            return self.choose_location()

        return x, y

    def update(self, failed_nodes):
        for n in failed_nodes:
            x, y, z = n
            self.risk_map[(x, y)] = self.risk_map.get((x, y), 0) + self.lr


# =========================================================
# 🏗️ BUILDING ENGINE
# =========================================================
class RLBuildingEngine:
    def generate(self, policy):
        buildings = []

        for _ in range(5):
            x, y = policy.choose_location()

            buildings.append({
                "x": x,
                "y": y,
                "floors": random.randint(3, 20),
                "grid": random.choice([6, 8, 10, 12]),
                "usage": random.choice(["Residential", "Commercial", "Industrial"])
            })

        return buildings


# =========================================================
# 🧱 PHYSICS ENGINE
# =========================================================
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

        return loads

    def collapse(self, loads):
        return {n for n, l in loads.items() if l > 2.0}


# =========================================================
# 🏙️ CITY ENGINE
# =========================================================
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

        return buildings, nodes, loads, failed, stability, reward


rl_engine = RLCityEngine()


# =========================================================
# 🧠 AGENTS
# =========================================================
class PlannerAgent:
    def act(self):
        return "Planning city expansion"

class DiplomacyAgent:
    def act(self):
        return random.choice(["Alliance formed", "Trade agreement signed", "Border tension detected"])

class WarAgent:
    def act(self):
        return random.choice(["Peace maintained", "Conflict escalation", "Defense mobilized"])


AGENTS = {
    "planner": PlannerAgent(),
    "diplomacy": DiplomacyAgent(),
    "war": WarAgent()
        }
