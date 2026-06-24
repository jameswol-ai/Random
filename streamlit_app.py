# =========================================================
# RANDOM V4 FULL BUILD (FIXED + HARDENED)
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="RANDOM V4", layout="wide")

# =========================================================
# MEMORY SYSTEM
# =========================================================

MEMORY_FILE = Path("random_memory.json")

DEFAULT_MEMORY = {
    "projects": [],
    "designs": [],
    "cities": [],
    "knowledge": [],
    "engines": [],
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            data = json.loads(MEMORY_FILE.read_text())

            # ensure all keys exist (prevents crashes)
            for k in DEFAULT_MEMORY:
                if k not in data:
                    data[k] = []

            return data
        except Exception:
            return DEFAULT_MEMORY.copy()

    return DEFAULT_MEMORY.copy()

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))


memory = load_memory()

# =========================================================
# ARCHITECTURE BRAIN
# =========================================================

def generate_rooms(building_type, bedrooms):
    rooms = ["Living Room", "Dining Room", "Kitchen"]
    for i in range(bedrooms):
        rooms.append(f"Bedroom {i+1}")
    rooms += ["Bathroom", "Laundry"]
    return rooms

def generate_adjacency(rooms):
    return {
        r: ([rooms[i + 1]] if i < len(rooms) - 1 else [])
        for i, r in enumerate(rooms)
    }

def generate_grid():
    return {"x": ["A", "B", "C", "D"], "y": ["1", "2", "3", "4"]}

def generate_columns(grid):
    return [f"{x}{y}" for x in grid["x"] for y in grid["y"]]

def score_design():
    scores = {
        "circulation": random.randint(70, 100),
        "daylighting": random.randint(70, 100),
        "efficiency": random.randint(70, 100),
        "structure": random.randint(70, 100),
    }
    scores["overall"] = round(sum(scores.values()) / 4, 1)
    return scores

def plot_floorplan(rooms):
    fig, ax = plt.subplots(figsize=(6, 4))

    for i, room in enumerate(rooms[:8]):
        x = (i % 4) * 2
        y = (i // 4) * 2
        ax.add_patch(plt.Rectangle((x, y), 2, 2, fill=False))
        ax.text(x + 1, y + 1, room[:8], ha="center", va="center")

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)
    ax.set_aspect("equal")
    ax.axis("off")

    return fig

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

page = st.sidebar.selectbox(
    "Module",
    [
        "Dashboard",
        "Projects",
        "Design Studio",
        "Structural Studio",
        "City Simulator",
        "Knowledge Base",
        "Engine Builder",
    ],
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏗 RANDOM V4 CORE")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projects", len(memory["projects"]))
    c2.metric("Designs", len(memory["designs"]))
    c3.metric("Cities", len(memory["cities"]))
    c4.metric("Knowledge", len(memory["knowledge"]))

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":
    st.title("📁 Projects")

    name = st.text_input("Project Name")

    if st.button("Create Project") and name.strip():
        memory["projects"].append({
            "id": str(uuid.uuid4())[:8],
            "name": name.strip(),
            "created": datetime.now().isoformat()
        })
        save_memory(memory)
        st.success("Project created")

    st.json(memory["projects"])

# =========================================================
# DESIGN STUDIO
# =========================================================

elif page == "Design Studio":
    st.title("🏠 Design Studio")

    building = st.selectbox("Building Type", ["House", "School", "Office"])
    bedrooms = st.slider("Bedrooms", 1, 10, 3)

    if st.button("Generate Design"):
        rooms = generate_rooms(building, bedrooms)
        adjacency = generate_adjacency(rooms)
        grid = generate_grid()
        columns = generate_columns(grid)
        scores = score_design()

        design = {
            "building": building,
            "rooms": rooms,
            "adjacency": adjacency,
            "grid": grid,
            "columns": columns,
            "scores": scores,
            "created": datetime.now().isoformat()
        }

        memory["designs"].append(design)
        save_memory(memory)

        st.subheader("Room Program")
        st.write(rooms)

        st.subheader("Adjacency")
        st.json(adjacency)

        st.subheader("Structural Grid Columns")
        st.write(columns)

        st.subheader("Design Scores")
        st.json(scores)

        st.subheader("Floor Plan")
        st.pyplot(plot_floorplan(rooms))

# =========================================================
# STRUCTURAL STUDIO
# =========================================================

elif page == "Structural Studio":
    st.title("🏗 Structural Studio")

    span = st.number_input("Beam Span (m)", value=6.0)

    load = span * 5
    st.metric("Estimated Load Index", round(load, 2))

# =========================================================
# CITY SIMULATOR
# =========================================================

elif page == "City Simulator":
    st.title("🌆 City Simulator")

    if st.button("Generate City"):
        city = {
            "population": random.randint(1000, 100000),
            "districts": random.randint(1, 20),
            "roads": random.randint(20, 500),
            "schools": random.randint(1, 50),
            "created": datetime.now().isoformat()
        }
        memory["cities"].append(city)
        save_memory(memory)

    st.json(memory["cities"])

# =========================================================
# KNOWLEDGE BASE
# =========================================================

elif page == "Knowledge Base":
    st.title("📚 Knowledge Base")

    item = st.text_input("Knowledge Entry")

    if st.button("Save Knowledge") and item.strip():
        memory["knowledge"].append({
            "text": item.strip(),
            "created": datetime.now().isoformat()
        })
        save_memory(memory)

    st.json(memory["knowledge"])

# =========================================================
# ENGINE BUILDER
# =========================================================

elif page == "Engine Builder":
    st.title("⚙ Engine Builder")

    engine = st.text_input("Engine Name")

    if st.button("Create Engine") and engine.strip():
        memory["engines"].append({
            "name": engine.strip(),
            "created": datetime.now().isoformat()
        })
        save_memory(memory)

    st.json(memory["engines"])
