# =========================================================
# ARC V42 ARCHITECTURE INTELLIGENCE OS
# Multi-Agent Structural + Cost + Spatial Engine
# Stable Streamlit Deployment Build
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
    page_title="ARC V42 OS",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# SAFE MEMORY SYSTEM (CRASH-PROOF)
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": []
}

def safe_load():
    if not MEMORY_FILE.exists():
        return DEFAULT_STATE.copy()
    try:
        data = json.loads(MEMORY_FILE.read_text())
        if not isinstance(data, dict):
            return DEFAULT_STATE.copy()
        return {**DEFAULT_STATE, **data}
    except:
        return DEFAULT_STATE.copy()

def safe_save():
    try:
        MEMORY_FILE.write_text(json.dumps(st.session_state.mem, indent=2))
    except:
        pass

def log(msg):
    st.session_state.mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    safe_save()

# init
if "mem" not in st.session_state:
    st.session_state.mem = safe_load()

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.mem

# =========================================================
# EAST AFRICAN COST ENGINE (BASE RATES)
# =========================================================

COST_RATES = {
    "Residential": 1400,
    "Commercial": 1800,
    "Industrial": 2200
}

MATERIAL_RATES = {
    "cement_m3": 130,
    "steel_ton": 1200,
    "block_unit": 0.65,
    "excavation_m3": 8
}

# =========================================================
# DOMAIN ENGINE
# =========================================================

ARCH = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}

def domain_of(t):
    for k, v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

# =========================================================
# DESIGN GENERATION ENGINE
# =========================================================

def generate_design(t, floors, rooms):
    base_area = 60 + (rooms * 18) + (floors * 35)

    return {
        "id": str(uuid.uuid4())[:8],
        "type": t,
        "domain": domain_of(t),
        "floors": floors,
        "rooms": rooms,
        "area": base_area,
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(25, 80)
        },
        "doors": rooms + random.randint(2, 6),
        "windows": rooms * 2 + random.randint(4, 12)
    }

def mutate(d):
    d = json.loads(json.dumps(d))

    d["structure"]["columns"] = max(10, d["structure"]["columns"] + random.randint(-2, 3))
    d["structure"]["beams"] = max(15, d["structure"]["beams"] + random.randint(-3, 5))

    if random.random() > 0.6:
        d["area"] += 15
        d["rooms"] += 1

    d["doors"] = d["rooms"] + random.randint(2, 6)
    d["windows"] = d["rooms"] * 2 + random.randint(4, 12)

    base = COST_RATES.get(d["domain"], 1500)
    d["cost"] = int(d["area"] * base)

    return d

# =========================================================
# MULTI-AGENT SYSTEM
# =========================================================

def architect_agent(d):
    return {
        "score": min(100, d["rooms"] * 8 + d["floors"] * 5),
        "note": "Spatial efficiency evaluated"
    }

def structural_agent(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    score = max(0, 100 - abs(ratio - 2.0) * 25)
    return {
        "score": int(score),
        "note": "Load path stability checked"
    }

def cost_agent(d):
    unit = d["cost"] / max(1, d["area"])
    score = max(0, 100 - abs(unit - 1600) * 0.05)
    return {
        "score": int(score),
        "note": "Cost benchmark evaluated"
    }

def mep_agent(d):
    score = max(50, 100 - abs(d["windows"] - d["doors"]) * 2)
    return {
        "score": int(score),
        "note": "MEP balance estimated"
    }

def run_agents(d):
    results = {
        "architect": architect_agent(d),
        "structural": structural_agent(d),
        "cost": cost_agent(d),
        "mep": mep_agent(d)
    }

    avg = sum(r["score"] for r in results.values()) // len(results)
    return results, avg

# =========================================================
# BOQ ENGINE (FIXED SAFE VERSION)
# =========================================================

def boq(d):
    return [
        ("Concrete (m³)", round(d["structure"]["columns"] * 2.4, 2)),
        ("Steel (tons)", round(d["structure"]["beams"] * 0.5, 2)),
        ("Blocks (units)", d["area"] * 40),
        ("Excavation (m³)", d["area"] * 0.8),
        ("Doors (units)", d["doors"]),
        ("Windows (units)", d["windows"]),
    ]

# =========================================================
# FLOOR PLAN (2D SIMULATION)
# =========================================================

def floor_plan(d):
    base = [
        {"name": "Living", "w": 6, "h": 5, "c": "#1f2937"},
        {"name": "Kitchen", "w": 4, "h": 4, "c": "#065f46"},
        {"name": "Bath", "w": 3, "h": 3, "c": "#7c2d12"},
    ]

    for i in range(d["rooms"]):
        base.append({
            "name": f"Room {i+1}",
            "w": 4,
            "h": 4,
            "c": "#312e81"
        })

    return base

def render(plan):
    html = "<div style='display:flex;flex-wrap:wrap;gap:10px;'>"
    for r in plan:
        html += f"""
        <div style='background:{r["c"]};padding:12px;border-radius:10px;color:white;width:160px'>
            <b>{r["name"]}</b><br>
            {r["w"]}m × {r["h"]}m
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# EVOLUTION ENGINE
# =========================================================

def evolve(t, floors, rooms, gens):
    pop = [generate_design(t, floors, rooms) for _ in range(8)]
    best = None

    for _ in range(gens):
        scored = []
        for d in pop:
            agents, score = run_agents(d)
            d["score"] = score
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        best = scored[0]

        pop = [mutate(best), mutate(scored[1])]

    return best

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏗️ ARC V42 OS")

mode = st.sidebar.radio("Mode", ["Dashboard", "Design Lab", "Memory"])

t = st.sidebar.selectbox("Building Type", sum(ARCH.values(), []))
floors = st.sidebar.slider("Floors", 1, 5, 1)
rooms = st.sidebar.slider("Rooms", 1, 12, 4)
gens = st.sidebar.slider("Generations", 2, 10, 5)

# =========================================================
# DASHBOARD
# =========================================================

if mode == "Dashboard":
    st.title("🏗️ ARC Intelligence Dashboard")

    st.metric("Designs", len(mem["designs"]))
    st.metric("Evolution Runs", len(mem["evolution"]))

    st.subheader("Logs")
    for l in mem["logs"][-5:]:
        st.write(l["time"], ":", l["msg"])

# =========================================================
# DESIGN LAB
# =========================================================

elif mode == "Design Lab":
    st.title("🧠 Multi-Agent Architecture Engine")

    if st.button("Run Full Simulation"):
        best = evolve(t, floors, rooms, gens)
        best["plan"] = floor_plan(best)
        best["boq"] = boq(best)

        agents, score = run_agents(best)
        best["agents"] = agents
        best["score"] = score

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "score": score,
            "time": datetime.now().isoformat()
        })

        st.session_state.active = best
        log(f"Generated {best['id']}")

    if st.session_state.active:
        d = st.session_state.active

        st.subheader(f"Design {d['id']}")
        st.metric("AI Score", d["score"])

        tab1, tab2, tab3 = st.tabs(["Plan", "Agents", "BOQ"])

        with tab1:
            render(d["plan"])

        with tab2:
            for k, v in d["agents"].items():
                st.write(k, v)

        with tab3:
            st.table(d["boq"])

# =========================================================
# MEMORY
# =========================================================

elif mode == "Memory":
    st.title("🧠 System Memory")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.mem = DEFAULT_STATE.copy()
        st.session_state.active = None
        safe_save()
        st.rerun()