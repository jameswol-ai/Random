# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# V7 — ARC STUDIO CORE (STABLE EDITION)
# Evolutionary Design Generator + Simple Studio UI
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
    page_title="Arc Studio V7",
    page_icon="🏗",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLE LAYER
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
}

.card {
    background: #0b1220;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "logs": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except:
        pass

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# Init
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

# =========================================================
# CORE GENERATIVE ENGINE
# =========================================================

def generate_design(goal):
    area = random.randint(100, 800)

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "goal": goal,
        "area": area,
        "cost": area * random.randint(1000, 2200),
        "structure": {
            "columns": random.randint(10, 40),
            "beams": random.randint(15, 80)
        },
        "rooms": ["Living", "Kitchen", "Bath"] + ["Room"] * random.randint(1, 5)
    }

def fitness(d):
    return (
        d["area"] * 0.2 +
        d["structure"]["columns"] * 1.3 +
        d["structure"]["beams"] * 1.1 -
        d["cost"] * 0.0001
    )

def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] += random.randint(-2, 2)
    d["structure"]["beams"] += random.randint(-3, 3)
    d["cost"] += random.randint(-3000, 3000)

    if random.random() > 0.7:
        d["rooms"].append("Adaptive Module")
        d["area"] += 10

    return d

def evolve(goal, generations=5, pop_size=6):
    pop = [generate_design(goal) for _ in range(pop_size)]
    history = []

    for _ in range(generations):
        pop.sort(key=fitness, reverse=True)
        history.append(fitness(pop[0]))

        survivors = pop[:max(2, pop_size // 2)]
        new_pop = []

        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate(s))

        pop = new_pop[:pop_size]

    return pop[0], history

def floor_plan(d):
    return [{"room": r, "size": random.randint(20, 60)} for r in d["rooms"]]

# =========================================================
# UI NAVIGATION
# =========================================================

st.sidebar.title("🏗 Arc Studio V7")

page = st.sidebar.radio(
    "Workspace",
    ["Dashboard", "Design Lab", "Memory"]
)

goal = st.sidebar.text_input("Design Goal", "Eco House")
run = st.sidebar.button("Generate")

# =========================================================
# GENERATION
# =========================================================

if run:
    best, hist = evolve(goal)

    best["plan"] = floor_plan(best)

    mem["designs"].append(best)
    st.session_state.active_design = best

    log(f"Generated design {best['id']}")

# =========================================================
# ACTIVE DESIGN
# =========================================================

d = st.session_state.active_design

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏗 Arc Studio Dashboard")

    st.metric("Total Designs", len(mem["designs"]))
    st.metric("Logs", len(mem["logs"]))

    st.markdown("---")

    for l in mem["logs"][-5:]:
        st.write(l)

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "Design Lab":
    st.title("📐 Design Lab")

    if d:
        st.subheader(f"Design {d['id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Area", f"{d['area']} m²")
        c2.metric("Cost", f"${d['cost']:,}")
        c3.metric("Rooms", len(d["rooms"]))

        st.markdown("### Structure")
        st.json(d["structure"])

        st.markdown("### Floor Plan")
        st.json(d["plan"])
    else:
        st.info("Generate a design first.")

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 Memory Core")

    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        save_memory()
        st.rerun()
