import streamlit as st
import json
import uuid
import random
import hashlib
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np
import math
import base64
import struct

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="RANDOM V4 Evolution Studio",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "random_users.json"
FONT = ImageFont.load_default()
XP_PER_LEVEL = 100

# ============================================================
# DARK PROFESSIONAL THEME CSS
# ============================================================
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, .stApp {
    background: #0f1117;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

h1, h2, h3, h4, h5, .stTitle, .stHeader {
    font-weight: 600;
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #16181d;
    border-right: 1px solid #1e293b;
}

.glass-card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #334155;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 1.5rem;
}

.banner {
    background: linear-gradient(135deg, #1a2a3a, #0f172a);
    padding: 2rem 2.5rem;
    border-radius: 24px;
    color: white;
    margin-bottom: 2rem;
    border: 1px solid #334155;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}

.metric-box {
    background: rgba(30,41,59,0.8);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    border-left: 4px solid #22c55e;
}

.concept-item {
    background: rgba(30,41,59,0.4);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1e293b;
}

.concept-score {
    background: rgba(34,197,94,0.15);
    padding: 0.25rem 1rem;
    border-radius: 20px;
    font-weight: 700;
    color: #4ade80;
}

.agent-box {
    background: rgba(30,41,59,0.5);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #334155;
}

.agent-name {
    font-weight: 600;
    color: #94a3b8;
    font-size: 0.85rem;
}

.agent-score {
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
}

.agent-sub {
    font-size: 0.7rem;
    color: #64748b;
}

.stButton > button {
    background: #22c55e;
    color: #0f172a;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: #16a34a;
    color: white;
    box-shadow: 0 8px 20px rgba(34,197,94,0.3);
}

.xp-container { display: flex; align-items: center; gap: 10px; margin-bottom: 1rem; }
.xp-bar-bg { flex: 1; height: 8px; background: #1e293b; border-radius: 4px; overflow: hidden; }
.xp-bar-fill { height: 100%; background: #22c55e; border-radius: 4px; }

.footer {
    text-align: center;
    padding: 1.5rem 0;
    color: #64748b;
    font-size: 0.8rem;
    border-top: 1px solid #1e293b;
}
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# ============================================================
# AUTH HELPERS
# ============================================================
def hash_password(password: str) -> str:
    return hashlib.sha256((password + "random_salt_42").encode()).hexdigest()

def load_users() -> list:
    if USER_FILE.exists():
        try:
            with open(USER_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_users(users: list):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user(username: str) -> dict | None:
    for u in load_users():
        if u["username"] == username:
            return u
    return None

def create_user(username: str, password: str, role: str = "user") -> dict:
    users = load_users()
    if get_user(username):
        raise ValueError("Username already exists.")
    user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "level": 1,
        "xp": 0,
        "badges": [],
        "created": datetime.now().isoformat()
    }
    users.append(user)
    save_users(users)
    return user

def authenticate(username: str, password: str) -> dict | None:
    user = get_user(username)
    if user and user["password_hash"] == hash_password(password):
        return user
    return None

def update_user_data(username: str, updates: dict):
    users = load_users()
    for u in users:
        if u["username"] == username:
            u.update(updates)
            break
    save_users(users)

def xp_for_level(level: int) -> int:
    return level * XP_PER_LEVEL

def add_xp(username: str, amount: int) -> bool:
    user = get_user(username)
    if not user:
        return False
    old_level = user["level"]
    user["xp"] += amount
    while user["xp"] >= xp_for_level(user["level"]):
        user["xp"] -= xp_for_level(user["level"])
        user["level"] += 1
        badge = f"level_{user['level']}"
        if user["level"] % 5 == 0 and badge not in user["badges"]:
            user["badges"].append(badge)
    update_user_data(username, {"level": user["level"], "xp": user["xp"], "badges": user["badges"]})
    return user["level"] > old_level

# ============================================================
# PER‑USER MEMORY
# ============================================================
def get_memory_path(username: str) -> Path:
    return DATA_DIR / f"{username}_random_memory.json"

DEFAULT_MEMORY = {
    "version": "V4 Evolution Studio",
    "projects": [],
    "saved_designs": [],
    "logs": []
}

def load_memory(username: str) -> dict:
    path = get_memory_path(username)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in DEFAULT_MEMORY:
                if key not in data:
                    data[key] = DEFAULT_MEMORY[key]
            return data
        except Exception:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(username: str, memory: dict):
    with open(get_memory_path(username), "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

# ============================================================
# ARCHITECTURAL KNOWLEDGE BASE
# ============================================================
ARCHITECTURE_TYPES = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse"],
    "Commercial": ["Boutique Office", "Corporate Hub", "Hotel Resort", "Medical Clinic"],
    "Industrial": ["Distribution Warehouse", "Manufacturing Facility"]
}

def get_domain(name):
    for domain, items in ARCHITECTURE_TYPES.items():
        if name in items:
            return domain
    return "General"

# Architectural standards
MIN_ROOM_SIZES = {
    "living": 16.0, "kitchen": 8.0, "dining": 10.0,
    "bedroom": 10.0, "bathroom": 4.0, "study": 8.0,
    "office": 10.0, "meeting": 12.0, "reception": 8.0,
    "hall": 6.0, "corridor": 1.5 * 1.2,
    "storage": 4.0
}

DOOR_WIDTHS = {
    "main": 0.9,
    "interior": 0.8,
    "bathroom": 0.75
}

WINDOW_RATIO = 0.15   # glazing area / floor area
STRUCTURAL_GRID = 4.0

ROOM_TYPES = {
    "Residential": ["living","kitchen","dining","bedroom","bathroom","corridor","study"],
    "Commercial": ["office","meeting","reception","kitchen","bathroom","corridor"],
    "Industrial": ["hall","storage","bathroom","office"]
}

# ============================================================
# DESIGN GENERATOR WITH ARCHITECTURAL STANDARDS
# ============================================================
def _assign_room_types(domain, count, building_type):
    if domain == "Residential":
        essential = ["living", "kitchen", "bathroom"]
        if "Villa" in building_type:
            essential.append("dining")
        if count < len(essential):
            types = essential[:count]
        else:
            types = essential + random.choices(["bedroom","study","corridor","bathroom"], k=count-len(essential))
    elif domain == "Commercial":
        essential = ["office", "bathroom", "corridor"]
        if "Hotel" in building_type:
            essential = ["reception","bathroom","corridor","bedroom"]
        types = essential + random.choices(["meeting","kitchen","office"], k=max(0, count-len(essential)))
    else:  # Industrial
        essential = ["hall", "bathroom", "storage"]
        types = essential + random.choices(["office","hall"], k=max(0, count-len(essential)))
    return types[:count]

def _place_doors(rooms, total_doors):
    for room in rooms:
        door_width = DOOR_WIDTHS["main"] if room["type"] in ["living","office","meeting","reception"] else DOOR_WIDTHS["interior"]
        if room["type"] == "bathroom":
            door_width = DOOR_WIDTHS["bathroom"]
        # alternate sides for better circulation
        wall_y = 0 if rooms.index(room) % 2 == 0 else room["polygon"][3][1]
        door_x = room["polygon"][0][0] + (room["polygon"][1][0] - room["polygon"][0][0]) / 2 - door_width/2
        room["openings"].append({
            "type": "door",
            "start": (door_x, wall_y),
            "end": (door_x, wall_y + (0.9 if wall_y == 0 else -0.9)),
            "width": door_width
        })
    extra = total_doors - len(rooms)
    for _ in range(max(0, extra)):
        room = random.choice(rooms)
        wall_y = room["polygon"][3][1]
        door_x = room["polygon"][0][0] + random.uniform(0.5, (room["polygon"][1][0] - room["polygon"][0][0]) - 0.5)
        room["openings"].append({
            "type": "door",
            "start": (door_x, wall_y),
            "end": (door_x, wall_y - 0.9),
            "width": DOOR_WIDTHS["interior"]
        })

def _place_windows(rooms, total_windows, depth, enforce_standards):
    habitable = [r for r in rooms if r["type"] not in ("corridor", "bathroom", "storage")]
    if not habitable:
        return
    base = total_windows // len(habitable)
    remainder = total_windows % len(habitable)
    assigned = 0
    for i, room in enumerate(habitable):
        nw = base + (1 if i < remainder else 0)
        if nw == 0:
            continue
        room_width = room["polygon"][1][0] - room["polygon"][0][0]
        if enforce_standards:
            room_area = room_width * depth
            glazing_area = room_area * WINDOW_RATIO
            win_width = glazing_area / 1.2   # assume window height 1.2 m
            win_width = min(win_width, room_width * 0.8)
        else:
            win_width = room_width * 0.6
        win_width = max(0.6, win_width)
        x0 = room["polygon"][0][0] + (room_width - win_width) / 2
        for _ in range(nw):
            room["openings"].append({
                "type": "window",
                "start": (x0, depth),
                "end": (x0 + win_width, depth),
                "width": win_width
            })
            assigned += 1
    remaining = total_windows - assigned
    while remaining > 0 and habitable:
        room = random.choice(habitable)
        room_width = room["polygon"][1][0] - room["polygon"][0][0]
        win_width = min(1.2, room_width * 0.4)
        x0 = room["polygon"][0][0] + random.uniform(0, room_width - win_width)
        room["openings"].append({
            "type": "window",
            "start": (x0, depth),
            "end": (x0 + win_width, depth),
            "width": win_width
        })
        remaining -= 1

def _create_walls(width, depth):
    return [
        {"start": (0,0), "end": (width,0), "thickness": 0.3},
        {"start": (width,0), "end": (width,depth), "thickness": 0.3},
        {"start": (width,depth), "end": (0,depth), "thickness": 0.3},
        {"start": (0,depth), "end": (0,0), "thickness": 0.3}
    ]

def _place_columns(width, depth, enforce_standards):
    cols = [
        {"center":(0,0),"size":0.3,"shape":"square"},
        {"center":(width,0),"size":0.3,"shape":"square"},
        {"center":(0,depth),"size":0.3,"shape":"square"},
        {"center":(width,depth),"size":0.3,"shape":"square"},
    ]
    if enforce_standards:
        for x in np.arange(STRUCTURAL_GRID, width, STRUCTURAL_GRID):
            for y in np.arange(STRUCTURAL_GRID, depth, STRUCTURAL_GRID):
                if x < width - 0.5 and y < depth - 0.5:
                    cols.append({"center":(x, y),"size":0.25,"shape":"circle"})
    else:
        for x in np.linspace(width*0.3, width*0.7, max(2, int(width/5))):
            cols.append({"center":(x, depth/2),"size":0.25,"shape":"circle"})
    return cols

def _place_beams(width, depth):
    return [
        {"start":(0, 0.2), "end":(width, 0.2), "width":0.2},
        {"start":(0, depth-0.2), "end":(width, depth-0.2), "width":0.2},
    ]

def create_floor_layout(level, building_type, total_area, modules,
                        floor_area_m2, num_rooms, num_doors, num_windows,
                        enforce_standards=True):
    if floor_area_m2 is None:
        floor_area_m2 = total_area / (modules * 0.5 + 1)

    side = int(math.sqrt(floor_area_m2)) + 1
    width = max(6, min(side, 20))
    depth = max(6, min(side, 20))
    if enforce_standards:
        width = max(STRUCTURAL_GRID, round(width / STRUCTURAL_GRID) * STRUCTURAL_GRID)
        depth = max(STRUCTURAL_GRID, round(depth / STRUCTURAL_GRID) * STRUCTURAL_GRID)

    domain = get_domain(building_type)
    if num_rooms is None:
        num_rooms = 4
    room_types = _assign_room_types(domain, num_rooms, building_type)

    # Calculate minimum widths
    min_widths = []
    for rt in room_types:
        min_area = MIN_ROOM_SIZES.get(rt, 8.0)
        if rt == "corridor":
            min_w = 1.5
        else:
            min_w = max(2.0, math.sqrt(min_area))
        min_widths.append(min_w)
    total_min = sum(min_widths) + 0.2 * len(room_types)

    available_width = width
    if total_min > available_width:
        scale = available_width / total_min
        min_widths = [w * scale for w in min_widths]
    else:
        extra = (available_width - total_min) / len(room_types)
        min_widths = [w + extra for w in min_widths]

    rooms = []
    cum_x = 0.0
    for i, rt in enumerate(room_types):
        w = min_widths[i]
        if cum_x + w > width:
            w = width - cum_x
        if w < 1.5:
            break
        poly = [(cum_x, 0), (cum_x + w, 0), (cum_x + w, depth), (cum_x, depth)]
        rooms.append({"name": f"{rt.capitalize()} {i+1}", "type": rt, "polygon": poly, "openings": []})
        cum_x += w

    if num_doors is None:
        num_doors = len(rooms) + 1
    _place_doors(rooms, num_doors)

    if num_windows is None:
        num_windows = len(rooms)
    _place_windows(rooms, num_windows, depth, enforce_standards)

    walls = _create_walls(width, depth)
    interior_walls = []
    cur_x = 0
    for room in rooms:
        if cur_x > 0:
            interior_walls.append({"start": (cur_x, 0), "end": (cur_x, depth), "thickness": 0.2})
        cur_x += room["polygon"][1][0] - room["polygon"][0][0]
    walls.extend(interior_walls)

    columns = _place_columns(width, depth, enforce_standards)
    beams = _place_beams(width, depth)

    return {
        "level": level,
        "height": 3.0,
        "rooms": rooms,
        "walls": walls,
        "columns": columns,
        "beams": beams,
        "slab": {"thickness": 0.2}
    }

def generate_design(building, modules, num_floors=None,
                    total_rooms=None, total_doors=None, total_windows=None,
                    enforce_standards=True):
    if num_floors is None:
        num_floors = random.randint(1, 3)
    total_area = 100 + modules * 25
    floor_area = total_area / num_floors

    if total_rooms:
        base_rooms = total_rooms // num_floors
        extra_rooms = total_rooms % num_floors
    if total_doors:
        base_doors = total_doors // num_floors
        extra_doors = total_doors % num_floors
    if total_windows:
        base_windows = total_windows // num_floors
        extra_windows = total_windows % num_floors

    floors = []
    for lvl in range(1, num_floors+1):
        nr = base_rooms + (1 if lvl <= extra_rooms else 0) if total_rooms else None
        nd = base_doors + (1 if lvl <= extra_doors else 0) if total_doors else None
        nw = base_windows + (1 if lvl <= extra_windows else 0) if total_windows else None
        floor = create_floor_layout(lvl, building, total_area, modules, floor_area,
                                    num_rooms=nr, num_doors=nd, num_windows=nw,
                                    enforce_standards=enforce_standards)
        if floor:
            floors.append(floor)

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "building": building,
        "domain": get_domain(building),
        "modules": modules,
        "floors": floors,
        "area": total_area,
        "num_floors": num_floors,
        "cost": 0,
        "target_rooms": total_rooms,
        "target_doors": total_doors,
        "target_windows": total_windows
    }

def generate_concepts(num=5):
    building_types = [item for sublist in ARCHITECTURE_TYPES.values() for item in sublist]
    concepts = []
    for _ in range(num):
        btype = random.choice(building_types)
        modules = random.randint(2, 7)
        num_floors = random.randint(1, 3)
        design = generate_design(btype, modules, num_floors)
        design["fitness"] = evaluate_design(design)
        design["score"] = total_score(design["fitness"])
        concepts.append(design)
    return concepts

# ============================================================
# EVOLUTION ENGINE
# ============================================================
def mutate(design):
    child = json.loads(json.dumps(design))
    for floor in child["floors"]:
        if random.random() < 0.3:
            floor["columns"].append({"center":(random.uniform(1,5), random.uniform(1,5)), "size":0.25, "shape":"circle"})
        if random.random() < 0.3:
            floor["beams"].append({"start":(0, random.uniform(0.5,5)), "end":(random.uniform(4,8), random.uniform(0.5,5)), "width":0.2})
    child["cost"] = int(child["area"] * random.randint(1400, 2800))
    return child

def evaluate_design(design, enforce_standards=True):
    structural_scores = []
    for floor in design["floors"]:
        ncol = len(floor["columns"]) + 1
        nbeam = len(floor["beams"]) + 1
        ratio = nbeam / ncol if ncol > 0 else 1
        structural_scores.append(max(0, 100 - int(abs(ratio - 1.5) * 25)))
    structural = int(np.mean(structural_scores)) if structural_scores else 80

    if design["cost"] == 0:
        economic = 80
    else:
        cost_rate = design["cost"] / design["area"]
        economic = max(0, 100 - int(abs(cost_rate - 1800) * 0.05))

    total_rooms = sum(len(f["rooms"]) for f in design["floors"])
    spatial = min(100, total_rooms * 8)

    total_wall_length = 0
    total_window_length = 0
    for floor in design["floors"]:
        for room in floor["rooms"]:
            for op in room["openings"]:
                if op["type"] == "window":
                    total_window_length += op["width"]
        for wall in floor["walls"]:
            total_wall_length += np.sqrt((wall["end"][0]-wall["start"][0])**2 + (wall["end"][1]-wall["start"][1])**2)
    if total_wall_length > 0:
        wwr = total_window_length / (total_wall_length * 3)
        sustainability = min(100, int(wwr * 200))
    else:
        sustainability = 70

    # Code Compliance
    code_penalty = 0
    for floor in design["floors"]:
        for room in floor["rooms"]:
            w = room["polygon"][1][0] - room["polygon"][0][0]
            d = room["polygon"][3][1] - room["polygon"][0][1]
            area = w * d
            min_area = MIN_ROOM_SIZES.get(room["type"], 8.0)
            if area < min_area:
                code_penalty += (min_area - area) * 5
            doors = [op for op in room["openings"] if op["type"] == "door"]
            if not doors:
                code_penalty += 20
            if room["type"] not in ("corridor","bathroom","storage"):
                windows = [op for op in room["openings"] if op["type"] == "window"]
                if not windows:
                    code_penalty += 25
                else:
                    glazing_area = sum(op["width"] * 1.2 for op in windows)
                    if area > 0 and (glazing_area / area) < WINDOW_RATIO:
                        code_penalty += 15
        col_xs = sorted([c["center"][0] for c in floor["columns"]])
        if len(col_xs) > 2:
            diffs = np.diff(col_xs)
            if np.std(diffs) > 1.0:
                code_penalty += 10
    code_score = max(0, 100 - code_penalty)

    # Target constraints penalty
    target_penalty = 0
    if "target_rooms" in design and design["target_rooms"]:
        actual_rooms = sum(len(f["rooms"]) for f in design["floors"])
        target_penalty += abs(actual_rooms - design["target_rooms"]) * 10
    if "target_doors" in design and design["target_doors"]:
        actual_doors = sum(1 for f in design["floors"] for r in f["rooms"] for o in r["openings"] if o["type"]=="door")
        target_penalty += abs(actual_doors - design["target_doors"]) * 8
    if "target_windows" in design and design["target_windows"]:
        actual_windows = sum(1 for f in design["floors"] for r in f["rooms"] for o in r["openings"] if o["type"]=="window")
        target_penalty += abs(actual_windows - design["target_windows"]) * 5

    return {
        "Structural Score": structural,
        "Economic Score": economic,
        "Spatial Score": spatial,
        "Sustainability Score": sustainability,
        "Code Compliance Score": code_score,
        "Target Penalty": target_penalty
    }

def total_score(metrics):
    base = sum(v for k,v in metrics.items() if k != "Target Penalty") / 5
    penalty = metrics.get("Target Penalty", 0)
    return max(0, int(base - penalty * 0.2))

def crossover(parent1, parent2):
    child = json.loads(json.dumps(parent1))
    if len(child["floors"]) > 1 and len(parent2["floors"]) > 1:
        swap_idx = random.randint(0, len(child["floors"])-1)
        if swap_idx < len(parent2["floors"]):
            child["floors"][swap_idx] = json.loads(json.dumps(parent2["floors"][swap_idx]))
    return child

def tournament_select(population, tournament_size=3, num_survivors=5):
    selected = []
    for _ in range(num_survivors):
        contestants = random.sample(population, min(tournament_size, len(population)))
        winner = max(contestants, key=lambda x: x["score"])
        selected.append(winner)
    return selected

def evolve_design_multi(building, modules, generations, population_size,
                        num_floors=None, total_rooms=None, total_doors=None, total_windows=None,
                        enforce_standards=True):
    def make_design():
        return generate_design(building, modules, num_floors,
                              total_rooms=total_rooms, total_doors=total_doors,
                              total_windows=total_windows, enforce_standards=enforce_standards)
    population = [make_design() for _ in range(population_size)]
    history = []
    for gen in range(generations):
        for d in population:
            d["fitness"] = evaluate_design(d, enforce_standards)
            d["score"] = total_score(d["fitness"])
        population.sort(key=lambda x: x["score"], reverse=True)
        history.append(population[0]["score"])
        survivors = tournament_select(population, 3, population_size//2)
        next_pop = []
        for parent in survivors:
            next_pop.append(parent)
            if random.random() < 0.5 and len(survivors) > 1:
                partner = random.choice([s for s in survivors if s != parent])
                child = crossover(parent, partner)
            else:
                child = mutate(parent)
            next_pop.append(child)
        population = next_pop[:population_size]
    for d in population:
        d["fitness"] = evaluate_design(d, enforce_standards)
        d["score"] = total_score(d["fitness"])
    return population[0], history, population

def pareto_front(designs):
    nondominated = []
    for i, d1 in enumerate(designs):
        dominated = False
        for j, d2 in enumerate(designs):
            if i == j: continue
            f1, f2 = d1["fitness"], d2["fitness"]
            if all(f2[k] >= f1[k] for k in f1) and any(f2[k] > f1[k] for k in f1):
                dominated = True
                break
        if not dominated:
            nondominated.append(d1)
    return nondominated

# ============================================================
# 2D & 3D RENDERING
# ============================================================
def generate_floor_plan(design, floor_index=0, scale=35):
    if floor_index >= len(design.get("floors", [])):
        return None
    floor = design["floors"][floor_index]
    all_points = []
    for wall in floor["walls"]:
        all_points.append(wall["start"])
        all_points.append(wall["end"])
    for col in floor["columns"]:
        all_points.append(col["center"])
    if not all_points:
        return None
    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    margin = 1.5
    width_px = int((max_x - min_x + 2*margin) * scale) + 60
    height_px = int((max_y - min_y + 2*margin) * scale) + 60
    img = Image.new('RGB', (width_px, height_px), color=(245,245,245))
    draw = ImageDraw.Draw(img)

    def tx(x, y):
        return ((x - min_x + margin) * scale + 30, (y - min_y + margin) * scale + 30)

    draw.rectangle([tx(min_x, min_y), tx(max_x, max_y)], outline=(150,150,150), width=2)

    for wall in floor["walls"]:
        p1 = tx(*wall["start"])
        p2 = tx(*wall["end"])
        thick = max(2, int(wall.get("thickness", 0.25) * scale))
        draw.line([p1, p2], fill=(40,40,40), width=thick)

    for col in floor["columns"]:
        c = tx(*col["center"])
        size = max(2, int(col["size"] * scale))
        if col.get("shape") == "circle":
            draw.ellipse([c[0]-size, c[1]-size, c[0]+size, c[1]+size], fill=(100,100,100))
        else:
            draw.rectangle([c[0]-size, c[1]-size, c[0]+size, c[1]+size], fill=(100,100,100))

    for beam in floor["beams"]:
        p1 = tx(*beam["start"])
        p2 = tx(*beam["end"])
        draw.line([p1, p2], fill=(255,180,0), width=5)

    room_colors = {
        "living": (200,240,200), "kitchen": (255,245,200), "dining": (240,230,200),
        "bedroom": (180,230,180), "bathroom": (210,190,230), "corridor": (235,240,235),
        "office": (200,235,200), "meeting": (220,200,240), "reception": (190,220,190),
        "hall": (210,210,190), "storage": (200,200,200), "study": (230,220,240)
    }
    default_color = (210,230,210)

    for room in floor["rooms"]:
        poly = [tx(x,y) for (x,y) in room["polygon"]]
        color = room_colors.get(room.get("type",""), default_color)
        draw.polygon(poly, fill=color, outline=(80,80,80))
        if poly:
            cx = sum(p[0] for p in poly)/len(poly)
            cy = sum(p[1] for p in poly)/len(poly)
            draw.text((cx-20, cy-5), room["name"][:12], fill=(0,0,0), font=FONT)
        for op in room["openings"]:
            s = tx(*op["start"])
            e = tx(*op["end"])
            if op["type"] == "door":
                draw.line([s,e], fill=(255,255,255), width=6)
                mid = ((s[0]+e[0])//2, (s[1]+e[1])//2)
                draw.arc([mid[0]-8, mid[1]-8, mid[0]+8, mid[1]+8], 0, 90, fill=(0,0,0))
            elif op["type"] == "window":
                draw.line([s,e], fill=(255,255,255), width=6)
                draw.line([s,e], fill=(34,197,94), width=3)

    draw.text((10,5), f"Floor {floor['level']} - {design.get('building','')}", fill=(20,20,20))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def cuboid_mesh(x0, y0, z0, dx, dy, dz):
    x = [x0, x0+dx, x0+dx, x0, x0, x0+dx, x0+dx, x0]
    y = [y0, y0, y0+dy, y0+dy, y0, y0, y0+dy, y0+dy]
    z = [z0, z0, z0, z0, z0+dz, z0+dz, z0+dz, z0+dz]
    i = [0,0,4,4, 0,1,5,4, 1,2,6,5, 2,3,7,6, 3,0,4,7, 1,0,3,2]
    j = [1,3,5,7, 1,5,6,5, 2,6,7,6, 3,7,4,7, 0,4,5,4, 0,3,2,1]
    k = [3,2,7,6, 4,4,5,5, 6,5,6,6, 7,6,7,7, 7,5,4,4, 3,2,1,0]
    return x, y, z, i, j, k

def cylinder_mesh(cx, cy, z_bottom, z_top, radius, n=12):
    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    x_bottom = cx + radius * np.cos(theta)
    y_bottom = cy + radius * np.sin(theta)
    x_top = x_bottom
    y_top = y_bottom
    z_b = np.full_like(x_bottom, z_bottom)
    z_t = np.full_like(x_top, z_top)
    x = np.concatenate([x_bottom, x_top])
    y = np.concatenate([y_bottom, y_top])
    z = np.concatenate([z_b, z_t])
    i, j, k = [], [], []
    for idx in range(n):
        nxt = (idx+1) % n
        i.extend([idx, nxt, n+nxt, n+idx])
        j.extend([nxt, n+nxt, n+nxt, n+idx])
        k.extend([n+nxt, n+idx, n+idx, nxt])
    return x, y, z, i, j, k

def build_3d_stacked_figure(design):
    fig = go.Figure()
    for fi, floor in enumerate(design["floors"]):
        z_base = fi * floor.get("height", 3.0)
        z_top = z_base + floor.get("height", 3.0)
        slab_thick = floor.get("slab", {}).get("thickness", 0.2)

        all_x = [p[0] for wall in floor["walls"] for p in (wall["start"],wall["end"])]
        all_y = [p[1] for wall in floor["walls"] for p in (wall["start"],wall["end"])]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        x,y,z,i,j,k = cuboid_mesh(min_x, min_y, z_base, max_x-min_x, max_y-min_y, slab_thick)
        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color=f'hsl({fi*60}, 60%, 50%)', opacity=0.3, name=f'Slab F{floor["level"]}'))

        for wall in floor["walls"]:
            sx, sy = wall["start"]
            ex, ey = wall["end"]
            dx = ex - sx
            dy = ey - sy
            length = np.sqrt(dx**2+dy**2)
            angle = np.arctan2(dy, dx)
            thick = wall.get("thickness", 0.25)
            wx, wy, wz, iw, jw, kw = cuboid_mesh(sx, sy-thick/2, z_base, length, thick, z_top-z_base)
            wx = np.array(wx) - sx
            wy = np.array(wy) - sy
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            rotx = wx * cos_a - wy * sin_a
            roty = wx * sin_a + wy * cos_a
            wx = rotx + sx
            wy = roty + sy
            fig.add_trace(go.Mesh3d(x=wx, y=wy, z=wz, i=iw, j=jw, k=kw, color='tan', opacity=0.7, showlegend=False))

        for col in floor["columns"]:
            cx, cy = col["center"]
            radius = col["size"]/2
            xc, yc, zc, ic, jc, kc = cylinder_mesh(cx, cy, z_base, z_top, radius)
            fig.add_trace(go.Mesh3d(x=xc, y=yc, z=zc, i=ic, j=jc, k=kc, color='grey', opacity=0.8, showlegend=False))

        beam_z_base = z_top - slab_thick - 0.4
        for beam in floor["beams"]:
            sx, sy = beam["start"]
            ex, ey = beam["end"]
            dx = ex - sx
            dy = ey - sy
            length = np.sqrt(dx**2+dy**2)
            angle = np.arctan2(dy, dx)
            bw = beam.get("width", 0.2)
            bh = 0.4
            bx, by, bz, ib, jb, kb = cuboid_mesh(sx, sy-bw/2, beam_z_base, length, bw, bh)
            bx = np.array(bx) - sx
            by = np.array(by) - sy
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            rotx = bx * cos_a - by * sin_a
            roty = bx * sin_a + by * cos_a
            bx = rotx + sx
            by = roty + sy
            fig.add_trace(go.Mesh3d(x=bx, y=by, z=bz, i=ib, j=jb, k=kb, color='seagreen', opacity=0.6, showlegend=False))

        cx = (min_x+max_x)/2
        cy = (min_y+max_y)/2
        fig.add_trace(go.Scatter3d(x=[cx], y=[cy], z=[z_top+0.2], mode='text', text=[f"Floor {floor['level']}"],
                                   textfont=dict(size=14, color='white'), showlegend=False))

    fig.update_layout(
        scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
                   aspectmode='data', camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))),
        margin=dict(l=0, r=0, t=30, b=0),
        height=600,
        title="3D Stacked View"
    )
    return fig

# ============================================================
# IFC EXPORT (Basic IFC2x3)
# ============================================================
def compress_guid(guid_str):
    raw_uuid = uuid.UUID(guid_str).bytes
    return base64.b64encode(raw_uuid, b"-_").decode()[:22]

def export_ifc(design):
    lines = []
    lines.append("ISO-10303-21;")
    lines.append("HEADER;")
    lines.append("FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');")
    lines.append("FILE_NAME('','',(''),(''),'IfcOpenShell-v0.7.0','RANDOM V4','');")
    lines.append("FILE_SCHEMA(('IFC2X3'));")
    lines.append("ENDSEC;")
    lines.append("DATA;")

    id_counter = 1
    def new_id():
        nonlocal id_counter
        oid = id_counter
        id_counter += 1
        return f"#{oid}"

    proj_id = new_id()
    site_id = new_id()
    building_id = new_id()
    storey_ids = [new_id() for _ in design["floors"]]
    owner_hist = new_id()
    lines.append(f"{owner_hist}=IFCOWNERHISTORY(#0,#0,$,.ADDED.,$,#0,$,0);")
    units = new_id()
    lines.append(f"{units}=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);")
    lines.append(f"{proj_id}=IFCPROJECT('{compress_guid(design['id'])}',#{owner_hist},'{design['building']}',$,$,$,$,(#{units}),#0);")
    lines.append(f"{site_id}=IFCSITE('{compress_guid(str(uuid.uuid4()))}',#{owner_hist},'Site',$,$,$,$,$,$,$,$,$,$);")
    lines.append(f"{building_id}=IFCBUILDING('{compress_guid(str(uuid.uuid4()))}',#{owner_hist},'Building',$,$,#{site_id},$,$,$,$);")
    rel_agg = new_id()
    lines.append(f"{rel_agg}=IFCRELAGGREGATES('{compress_guid(str(uuid.uuid4()))}',#{owner_hist},$,$,#{proj_id},(#{site_id}));")
    rel_agg2 = new_id()
    lines.append(f"{rel_agg2}=IFCRELAGGREGATES('{compress_guid(str(uuid.uuid4()))}',#{owner_hist},$,$,#{site_id},(#{building_id}));")

    for idx, storey_id in enumerate(storey_ids):
        z = idx * 3.0
        placement = new_id()
        lines.append(f"{placement}=IFCLOCALPLACEMENT($,IFCAXIS2PLACEMENT3D(IFCCARTESIANPOINT((0.,0.,{z})),IFCDIRECTION((0.,0.,1.)),IFCDIRECTION((1.,0.,0.))));")
        lines.append(f"{storey_id}=IFCBUILDINGSTOREY('{compress_guid(str(uuid.uuid4()))}',#{owner_hist},'Storey {idx+1}',$,$,{placement},$,$,$);")

    # Simplified walls for demonstration
    for fi, floor in enumerate(design["floors"]):
        for wall in floor["walls"]:
            wall_id = new_id()
            lines.append(f"{wall_id}=IFCWALL('{compress_guid(str(uuid.uuid4()))}',#{owner_hist},'Wall',$,$,{storey_ids[fi]},$,$);")

    lines.append("ENDSEC;")
    lines.append("END-ISO-10303-21;")
    return "\n".join(lines)

# ============================================================
# GLTF EXPORT (placeholder – minimal cube)
# ============================================================
def design_to_glb(design):
    # Minimal valid GLB (a single triangle for demonstration)
    vertices = [0.0, 0.0, 0.0,  1.0, 0.0, 0.0,  0.0, 1.0, 0.0]
    indices = [0, 1, 2]
    vertices_binary = struct.pack(f'<{len(vertices)}f', *vertices)
    indices_binary = struct.pack(f'<{len(indices)}H', *indices)

    from pygltflib import GLTF2, Buffer, BufferView, Accessor, Mesh, Primitive, Node, Scene, Asset, ELEMENT_ARRAY_BUFFER, ARRAY_BUFFER, FLOAT, UNSIGNED_SHORT
    gltf = GLTF2()
    gltf.asset = Asset(version="2.0")
    buffer = Buffer(byteLength=len(vertices_binary)+len(indices_binary))
    gltf.buffers.append(buffer)
    bv_vertices = BufferView(buffer=0, byteOffset=0, byteLength=len(vertices_binary), target=ARRAY_BUFFER)
    bv_indices = BufferView(buffer=0, byteOffset=len(vertices_binary), byteLength=len(indices_binary), target=ELEMENT_ARRAY_BUFFER)
    gltf.bufferViews.extend([bv_vertices, bv_indices])
    acc_vertices = Accessor(bufferView=0, byteOffset=0, componentType=FLOAT, count=len(vertices)//3, type="VEC3", max=[1.0,1.0,0.0], min=[0.0,0.0,0.0])
    acc_indices = Accessor(bufferView=1, byteOffset=0, componentType=UNSIGNED_SHORT, count=len(indices), type="SCALAR", max=[2], min=[0])
    gltf.accessors.extend([acc_vertices, acc_indices])
    primitive = Primitive(attributes={"POSITION": 0}, indices=1)
    mesh = Mesh(primitives=[primitive])
    gltf.meshes.append(mesh)
    node = Node(mesh=0)
    gltf.nodes.append(node)
    scene = Scene(nodes=[0])
    gltf.scenes.append(scene)
    gltf.scene = 0
    gltf.binary_blob = vertices_binary + indices_binary
    return gltf.save_to_bytes()

# ============================================================
# ROOM EDITOR
# ============================================================
def render_room_editor(design):
    if "floors" not in design:
        st.warning("No floor data.")
        return
    floor_idx = st.slider("Floor to edit", 0, len(design["floors"])-1, 0, key="room_editor_floor")
    floor = design["floors"][floor_idx]
    room_names = [f"{r['name']} ({r['type']})" for r in floor["rooms"]]
    selected_room = st.selectbox("Select room", room_names)
    room_idx = room_names.index(selected_room)
    room = floor["rooms"][room_idx]

    col1, col2 = st.columns(2)
    with col1:
        new_width = st.number_input("New width (m)", min_value=1.0, max_value=20.0,
                                    value=float(room["polygon"][1][0] - room["polygon"][0][0]))
    with col2:
        room_types_list = list(ROOM_TYPES.get(get_domain(design["building"]), ["office","meeting","bathroom","corridor"]))
        new_type = st.selectbox("Room type", room_types_list,
                                index=room_types_list.index(room["type"]) if room["type"] in room_types_list else 0)

    if st.button("Update Room"):
        old_width = room["polygon"][1][0] - room["polygon"][0][0]
        scale = new_width / old_width
        for i in range(len(room["polygon"])):
            x, y = room["polygon"][i]
            room["polygon"][i] = (x * scale, y)
        for op in room["openings"]:
            op["start"] = (op["start"][0] * scale, op["start"][1])
            op["end"] = (op["end"][0] * scale, op["end"][1])
        room["type"] = new_type
        st.success("Room updated!")
        st.image(generate_floor_plan(design, floor_idx), caption="Updated Floor Plan", use_column_width=True)

# ============================================================
# SESSION INIT
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.memory = DEFAULT_MEMORY.copy()
    st.session_state.page = "Dashboard"
    st.session_state.generated_concepts = []
    st.session_state.unit_system = "Metric"
    st.session_state.all_final_designs = []

if not load_users():
    create_user("admin", "admin123", role="admin")

# ============================================================
# LOGIN PAGE
# ============================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#4ade80;'>🏗️ RANDOM V4</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8;'>Evolution AI Design Studio</p>", unsafe_allow_html=True)
        with st.form("auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col_login, col_reg = st.columns(2)
            with col_login:
                login_btn = st.form_submit_button("Login")
            with col_reg:
                register_btn = st.form_submit_button("Register")

            if login_btn:
                user = authenticate(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_data = user
                    st.session_state.memory = load_memory(username)
                    st.session_state.generated_concepts = []
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

            if register_btn:
                if not username or not password:
                    st.error("Please fill all fields.")
                else:
                    try:
                        create_user(username, password)
                        st.success("Account created! You can now log in.")
                    except ValueError as e:
                        st.error(str(e))
    st.stop()

# ============================================================
# LOGGED IN – SIMPLE PRACTICAL SIDEBAR
# ============================================================
username = st.session_state.username
user_data = st.session_state.user_data
memory = st.session_state.memory

with st.sidebar:
    st.markdown("### 🏗️ RANDOM V4")
    st.markdown(f"**👤 {username}**")

    # XP bar
    lvl = user_data.get("level", 1)
    xp = user_data.get("xp", 0)
    needed = xp_for_level(lvl)
    progress = xp / needed if needed > 0 else 1.0
    st.markdown(f"""
    <div class="xp-container">
        <span style="font-size:12px; color:#94a3b8;">LVL {lvl}</span>
        <div class="xp-bar-bg">
            <div class="xp-bar-fill" style="width:{progress*100}%;"></div>
        </div>
        <span style="font-size:10px; color:#64748b;">{xp}/{needed} XP</span>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    nav = st.radio(
        "Go to",
        ["Dashboard", "Random Copilot", "Concepts", "Comparison", "2D Plans",
         "Room Editor", "3D Viewer", "Reports", "Memory", "Settings"]
    )
    st.session_state.page = nav
    st.divider()

    # Admin panel (compact)
    if user_data.get("role") == "admin":
        with st.expander("🛡️ Admin"):
            users = load_users()
            for u in users:
                cols = st.columns([3,1])
                cols[0].write(f"**{u['username']}** (Lvl {u['level']})")
                if u["username"] != username:
                    if cols[1].button("🗑️", key=f"del_{u['username']}"):
                        users.remove(u)
                        save_users(users)
                        st.rerun()
                else:
                    cols[1].write("you")

    # Recent projects
    st.markdown("### 📁 Recent Projects")
    for proj in memory["projects"][-5:]:
        st.markdown(f"• {proj['name']} *({proj['date']})*")

    if st.button("➕ New Project", use_container_width=True):
        new_name = f"Project {len(memory['projects'])+1}"
        memory["projects"].append({"name": new_name, "date": datetime.now().strftime("%b %d, %Y")})
        save_memory(username, memory)
        st.rerun()

    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        save_memory(username, memory)
        for key in ["logged_in", "username", "user_data", "memory", "generated_concepts", "all_final_designs"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ============================================================
# PAGE ROUTING
# ============================================================
page = st.session_state.page

if page == "Dashboard":
    st.markdown('<div class="banner"><h1>Welcome back, Architect</h1><p>Create. Evolve. Perfect.</p></div>', unsafe_allow_html=True)

    if not st.session_state.generated_concepts:
        with st.spinner("Generating 5 unique design concepts..."):
            st.session_state.generated_concepts = generate_concepts(5)
            leveled_up = add_xp(username, 10)
            st.session_state.user_data = get_user(username)
            if leveled_up:
                st.balloons()

    concepts = st.session_state.generated_concepts
    if len(concepts) < 5:
        concepts.extend(generate_concepts(5 - len(concepts)))
        st.session_state.generated_concepts = concepts

    st.markdown("## 🔬 EVOLUTION ENGINE RESULTS")
    for idx, design in enumerate(concepts[:5]):
        score = design.get("score", 0)
        name = f"Concept {['Alpha','Beta','Gamma','Delta','Epsilon'][idx]}"
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown(f"**{idx+1}. {name}**")
        col2.markdown(f"<div class='concept-score'>{score}</div>", unsafe_allow_html=True)
        col3.progress(score/100)

    st.divider()
    best = concepts[0]
    fitness = best.get("fitness", {})
    agent_scores = {
        "Architect AI": {"sub": "Function & Aesthetics", "score": int((fitness.get("Structural Score",0)+fitness.get("Spatial Score",0))/2)},
        "Structural AI": {"sub": "Safety & Stability", "score": fitness.get("Structural Score",0)},
        "Sustainability AI": {"sub": "Green & Efficiency", "score": fitness.get("Sustainability Score",0)},
        "Cost AI": {"sub": "Budget & Value", "score": fitness.get("Economic Score",0)},
        "Code AI": {"sub": "Standards & Compliance", "score": fitness.get("Code Compliance Score",0)}
    }
    st.markdown("### 🤖 AI AGENT EVALUATION SUMMARY")
    cols = st.columns(5)
    for i, (agent, data) in enumerate(agent_scores.items()):
        with cols[i]:
            st.markdown(f'''<div class="agent-box">
                <div class="agent-name">{agent}</div>
                <div class="agent-score">{data['score']}/100</div>
                <div class="agent-sub">{data['sub']}</div>
                </div>''', unsafe_allow_html=True)

    st.divider()
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### 🗺️ 2D FLOOR PLAN – CONCEPT ALPHA")
        if best.get("floors"):
            plan_img = generate_floor_plan(best, 0)
            if plan_img:
                st.image(plan_img, use_column_width=True)
    with col_right:
        st.markdown("### 🏗️ 3D MASSING – CONCEPT ALPHA")
        if best.get("floors"):
            fig = build_3d_stacked_figure(best)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

elif page == "Random Copilot":
    st.markdown("## 🧠 Random Copilot – Full Design Control")

    category = st.radio("Building Category", list(ARCHITECTURE_TYPES.keys()), horizontal=True)
    building = st.selectbox("Building Type", ARCHITECTURE_TYPES[category])

    col1, col2 = st.columns(2)
    with col1:
        num_floors = st.slider("Floors", 1, 5, 2)
        total_rooms = st.slider("Total Rooms", num_floors, num_floors*8, num_floors*2,
                                help="Total across all floors")
    with col2:
        total_doors = st.slider("Total Doors", total_rooms, total_rooms*3, total_rooms+num_floors)
        total_windows = st.slider("Total Windows", max(0, total_rooms - num_floors), total_rooms*2, total_rooms)

    modules = st.slider("Complexity (Modules)", 1, 10, 4)
    generations = st.slider("Evolution Cycles", 2, 30, 8)
    population = st.slider("Population", 4, 40, 12)
    enforce_standards = st.checkbox("Enforce Architectural Standards", value=True)

    if st.button("🚀 Generate Design"):
        with st.spinner("Evolving with standards..."):
            best, history, all_designs = evolve_design_multi(
                building=building,
                modules=modules,
                generations=generations,
                population_size=population,
                num_floors=num_floors,
                total_rooms=total_rooms,
                total_doors=total_doors,
                total_windows=total_windows,
                enforce_standards=enforce_standards
            )
            st.success(f"Design {best['id']} created!")
            st.session_state.generated_concepts.insert(0, best)
            if len(st.session_state.generated_concepts) > 10:
                st.session_state.generated_concepts = st.session_state.generated_concepts[:10]
            st.session_state.all_final_designs = all_designs
            leveled_up = add_xp(username, 20)
            st.session_state.user_data = get_user(username)
            if leveled_up:
                st.balloons()
            memory["projects"].append({"name": best["building"], "date": datetime.now().strftime("%b %d, %Y")})
            save_memory(username, memory)

            st.json({k: best[k] for k in ["id","building","area","score","fitness"]})
            st.line_chart(history)

            pareto_designs = pareto_front(all_designs)
            if pareto_designs:
                st.markdown("### 📊 Pareto Front (Final Generation)")
                df = pd.DataFrame([d["fitness"] for d in pareto_designs])
                df["score"] = [d["score"] for d in pareto_designs]
                fig = px.parallel_coordinates(df, color="score", color_continuous_scale=px.colors.sequential.Viridis)
                st.plotly_chart(fig, use_container_width=True)

elif page == "Concepts":
    st.markdown("## 📋 Concepts")
    if not st.session_state.generated_concepts:
        st.info("No concepts yet.")
    else:
        for i, design in enumerate(st.session_state.generated_concepts):
            with st.expander(f"Concept {i+1} – {design['building']} (Score: {design.get('score',0)})"):
                col1, col2 = st.columns([1,2])
                with col1:
                    if design.get("floors"):
                        img = generate_floor_plan(design, 0)
                        if img:
                            st.image(img, caption="Floor 1")
                with col2:
                    st.json({k: design[k] for k in ["id","building","area","num_floors","cost","score","fitness"]})

elif page == "Comparison":
    st.markdown("## 🔄 Design Comparison")
    concepts = st.session_state.generated_concepts
    if len(concepts) < 2:
        st.warning("Need at least two concepts.")
    else:
        names = [f"{d['building']} ({d['id']})" for d in concepts]
        left = st.selectbox("Design A", range(len(names)), format_func=lambda x: names[x], key="comp_a")
        right = st.selectbox("Design B", range(len(names)), format_func=lambda x: names[x], key="comp_b")
        if left == right:
            st.info("Select two different designs.")
        else:
            a, b = concepts[left], concepts[right]
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(names[left])
                st.metric("Score", a["score"])
                if a.get("floors"):
                    st.image(generate_floor_plan(a,0), use_column_width=True)
            with col2:
                st.subheader(names[right])
                st.metric("Score", b["score"])
                if b.get("floors"):
                    st.image(generate_floor_plan(b,0), use_column_width=True)
            cats = list(a["fitness"].keys())
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=[a["fitness"][c] for c in cats], theta=cats, fill='toself', name=f'A: {a["building"]}'))
            fig.add_trace(go.Scatterpolar(r=[b["fitness"][c] for c in cats], theta=cats, fill='toself', name=f'B: {b["building"]}'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])))
            st.plotly_chart(fig, use_container_width=True)

elif page == "2D Plans":
    st.markdown("## 🗺️ 2D Floor Plans")
    concepts = st.session_state.generated_concepts
    if not concepts:
        st.info("No designs.")
    else:
        idx = st.selectbox("Select design", range(len(concepts)),
                           format_func=lambda i: f"{concepts[i]['building']} ({concepts[i]['id']})")
        design = concepts[idx]
        if design.get("floors"):
            floor = st.slider("Floor", 0, len(design["floors"])-1, 0)
            img = generate_floor_plan(design, floor)
            if img:
                st.image(img, use_column_width=True)

elif page == "Room Editor":
    st.markdown("## ✏️ Interactive Room Editor")
    concepts = st.session_state.generated_concepts
    if not concepts:
        st.info("No designs.")
    else:
        idx = st.selectbox("Select design", range(len(concepts)),
                           format_func=lambda i: f"{concepts[i]['building']} ({concepts[i]['id']})")
        render_room_editor(concepts[idx])

elif page == "3D Viewer":
    st.markdown("## 🏗️ 3D BIM Viewer (Stacked)")
    concepts = st.session_state.generated_concepts
    if not concepts:
        st.info("No designs.")
    else:
        idx = st.selectbox("Select design", range(len(concepts)),
                           format_func=lambda i: f"{concepts[i]['building']} ({concepts[i]['id']})", key="3d_sel")
        design = concepts[idx]
        if design.get("floors"):
            fig = build_3d_stacked_figure(design)
            st.plotly_chart(fig, use_container_width=True)

elif page == "Reports":
    st.markdown("## 📊 Design Report")
    concepts = st.session_state.generated_concepts
    if not concepts:
        st.info("No designs.")
    else:
        idx = st.selectbox("Choose design", range(len(concepts)),
                           format_func=lambda i: f"{concepts[i]['building']} ({concepts[i]['id']})")
        design = concepts[idx]
        st.subheader(f"Report for {design['building']}")
        st.write("**ID:**", design["id"])
        st.write("**Area:**", f"{design['area']:.1f} m²")
        st.write("**Floors:**", design["num_floors"])
        st.write("**Overall Score:**", design.get("score"))
        if "fitness" in design:
            df = pd.DataFrame(design["fitness"].items(), columns=["Agent", "Score"])
            fig = px.bar(df, x="Agent", y="Score", color="Score", range_y=[0,100])
            st.plotly_chart(fig, use_container_width=True)
        for i in range(len(design.get("floors",[]))):
            img = generate_floor_plan(design, i)
            if img:
                st.image(img, caption=f"Floor {design['floors'][i]['level']}", width=500)
        json_str = json.dumps(design, indent=4)
        st.download_button("📥 Download Design JSON", json_str, file_name=f"{design['id']}.json", mime="application/json")
        if st.button("📐 Export IFC"):
            ifc_text = export_ifc(design)
            st.download_button("⬇️ Download IFC", ifc_text, file_name=f"{design['id']}.ifc", mime="text/plain")
        if st.button("🧊 Export glTF (Beta)"):
            glb_data = design_to_glb(design)
            st.download_button("⬇️ Download GLB", glb_data, file_name=f"{design['id']}.glb", mime="model/gltf-binary")

elif page == "Memory":
    st.markdown("## 🧠 Memory & Saved Designs")
    if not memory["saved_designs"]:
        st.info("No saved designs.")
    else:
        for idx, saved in enumerate(memory["saved_designs"]):
            with st.expander(f"{saved.get('building','')} - {saved.get('id','')} (Score: {saved.get('score','')})"):
                st.json(saved)
                if st.button(f"Delete {saved['id']}", key=f"del_{idx}"):
                    memory["saved_designs"].pop(idx)
                    save_memory(username, memory)
                    st.rerun()
    if st.session_state.generated_concepts:
        best = st.session_state.generated_concepts[0]
        if st.button(f"Save {best.get('id','')}"):
            memory["saved_designs"].append(best)
            save_memory(username, memory)
            st.success("Saved!")

elif page == "Settings":
    st.markdown("## ⚙️ Settings")
    unit = st.selectbox("Unit System", ["Metric", "Imperial", "Dual"], index=0)
    st.session_state.unit_system = unit
    st.success("Settings updated.")

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="footer"><span>AI Powered</span> · <span>Data Driven</span> · <span>Secure</span> · <span>Scalable</span></div>', unsafe_allow_html=True)
