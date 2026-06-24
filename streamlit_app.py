# =========================================================
# RANDOM V3 - Autonomous Architecture & Civilization OS
# Single-File Streamlit Edition
# =========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random, json
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="RANDOM V3", page_icon="🏗️", layout="wide")

MEMORY_FILE = Path("random_memory.json")

DEFAULT_MEMORY = {
    "projects": [],
    "cities": [],
    "history": []
}

def load_memory():
    try:
        if MEMORY_FILE.exists():
            data = json.loads(MEMORY_FILE.read_text())
            if isinstance(data, dict):
                data.setdefault("projects", [])
                data.setdefault("cities", [])
                data.setdefault("history", [])
                return data
    except Exception:
        pass
    return DEFAULT_MEMORY.copy()

def save_memory(data):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))

memory = load_memory()

ENGINES = {
    "Architecture AI":"ACTIVE",
    "Structural AI":"ACTIVE",
    "Eurocode Engine":"ACTIVE",
    "Civilization Engine":"ACTIVE",
    "Building Generator":"ACTIVE",
    "Memory Core":"ACTIVE"
}

AGENTS = {
    "Architect":"ACTIVE",
    "Structural Engineer":"ACTIVE",
    "Urban Planner":"ACTIVE",
    "Research Agent":"ACTIVE"
}

def generate_building(building_type):
    templates = {
        "Residential House": {"floors": random.randint(1,3),
                              "rooms":["Living","Kitchen","Dining","Bedrooms","Bathrooms"]},
        "Apartment": {"floors": random.randint(3,12),
                      "rooms":["Units","Lobby","Stairs","Lift Core"]},
        "Office": {"floors": random.randint(2,20),
                   "rooms":["Open Office","Meeting Rooms","Reception"]},
        "School": {"floors": random.randint(1,5),
                   "rooms":["Classrooms","Labs","Offices"]},
        "Hospital": {"floors": random.randint(2,10),
                     "rooms":["Wards","Theatre","Labs"]},
        "Hotel": {"floors": random.randint(2,15),
                  "rooms":["Rooms","Lobby","Restaurant"]},
    }
    return templates.get(building_type, templates["Residential House"])

def estimate_column_size(floors):
    if floors <= 2: return "250x250 mm"
    if floors <= 5: return "300x300 mm"
    if floors <= 10: return "400x400 mm"
    return "500x500 mm"

def estimate_beam_depth(span):
    return round(span * 1000 / 15)

def eurocode_check(span):
    if span <= 8: return "PASS"
    if span <= 12: return "WARNING"
    return "FAIL"

def evolve_city():
    return {
        "population": random.randint(1000,1000000),
        "economy": random.randint(1,100),
        "infrastructure": random.randint(1,100),
        "happiness": random.randint(1,100),
    }

def draw_floorplan():
    fig, ax = plt.subplots(figsize=(6,4))
    rooms = [
        (0,2,6,2,"Living"),
        (0,0,3,2,"Bedroom"),
        (3,0,3,2,"Bedroom"),
        (6,0,2,2,"Bath"),
        (6,2,2,2,"Kitchen"),
    ]
    for x,y,w,h,label in rooms:
        ax.add_patch(Rectangle((x,y),w,h,fill=False))
        ax.text(x+w/2,y+h/2,label,ha="center")
    ax.set_xlim(0,8); ax.set_ylim(0,4); ax.set_aspect("equal")
    return fig

st.sidebar.title("RANDOM V3")
page = st.sidebar.radio("Navigate",[
    "Dashboard","Architecture AI","Building Generator",
    "Structural AI","Eurocode","Civilization",
    "Projects","Memory","System Health"
])

if page == "Dashboard":
    st.title("🏗️ RANDOM V3")
    c1,c2,c3 = st.columns(3)
    c1.metric("Engines", len(ENGINES))
    c2.metric("Projects", len(memory["projects"]))
    c3.metric("Cities", len(memory["cities"]))
    st.subheader("Agents")
    st.json(AGENTS)

elif page == "Architecture AI":
    st.header("2D Floor Plan Generator")
    st.pyplot(draw_floorplan())

elif page == "Building Generator":
    st.header("Autonomous Building Generator")
    btype = st.selectbox("Building Type",
        ["Residential House","Apartment","Office","School","Hospital","Hotel"])
    pname = st.text_input("Project Name","Project Alpha")

    if st.button("Generate Building"):
        building = generate_building(btype)
        project = {
            "name": pname,
            "building": building,
            "created": str(datetime.now())
        }
        memory["projects"].append(project)
        save_memory(memory)

        st.json(building)
        st.success("Project saved")

elif page == "Structural AI":
    st.header("Structural AI")
    floors = st.number_input("Floors",1,50,3)
    span = st.number_input("Span (m)",1.0,30.0,6.0)

    st.write("Column Size:", estimate_column_size(floors))
    st.write("Beam Depth:", f"{estimate_beam_depth(span)} mm")

elif page == "Eurocode":
    st.header("Eurocode Preliminary Check")
    span = st.number_input("Check Span (m)",1.0,30.0,6.0,key="ec")
    st.write("Result:", eurocode_check(span))

elif page == "Civilization":
    st.header("City Evolution")
    if st.button("Evolve City"):
        city = evolve_city()
        memory["cities"].append(city)
        save_memory(memory)
        st.json(city)

elif page == "Projects":
    st.header("Projects")
    st.json(memory["projects"])

elif page == "Memory":
    st.header("Memory Core")
    st.json(memory)
    if st.button("Reset Memory"):
        memory = DEFAULT_MEMORY.copy()
        save_memory(memory)

elif page == "System Health":
    st.header("Diagnostics")
    st.write("Memory file exists:", MEMORY_FILE.exists())
    st.write("Projects:", len(memory["projects"]))
    st.write("Cities:", len(memory["cities"]))
