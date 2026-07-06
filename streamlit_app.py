# =============================
# ARC STUDIO ENGINE v12
# Unified AI + AEC + BIM-like System
# =============================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Arc Studio Engine v12",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# MEMORY
# =========================================================

DEFAULT = {"projects": [], "designs": [], "logs": [], "evolution": []}

def load():
    if MEMORY_FILE.exists():
        return json.load(open(MEMORY_FILE, "r"))
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

if "active" not in st.session_state:
    st.session_state.active = None

if "history" not in st.session_state:
    st.session_state.history = []

mem = st.session_state.mem

# =========================================================
# SIDEBAR CONFIG
# =========================================================

st.sidebar.title("📐 Arc Studio")

page = st.sidebar.radio("Navigation", ["Dashboard", "Design", "Memory"])

typology = st.sidebar.selectbox("Building Type", ["Residential", "Commercial", "Industrial"])
floors = st.sidebar.slider("Floors", 1, 60, 8)
rooms_pf = st.sidebar.slider("Rooms / Floor", 1, 15, 5)
population = st.sidebar.slider("Occupancy", 0, 5000, 300)

pop_size = st.sidebar.slider("Population Size", 10, 120, 30)
gens = st.sidebar.slider("Epochs", 2, 25, 8)

# =========================================================
# AEC ENGINE
# =========================================================

def generate():
    total_rooms = floors * rooms_pf

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": typology,
        "floors": floors,
        "rooms_pf": rooms_pf,
        "rooms": [f"Room {i+1}" for i in range(total_rooms)],
        "area": 80 + total_rooms * 14,
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(24, 80)
        }
    }

def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-3, 5)
    if random.random() > 0.6:
        d["rooms"].append("Expansion Node")
        d["area"] += 15
    return d

def fitness(d):
    ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    structural = max(0, 100 - abs(ratio - 2.0) * 20)

    cost = d["area"] * 1600
    cost_score = max(0, 100 - cost / 100000)

    complexity = min(100, len(d["rooms"]) * 2)

    return {
        "structural": structural,
        "cost": cost_score,
        "complexity": complexity
    }

def score(f):
    return sum(f.values()) / 3

def evolve():
    pop = [generate() for _ in range(pop_size)]
    hist = []

    for _ in range(gens):
        scored = []
        for d in pop:
            f = fitness(d)
            d["score"] = score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        hist.append(scored[0]["score"])

        survivors = scored[:max(2, len(scored)//2)]
        new = []

        for s in survivors:
            new.append(s)
            new.append(mutate(s))

        pop = new[:pop_size]

    return scored[0], hist

# =========================================================
# 2D FLOOR PLAN
# =========================================================

def plan2d(d):
    rooms = []
    x = y = 0

    for i, r in enumerate(d["rooms"][:d["rooms_pf"] * 2]):
        w = 4 + (i % 3)
        h = 4

        rooms.append({"name": r, "x": x, "y": y, "w": w, "h": h})

        x += w + 1
        if x > 18:
            x = 0
            y += 5

    return rooms

def render2d(plan):
    fig = go.Figure()

    for r in plan:
        fig.add_shape(
            type="rect",
            x0=r["x"], y0=r["y"],
            x1=r["x"] + r["w"],
            y1=r["y"] + r["h"],
            line=dict(color="white"),
            fillcolor="rgba(80,120,255,0.4)"
        )

        fig.add_annotation(
            x=r["x"] + r["w"]/2,
            y=r["y"] + r["h"]/2,
            text=r["name"],
            showarrow=False,
            font=dict(size=10)
        )

    fig.update_layout(height=500, paper_bgcolor="#0b1220")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 3D MODEL
# =========================================================

def render3d(d):
    fig = go.Figure()

    for f in range(d["floors"]):
        z = f * 3

        fig.add_trace(go.Mesh3d(
            x=[0,10,10,0],
            y=[0,0,10,10],
            z=[z,z,z,z],
            opacity=0.5
        ))

        for i in range(4):
            fig.add_trace(go.Scatter3d(
                x=[(i%2)*10, (i%2)*10],
                y=[(i//2)*10, (i//2)*10],
                z=[z, z+3],
                mode="lines"
            ))

    fig.update_layout(scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False)
    ))

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# MEP + COST + AI
# =========================================================

def boq(d):
    area = d["area"]
    return {
        "Concrete": area * 0.35 * 130,
        "Steel": area * 0.08 * 950,
        "Finishes": area * 120
    }

def mep(d):
    return {
        "Power": d["area"] * 0.12,
        "Water": d["area"] * 18,
        "Cooling": d["area"] * 0.09
    }

def ai_review(d):
    issues = []
    if d["structure"]["beams"] < d["structure"]["columns"] * 1.5:
        issues.append("Weak structural ratio")

    return {
        "issues": issues if issues else ["OK"],
        "suggestion": "Optimize beam-column ratio"
    }

# =========================================================
# UI
# =========================================================

st.title("📐 Arc Studio Engine v12")

if page == "Dashboard":
    st.metric("Projects", len(mem["projects"]))
    st.metric("Designs", len(mem["designs"]))

    if st.button("Run Evolution"):
        best, hist = evolve()
        st.session_state.active = best
        st.session_state.history = hist
        mem["designs"].append(best)
        save()
        log("Evolution run complete")

    if st.session_state.active:
        d = st.session_state.active

        st.subheader(f"Design {d['id']}")
        st.metric("Score", d["score"])

        tab1, tab2, tab3 = st.tabs(["2D", "3D", "Analytics"])

        with tab1:
            render2d(plan2d(d))

        with tab2:
            render3d(d)

        with tab3:
            st.line_chart(st.session_state.history)
            st.json(boq(d))
            st.json(mep(d))
            st.json(ai_review(d))

elif page == "Design":
    st.json(st.session_state.active)

elif page == "Memory":
    st.json(mem)

    if st.button("Reset"):
        st.session_state.mem = DEFAULT.copy()
        save()
        st.rerun()
