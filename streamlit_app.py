# =========================================================
# V31 — 3D WORLD KERNEL
# Procedural Spatial Simulation Engine (Voxel + Agent Layer)
# =========================================================

import streamlit as st
import numpy as np
import random
import math
from dataclasses import dataclass
from pathlib import Path

st.set_page_config(page_title="V31 World Kernel", layout="wide")

# =========================================================
# WORLD CONFIG
# =========================================================

WORLD_SIZE = 30  # 30x30x30 voxel world

EMPTY = 0
GROUND = 1
BUILDING = 2
WATER = 3
AGENT = 9

# =========================================================
# STATE
# =========================================================

if "world" not in st.session_state:
    st.session_state.world = np.zeros((WORLD_SIZE, WORLD_SIZE, WORLD_SIZE), dtype=np.int8)

if "agent" not in st.session_state:
    st.session_state.agent = [15, 15, 10]

# =========================================================
# WORLD GENERATION
# =========================================================

def generate_terrain():
    world = np.zeros((WORLD_SIZE, WORLD_SIZE, WORLD_SIZE), dtype=np.int8)

    # terrain height map
    for x in range(WORLD_SIZE):
        for y in range(WORLD_SIZE):
            height = int(
                6 * math.sin(x * 0.25) +
                6 * math.cos(y * 0.25) +
                random.randint(0, 3)
            )
            height = max(1, min(WORLD_SIZE - 1, height + 12))

            for z in range(height):
                world[x, y, z] = GROUND

    # water layer
    for x in range(WORLD_SIZE):
        for y in range(WORLD_SIZE):
            if random.random() < 0.08:
                world[x, y, 5:7] = WATER

    return world

# =========================================================
# BUILDINGS (PROCEDURAL CITIES)
# =========================================================

def spawn_buildings(world, count=40):
    for _ in range(count):
        x = random.randint(3, WORLD_SIZE - 3)
        y = random.randint(3, WORLD_SIZE - 3)
        h = random.randint(3, 10)

        for z in range(h):
            if world[x, y, z] == GROUND:
                world[x, y, z] = BUILDING

    return world

# =========================================================
# AGENT SYSTEM (WALKABLE ENTITY)
# =========================================================

def move_agent(world, dx, dy, dz):
    x, y, z = st.session_state.agent

    nx, ny, nz = x + dx, y + dy, z + dz

    if 0 <= nx < WORLD_SIZE and 0 <= ny < WORLD_SIZE and 0 <= nz < WORLD_SIZE:
        if world[nx, ny, nz] != BUILDING:
            st.session_state.agent = [nx, ny, max(0, nz)]

# =========================================================
# SIMPLE "PHYSICS" (GRAVITY)
# =========================================================

def apply_gravity(world):
    x, y, z = st.session_state.agent

    while z > 0 and world[x, y, z - 1] == EMPTY:
        z -= 1

    st.session_state.agent[2] = z

# =========================================================
# 3D → 2D PROJECTION (KERNEL RENDER)
# =========================================================

def project(world):
    view = []

    ax, ay, az = st.session_state.agent

    for x in range(WORLD_SIZE):
        for y in range(WORLD_SIZE):
            for z in range(WORLD_SIZE):
                if world[x, y, z] != EMPTY:
                    dx = x - ax
                    dy = y - ay
                    dz = z - az

                    # simple pseudo perspective
                    depth = max(1, dz + 15)
                    px = int(200 + dx * (300 / depth))
                    py = int(200 + dy * (300 / depth))

                    view.append((px, py, world[x, y, z]))

    return view

# =========================================================
# UI CONTROLS
# =========================================================

st.sidebar.title("🧠 V31 World Kernel")

if st.sidebar.button("🌍 Generate World"):
    st.session_state.world = generate_terrain()
    st.session_state.world = spawn_buildings(st.session_state.world)

if st.sidebar.button("⬆ Move Forward"):
    move_agent(st.session_state.world, 0, 1, 0)

if st.sidebar.button("⬇ Move Back"):
    move_agent(st.session_state.world, 0, -1, 0)

if st.sidebar.button("⬅ Left"):
    move_agent(st.session_state.world, -1, 0, 0)

if st.sidebar.button("➡ Right"):
    move_agent(st.session_state.world, 1, 0, 0)

if st.sidebar.button("⬆ Jump"):
    move_agent(st.session_state.world, 0, 0, 3)

# =========================================================
# ENGINE LOOP
# =========================================================

apply_gravity(st.session_state.world)
render = project(st.session_state.world)

# =========================================================
# MAIN VIEW
# =========================================================

st.title("🌐 V31 — 3D WORLD KERNEL")

x, y, z = st.session_state.agent
st.markdown(f"### Agent Position: `{x}, {y}, {z}`")

# fake 3D visualization
canvas = ""

for px, py, t in render[:800]:
    if t == BUILDING:
        color = "🟥"
    elif t == WATER:
        color = "🟦"
    else:
        color = "🟩"

    canvas += color

st.markdown("### World Slice Render")
st.text(canvas[:3000])

# =========================================================
# WORLD INTROSPECTION
# =========================================================

st.markdown("### 🧠 Kernel Diagnostics")

st.json({
    "world_size": WORLD_SIZE,
    "agent": st.session_state.agent,
    "voxels": int(np.count_nonzero(st.session_state.world)),
    "buildings": int(np.sum(st.session_state.world == BUILDING)),
    "water": int(np.sum(st.session_state.world == WATER))
})