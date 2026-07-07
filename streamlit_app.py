# ============================================================
# RANDOM V3 EVOLUTION AI DESIGN STUDIO
# AI Architecture + BIM Intelligence Engine
# Evolutionary Spatial Synthesis
# Single File Streamlit Edition – Enhanced Multi-Storey BIM
# ============================================================

import streamlit as st
import json
import uuid
import random
import hashlib
from pathlib import Path
from datetime import datetime, date
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RANDOM V3 Evolution Studio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "random_users.json"
FONT = ImageFont.load_default()
XP_PER_LEVEL = 100

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
    """Returns True if user leveled up."""
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
    "version": "V3 Evolution Studio",
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

def log_event(username: str, memory: dict, text: str):
    memory["logs"].append({"time": datetime.now().isoformat(), "event": text})
    save_memory(username, memory)

# ============================================================
# GREEN THEME – VISUAL SYSTEM
# ============================================================

GREEN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body, .stApp {
    background: #0a1a0f;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #e6f4ea;
}

h1, h2, h3, h4, h5, .stTitle, .stHeader {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    color: #b9f5d8;
    text-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #051007, #0e2b16);
    border-right: 1px solid rgba(34, 197, 94, 0.15);
}

.glass-card {
    background: rgba(34, 197, 94, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid rgba(34, 197, 94, 0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    margin-bottom: 1.5rem;
}

.banner {
    background: linear-gradient(135deg, #0d2818, #14532d);
    padding: 2rem 2.5rem;
    border-radius: 28px;
    color: white;
    margin-bottom: 2rem;
    border: 1px solid rgba(34, 197, 94, 0.3);
    box-shadow: 0 20px 60px rgba(0,60,30,0.4);
}

.metric-box {
    background: rgba(34, 197, 94, 0.06);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    border-left: 4px solid #22c55e;
}

.concept-item {
    background: rgba(34, 197, 94, 0.03);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(34, 197, 94, 0.1);
}

.concept-score {
    background: rgba(34, 197, 94, 0.15);
    padding: 0.25rem 1rem;
    border-radius: 20px;
    font-weight: 700;
    color: #4ade80;
}

.agent-box {
    background: rgba(34, 197, 94, 0.04);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(34, 197, 94, 0.15);
}

.agent-name {
    font-weight: 600;
    color: #86efac;
    font-size: 0.9rem;
}

.agent-score {
    font-size: 2rem;
    font-weight: 700;
    color: #dcfce7;
}

.agent-sub {
    font-size: 0.75rem;
    color: #6b7280;
}

.divider {
    border-top: 1px solid rgba(34, 197, 94, 0.1);
    margin: 1.5rem 0;
}

.footer {
    text-align: center;
    padding: 1.5rem 0;
    color: #4b5563;
    font-size: 0.8rem;
    border-top: 1px solid rgba(34, 197, 94, 0.1);
}

.stButton > button {
    background: linear-gradient(135deg, #16a34a, #15803d);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    transition: all 0.2s;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 30px rgba(34, 197, 94, 0.4);
}

.recommendation-badge {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    padding: 0.4rem 1.8rem;
    border-radius: 30px;
    color: white;
    font-weight: 700;
    display: inline-block;
}

/* XP Bar */
.xp-container {
    display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;
}
.xp-bar-bg {
    flex: 1; height: 10px; background: #1e293b; border-radius: 5px; overflow: hidden;
}
.xp-bar-fill {
    height: 100%; background: linear-gradient(90deg, #22c55e, #4ade80);
    border-radius: 5px; box-shadow: 0 0 8px #4ade80;
}
</style>
"""
st.markdown(GREEN_CSS, unsafe_allow_html=True)

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

# Auto‑create admin if no users
if not load_users():
    create_user("admin", "admin123", role="admin")

# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#4ade80;'>🌿 RANDOM V3</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#86efac;'>Evolution AI Design Studio</p>", unsafe_allow_html=True)
        with st.form("auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col_login, col_reg = st.columns(2)
            with col_login:
                login_btn = st.form_submit_button("🌱 Login")
            with col_reg:
                register_btn = st.form_submit_button("✨ Register")

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
# LOGGED IN – SETUP
# ============================================================

username = st.session_state.username
user_data = st.session_state.user_data
memory = st.session_state.memory

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

# ============================================================
# LAYOUT GENERATOR FOR FLOORS (enriched BIM)
# ============================================================

def create_floor_layout(level, building_type, area, modules, floor_area_m2=None):
    if floor_area_m2 is None:
        floor_area_m2 = (area / (modules * 0.5 + 1))
    side = int(np.sqrt(floor_area_m2)) + 1
    width = max(6, min(side, 15))
    depth = max(6, min(side, 15))
    
    rooms = []
    if "Residential" in get_domain(building_type) or "Apartment" in building_type:
        if level == 1:
            room_types = [
                ("Living Room", "living", 0.4),
                ("Kitchen", "kitchen", 0.25),
                ("Dining", "dining", 0.2),
                ("Bathroom", "bathroom", 0.1),
                ("Corridor", "corridor", 0.05)
            ]
        else:
            room_types = [
                ("Bedroom", "bedroom", 0.35),
                ("Bedroom", "bedroom", 0.3),
                ("Bathroom", "bathroom", 0.15),
                ("Study", "study", 0.2)
            ]
    elif "Office" in building_type:
        room_types = [
            ("Open Office", "office", 0.5),
            ("Meeting Room", "meeting", 0.25),
            ("Kitchenette", "kitchen", 0.1),
            ("Reception", "reception", 0.15)
        ]
    else:
        room_types = [
            ("Main Hall", "hall", 0.5),
            ("Storage", "storage", 0.3),
            ("Toilet", "bathroom", 0.2)
        ]
    
    total_width = width
    cum_x = 0
    for name, rtype, fraction in room_types:
        if cum_x >= total_width:
            break
        w = max(1.5, fraction * total_width)
        if cum_x + w > total_width:
            w = total_width - cum_x
        if w < 1.5:
            break
        poly = [(cum_x, 0), (cum_x + w, 0), (cum_x + w, depth), (cum_x, depth)]
        door_x = cum_x + w/2 - 0.45
        door_y = 0
        openings = [
            {"type": "door", "start": (door_x, door_y), "end": (door_x, door_y+0.9), "width": 0.9}
        ]
        if rtype != "corridor":
            win_start = (cum_x + w*0.2, depth)
            win_end = (cum_x + w*0.8, depth)
            openings.append({"type": "window", "start": win_start, "end": win_end, "width": w*0.6})
        rooms.append({"name": name, "type": rtype, "polygon": poly, "openings": openings})
        cum_x += w
    
    walls = [
        {"start": (0,0), "end": (width,0), "thickness": 0.3},
        {"start": (width,0), "end": (width,depth), "thickness": 0.3},
        {"start": (width,depth), "end": (0,depth), "thickness": 0.3},
        {"start": (0,depth), "end": (0,0), "thickness": 0.3}
    ]
    interior_walls = []
    cur_x = 0
    for i, room in enumerate(rooms):
        if i == 0:
            continue
        interior_walls.append({"start": (cur_x, 0), "end": (cur_x, depth), "thickness": 0.2})
        cur_x += room["polygon"][1][0] - room["polygon"][0][0]
    walls.extend(interior_walls)
    
    columns = [
        {"center": (0,0), "size": 0.3, "shape": "square"},
        {"center": (width,0), "size": 0.3, "shape": "square"},
        {"center": (0,depth), "size": 0.3, "shape": "square"},
        {"center": (width,depth), "size": 0.3, "shape": "square"},
    ]
    for x in np.linspace(width*0.3, width*0.7, 2):
        columns.append({"center": (x, depth/2), "size": 0.25, "shape": "circle"})
    
    beams = [
        {"start": (0,0.2), "end": (width,0.2), "width": 0.2},
        {"start": (0,depth-0.2), "end": (width,depth-0.2), "width": 0.2},
    ]
    
    return {
        "level": level,
        "height": 3.0,
        "rooms": rooms,
        "walls": walls,
        "columns": columns,
        "beams": beams,
        "slab": {"thickness": 0.2}
    }

# ============================================================
# AI DESIGN DNA GENERATOR
# ============================================================

def generate_design(building, modules, num_floors=None):
    if num_floors is None:
        num_floors = random.randint(1, 3)
    total_area = 100 + modules * 25
    floor_area = total_area / num_floors
    floors = []
    for lvl in range(1, num_floors+1):
        floors.append(create_floor_layout(lvl, building, total_area, modules, floor_area))
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "building": building,
        "domain": get_domain(building),
        "modules": modules,
        "floors": floors,
        "area": total_area,
        "num_floors": num_floors,
        "cost": 0
    }

def mutate(design):
    child = json.loads(json.dumps(design))
    for floor in child["floors"]:
        if random.random() < 0.3:
            floor["columns"].append({"center": (random.uniform(1,5), random.uniform(1,5)), "size": 0.25, "shape": "circle"})
        if random.random() < 0.3:
            floor["beams"].append({"start": (0, random.uniform(0.5,5)), "end": (random.uniform(4,8), random.uniform(0.5,5)), "width": 0.2})
    child["cost"] = int(child["area"] * random.randint(1400, 2800))
    return child

def evaluate_design(design):
    structural_scores = []
    for floor in design["floors"]:
        ncol = len(floor["columns"])+1
        nbeam = len(floor["beams"])+1
        ratio = nbeam / ncol
        structural_scores.append(max(0, 100 - int(abs(ratio - 1.5) * 25)))
    structural = int(np.mean(structural_scores)) if structural_scores else 80
    
    if design["cost"] == 0:
        economic = 80
    else:
        cost_rate = design["cost"] / design["area"]
        economic = max(0, 100 - int(abs(cost_rate - 1800) * 0.05))
    
    total_rooms = sum(len(floor["rooms"]) for floor in design["floors"])
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
    
    return {
        "Structural Score": structural,
        "Economic Score": economic,
        "Spatial Score": spatial,
        "Sustainability Score": sustainability
    }

def total_score(metrics):
    return int(sum(metrics.values()) / len(metrics))

def evolve_design(building, modules, generations, population_size, num_floors=None):
    population = [generate_design(building, modules, num_floors) for _ in range(population_size)]
    history = []
    for gen in range(generations):
        evaluated = []
        for d in population:
            d["fitness"] = evaluate_design(d)
            d["score"] = total_score(d["fitness"])
            evaluated.append(d)
        evaluated.sort(key=lambda x: x["score"], reverse=True)
        history.append(evaluated[0]["score"])
        survivors = evaluated[:max(2, population_size // 2)]
        next_pop = []
        for parent in survivors:
            next_pop.append(parent)
            next_pop.append(mutate(parent))
        population = next_pop[:population_size]
    return evaluated[0], history

# ============================================================
# 2D & 3D RENDERING (unchanged, just adjust colors for green theme)
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
    img = Image.new('RGB', (width_px, height_px), color=(245, 255, 245))  # light green tint
    draw = ImageDraw.Draw(img)
    
    def tx(x, y):
        return ((x - min_x + margin) * scale + 30, (y - min_y + margin) * scale + 30)
    
    draw.rectangle([tx(min_x, min_y), tx(max_x, max_y)], outline=(150,180,150), width=2)
    
    for wall in floor["walls"]:
        p1 = tx(*wall["start"])
        p2 = tx(*wall["end"])
        thick = max(2, int(wall.get("thickness", 0.25) * scale))
        draw.line([p1, p2], fill=(40,60,40), width=thick)
    
    for col in floor["columns"]:
        c = tx(*col["center"])
        size = max(2, int(col["size"] * scale))
        if col.get("shape") == "circle":
            draw.ellipse([c[0]-size, c[1]-size, c[0]+size, c[1]+size], fill=(100,120,100))
        else:
            draw.rectangle([c[0]-size, c[1]-size, c[0]+size, c[1]+size], fill=(100,120,100))
    
    for beam in floor["beams"]:
        p1 = tx(*beam["start"])
        p2 = tx(*beam["end"])
        draw.line([p1, p2], fill=(255,180,0), width=5)  # kept orange for contrast
    
    room_colors = {
        "living": (200, 240, 200),
        "kitchen": (255, 245, 200),
        "dining": (240, 230, 200),
        "bedroom": (180, 230, 180),
        "bathroom": (210, 190, 230),
        "corridor": (235, 240, 235),
        "office": (200, 235, 200),
        "meeting": (220, 200, 240),
        "reception": (190, 220, 190),
        "hall": (210, 210, 190),
        "storage": (200, 200, 200),
        "study": (230, 220, 240)
    }
    default_room_color = (210, 230, 210)
    
    for room in floor["rooms"]:
        poly = [tx(x,y) for (x,y) in room["polygon"]]
        color = room_colors.get(room.get("type",""), default_room_color)
        draw.polygon(poly, fill=color, outline=(80,100,80))
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
                draw.line([s,e], fill=(34,197,94), width=3)  # green windows!
    
    draw.text((10,5), f"Floor {floor['level']} - {design.get('building','')}", fill=(20,60,20))
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

def build_3d_figure(design, floor_index=0):
    if floor_index >= len(design["floors"]):
        return go.Figure()
    floor = design["floors"][floor_index]
    fig = go.Figure()
    z_base = (floor_index) * (floor.get("height", 3.0))
    z_top = z_base + floor.get("height", 3.0)
    slab_thick = floor.get("slab", {}).get("thickness", 0.2)
    
    all_x = [p[0] for wall in floor["walls"] for p in (wall["start"],wall["end"])]
    all_y = [p[1] for wall in floor["walls"] for p in (wall["start"],wall["end"])]
    if not all_x:
        all_x = [0,10]; all_y = [0,10]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    # Slab
    x,y,z,i,j,k = cuboid_mesh(min_x, min_y, z_base, max_x-min_x, max_y-min_y, slab_thick)
    fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color='lightgreen', opacity=0.3, name='Slab'))
    
    # Walls
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
        fig.add_trace(go.Mesh3d(x=wx, y=wy, z=wz, i=iw, j=jw, k=kw, color='tan', opacity=0.7, name='Wall'))
    
    # Columns
    for col in floor["columns"]:
        cx, cy = col["center"]
        radius = col["size"]/2
        xc, yc, zc, ic, jc, kc = cylinder_mesh(cx, cy, z_base, z_top, radius)
        fig.add_trace(go.Mesh3d(x=xc, y=yc, z=zc, i=ic, j=jc, k=kc, color='grey', opacity=0.8, name='Column'))
    
    # Beams
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
        fig.add_trace(go.Mesh3d(x=bx, y=by, z=bz, i=ib, j=jb, k=kb, color='seagreen', opacity=0.6, name='Beam'))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=500,
        title=f"3D View – Floor {floor['level']}"
    )
    return fig

# ============================================================
# CONCEPT GENERATION
# ============================================================

def generate_concepts(num=5):
    building_types = sum(ARCHITECTURE_TYPES.values(), [])
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
# UNIT SYSTEM
# ============================================================

def area_display(value):
    if st.session_state.unit_system == "Imperial":
        return f"{value * 10.7639:.1f} ft²"
    if st.session_state.unit_system == "Dual":
        return f"{value:.1f} m² | {value * 10.7639:.1f} ft²"
    return f"{value:.1f} m²"

# ============================================================
# SIDEBAR + NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("### 🌿 RANDOM V3")
    st.markdown(f"**👤 {username}**")
    # XP Bar
    lvl = user_data.get("level", 1)
    xp = user_data.get("xp", 0)
    needed = xp_for_level(lvl)
    progress = xp / needed if needed > 0 else 1.0
    st.markdown(f"""
    <div class="xp-container">
        <span style="font-size:12px; color:#86efac;">LVL {lvl}</span>
        <div class="xp-bar-bg">
            <div class="xp-bar-fill" style="width:{progress*100}%;"></div>
        </div>
        <span style="font-size:10px; color:#9ca3af;">{xp}/{needed} XP</span>
    </div>
    """, unsafe_allow_html=True)
    
    nav = st.radio(
        "Navigation",
        ["Dashboard", "Random Copilot", "Concepts", "Comparison", "2D Plans", "3D Viewer", "Reports", "Memory", "Settings"]
    )
    st.session_state.page = nav
    st.divider()
    
    # Admin panel
    if user_data.get("role") == "admin":
        with st.expander("🛡️ Admin Panel"):
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
    
    st.markdown("### 📁 PROJECT MEMORY")
    for proj in memory["projects"][-5:]:
        col1, col2 = st.columns([3,2])
        col1.markdown(f"**{proj['name']}**")
        col2.markdown(f"<span style='color:#6b7280;font-size:0.8rem;'>{proj['date']}</span>", unsafe_allow_html=True)
    
    if st.button("➕ New Project", use_container_width=True):
        new_name = f"Project {len(memory['projects'])+1}"
        memory["projects"].append({"name": new_name, "date": datetime.now().strftime("%b %d, %Y")})
        save_memory(username, memory)
        st.rerun()
    
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        save_memory(username, memory)
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_data = None
        st.session_state.memory = DEFAULT_MEMORY.copy()
        st.session_state.generated_concepts = []
        st.rerun()

# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "Dashboard":
    st.markdown('<div class="banner"><h1>Welcome back, Architect 🌿</h1><p>Create. Evolve. Perfect.</p></div>', unsafe_allow_html=True)
    
    if not st.session_state.generated_concepts:
        with st.spinner("Generating 5 unique design concepts..."):
            st.session_state.generated_concepts = generate_concepts(5)
            # Award XP for generation
            leveled_up = add_xp(username, 10)
            st.session_state.user_data = get_user(username)
            if leveled_up:
                st.balloons()
    
    concepts = st.session_state.generated_concepts
    if len(concepts) < 5:
        concepts.extend(generate_concepts(5 - len(concepts)))
        st.session_state.generated_concepts = concepts
    
    st.markdown("## 🔬 EVOLUTION ENGINE RESULTS")
    st.markdown("*5 unique design concepts generated and evaluated by AI Agents*")
    
    for idx, design in enumerate(concepts[:5]):
        score = design.get("score", 0)
        name = f"Concept {['Alpha','Beta','Gamma','Delta','Epsilon'][idx]}"
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown(f"**{idx+1}. {name}**")
        col2.markdown(f"<div class='concept-score'>{score}</div>", unsafe_allow_html=True)
        col3.progress(score/100)
    
    st.divider()
    
    best = concepts[0]
    fitness = best.get("fitness", evaluate_design(best))
    agent_scores = {
        "Architect AI": {"sub": "Function & Aesthetics", "score": int((fitness["Structural Score"]+fitness["Spatial Score"])/2)},
        "Structural AI": {"sub": "Safety & Stability", "score": fitness["Structural Score"]},
        "Sustainability AI": {"sub": "Green & Efficiency", "score": fitness["Sustainability Score"]},
        "Cost AI": {"sub": "Budget & Value", "score": fitness["Economic Score"]}
    }
    
    st.markdown("### 🤖 AI AGENT EVALUATION SUMMARY")
    cols = st.columns(4)
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
            plan_img = generate_floor_plan(best, floor_index=0)
            if plan_img:
                st.image(plan_img, use_column_width=True)
            else:
                st.info("Plan generation failed.")
        else:
            st.info("No floor data available.")
    
    with col_right:
        st.markdown("### 🏗️ 3D MASSING – CONCEPT ALPHA")
        if best.get("floors"):
            fig_3d = build_3d_figure(best, floor_index=0)
            st.plotly_chart(fig_3d, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No 3D data.")
    
    st.divider()
    st.markdown("### 💡 DESIGN INSIGHTS")
    st.write("Concept Alpha offers the best balance of structural efficiency, spatial quality, sustainability and cost.")
    st.markdown("<div class='recommendation-badge'>Concept Alpha</div>", unsafe_allow_html=True)

elif st.session_state.page == "Random Copilot":
    st.markdown("## 🧠 Random Copilot")
    building = st.selectbox("Building Typology", sum(ARCHITECTURE_TYPES.values(), []))
    modules = st.slider("Modules", 1, 10, 4)
    num_floors = st.slider("Number of Floors", 1, 5, 2)
    generations = st.slider("Evolution Cycles", 2, 30, 8)
    population = st.slider("Population", 4, 40, 12)
    
    if st.button("🚀 Generate Design"):
        with st.spinner("Evolving..."):
            best_design, history = evolve_design(building, modules, generations, population, num_floors)
            st.success(f"Design {best_design['id']} created!")
            st.session_state.generated_concepts.insert(0, best_design)
            if len(st.session_state.generated_concepts) > 10:
                st.session_state.generated_concepts = st.session_state.generated_concepts[:10]
            # XP for design generation
            leveled_up = add_xp(username, 20)
            st.session_state.user_data = get_user(username)
            if leveled_up:
                st.balloons()
            # Save to memory
            memory["projects"].append({"name": best_design["building"], "date": datetime.now().strftime("%b %d, %Y")})
            save_memory(username, memory)
            st.json({k: best_design[k] for k in ["id","building","area","score","fitness"]})
            st.line_chart(history)

elif st.session_state.page == "Concepts":
    st.markdown("## 📋 Concepts")
    if not st.session_state.generated_concepts:
        st.info("No concepts yet. Visit Dashboard or Copilot.")
    else:
        for i, design in enumerate(st.session_state.generated_concepts):
            with st.expander(f"Concept {i+1} – {design['building']} (Score: {design.get('score',0)})"):
                col1, col2 = st.columns([1,2])
                with col1:
                    if design.get("floors"):
                        plan_img = generate_floor_plan(design, floor_index=0)
                        if plan_img:
                            st.image(plan_img, caption="Floor 1")
                with col2:
                    st.json({k: design[k] for k in ["id","building","area","num_floors","cost","score","fitness"]})

elif st.session_state.page == "Comparison":
    st.markdown("## 🔄 Design Comparison")
    concepts = st.session_state.generated_concepts
    if len(concepts) < 2:
        st.warning("Need at least two concepts to compare.")
    else:
        names = [f"{d['building']} ({d['id']})" for d in concepts]
        left_idx = st.selectbox("Design A", range(len(names)), format_func=lambda x: names[x], key="comp_a")
        right_idx = st.selectbox("Design B", range(len(names)), format_func=lambda x: names[x], key="comp_b")
        if left_idx == right_idx:
            st.info("Select two different designs.")
        else:
            a = concepts[left_idx]
            b = concepts[right_idx]
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(names[left_idx])
                st.metric("Score", a["score"])
                st.write("Area:", area_display(a["area"]))
                st.write("Floors:", a["num_floors"])
                if a.get("floors"):
                    st.image(generate_floor_plan(a, 0), use_column_width=True)
            with col2:
                st.subheader(names[right_idx])
                st.metric("Score", b["score"])
                st.write("Area:", area_display(b["area"]))
                st.write("Floors:", b["num_floors"])
                if b.get("floors"):
                    st.image(generate_floor_plan(b, 0), use_column_width=True)
            categories = list(a["fitness"].keys())
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[a["fitness"][c] for c in categories],
                theta=categories,
                fill='toself',
                name=f'A: {a["building"]}'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[b["fitness"][c] for c in categories],
                theta=categories,
                fill='toself',
                name=f'B: {b["building"]}'
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])))
            st.plotly_chart(fig_radar, use_container_width=True)

elif st.session_state.page == "2D Plans":
    st.markdown("## 🗺️ 2D Floor Plans")
    if not st.session_state.generated_concepts:
        st.info("No designs loaded.")
    else:
        designs = st.session_state.generated_concepts
        design_names = [f"{d.get('building','')} - {d.get('id','')}" for d in designs]
        chosen = st.selectbox("Select design", range(len(designs)), format_func=lambda x: design_names[x])
        design = designs[chosen]
        if "floors" not in design:
            st.warning("This design has no detailed floors.")
        else:
            floor_count = len(design["floors"])
            floor_idx = st.slider("Floor", 0, floor_count-1, 0)
            img_data = generate_floor_plan(design, floor_idx)
            if img_data:
                st.image(img_data, caption=f"Floor {design['floors'][floor_idx]['level']}", use_column_width=True)
            else:
                st.error("Could not render plan.")

elif st.session_state.page == "3D Viewer":
    st.markdown("## 🏗️ 3D BIM Viewer")
    if not st.session_state.generated_concepts:
        st.info("No designs loaded.")
    else:
        designs = st.session_state.generated_concepts
        design_names = [f"{d.get('building','')} - {d.get('id','')}" for d in designs]
        chosen = st.selectbox("Select design", range(len(designs)), format_func=lambda x: design_names[x], key="3d_sel")
        design = designs[chosen]
        if "floors" not in design:
            st.warning("No 3D data.")
        else:
            floor_count = len(design["floors"])
            floor_idx = st.slider("Floor", 0, floor_count-1, 0, key="3d_floor")
            fig = build_3d_figure(design, floor_idx)
            st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == "Reports":
    st.markdown("## 📊 Design Report")
    if not st.session_state.generated_concepts:
        st.info("No designs available.")
    else:
        designs = st.session_state.generated_concepts
        design_names = [f"{d.get('building','')} ({d.get('id','')})" for d in designs]
        chosen = st.selectbox("Choose design", range(len(designs)), format_func=lambda x: design_names[x])
        design = designs[chosen]
        st.subheader(f"Report for {design['building']}")
        st.write("**ID:**", design["id"])
        st.write("**Area:**", area_display(design["area"]))
        st.write("**Floors:**", design["num_floors"])
        st.write("**Overall Score:**", design.get("score", "N/A"))
        st.markdown("### Agent Scores")
        if "fitness" in design:
            df = pd.DataFrame(design["fitness"].items(), columns=["Agent", "Score"])
            fig_bar = px.bar(df, x="Agent", y="Score", color="Score", range_y=[0,100])
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("### Floor Plans")
        for i in range(len(design.get("floors",[]))):
            plan_img = generate_floor_plan(design, i)
            if plan_img:
                st.image(plan_img, caption=f"Floor {design['floors'][i]['level']}", width=500)
        json_str = json.dumps(design, indent=4)
        st.download_button("📥 Download Design JSON", json_str, file_name=f"{design['id']}.json", mime="application/json")

elif st.session_state.page == "Memory":
    st.markdown("## 🧠 Memory & Saved Designs")
    st.subheader("Saved Designs")
    if not memory["saved_designs"]:
        st.info("No saved designs yet.")
    else:
        for idx, saved in enumerate(memory["saved_designs"]):
            with st.expander(f"{saved.get('building','')} - {saved.get('id','')} (Score: {saved.get('score','')})"):
                st.json(saved)
                if st.button(f"Delete {saved['id']}", key=f"del_{idx}"):
                    memory["saved_designs"].pop(idx)
                    save_memory(username, memory)
                    st.rerun()
    
    st.divider()
    st.subheader("Save Current Best Concept")
    if st.session_state.generated_concepts:
        best = st.session_state.generated_concepts[0]
        if st.button(f"Save {best.get('id','')}"):
            memory["saved_designs"].append(best)
            save_memory(username, memory)
            st.success("Saved to memory!")
    else:
        st.info("Generate concepts first.")

elif st.session_state.page == "Settings":
    st.markdown("## ⚙️ Settings")
    unit = st.selectbox("Unit System", ["Metric", "Imperial", "Dual"], index=0)
    st.session_state.unit_system = unit
    st.success("Settings updated.")

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="footer"><span>AI Powered</span> · <span>Data Driven</span> · <span>Secure</span> · <span>Scalable</span></div>', unsafe_allow_html=True)
