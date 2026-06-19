# =========================================================
# 🏗️ RANDOM AI — AUTONOMOUS CIVILIZATION OPERATING SYSTEM
# RL Cities + Architecture + Eurocodes + Agents + Memory
# + 🧠 Auto-Building Architecture Generator
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
# PATH SETUP (STABLE)
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
# CORE IMPORTS (FAIL-SAFE)
# =========================================================
try:
    from core.registry import run_pipeline, REGISTRIES
    from core.event_bus import event_bus
    from core.safe_execution import safe_execute
except Exception:
    run_pipeline = lambda *args, **kwargs: {"error": "core_missing"}
    REGISTRIES = {}

    class DummyBus:
        def emit(self, *args, **kwargs):
            pass

    event_bus = DummyBus()

    def safe_execute(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}

# =========================================================
# 🧠 APP CONFIG
# =========================================================
st.set_page_config(page_title="Random AI Civilization OS", layout="wide")
st.title("🏗️ RANDOM AI — Civilization Operating System")


# =========================================================
# 🧠 SESSION STATE
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
            "intelligence": random.random(),
            "adaptation": random.random(),
        }

    def think(self, text):
        log(f"Brain: {text}")
        return {
            "intent": text,
            "complexity": len(text.split()),
            "priority": random.choice(["housing", "industry", "transport"])
        }

    def evolve(self):
        self.state["awareness"] = np.clip(self.state["awareness"] + random.uniform(-0.05, 0.05), 0, 1)
        self.state["intelligence"] = np.clip(self.state["intelligence"] + random.uniform(-0.05, 0.05), 0, 1)

    def summary(self):
        return self.state


brain = RandomBrain()


# =========================================================
# 🧠 MEMORY ENGINE
# =========================================================
class MemoryEngine:
    def remember(self, item):
        st.session_state.city_memory.append(item)

    def recall(self):
        return st.session_state.city_memory[-10:]


memory = MemoryEngine()


# =========================================================
# 🏗️ AUTO ARCHITECTURE FORGE (NEW CORE FEATURE)
# =========================================================
class AutoArchitectureForge:

    def __init__(self):
        self.engines = {}

    def create_engine(self, name, purpose="general"):

        class DynamicEngine:
            def __init__(self):
                self.name = name
                self.purpose = purpose
                self.version = 1.0

            def run(self, data=None):
                return {
                    "engine": self.name,
                    "purpose": self.purpose,
                    "status": "active",
                    "input": data,
                    "output": f"Processed by {self.name}"
                }

            def evolve(self):
                self.version += 0.1
                return self.version

        engine = DynamicEngine()
        self.engines[name] = engine

        try:
            REGISTRIES[name] = engine
        except:
            pass

        return engine

    def list_engines(self):
        return {
            k: {"purpose": v.purpose, "version": v.version}
            for k, v in self.engines.items()
        }

    def run_engine(self, name, data=None):
        engine = self.engines.get(name)
        if not engine:
            return {"error": "engine_not_found"}
        return engine.run(data)


forge = AutoArchitectureForge()


# =========================================================
# 🏙️ CITY ENGINE (MINIMAL STABLE VERSION)
# =========================================================
class RLCityEngine:
    def step(self):
        return {
            "status": "city_step_complete",
            "stability": random.random(),
            "reward": random.random()
        }


rl_engine = RLCityEngine()


# =========================================================
# 🧠 AGENTS
# =========================================================
class PlannerAgent:
    def act(self): return "Planning expansion"

class DiplomacyAgent:
    def act(self): return random.choice(["Alliance", "Trade", "Tension"])

class WarAgent:
    def act(self): return random.choice(["Peace", "Conflict", "Defense"])


AGENTS = {
    "planner": PlannerAgent(),
    "diplomacy": DiplomacyAgent(),
    "war": WarAgent()
}


# =========================================================
# 🧭 SIDEBAR
# =========================================================
mode = st.sidebar.selectbox(
    "SYSTEM MODULE",
    [
        "🧠 AI Brain",
        "🏛️ Architecture",
        "🏙️ City",
        "📚 Memory",
        "🤖 Agents",
        "🛰️ Registry",
        "🏗️ Auto Architecture Forge"
    ]
)


# =========================================================
# 🧠 AI BRAIN
# =========================================================
if mode == "🧠 AI Brain":

    st.header("Brain")

    text = st.text_area("Intent", value=st.session_state.intent_text)

    if st.button("Run"):
        analysis = brain.think(text)
        result = safe_execute(run_pipeline, "main", analysis)
        st.session_state.result = result
        brain.evolve()
        st.json(result)

    st.json(brain.summary())


# =========================================================
# 🏛️ ARCHITECTURE
# =========================================================
elif mode == "🏛️ Architecture":

    floors = st.slider("Floors", 1, 50, 10)

    if st.button("Generate"):
        st.json([
            {"floor": i, "rooms": random.randint(3, 10)}
            for i in range(floors)
        ])


# =========================================================
# 🏙️ CITY
# =========================================================
elif mode == "🏙️ City":

    if st.button("Run Step"):
        st.json(rl_engine.step())


# =========================================================
# 📚 MEMORY
# =========================================================
elif mode == "📚 Memory":

    st.json(memory.recall())


# =========================================================
# 🤖 AGENTS
# =========================================================
elif mode == "🤖 Agents":

    for k, v in AGENTS.items():
        st.write(k, "→", v.act())


# =========================================================
# 🛰️ REGISTRY
# =========================================================
elif mode == "🛰️ Registry":

    st.json(REGISTRIES)


# =========================================================
# 🏗️ AUTO ARCHITECTURE FORGE UI
# =========================================================
elif mode == "🏗️ Auto Architecture Forge":

    st.header("Auto-Building Engine Generator")

    name = st.text_input("Engine Name", "VisionEngine")
    purpose = st.text_input("Purpose", "analysis")

    if st.button("Forge Engine"):
        forge.create_engine(name, purpose)
        st.success(f"Engine '{name}' created")

    st.subheader("Generated Engines")
    st.json(forge.list_engines())

    st.subheader("Run Engine")

    run_name = st.text_input("Engine to Run", name)
    data = st.text_area("Input Data", "test")

    if st.button("Execute Engine"):
        st.json(forge.run_engine(run_name, data))
