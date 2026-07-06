# =============================
# ARC STUDIO ENGINE v14
# AI ARCHITECT COPILOT EDITION
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
    page_title="Arc Studio AI Copilot v14",
    page_icon="🧠🏗️",
    layout="wide"
)

# =========================================================
# MEMORY
# =========================================================

MEM_FILE = Path("arc_copilot_memory.json")

DEFAULT = {"models": [], "chat": []}

def load():
    if MEM_FILE.exists():
        return json.load(open(MEM_FILE))
    return DEFAULT.copy()

def save(mem):
    json.dump(mem, open(MEM_FILE, "w"), indent=2)

if "mem" not in st.session_state:
    st.session_state.mem = load()

if "active" not in st.session_state:
    st.session_state.active = None

if "chat" not in st.session_state:
    st.session_state.chat = []

mem = st.session_state.mem

# =========================================================
# COPILOT UI
# =========================================================

st.title("🧠 Arc Studio AI Copilot v14")

st.markdown("### Speak your building into existence")

user_prompt = st.text_area(
    "Describe your building",
    placeholder="e.g. Design a 10-floor commercial tower with 2000 people capacity and low cost HVAC"
)

# =========================================================
# SIMPLE NLP → STRUCTURE PARSER (COPILOT BRAIN)
# =========================================================

def interpret(text):

    text = text.lower()

    floors = 10
    rooms = 5
    btype = "Commercial"
    intent = []

    if "hospital" in text:
        btype = "Residential"
        rooms = 8

    if "industrial" in text:
        btype = "Industrial"

    if "small" in text:
        floors = 3

    if "tall" in text or "tower" in text:
        floors = 20

    if "cheap" in text or "low cost" in text:
        intent.append("cost_optimize")

    if "green" in text or "sustainable" in text:
        intent.append("sustainability")

    if "large" in text or "capacity" in text:
        rooms = 10

    return btype, floors, rooms, intent

# =========================================================
# BIM GENERATION
# =========================================================

def generate(btype, floors, rooms):
    return {
        "id": str(uuid.uuid4())[:8],
        "type": btype,
        "floors": [
            {
                "level": f,
                "spaces": [
                    {
                        "name": f"Room_{f}_{r}",
                        "area": random.randint(25, 80)
                    }
                    for r in range(rooms)
                ]
            }
            for f in range(floors)
        ]
    }

# =========================================================
# AI ANALYSIS ENGINE
# =========================================================

def analyze(model, intent):

    area = sum(s["area"] for f in model["floors"] for s in f["spaces"])

    issues = []
    suggestions = []

    if "cost_optimize" in intent and area > 3000:
        issues.append("High cost risk detected")
        suggestions.append("Reduce floor count or optimize materials")

    if "sustainability" in intent:
        suggestions.append("Introduce passive cooling + natural ventilation zones")

    if area < 1500:
        issues.append("Low capacity design")

    return issues, suggestions

# =========================================================
# BOQ + MEP
# =========================================================

def boq(model):
    area = sum(s["area"] for f in model["floors"] for s in f["spaces"])
    return {
        "Concrete": area * 0.35 * 130,
        "Steel": area * 0.08 * 950,
        "Finishes": area * 120
    }

def mep(model):
    area = sum(s["area"] for f in model["floors"] for s in f["spaces"])
    return {
        "Power (kW)": area * 0.1,
        "Water (L/day)": area * 18,
        "Cooling (kW)": area * 0.08
    }

# =========================================================
# VISUALIZATION
# =========================================================

def render_2d(model):
    fig = go.Figure()
    y = 0

    for f in model["floors"]:
        x = 0
        for s in f["spaces"]:
            size = s["area"] ** 0.5

            fig.add_shape(
                type="rect",
                x0=x, y0=y,
                x1=x+size, y1=y+size,
                fillcolor="rgba(99,102,241,0.4)",
                line=dict(color="white")
            )

            x += size + 1
        y += 8

    fig.update_layout(height=450, paper_bgcolor="#0b1220")
    st.plotly_chart(fig, use_container_width=True)

def render_3d(model):
    fig = go.Figure()

    for f in model["floors"]:
        z = f["level"] * 3
        fig.add_trace(go.Mesh3d(
            x=[0,10,10,0],
            y=[0,0,10,10],
            z=[z,z,z,z],
            opacity=0.4
        ))

    fig.update_layout(scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False)
    ))

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# CHAT MEMORY
# =========================================================

def add_chat(role, msg):
    st.session_state.chat.append({"role": role, "msg": msg})

# =========================================================
# UI LAYOUT
# =========================================================

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("## 💬 Copilot Input")

    if st.button("🧠 Generate from Prompt"):

        btype, floors, rooms, intent = interpret(user_prompt)

        model = generate(btype, floors, rooms)

        issues, suggestions = analyze(model, intent)

        st.session_state.active = {
            "model": model,
            "intent": intent,
            "issues": issues,
            "suggestions": suggestions
        }

        mem["models"].append(model)
        save(mem)

        add_chat("user", user_prompt)
        add_chat("ai", f"Generated {btype} building with {floors} floors")

with col2:
    st.markdown("## 🧠 AI Response")

    if st.session_state.active:
        active = st.session_state.active

        st.markdown("### ⚠ Issues")
        for i in active["issues"]:
            st.error(i)

        st.markdown("### 💡 Suggestions")
        for s in active["suggestions"]:
            st.info(s)

# =========================================================
# VISUALS
# =========================================================

if st.session_state.active:

    model = st.session_state.active["model"]

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🗺 2D Plan", "🏢 3D Model", "📊 Analytics"])

    with tab1:
        render_2d(model)

    with tab2:
        render_3d(model)

    with tab3:
        st.json(boq(model))
        st.json(mep(model))

# =========================================================
# CHAT HISTORY
# =========================================================

st.markdown("---")
st.markdown("## 💬 Copilot Memory")

for c in st.session_state.chat[-6:]:
    if c["role"] == "user":
        st.markdown(f"🧑‍💻 **You:** {c['msg']}")
    else:
        st.markdown(f"🧠 **Copilot:** {c['msg']}")
