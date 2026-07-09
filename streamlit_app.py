# ============================================================
# RANDOM Evolution Studio – AI-Powered Architectural Design
# ============================================================

import streamlit as st
import json, uuid, random, hashlib
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io, numpy as np, math, base64, struct

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(page_title="RANDOM Studio", page_icon="🏗️", layout="wide")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "random_users.json"
FONT = ImageFont.load_default()
XP_PER_LEVEL = 100

# ============================================================
# LUXURIOUS DARK THEME
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, .stApp {
    background: radial-gradient(circle at top, #0a0f14, #05080c);
    font-family: 'Inter', sans-serif;
    color: #e0e5eb;
}
h1, h2, h3, h4, h5, h6 { font-weight: 600; color: #f0f4f8; letter-spacing: -0.5px; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1319, #080b10);
    border-right: 1px solid #2a2f38;
    box-shadow: inset -4px 0 12px rgba(0,0,0,0.3);
}
.glass-card {
    background: rgba(20, 25, 35, 0.7);
    backdrop-filter: blur(16px);
    border-radius: 24px;
    padding: 1.8rem;
    border: 1px solid rgba(74, 222, 128, 0.15);
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    margin-bottom: 1.5rem;
}
.logo-text {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #22c55e, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.stButton > button {
    background: linear-gradient(135deg, #22c55e, #059669);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.7rem 2rem;
    font-weight: 600;
    transition: all 0.3s;
    box-shadow: 0 6px 20px rgba(34,197,94,0.25);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(34,197,94,0.4);
}
.xp-container { display: flex; align-items: center; gap: 10px; margin-bottom: 1.2rem; }
.xp-bar-bg { flex: 1; height: 10px; background: #1e293b; border-radius: 6px; overflow: hidden; }
.xp-bar-fill { height: 100%; background: linear-gradient(90deg, #22c55e, #4ade80); border-radius: 6px; box-shadow: 0 0 10px #4ade80; }
.footer { text-align: center; padding: 1.5rem 0; color: #5f6b7a; font-size: 0.8rem; border-top: 1px solid #2a2f38; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# AUTH HELPERS
# ============================================================
def hash_password(pw: str) -> str:
    return hashlib.sha256((pw + "random_salt_42").encode()).hexdigest()

def load_users() -> list:
    if USER_FILE.exists():
        try:
            with open(USER_FILE) as f:
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
# MEMORY
# ============================================================
def get_memory_path(username: str) -> Path:
    return DATA_DIR / f"{username}_random_memory.json"

DEFAULT_MEMORY = {"projects": [], "saved_designs": [], "logs": []}

def load_memory(username: str) -> dict:
    path = get_memory_path(username)
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for key in DEFAULT_MEMORY:
                if key not in data:
                    data[key] = DEFAULT_MEMORY[key]
            return data
        except:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(username: str, memory: dict):
    with open(get_memory_path(username), "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

# ============================================================
# ARCHITECTURAL STANDARDS
# ============================================================
ARCHITECTURE_TYPES = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse"],
    "Commercial": ["Boutique Office", "Corporate Hub", "Hotel Resort", "Medical Clinic"],
    "Industrial": ["Distribution Warehouse", "Manufacturing Facility"]
}

def get_domain(name):
    for dom, items in ARCHITECTURE_TYPES.items():
        if name in items:
            return dom
    return "General"

MIN_ROOM_SIZES = {
    "living": 16, "kitchen": 8, "dining": 10,
    "bedroom": 10, "bathroom": 4, "study": 8,
    "office": 10, "meeting": 12, "reception": 8,
    "hall": 6, "corridor": 1.5*1.2, "storage": 4
}
DOOR_WIDTHS = {"main": 0.9, "interior": 0.8, "bathroom": 0.75}
WINDOW_RATIO = 0.15
STRUCTURAL_GRID = 4.0
ROOM_TYPES = {
    "Residential": ["living","kitchen","dining","bedroom","bathroom","corridor","study"],
    "Commercial": ["office","meeting","reception","kitchen","bathroom","corridor"],
    "Industrial": ["hall","storage","bathroom","office"]
}
FLOORING_OPTS = ["tiles","wood","concrete","carpet","marble"]
CEILING_OPTS = ["flat","hanging","vaulted","exposed","coffered"]

# ============================================================
# DESIGN GENERATOR
# ============================================================
def _assign_room_types(domain, count, building):
    if domain == "Residential":
        ess = ["living","kitchen","bathroom"]
        if "Villa" in building: ess.append("dining")
        types = ess[:count] if count <= len(ess) else ess + random.choices(
            ["bedroom","study","corridor","bathroom"], k=count-len(ess))
    elif domain == "Commercial":
        ess = ["office","bathroom","corridor"]
        if "Hotel" in building: ess = ["reception","bathroom","corridor","bedroom"]
        types = ess[:count] if count <= len(ess) else ess + random.choices(
            ["meeting","kitchen","office"], k=max(0, count-len(ess)))
    else:
        ess = ["hall","bathroom","storage"]
        types = ess[:count] if count <= len(ess) else ess + random.choices(
            ["office","hall"], k=max(0, count-len(ess)))
    return types[:count]

def _create_walls(w, d):
    return [
        {"start":(0,0),"end":(w,0),"thickness":0.3},
        {"start":(w,0),"end":(w,d),"thickness":0.3},
        {"start":(w,d),"end":(0,d),"thickness":0.3},
        {"start":(0,d),"end":(0,0),"thickness":0.3}
    ]

def _place_columns(w, d, enforce):
    cols = [{"center":(0,0),"size":0.3,"shape":"square"},
            {"center":(w,0),"size":0.3,"shape":"square"},
            {"center":(0,d),"size":0.3,"shape":"square"},
            {"center":(w,d),"size":0.3,"shape":"square"}]
    if enforce:
        for x in np.arange(STRUCTURAL_GRID, w, STRUCTURAL_GRID):
            for y in np.arange(STRUCTURAL_GRID, d, STRUCTURAL_GRID):
                if x < w-0.5 and y < d-0.5:
                    cols.append({"center":(x,y),"size":0.25,"shape":"circle"})
    else:
        for x in np.linspace(w*0.3, w*0.7, max(2, int(w/5))):
            cols.append({"center":(x, d/2),"size":0.25,"shape":"circle"})
    return cols

def _place_beams(w, d):
    return [{"start":(0,0.2),"end":(w,0.2),"width":0.2},
            {"start":(0,d-0.2),"end":(w,d-0.2),"width":0.2}]

def create_floor_layout(lvl, btype, total_area, modules, floor_area, n_rooms, n_doors, n_windows, enforce):
    if floor_area is None:
        floor_area = total_area / (modules*0.5+1)
    side = int(math.sqrt(floor_area)) + 1
    w = max(6, min(side, 20))
    d = max(6, min(side, 20))
    if enforce:
        w = max(STRUCTURAL_GRID, round(w/STRUCTURAL_GRID)*STRUCTURAL_GRID)
        d = max(STRUCTURAL_GRID, round(d/STRUCTURAL_GRID)*STRUCTURAL_GRID)

    domain = get_domain(btype)
    if n_rooms is None: n_rooms = 4
    room_types = _assign_room_types(domain, n_rooms, btype)

    # compute widths
    min_widths = []
    for rt in room_types:
        min_a = MIN_ROOM_SIZES.get(rt, 8)
        mw = 1.5 if rt=="corridor" else max(2.0, math.sqrt(min_a))
        min_widths.append(mw)
    total_min = sum(min_widths) + 0.2*len(room_types)
    avail = w
    if total_min > avail:
        scale = avail / total_min
        min_widths = [mw*scale for mw in min_widths]
    else:
        extra = (avail - total_min) / len(room_types)
        min_widths = [mw+extra for mw in min_widths]

    rooms = []
    cum_x = 0.0
    for i, rt in enumerate(room_types):
        rw = min_widths[i]
        if cum_x+rw > w: rw = w - cum_x
        if rw < 1.5: break
        poly = [(cum_x,0),(cum_x+rw,0),(cum_x+rw,d),(cum_x,d)]
        rooms.append({
            "name": f"{rt.capitalize()} {i+1}",
            "type": rt,
            "polygon": poly,
            "openings": [],
            "flooring": random.choice(FLOORING_OPTS),
            "ceiling": random.choice(CEILING_OPTS),
            "ceiling_height": 2.7
        })
        cum_x += rw

    # doors & windows
    for room in rooms:
        door_type = "main" if room["type"] in ["living","office","meeting","reception"] else "interior"
        if room["type"]=="bathroom": door_type="bathroom"
        room["openings"].append({"type":"door","wall":random.choice(["north","south","east","west"]),
                                 "width":DOOR_WIDTHS[door_type],"door_type":door_type})
        if room["type"] not in ("corridor","bathroom","storage"):
            ww = min(room["polygon"][1][0]-room["polygon"][0][0]*0.6, 2.0)
            room["openings"].append({"type":"window","wall":"south","width":ww})

    walls = _create_walls(w,d)
    int_walls = []
    cur_x = 0
    for room in rooms:
        if cur_x > 0:
            int_walls.append({"start":(cur_x,0),"end":(cur_x,d),"thickness":0.2})
        cur_x += room["polygon"][1][0]-room["polygon"][0][0]
    walls.extend(int_walls)
    cols = _place_columns(w,d,enforce)
    beams = _place_beams(w,d)
    return {"level":lvl,"height":3.0,"rooms":rooms,"walls":walls,"columns":cols,"beams":beams,"slab":{"thickness":0.2}}

def generate_design(building, modules, num_floors=None, enforce=True):
    if num_floors is None: num_floors = random.randint(1,3)
    total_area = 100 + modules*25
    floor_area = total_area / num_floors
    floors = []
    for lvl in range(1, num_floors+1):
        floor = create_floor_layout(lvl, building, total_area, modules, floor_area, None, None, None, enforce)
        if floor: floors.append(floor)
    return {"id":str(uuid.uuid4())[:8].upper(),"building":building,"domain":get_domain(building),
            "modules":modules,"floors":floors,"area":total_area,"num_floors":num_floors,"cost":0}

# ============================================================
# EVOLUTION ENGINE
# ============================================================
def mutate(design):
    child = json.loads(json.dumps(design))
    for floor in child["floors"]:
        if random.random()<0.3:
            floor["columns"].append({"center":(random.uniform(1,5),random.uniform(1,5)),"size":0.25,"shape":"circle"})
        if random.random()<0.3:
            floor["beams"].append({"start":(0,random.uniform(0.5,5)),"end":(random.uniform(4,8),random.uniform(0.5,5)),"width":0.2})
    child["cost"] = int(child["area"] * random.randint(1400,2800))
    return child

def evaluate_design(design):
    return {"Structural Score":80,"Economic Score":80,"Spatial Score":80,"Sustainability Score":80,"Code Compliance Score":80}

def total_score(metrics):
    return int(sum(metrics.values())/len(metrics))

def evolve_design_multi(building, modules, gens, pop, num_floors=None, enforce=True):
    def make(): return generate_design(building, modules, num_floors, enforce)
    population = [make() for _ in range(pop)]
    history = []
    for gen in range(gens):
        for d in population:
            d["fitness"] = evaluate_design(d)
            d["score"] = total_score(d["fitness"])
        population.sort(key=lambda x: x["score"], reverse=True)
        history.append(population[0]["score"])
        survivors = population[:pop//2]
        next_pop = []
        for parent in survivors:
            next_pop.append(parent)
            next_pop.append(mutate(parent))
        population = next_pop[:pop]
    for d in population:
        d["fitness"] = evaluate_design(d)
        d["score"] = total_score(d["fitness"])
    return population[0], history, population

# ============================================================
# 2D RENDERING (wall‑aware openings)
# ============================================================
def draw_opening(draw, poly, opening, scale, tx_func):
    wall = opening.get("wall","south")
    wid = opening.get("width",0.9)
    if wall == "north":
        p1, p2 = poly[0], poly[1]
    elif wall == "south":
        p1, p2 = poly[3], poly[2]
    elif wall == "east":
        p1, p2 = poly[1], poly[2]
    else:  # west
        p1, p2 = poly[0], poly[3]
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    length = math.hypot(dx, dy)
    if length == 0: return
    start_frac = 0.5 - (wid/length)/2
    if start_frac < 0: start_frac = 0
    sx = p1[0] + dx * start_frac
    sy = p1[1] + dy * start_frac
    ex = sx + dx * (wid/length)
    ey = sy + dy * (wid/length)
    s = tx_func(sx, sy)
    e = tx_func(ex, ey)
    if opening["type"] == "door":
        draw.line([s, e], fill=(255,255,255), width=6)
        mid = ((s[0]+e[0])//2, (s[1]+e[1])//2)
        draw.arc([mid[0]-8,mid[1]-8,mid[0]+8,mid[1]+8], 0, 90, fill=(0,0,0))
    else:
        draw.line([s, e], fill=(255,255,255), width=6)
        draw.line([s, e], fill=(34,197,94), width=3)

def generate_floor_plan(design, floor_index=0, scale=35):
    if floor_index >= len(design.get("floors",[])): return None
    floor = design["floors"][floor_index]
    all_pts = []
    for wall in floor["walls"]:
        all_pts.extend([wall["start"], wall["end"]])
    for col in floor["columns"]:
        all_pts.append(col["center"])
    if not all_pts: return None
    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    margin = 1.5
    wp = int((max_x-min_x+2*margin)*scale) + 60
    hp = int((max_y-min_y+2*margin)*scale) + 60
    img = Image.new('RGB', (wp, hp), color=(245,245,245))
    draw = ImageDraw.Draw(img)

    def tx(x, y):
        return ((x-min_x+margin)*scale+30, (y-min_y+margin)*scale+30)

    draw.rectangle([tx(min_x, min_y), tx(max_x, max_y)], outline=(150,150,150), width=2)
    for wall in floor["walls"]:
        p1, p2 = tx(*wall["start"]), tx(*wall["end"])
        thick = max(2, int(wall.get("thickness",0.25)*scale))
        draw.line([p1,p2], fill=(40,40,40), width=thick)
    for col in floor["columns"]:
        c = tx(*col["center"])
        size = max(2, int(col["size"]*scale))
        if col.get("shape")=="circle":
            draw.ellipse([c[0]-size,c[1]-size,c[0]+size,c[1]+size], fill=(100,100,100))
        else:
            draw.rectangle([c[0]-size,c[1]-size,c[0]+size,c[1]+size], fill=(100,100,100))
    for beam in floor["beams"]:
        p1, p2 = tx(*beam["start"]), tx(*beam["end"])
        draw.line([p1,p2], fill=(255,180,0), width=5)

    room_colors = {
        "living":(200,240,200),"kitchen":(255,245,200),"dining":(240,230,200),
        "bedroom":(180,230,180),"bathroom":(210,190,230),"corridor":(235,240,235),
        "office":(200,235,200),"meeting":(220,200,240),"reception":(190,220,190),
        "hall":(210,210,190),"storage":(200,200,200),"study":(230,220,240)
    }
    for room in floor["rooms"]:
        poly = [tx(x,y) for (x,y) in room["polygon"]]
        color = room_colors.get(room.get("type",""), (210,230,210))
        draw.polygon(poly, fill=color, outline=(80,80,80))
        if poly:
            cx = sum(p[0] for p in poly)/len(poly)
            cy = sum(p[1] for p in poly)/len(poly)
            draw.text((cx-20,cy-5), room["name"][:10], fill=(0,0,0), font=FONT)
        for op in room.get("openings",[]):
            draw_opening(draw, room["polygon"], op, scale, tx)

    draw.text((10,5), f"Floor {floor['level']} - {design.get('building','')}", fill=(20,20,20))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ============================================================
# 3D STACKED VIEWER (full implementation)
# ============================================================
def cuboid_mesh(x0,y0,z0,dx,dy,dz):
    x = [x0,x0+dx,x0+dx,x0,x0,x0+dx,x0+dx,x0]
    y = [y0,y0,y0+dy,y0+dy,y0,y0,y0+dy,y0+dy]
    z = [z0,z0,z0,z0,z0+dz,z0+dz,z0+dz,z0+dz]
    i = [0,0,4,4,0,1,5,4,1,2,6,5,2,3,7,6,3,0,4,7,1,0,3,2]
    j = [1,3,5,7,1,5,6,5,2,6,7,6,3,7,4,7,0,4,5,4,0,3,2,1]
    k = [3,2,7,6,4,4,5,5,6,5,6,6,7,6,7,7,7,5,4,4,3,2,1,0]
    return x,y,z,i,j,k

def cylinder_mesh(cx,cy,zb,zt,radius,n=12):
    theta = np.linspace(0,2*np.pi,n,endpoint=False)
    xb = cx+radius*np.cos(theta)
    yb = cy+radius*np.sin(theta)
    xt, yt = xb, yb
    zb_arr = np.full_like(xb,zb)
    zt_arr = np.full_like(xt,zt)
    x = np.concatenate([xb,xt])
    y = np.concatenate([yb,yt])
    z = np.concatenate([zb_arr,zt_arr])
    i,j,k = [],[],[]
    for idx in range(n):
        nxt = (idx+1)%n
        i.extend([idx,nxt,n+nxt,n+idx])
        j.extend([nxt,n+nxt,n+nxt,n+idx])
        k.extend([n+nxt,n+idx,n+idx,nxt])
    return x,y,z,i,j,k

def build_3d_stacked_figure(design):
    fig = go.Figure()
    for fi, floor in enumerate(design["floors"]):
        z_base = fi * floor.get("height",3.0)
        z_top = z_base + floor.get("height",3.0)
        slab_thick = floor.get("slab",{}).get("thickness",0.2)
        all_x = [p[0] for wall in floor["walls"] for p in (wall["start"],wall["end"])]
        all_y = [p[1] for wall in floor["walls"] for p in (wall["start"],wall["end"])]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        x,y,z,i,j,k = cuboid_mesh(min_x, min_y, z_base, max_x-min_x, max_y-min_y, slab_thick)
        fig.add_trace(go.Mesh3d(x=x,y=y,z=z,i=i,j=j,k=k,color=f'hsl({fi*60},60%,50%)',opacity=0.3,name=f'Slab F{floor["level"]}'))

        for wall in floor["walls"]:
            sx,sy = wall["start"]; ex,ey = wall["end"]
            dx = ex-sx; dy = ey-sy; length = np.sqrt(dx**2+dy**2)
            angle = np.arctan2(dy,dx); thick = wall.get("thickness",0.25)
            wx,wy,wz,iw,jw,kw = cuboid_mesh(sx, sy-thick/2, z_base, length, thick, z_top-z_base)
            wx, wy = np.array(wx)-sx, np.array(wy)-sy
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            rotx = wx*cos_a - wy*sin_a; roty = wx*sin_a + wy*cos_a
            wx = rotx + sx; wy = roty + sy
            fig.add_trace(go.Mesh3d(x=wx,y=wy,z=wz,i=iw,j=jw,k=kw,color='tan',opacity=0.7,showlegend=False))

        for col in floor["columns"]:
            cx,cy = col["center"]; radius = col["size"]/2
            xc,yc,zc,ic,jc,kc = cylinder_mesh(cx,cy,z_base,z_top,radius)
            fig.add_trace(go.Mesh3d(x=xc,y=yc,z=zc,i=ic,j=jc,k=kc,color='grey',opacity=0.8,showlegend=False))

        beam_z_base = z_top - slab_thick - 0.4
        for beam in floor["beams"]:
            sx,sy = beam["start"]; ex,ey = beam["end"]
            dx = ex-sx; dy = ey-sy; length = np.sqrt(dx**2+dy**2); angle = np.arctan2(dy,dx)
            bw = beam.get("width",0.2); bh = 0.4
            bx,by,bz,ib,jb,kb = cuboid_mesh(sx, sy-bw/2, beam_z_base, length, bw, bh)
            bx, by = np.array(bx)-sx, np.array(by)-sy
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            rotx = bx*cos_a - by*sin_a; roty = bx*sin_a + by*cos_a
            bx = rotx + sx; by = roty + sy
            fig.add_trace(go.Mesh3d(x=bx,y=by,z=bz,i=ib,j=jb,k=kb,color='seagreen',opacity=0.6,showlegend=False))

        cx = (min_x+max_x)/2; cy = (min_y+max_y)/2
        fig.add_trace(go.Scatter3d(x=[cx],y=[cy],z=[z_top+0.2],mode='text',text=[f"Floor {floor['level']}"],
                                   textfont=dict(size=14,color='white'),showlegend=False))

    fig.update_layout(scene=dict(xaxis=dict(visible=False),yaxis=dict(visible=False),zaxis=dict(visible=False),
                                 aspectmode='data',camera=dict(eye=dict(x=1.5,y=1.5,z=1.2))),
                      margin=dict(l=0,r=0,t=30,b=0),height=600,title="3D Stacked View")
    return fig

# ============================================================
# EXPORT FUNCTIONS
# ============================================================
def export_ifc(design):
    # minimal IFC (same as earlier)
    lines = ["ISO-10303-21;","HEADER;","FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');",
             "FILE_NAME('','',(''),(''),'RANDOM','','');","FILE_SCHEMA(('IFC2X3'));","ENDSEC;","DATA;"]
    return "\n".join(lines)

def design_to_glb(design):
    # minimal GLB placeholder
    verts = [0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0]; inds = [0,1,2]
    vbin = struct.pack(f'<{len(verts)}f',*verts); ibin = struct.pack(f'<{len(inds)}H',*inds)
    try:
        from pygltflib import GLTF2, Buffer, BufferView, Accessor, Mesh, Primitive, Node, Scene, Asset, ELEMENT_ARRAY_BUFFER, ARRAY_BUFFER, FLOAT, UNSIGNED_SHORT
    except:
        return None
    gltf = GLTF2(); gltf.asset = Asset(version="2.0")
    buf = Buffer(byteLength=len(vbin)+len(ibin)); gltf.buffers.append(buf)
    bv1 = BufferView(buffer=0,byteOffset=0,byteLength=len(vbin),target=ARRAY_BUFFER)
    bv2 = BufferView(buffer=0,byteOffset=len(vbin),byteLength=len(ibin),target=ELEMENT_ARRAY_BUFFER)
    gltf.bufferViews.extend([bv1,bv2])
    acc1 = Accessor(bufferView=0,byteOffset=0,componentType=FLOAT,count=len(verts)//3,type="VEC3",max=[1,1,0],min=[0,0,0])
    acc2 = Accessor(bufferView=1,byteOffset=0,componentType=UNSIGNED_SHORT,count=len(inds),type="SCALAR",max=[2],min=[0])
    gltf.accessors.extend([acc1,acc2])
    prim = Primitive(attributes={"POSITION":0},indices=1)
    mesh = Mesh(primitives=[prim]); gltf.meshes.append(mesh)
    node = Node(mesh=0); gltf.nodes.append(node)
    scene = Scene(nodes=[0]); gltf.scenes.append(scene); gltf.scene = 0
    gltf.binary_blob = vbin+ibin
    return gltf.save_to_bytes()

# ============================================================
# ROOM EDITOR (Enhanced)
# ============================================================
def render_room_editor(design):
    if "floors" not in design:
        st.warning("No floor data."); return

    floor_idx = st.selectbox("Floor", range(len(design["floors"])),
                             format_func=lambda i: f"Floor {design['floors'][i]['level']}")
    floor = design["floors"][floor_idx]
    room_names = [f"{r['name']} ({r['type']})" for r in floor["rooms"]]
    selected = st.selectbox("Select room", room_names)
    if selected is None: return
    room_idx = room_names.index(selected)
    room = floor["rooms"][room_idx]

    st.markdown("---")
    st.subheader(f"✏️ Editing: {room['name']}")
    c1, c2 = st.columns(2)
    with c1:
        new_width = st.number_input("Width (m)", 1.0, 20.0,
                                    float(room["polygon"][1][0]-room["polygon"][0][0]))
    with c2:
        domain = get_domain(design["building"])
        rtypes = ROOM_TYPES.get(domain, ["office","meeting","bathroom","corridor"])
        new_type = st.selectbox("Type", rtypes,
                                index=rtypes.index(room["type"]) if room["type"] in rtypes else 0)
    c3, c4 = st.columns(2)
    with c3:
        new_flooring = st.selectbox("Flooring", FLOORING_OPTS,
                                    index=FLOORING_OPTS.index(room.get("flooring","wood")) if room.get("flooring") in FLOORING_OPTS else 0)
    with c4:
        new_ceiling = st.selectbox("Ceiling", CEILING_OPTS,
                                   index=CEILING_OPTS.index(room.get("ceiling","flat")) if room.get("ceiling") in CEILING_OPTS else 0)

    st.markdown("#### Openings (doors & windows)")
    openings = room.get("openings", [])
    for i, op in enumerate(openings):
        cols = st.columns([2,2,2,1])
        op_type = cols[0].selectbox("Type", ["door","window"], index=0 if op["type"]=="door" else 1, key=f"optype_{i}")
        wall = cols[1].selectbox("Wall", ["north","south","east","west"],
                                 index=["north","south","east","west"].index(op.get("wall","south")), key=f"opwall_{i}")
        width_val = cols[2].number_input("Width (m)", 0.5, 3.0, float(op.get("width",0.9)), 0.1, key=f"opwidth_{i}")
        if op_type == "door":
            door_style = cols[0].selectbox("Style", ["main","interior","bathroom"],
                                           index=["main","interior","bathroom"].index(op.get("door_type","interior")),
                                           key=f"opdoor_{i}")
        if cols[3].button("🗑", key=f"opdel_{i}"):
            openings.pop(i)
            st.rerun()
        # update in place
        op["type"] = op_type
        op["wall"] = wall
        op["width"] = width_val
        if op_type == "door":
            op["door_type"] = door_style

    if st.button("➕ Add Opening"):
        openings.append({"type":"door","wall":"south","width":0.9,"door_type":"interior"})
        st.rerun()

    if st.button("💾 Apply Room Changes"):
        old_w = room["polygon"][1][0]-room["polygon"][0][0]
        scale = new_width / old_w
        for i in range(len(room["polygon"])):
            x,y = room["polygon"][i]
            room["polygon"][i] = (x*scale, y)
        room["type"] = new_type
        room["flooring"] = new_flooring
        room["ceiling"] = new_ceiling
        st.success("Room updated!")

    st.markdown("---")
    col_add, col_del = st.columns(2)
    with col_add:
        new_name = st.text_input("New room name")
        new_rt = st.selectbox("Type for new room", rtypes, key="new_room_type")
        if st.button("➕ Add Room") and new_name:
            last_x = floor["rooms"][-1]["polygon"][1][0] if floor["rooms"] else 0
            w = 3.0
            d = floor["walls"][2]["end"][1]
            poly = [(last_x,0),(last_x+w,0),(last_x+w,d),(last_x,d)]
            floor["rooms"].append({"name":new_name,"type":new_rt,"polygon":poly,"openings":[],"flooring":"wood","ceiling":"flat"})
            st.rerun()
    with col_del:
        if st.button("🗑 Delete This Room") and len(floor["rooms"])>1:
            floor["rooms"].pop(room_idx)
            st.rerun()

    st.markdown("### Current Floor Plan")
    st.image(generate_floor_plan(design, floor_idx), use_column_width=True)

# ============================================================
# SESSION INIT
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.memory = DEFAULT_MEMORY.copy()
    st.session_state.page = "Random Copilot"
    st.session_state.generated_concepts = []
    st.session_state.unit_system = "Metric"

if not load_users():
    create_user("admin", "admin123", role="admin")

# ============================================================
# LOGIN PAGE (beautiful)
# ============================================================
if not st.session_state.logged_in:
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("<div style='text-align:center;margin-top:4rem;'><span class='logo-text'>🏗️ RANDOM</span></div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;color:#94a3b8;font-size:1.1rem;'>Evolutionary AI Design Studio</p>", unsafe_allow_html=True)
            with st.form("auth_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                colA, colB = st.columns(2)
                with colA:
                    login_btn = st.form_submit_button("Login")
                with colB:
                    register_btn = st.form_submit_button("Register")
                if login_btn:
                    user = authenticate(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_data = user
                        st.session_state.memory = load_memory(username)
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                if register_btn:
                    if not username or not password:
                        st.error("Fill all fields.")
                    else:
                        try:
                            create_user(username, password)
                            st.success("Account created! You can now log in.")
                        except ValueError as e:
                            st.error(str(e))
    st.stop()

# ============================================================
# LOGGED IN – SIDEBAR (clean, with logo)
# ============================================================
username = st.session_state.username
user_data = st.session_state.user_data
memory = st.session_state.memory

with st.sidebar:
    st.markdown("<div class='logo-text' style='font-size:1.8rem;'>🏗️ RANDOM</div>", unsafe_allow_html=True)
    st.markdown(f"**👤 {username}**")
    lvl = user_data.get("level",1)
    xp = user_data.get("xp",0)
    needed = xp_for_level(lvl)
    progress = xp/needed if needed>0 else 1.0
    st.markdown(f"""
    <div class="xp-container">
        <span style="font-size:12px;color:#94a3b8;">LVL {lvl}</span>
        <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{progress*100}%;"></div></div>
        <span style="font-size:10px;color:#64748b;">{xp}/{needed} XP</span>
    </div>""", unsafe_allow_html=True)

    page = st.radio("Go to", ["Random Copilot","2D Plans","Room Editor","3D Viewer","Reports","Memory","Settings"])
    st.session_state.page = page

    st.divider()
    if user_data.get("role")=="admin":
        with st.expander("🛡️ Admin"):
            for u in load_users():
                if u["username"] != username:
                    if st.button(f"🗑 {u['username']}", key=f"del_{u['username']}"):
                        users = load_users()
                        users.remove(u)
                        save_users(users)
                        st.rerun()

    st.markdown("### Design Log")
    for proj in memory["projects"][-5:]:
        st.markdown(f"• {proj['name']} *({proj['date']})*")
    if st.button("➕ New Project"):
        memory["projects"].append({"name":f"Project {len(memory['projects'])+1}","date":datetime.now().strftime("%b %d, %Y")})
        save_memory(username, memory)
        st.rerun()

    if st.button("🚪 Logout"):
        save_memory(username, memory)
        for key in ["logged_in","username","user_data","memory","generated_concepts"]:
            if key in st.session_state: del st.session_state[key]
        st.rerun()

# ============================================================
# PAGE ROUTING
# ============================================================
page = st.session_state.page

if page == "Random Copilot":
    st.markdown("<div style='text-align:center;margin-bottom:2rem;'><h1>🧠 Random Copilot</h1><p style='color:#94a3b8;'>Define your building, evolve, and let AI create the perfect design.</p></div>", unsafe_allow_html=True)
    cat = st.radio("Category", list(ARCHITECTURE_TYPES.keys()), horizontal=True)
    bld = st.selectbox("Building Type", ARCHITECTURE_TYPES[cat])
    col1, col2 = st.columns(2)
    with col1:
        floors = st.slider("Floors", 1,5,2)
        modules = st.slider("Complexity", 1,10,4)
    with col2:
        gens = st.slider("Evolution Cycles", 2,30,8)
        pop = st.slider("Population", 4,40,12)
    enforce = st.checkbox("Enforce Architectural Standards", value=True)
    if st.button("🚀 Generate Design"):
        with st.spinner("Evolving... the perfect structure awaits."):
            best, history, _ = evolve_design_multi(bld, modules, gens, pop, num_floors=floors, enforce=enforce)
            st.success(f"Design **{best['id']}** created!")
            st.session_state.generated_concepts = [best]
            add_xp(username, 20)
            st.session_state.user_data = get_user(username)
            memory["projects"].append({"name": best["building"], "date": datetime.now().strftime("%b %d, %Y")})
            save_memory(username, memory)
            st.json({k:best[k] for k in ["id","building","area","score","fitness"]})
            st.line_chart(history)

elif page == "2D Plans":
    if not st.session_state.generated_concepts:
        st.info("No design yet. Generate one in Random Copilot.")
    else:
        design = st.session_state.generated_concepts[0]
        if design.get("floors"):
            floor_idx = st.slider("Floor", 0, len(design["floors"])-1, 0)
            img = generate_floor_plan(design, floor_idx)
            if img: st.image(img, use_column_width=True)

elif page == "Room Editor":
    if not st.session_state.generated_concepts:
        st.info("No design yet.")
    else:
        design = st.session_state.generated_concepts[0]
        render_room_editor(design)

elif page == "3D Viewer":
    if not st.session_state.generated_concepts:
        st.info("No design yet.")
    else:
        design = st.session_state.generated_concepts[0]
        if design.get("floors"):
            fig = build_3d_stacked_figure(design)
            st.plotly_chart(fig, use_container_width=True)

elif page == "Reports":
    if not st.session_state.generated_concepts:
        st.info("No design yet.")
    else:
        design = st.session_state.generated_concepts[0]
        st.subheader(f"📄 {design['building']}")
        for i, floor in enumerate(design["floors"]):
            with st.expander(f"Floor {floor['level']}"):
                for room in floor["rooms"]:
                    w = room["polygon"][1][0]-room["polygon"][0][0]
                    d = room["polygon"][3][1]-room["polygon"][0][1]
                    st.write(f"**{room['name']}** – {room['type']}, Area: {w*d:.1f}m², Floor: {room.get('flooring','wood')}, Ceiling: {room.get('ceiling','flat')}")
        st.download_button("📥 Download JSON", json.dumps(design, indent=4), file_name=f"{design['id']}.json")
        if st.button("📐 Export IFC"):
            st.download_button("⬇️ IFC", export_ifc(design), file_name=f"{design['id']}.ifc")
        if st.button("🧊 Export glTF"):
            glb = design_to_glb(design)
            if glb: st.download_button("⬇️ GLB", glb, file_name=f"{design['id']}.glb")

elif page == "Memory":
    if not memory["saved_designs"]:
        st.info("No saved designs yet.")
    else:
        for i, saved in enumerate(memory["saved_designs"]):
            with st.expander(f"{saved.get('building','')} – {saved.get('id','')}"):
                st.json(saved)
                if st.button(f"Delete {saved['id']}", key=f"memdel_{i}"):
                    memory["saved_designs"].pop(i)
                    save_memory(username, memory)
                    st.rerun()
    if st.session_state.generated_concepts:
        best = st.session_state.generated_concepts[0]
        if st.button(f"Save {best['id']} to Memory"):
            memory["saved_designs"].append(best)
            save_memory(username, memory)
            st.success("Design saved!")

elif page == "Settings":
    st.markdown("## ⚙️ Settings")
    unit = st.selectbox("Unit System", ["Metric","Imperial","Dual"])
    st.session_state.unit_system = unit
    st.success("Settings updated.")

# Footer
st.markdown('<div class="footer">AI Powered · Data Driven · Secure · Scalable</div>', unsafe_allow_html=True)
