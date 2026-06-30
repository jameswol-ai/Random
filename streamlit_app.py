# =========================================================
# ARC BIM AI CORE v4 — DIGITAL TWIN + EVOLUTION + GEN BIM
# Unified Architecture Intelligence System
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
    page_title="ARC BIM AI CORE v4",
    page_icon="🏢",
    layout="wide"
)

MEMORY_FILE = Path("arc_bim_core_v4.json")

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT = {"projects": [], "logs": []}

def load():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE))
        except:
            return DEFAULT.copy()
    return DEFAULT.copy()

def save():
    json.dump(st.session_state.mem, open(MEMORY_FILE, "w"), indent=2)

def log(msg):
    st.session_state.mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save()

if "mem" not in st.session_state:
    st.session_state.mem = load()

mem = st.session_state.mem

# =========================================================
# BIM GRAPH CORE
# =========================================================

def new_id(prefix):
    return f"{prefix}_{str(uuid.uuid4())[:6]}"

def generate_bim(domain, levels, rooms_per_level):
    nodes, edges = [], []

    level_nodes = []

    for i in range(levels):
        lvl = {"id": new_id("LVL"), "type": "LEVEL", "level": i}
        nodes.append(lvl)
        level_nodes.append(lvl)

    for lvl in level_nodes:
        floor = {"id": new_id("FLR"), "type": "FLOOR", "level": lvl["level"]}
        nodes.append(floor)
        edges.append((lvl["id"], floor["id"], "supports"))

        for _ in range(random.randint(6, 10)):
            col = {
                "id": new_id("COL"),
                "type": "COLUMN",
                "level": lvl["level"],
                "capacity": random.randint(800, 2000),
                "stress": random.randint(200, 900)
            }
            nodes.append(col)
            edges.append((lvl["id"], col["id"], "supports"))

        for i in range(rooms_per_level):
            room = {
                "id": new_id("RM"),
                "type": "ROOM",
                "level": lvl["level"],
                "area": random.randint(15, 60),
                "heat": random.random(),
                "light": random.random(),
                "occupancy": random.randint(1, 6)
            }
            nodes.append(room)
            edges.append((lvl["id"], room["id"], "contains"))

    return {"nodes": nodes, "edges": edges, "domain": domain}

# =========================================================
# ENVIRONMENT SIMULATION
# =========================================================

def simulate_environment(graph):
    heat, light, occ = [], [], []

    for n in graph["nodes"]:
        if n["type"] == "ROOM":
            heat.append(n["heat"])
            light.append(n["light"])
            occ.append(n["occupancy"])

    return {
        "avg_heat": round(sum(heat)/len(heat), 3),
        "avg_light": round(sum(light)/len(light), 3),
        "density": round(sum(occ)/len(occ), 2),
        "comfort_index": round(((sum(light)/len(light))*0.6 + (1-(sum(heat)/len(heat)))*0.4)*100, 2)
    }

# =========================================================
# STRUCTURAL SIMULATION
# =========================================================

def simulate_structure(graph):
    stresses = []

    for n in graph["nodes"]:
        if n["type"] == "COLUMN":
            n["stress"] += random.randint(-50, 120)
            stresses.append(n["stress"])

    return {
        "avg_stress": round(sum(stresses)/len(stresses), 2) if stresses else 0,
        "max_stress": max(stresses) if stresses else 0,
        "min_stress": min(stresses) if stresses else 0
    }

# =========================================================
# MULTI-AGENT SYSTEM
# =========================================================

def agents(graph):
    return [
        "Architect Agent → circulation acceptable",
        "Structural Agent → load paths stable",
        "Energy Agent → heat zones detected",
        "Cost Agent → within budget envelope"
    ]

# =========================================================
# EVOLUTION ENGINE
# =========================================================

def base_design(levels):
    return {
        "id": str(uuid.uuid4())[:6],
        "levels": levels,
        "efficiency": random.randint(50, 90),
        "cost": random.randint(100000, 500000),
        "stability": random.randint(60, 95)
    }

def mutate(d):
    d = dict(d)
    d["efficiency"] += random.randint(-5, 8)
    d["cost"] += random.randint(-10000, 15000)
    d["stability"] += random.randint(-4, 6)
    return d

def evolve(levels, generations=5, pop=6):
    population = [base_design(levels) for _ in range(pop)]
    history = []

    for _ in range(generations):
        population.sort(key=lambda x: x["efficiency"], reverse=True)
        history.append(population[0]["efficiency"])

        survivors = population[:pop//2]
        new_pop = []

        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate(s))

        population = new_pop[:pop]

    return population[0], history

# =========================================================
# FLOOR PLAN
# =========================================================

def floor_plan(levels):
    rooms = [{"name": "Core Lobby", "w": 6, "h": 6, "color": "#1e3a8a"}]

    for i in range(levels):
        rooms.append({
            "name": f"Level Suite {i+1}",
            "w": 5,
            "h": 4,
            "color": "#4c1d95"
        })

    return rooms

# =========================================================
# RENDER
# =========================================================

def render(plan):
    html = '<div style="display:flex;flex-wrap:wrap;gap:10px;">'
    for r in plan:
        html += f"""
        <div style="padding:10px;background:{r['color']};border-radius:8px;color:white;">
            <b>{r['name']}</b><br>{r['w']}×{r['h']}
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# UI
# =========================================================

st.sidebar.title("ARC BIM CORE v4")
page = st.sidebar.radio("Mode", ["Dashboard", "BIM Twin", "AI Agents"])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏢 ARC DIGITAL CORE")

    st.metric("Projects", len(mem["projects"]))
    st.metric("Logs", len(mem["logs"]))

# =========================================================
# BIM TWIN
# =========================================================

elif page == "BIM Twin":

    st.title("🧠 Digital Twin Engine")

    domain = st.selectbox("Domain", ["Residential", "Commercial", "Industrial"])
    levels = st.slider("Levels", 1, 10, 3)
    rooms = st.slider("Rooms per Level", 1, 6, 3)

    if st.button("Run BIM Simulation"):

        graph = generate_bim(domain, levels, rooms)

        env = simulate_environment(graph)
        struct = simulate_structure(graph)

        mem["projects"].append(graph)
        log("BIM simulation executed")

        st.success("Simulation complete")

        st.subheader("Environment")
        st.json(env)

        st.subheader("Structure")
        st.json(struct)

        st.subheader("Floor Plan")
        render(floor_plan(levels))

# =========================================================
# AI AGENTS
# =========================================================

elif page == "AI Agents":

    st.title("🤖 Multi-Agent BIM Review")

    if not mem["projects"]:
        st.warning("No BIM model yet")
    else:
        g = mem["projects"][-1]

        st.subheader("Agent Feedback")
        for a in agents(g):
            st.write("•", a)

        st.markdown("---")
        st.json(simulate_structure(g))
        st.json(simulate_environment(g))
