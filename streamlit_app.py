# =========================================================
# RANDOM V15
# Multi-Agent Architecture Civilization OS
# Swarm Intelligence Design System
# =========================================================

import streamlit as st
import uuid
import random
import json
from datetime import datetime
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random AIOS V15",
    page_icon="🏛️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# MEMORY
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "logs": [],
    "civilization_history": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2), encoding="utf-8")

def log(mem, msg):
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory(mem)

mem = load_memory()

# =========================================================
# MULTI-AGENT SYSTEM (THE CIVILIZATION)
# =========================================================

def structural_agent(design):
    ratio = design["beams"] / max(1, design["columns"])
    score = max(0, 100 - abs(2.0 - ratio) * 25)
    return score

def cost_agent(design):
    cost_per_sqm = design["cost"] / max(1, design["area"])
    score = max(0, 100 - abs(cost_per_sqm - 1600) * 0.03)
    return score

def sustainability_agent(design):
    score = max(40, 100 - design["area"] * 0.05)
    return score

def compliance_agent(design):
    violations = 0
    if design["columns"] < 12:
        violations += 1
    if design["beams"] < 20:
        violations += 1
    return max(0, 100 - violations * 25)

# =========================================================
# AGGREGATOR (CIVILIZATION COUNCIL VOTE)
# =========================================================

def council_vote(design):
    votes = {
        "structural": structural_agent(design),
        "cost": cost_agent(design),
        "sustainability": sustainability_agent(design),
        "compliance": compliance_agent(design)
    }

    final_score = sum(votes.values()) / len(votes)

    return final_score, votes

# =========================================================
# GENERATION SYSTEM
# =========================================================

def generate_design():
    return {
        "id": str(uuid.uuid4())[:8],
        "area": random.randint(120, 800),
        "cost": random.randint(100000, 900000),
        "columns": random.randint(8, 40),
        "beams": random.randint(15, 80),
    }

def run_civilization(pop_size=10):
    population = [generate_design() for _ in range(pop_size)]

    evaluated = []
    for d in population:
        score, votes = council_vote(d)
        d["score"] = score
        d["votes"] = votes
        evaluated.append(d)

    evaluated.sort(key=lambda x: x["score"], reverse=True)

    return evaluated

# =========================================================
# EVOLUTION ENGINE (SELECTION OF BEST CIVILIZATION DESIGN)
# =========================================================

def evolve_civilization(pop_size):
    population = run_civilization(pop_size)

    best = population[0]
    history = [p["score"] for p in population]

    mem["designs"].append(best)
    mem["civilization_history"].append({
        "id": best["id"],
        "score": best["score"],
        "time": datetime.now().isoformat()
    })

    log(mem, f"Civilization evolved design {best['id']} with score {best['score']:.2f}")

    return best, history

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏛️ AIOS Civilization V15")

page = st.sidebar.radio(
    "Civilization Layer",
    [
        "🏠 Dashboard",
        "🏗 Simulation",
        "🧠 Council View",
        "📊 Evolution History",
        "📜 Memory"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":
    st.title("🏛 Architecture Civilization OS")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Civilization Events", len(mem["civilization_history"]))
    c3.metric("Logs", len(mem["logs"]))

    st.subheader("Recent Activity")
    for l in mem["logs"][-6:][::-1]:
        st.write(f"⏱ {l['time'][11:19]} → {l['msg']}")

# =========================================================
# SIMULATION
# =========================================================

elif page == "🏗 Simulation":
    st.title("🏗 Civilization Simulation Engine")

    pop = st.slider("Population Size", 4, 30, 10)

    if st.button("Run Civilization Evolution"):
        best, history = evolve_civilization(pop)

        st.success("Civilization step completed")

        st.metric("Best Design Score", round(best["score"], 2))
        st.json(best)

        st.line_chart(history)

# =========================================================
# COUNCIL VIEW
# =========================================================

elif page == "🧠 Council View":
    st.title("🧠 Architecture Council")

    sample = generate_design()
    score, votes = council_vote(sample)

    st.write("Sample Design")
    st.json(sample)

    st.write("Council Votes")
    st.json(votes)

    st.metric("Final Consensus Score", round(score, 2))

# =========================================================
# HISTORY
# =========================================================

elif page == "📊 Evolution History":
    st.title("📊 Civilization Evolution History")

    if mem["civilization_history"]:
        scores = [x["score"] for x in mem["civilization_history"]]
        st.line_chart(scores)
    else:
        st.info("No evolution history yet.")

# =========================================================
# MEMORY
# =========================================================

elif page == "📜 Memory":
    st.title("📜 Civilization Memory")

    st.json(mem)

    if st.button("Reset Civilization"):
        mem = DEFAULT_STATE.copy()
        save_memory(mem)
        st.rerun()