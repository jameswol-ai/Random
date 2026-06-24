# =========================================================
# 🧠 RANDOM V4.1 — SELF-EXPANDING ARCHITECTURE ENGINE
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="RANDOM V4.1", layout="wide")

# =========================================================
# MEMORY CORE
# =========================================================

MEMORY_FILE = Path("random_memory.json")

DEFAULT_MEMORY = {
    "projects": [],
    "designs": [],
    "cities": [],
    "knowledge": [],
    "engines": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            data = json.loads(MEMORY_FILE.read_text())
            for k in DEFAULT_MEMORY:
                if k not in data:
                    data[k] = []
            return data
        except:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

memory = load_memory()

# =========================================================
# ENGINE REGISTRY (SELF-EXPANDING CORE)
# =========================================================

def register_engine(name, desc, ui_type):
    memory["engines"].append({
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "desc": desc,
        "ui": ui_type,
        "created": datetime.now().isoformat()
    })
    save_memory(memory)

def get_engine_names():
    return [e["name"] for e in memory["engines"]]

# =========================================================
# ARCHITECTURE GENERATORS
# =========================================================

def generate_rooms(bedrooms):
    base = ["Living", "Kitchen", "Dining"]
    return base + [f"Bedroom {i+1}" for i in range(bedrooms)] + ["Bath"]

def score_design():
    scores = {k: random.randint(70, 100) for k in
              ["circulation", "light", "efficiency", "structure"]}
    scores["overall"] = round(sum(scores.values()) / 4, 1)
    return scores

def plot_rooms(rooms):
    fig, ax = plt.subplots()
    for i, r in enumerate(rooms[:8]):
        ax.add_patch(plt.Rectangle((i % 4, i // 4), 1, 1, fill=False))
        ax.text(i % 4 + 0.5, i // 4 + 0.5, r[:6], ha="center")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2)
    ax.axis("off")
    return fig

# =========================================================
# SIDEBAR (DYNAMIC EXPANSION)
# =========================================================

base_pages = [
    "Dashboard",
    "Projects",
    "Design Studio",
    "City Simulator",
    "Knowledge Base",
    "Engine Builder"
]

dynamic_pages = base_pages + get_engine_names()

page = st.sidebar.selectbox("RANDOM CORE", dynamic_pages)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🧠 RANDOM V4.1 CORE")

    cols = st.columns(4)
    cols[0].metric("Projects", len(memory["projects"]))
    cols[1].metric("Designs", len(memory["designs"]))
    cols[2].metric("Cities", len(memory["cities"]))
    cols[3].metric("Engines", len(memory["engines"]))

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":
    st.title("📁 Projects")

    name = st.text_input("Project Name")

    if st.button("Create") and name.strip():
        memory["projects"].append({
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "created": datetime.now().isoformat()
        })
        save_memory(memory)
        st.success("Project created")

    st.json(memory["projects"])

# =========================================================
# DESIGN STUDIO
# =========================================================

elif page == "Design Studio":
    st.title("🏗 Design Studio")

    bedrooms = st.slider("Bedrooms", 1, 10, 3)

    if st.button("Generate Design"):
        rooms = generate_rooms(bedrooms)
        design = {
            "rooms": rooms,
            "scores": score_design(),
            "created": datetime.now().isoformat()
        }

        memory["designs"].append(design)
        save_memory(memory)

        st.subheader("Rooms")
        st.write(rooms)

        st.subheader("Score")
        st.json(design["scores"])

        st.subheader("Plan")
        st.pyplot(plot_rooms(rooms))

# =========================================================
# CITY SIMULATOR
# =========================================================

elif page == "City Simulator":
    st.title("🌆 City Evolution Simulator")

    if st.button("Generate City"):
        city = {
            "population": random.randint(5000, 200000),
            "districts": random.randint(2, 25),
            "infrastructure": random.randint(10, 100),
            "created": datetime.now().isoformat()
        }
        memory["cities"].append(city)
        save_memory(memory)

    st.json(memory["cities"])

# =========================================================
# KNOWLEDGE BASE
# =========================================================

elif page == "Knowledge Base":
    st.title("📚 Knowledge Core")

    text = st.text_input("Add Knowledge")

    if st.button("Save") and text.strip():
        memory["knowledge"].append({
            "text": text,
            "created": datetime.now().isoformat()
        })
        save_memory(memory)

    st.json(memory["knowledge"])

# =========================================================
# ENGINE BUILDER (THE MAGIC LAYER)
# =========================================================

elif page == "Engine Builder":
    st.title("⚙ Engine Builder")

    name = st.text_input("Engine Name")
    desc = st.text_area("Engine Description")

    ui_type = st.selectbox("Engine Type", ["Dashboard Panel", "Simulation Node", "Analyzer"])

    if st.button("Forge Engine") and name.strip():
        register_engine(name, desc, ui_type)
        st.success("Engine created — it now exists in the system")

    st.subheader("Active Engines")
    st.json(memory["engines"])

# =========================================================
# DYNAMIC ENGINE RENDERING
# =========================================================

elif page in get_engine_names():
    st.title(f"🧬 Engine: {page}")

    engine = next((e for e in memory["engines"] if e["name"] == page), None)

    if engine:
        st.write("Description:", engine["desc"])
        st.write("Type:", engine["ui"])

        st.info("This engine is a placeholder node. Future versions will allow live execution logic per engine.")
