# ============================================================
# RANDOM – AI Architectural Engineering & Construction Studio
# Improved Specification Studio + South Sudanese Pounds (SSP)
# ============================================================
import streamlit as st
import json, uuid, hashlib, math, random
from pathlib import Path
from datetime import datetime
import pandas as pd

# ---------- CONFIG ----------
st.set_page_config(page_title="RANDOM Studio", page_icon="⚡", layout="wide")
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "users.json"
XP_PER_LEVEL = 100
SPEC_FILE = DATA_DIR / "specs.json"
if not SPEC_FILE.exists():
    SPEC_FILE.write_text("[]")

# ---------- THEME ----------
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html,body,.stApp{background:radial-gradient(circle at top,#0a0f14,#05080c);font-family:'Inter',sans-serif;color:#e0e5eb}
h1,h2,h3,h4,h5,h6{font-weight:600;color:#f0f4f8;letter-spacing:-0.5px}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f1319,#080b10);border-right:1px solid #2a2f38;box-shadow:inset -4px 0 12px rgba(0,0,0,0.3)}
.logo-text{font-size:2.4rem;font-weight:700;background:linear-gradient(135deg,#fbbf24,#f97316);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.5rem}
.stButton>button{background:linear-gradient(135deg,#fbbf24,#f97316);color:#0f172a;border:none;border-radius:14px;padding:0.7rem 2rem;font-weight:600;transition:all 0.3s;box-shadow:0 6px 20px rgba(251,191,36,0.25)}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(251,191,36,0.4)}
.xp-container{display:flex;align-items:center;gap:10px;margin-bottom:1.2rem}
.xp-bar-bg{flex:1;height:10px;background:#1e293b;border-radius:6px;overflow:hidden}
.xp-bar-fill{height:100%;background:linear-gradient(90deg,#fbbf24,#f97316);border-radius:6px;box-shadow:0 0 10px #f97316}
.footer{text-align:center;padding:1.5rem 0;color:#5f6b7a;font-size:0.8rem;border-top:1px solid #2a2f38}
</style>""", unsafe_allow_html=True)

# ---------- AUTH ----------
def hash_password(pw): return hashlib.sha256((pw+"rand_salt").encode()).hexdigest()
def load_users():
    if USER_FILE.exists():
        try:
            with open(USER_FILE) as f: return json.load(f)
        except: return []
    return []
def save_users(users):
    with open(USER_FILE,"w") as f: json.dump(users,f,indent=2)
def get_user(uname):
    for u in load_users():
        if u["username"]==uname: return u
    return None
def create_user(uname,pw,role="user"):
    users=load_users()
    if get_user(uname): raise ValueError("Username exists")
    user={"username":uname,"password_hash":hash_password(pw),"role":role,"level":1,"xp":0,"badges":[],"created":datetime.now().isoformat()}
    users.append(user); save_users(users)
    return user
def authenticate(uname,pw):
    u=get_user(uname)
    if u and u["password_hash"]==hash_password(pw): return u
    return None
def update_user_data(uname,updates):
    users=load_users()
    for u in users:
        if u["username"]==uname: u.update(updates); break
    save_users(users)
def xp_for_level(lvl): return lvl*XP_PER_LEVEL
def add_xp(uname,amount):
    u=get_user(uname)
    if not u: return False
    old=u["level"]; u["xp"]+=amount
    while u["xp"]>=xp_for_level(u["level"]):
        u["xp"]-=xp_for_level(u["level"]); u["level"]+=1
        if u["level"]%5==0 and f"level_{u['level']}" not in u["badges"]:
            u["badges"].append(f"level_{u['level']}")
    update_user_data(uname,{"level":u["level"],"xp":u["xp"],"badges":u["badges"]})
    return u["level"]>old

# ---------- MEMORY ----------
def get_memory_path(uname): return DATA_DIR/f"{uname}_memory.json"
DEFAULT_MEMORY={"projects":[],"saved_designs":[],"logs":[]}
def load_memory(uname):
    path=get_memory_path(uname)
    if path.exists():
        try:
            with open(path,encoding="utf-8") as f: data=json.load(f)
            for k in DEFAULT_MEMORY:
                if k not in data: data[k]=DEFAULT_MEMORY[k]
            return data
        except: return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()
def save_memory(uname,mem):
    with open(get_memory_path(uname),"w",encoding="utf-8") as f: json.dump(mem,f,indent=4)

# ---------- SESSION INIT ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False; st.session_state.username=None
    st.session_state.user_data=None; st.session_state.memory=DEFAULT_MEMORY.copy()
    st.session_state.page="Specification Studio"; st.session_state.unit_system="Metric"

if not load_users():
    create_user("admin","admin123",role="admin")

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        st.markdown("<div class='logo-text' style='text-align:center;margin-top:4rem;'>⚡ RANDOM</div>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#94a3b8;'>AI Architectural Engineering & Construction Studio</p>",unsafe_allow_html=True)
        with st.form("auth"):
            uname=st.text_input("Username"); pw=st.text_input("Password",type="password")
            colA,colB=st.columns(2)
            with colA: login_btn=st.form_submit_button("Login")
            with colB: reg_btn=st.form_submit_button("Register")
            if login_btn:
                user=authenticate(uname,pw)
                if user:
                    st.session_state.logged_in=True; st.session_state.username=uname
                    st.session_state.user_data=user; st.session_state.memory=load_memory(uname)
                    st.rerun()
                else: st.error("Invalid credentials")
            if reg_btn:
                if not uname or not pw: st.error("Fill all fields")
                else:
                    try:
                        create_user(uname,pw); st.success("Account created!")
                    except ValueError as e: st.error(str(e))
    st.stop()

# ---------- SIDEBAR ----------
uname=st.session_state.username; user_data=st.session_state.user_data; memory=st.session_state.memory
with st.sidebar:
    st.markdown("<div class='logo-text' style='font-size:1.8rem;'>⚡ RANDOM</div>",unsafe_allow_html=True)
    st.markdown(f"**👤 {uname}**")
    lvl=user_data["level"]; xp=user_data["xp"]; needed=xp_for_level(lvl)
    progress=xp/needed if needed>0 else 1.0
    st.markdown(f"""<div class="xp-container"><span style="font-size:12px;color:#94a3b8;">LVL {lvl}</span>
    <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{progress*100}%;"></div></div>
    <span style="font-size:10px;color:#64748b;">{xp}/{needed} XP</span></div>""",unsafe_allow_html=True)
    page = st.radio("Go to", [
        "Specification Studio",
        "Architecture Spaces",
        "Engineering",
        "Construction",
        "Ram Assistant",
        "Roofing",
        "Materials & Cost",
        "Diagnostics",
        "Saved Specs",
        "Settings"
    ])
    st.session_state.page = page
    unit_choice = st.selectbox("Units", ["Metric", "Imperial"], index=0 if st.session_state.unit_system=="Metric" else 1)
    st.session_state.unit_system = unit_choice
    st.divider()
    if user_data.get("role")=="admin":
        with st.expander("🛡️ Admin"):
            for u in load_users():
                if u["username"]!=uname:
                    if st.button(f"🗑 {u['username']}",key=f"del_{u['username']}"):
                        users=load_users(); users.remove(u); save_users(users); st.rerun()
    st.markdown("### 📁 Recent")
    for proj in memory["projects"][-5:]:
        st.markdown(f"• {proj['name']} *({proj['date']})*")
    if st.button("➕ New Project"):
        memory["projects"].append({"name":f"Project {len(memory['projects'])+1}","date":datetime.now().strftime("%b %d, %Y")})
        save_memory(uname,memory); st.rerun()
    if st.button("🚪 Logout"):
        save_memory(uname,memory)
        for k in ["logged_in","username","user_data","memory"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

# ---------- UNIT HELPERS ----------
IMPERIAL_LENGTH = 3.28084
IMPERIAL_AREA = 10.7639

def fmt_length(val, unit='Metric'):
    if unit == 'Imperial': return f"{val*IMPERIAL_LENGTH:.1f} ft"
    return f"{val:.2f} m"
def fmt_area(val, unit='Metric'):
    if unit == 'Imperial': return f"{val*IMPERIAL_AREA:.0f} ft²"
    return f"{val:.1f} m²"

# ============================================================
# DEFAULT SPEC (extended with gridline_ref)
# ============================================================
DEFAULT_ROOM = {"name":"Living Room","type":"living","width":6.0,"length":5.0,"height":3.0,
                "flooring":"wood","ceiling":"flat","bulbs":4,"sockets":6,"switches":2,
                "furniture":[{"item":"Sofa","w":2.0,"d":1.0,"h":0.9}]}

if "spec" not in st.session_state:
    st.session_state.spec = {
        "building_name": "",
        "category": "Residential",
        "shape": "Rectangle",
        "floors": 2,
        "floor_height": 3.0,
        "plot_length": 30.0,
        "plot_width": 25.0,
        "setback_front": 5.0,
        "setback_back": 3.0,
        "setback_left": 2.0,
        "setback_right": 2.0,
        "overall_length": 20.0,
        "overall_width": 15.0,
        "grid": {"spacing_x":6.0,"spacing_y":6.0,"column_size":0.4,"gridline_ref":"Centerline"},
        "exterior_wall": "Cavity Brick (280mm)",
        "interior_wall": "Brick Partition (115mm)",
        "plaster_exterior": "Cement Plaster + Paint (20mm)",
        "plaster_interior": "Gypsum Plaster + Paint (15mm)",
        "foundation": "Strip Foundation",
        "foundation_depth": 1.2,
        "soil_type": "Clay",
        "column_type": "RC Rectangular 300x300mm",
        "beam_type": "RC 230x300mm",
        "roof_type": "Pitched",
        "roof_material": "Concrete Tiles",
        "roof_pitch": 30,
        "flooring": "tiles",
        "ceiling": "flat",
        "rooms": [DEFAULT_ROOM],
        "doors": [{"type":"Main Entrance","width":1.0,"height":2.1,"wall":"south","height_above_floor":0.0,"material":"Wood"}],
        "windows": [{"type":"Sliding","width":1.5,"height":1.2,"wall":"north","height_above_floor":0.9,"glazing":"Double"}],
        "stairs":{"count":1,"type":"U-shaped","width":1.2},
        "lifts":{"count":0,"type":"Passenger","capacity":8},
        "hvac": "Natural Ventilation",
        "orientation": "South",
        "wind_direction": "North",
        "mep_details":{"plumbing_fixtures_per_floor":4,"electrical_load_per_sqm":50},
        "east_africa_country": "Uganda",
        "labour_rate_per_day": 15,
    }

# ---------- EAST AFRICAN MATERIALS (includes SSP) ----------
EA_MATERIALS = {
    "Cement (50kg bag)": {"USD": 8, "UGX": 29000, "KES": 1100, "TZS": 20000, "RWF": 9000, "SSP": 12000},
    "Steel Rebar (ton)": {"USD": 800, "UGX": 2900000, "KES": 110000, "TZS": 2000000, "RWF": 900000, "SSP": 1200000},
    "Concrete Blocks (1000 units)": {"USD": 250, "UGX": 900000, "KES": 34000, "TZS": 600000, "RWF": 270000, "SSP": 375000},
    "Timber (m³)": {"USD": 300, "UGX": 1100000, "KES": 41000, "TZS": 750000, "RWF": 330000, "SSP": 450000},
    "Roofing Sheets (per m²)": {"USD": 5, "UGX": 18000, "KES": 680, "TZS": 12000, "RWF": 5500, "SSP": 7500},
}
EA_COUNTRIES = {"Uganda":"UGX", "Kenya":"KES", "Tanzania":"TZS", "Rwanda":"RWF", "South Sudan":"SSP", "USD reference":"USD"}

def get_ea_cost(material, country, quantity=1):
    curr = EA_COUNTRIES.get(country, "UGX")
    base = EA_MATERIALS.get(material, {"USD":10,"UGX":36000,"KES":1300,"TZS":24000,"RWF":11000,"SSP":15000})
    cost = base.get(curr, base["USD"])
    return cost * quantity

# ---------- SPEC SAVING ----------
def save_spec(spec):
    data = json.loads(SPEC_FILE.read_text())
    spec["id"] = str(uuid.uuid4())[:8].upper()
    spec["created"] = datetime.now().isoformat()
    data.append(spec)
    SPEC_FILE.write_text(json.dumps(data, indent=2))
def load_specs():
    return json.loads(SPEC_FILE.read_text())

# ---------- RAM AI ----------
def ram_advisor(query: str, spec: dict) -> str:
    q = query.lower()
    if "floorplan" in q or "layout" in q:
        return generate_floorplan_text(spec)
    if "cost" in q or "estimate" in q:
        area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
        cost = area * 1500
        return f"Estimated construction cost: ${cost:,.0f} (based on {area:.0f} m² at $1500/m²)."
    if "standard" in q:
        return f"According to East African standards, minimum room sizes: Living 20m², Bedroom 12m², Bathroom 5m². Corridor width ≥ 1.2m."
    if "material" in q:
        return f"Recommended materials: {spec['exterior_wall']} for exterior, {spec['interior_wall']} for interior."
    if "schedule" in q:
        return f"For a {spec['floors']}-storey building, a realistic timeline is {spec['floors']*4} – {spec['floors']*6} months."
    return "I can help with floorplans, cost estimation, standards checking, material suggestions, and scheduling. Please be specific."

def generate_floorplan_text(spec):
    rooms = spec["rooms"]
    grid_x = spec["grid"]["spacing_x"]
    grid_y = spec["grid"]["spacing_y"]
    cols = int(spec["overall_length"] / grid_x)
    rows = int(spec["overall_width"] / grid_y)
    if cols<1 or rows<1: return "Grid too small for building footprint."
    plan = [["--" for _ in range(cols)] for _ in range(rows)]
    for room in rooms:
        rw = max(1, int(room["width"] / grid_x))
        rl = max(1, int(room["length"] / grid_y))
        placed = False
        for attempt in range(20):
            x = random.randint(0, cols-rw)
            y = random.randint(0, rows-rl)
            free = True
            for i in range(x, x+rw):
                for j in range(y, y+rl):
                    if plan[j][i] != "--":
                        free = False; break
                if not free: break
            if free:
                for i in range(x, x+rw):
                    for j in range(y, y+rl):
                        plan[j][i] = room["name"][:2].center(2)
                placed = True; break
        if not placed:
            for y in range(rows):
                for x in range(cols):
                    if plan[y][x] == "--":
                        plan[y][x] = room["name"][:2].center(2); placed = True; break
                if placed: break
    plan_str = "\n".join([" ".join(row) for row in plan])
    return f"Suggested layout based on your grid ({grid_x}m x {grid_y}m):\n```\n{plan_str}\n```"

# ============================================================
# PAGE ROUTING
# ============================================================
page = st.session_state.page
unit = st.session_state.unit_system
spec = st.session_state.spec

if page == "Specification Studio":
    st.title("⚡ RANDOM – Specification Studio")
    st.markdown("Define every aspect of your building with detailed control over spaces, grids, doors, windows, and MEP.")

    # ---------- PROJECT IDENTITY ----------
    with st.expander("🏢 Project Identity & Shape", expanded=True):
        spec["building_name"] = st.text_input("Project Name", spec["building_name"])
        col1, col2, col3 = st.columns(3)
        spec["category"] = col1.selectbox("Building Category", ["Residential","Commercial","Industrial"], index=0)
        spec["shape"] = col2.selectbox("Building Shape", ["Rectangle","L-shape","T-shape","U-shape","Courtyard"], index=0)
        spec["floors"] = col3.slider("Number of Floors", 1, 50, spec["floors"])
        spec["floor_height"] = st.slider("Floor Height (m)", 2.4, 5.0, spec["floor_height"])

    # ---------- PLOT & SETBACKS ----------
    with st.expander("📐 Plot & Setbacks", expanded=False):
        col1, col2 = st.columns(2)
        spec["plot_length"] = col1.number_input("Plot Length (m)", 10.0,500.0, spec["plot_length"])
        spec["plot_width"] = col2.number_input("Plot Width (m)", 10.0,500.0, spec["plot_width"])
        col1, col2, col3, col4 = st.columns(4)
        spec["setback_front"] = col1.number_input("Front Setback (m)", 0.0,50.0, spec["setback_front"])
        spec["setback_back"] = col2.number_input("Rear Setback (m)", 0.0,50.0, spec["setback_back"])
        spec["setback_left"] = col3.number_input("Left Setback (m)", 0.0,50.0, spec["setback_left"])
        spec["setback_right"] = col4.number_input("Right Setback (m)", 0.0,50.0, spec["setback_right"])

    # ---------- BUILDING FOOTPRINT ----------
    with st.expander("📏 Building Footprint", expanded=False):
        col1, col2 = st.columns(2)
        spec["overall_length"] = col1.number_input("Overall Length (m)", 5.0, spec["plot_length"], spec["overall_length"])
        spec["overall_width"] = col2.number_input("Overall Width (m)", 5.0, spec["plot_width"], spec["overall_width"])

    # ---------- GRID SYSTEM & WALLS ----------
    with st.expander("🔲 Grid System & Walls", expanded=False):
        st.markdown("**Grid System**")
        col1, col2, col3 = st.columns(3)
        spec["grid"]["spacing_x"] = col1.number_input("Column Spacing X (m)", 3.0, 9.0, spec["grid"]["spacing_x"])
        spec["grid"]["spacing_y"] = col2.number_input("Column Spacing Y (m)", 3.0, 9.0, spec["grid"]["spacing_y"])
        spec["grid"]["column_size"] = col3.number_input("Column Size (m)", 0.3, 1.0, spec["grid"]["column_size"])
        spec["grid"]["gridline_ref"] = st.selectbox("Gridline Reference", ["Centerline", "Interior Face", "Exterior Face"],
                                                    index=0 if spec["grid"].get("gridline_ref","Centerline")=="Centerline" else 1)

        st.markdown("**Walls**")
        col1, col2 = st.columns(2)
        spec["exterior_wall"] = col1.selectbox("Exterior Wall Type", 
                                               ["Cavity Brick (280mm)","Solid Brick (230mm)","Concrete Block (200mm)",
                                                "AAC Block (200mm)","Timber Frame + Cladding","Steel Frame + Cladding"],
                                               index=0)
        spec["plaster_exterior"] = col1.selectbox("Exterior Finish",
                                                  ["Cement Plaster + Paint (20mm)","Gypsum Plaster + Paint (15mm)",
                                                   "Tile Cladding (10mm)","Stone Cladding (30mm)","Exposed Brick (no plaster)"])
        spec["interior_wall"] = col2.selectbox("Interior Partition Type",
                                               ["Brick Partition (115mm)","Concrete Block (100mm)",
                                                "Timber Stud + Plasterboard","Glass Partition"],
                                               index=0)
        spec["plaster_interior"] = col2.selectbox("Interior Finish",
                                                  ["Gypsum Plaster + Paint (15mm)","Cement Plaster + Paint (20mm)",
                                                   "Tile Cladding (10mm)","Exposed Brick (no plaster)"])

    # ---------- ROOMS ----------
    with st.expander("🛏️ Rooms & Spaces", expanded=True):
        for i, room in enumerate(spec["rooms"]):
            with st.container():
                st.markdown(f"**{room.get('name','Room')} ({room.get('type','living')})**")
                col1, col2, col3 = st.columns([2,2,1])
                room["name"] = col1.text_input("Name", room["name"], key=f"rname_{i}")
                room["type"] = col2.selectbox("Type", ["living","kitchen","dining","master_bedroom","bedroom",
                                                       "bathroom","storage","balcony","corridor"],
                                             key=f"rtype_{i}")
                room["width"] = col3.number_input("Width (m)", 1.0, 20.0, room["width"], key=f"rw_{i}")
                col4, col5, col6 = st.columns([1,1,1])
                room["length"] = col4.number_input("Length (m)", 1.0, 20.0, room["length"], key=f"rl_{i}")
                room["height"] = col5.number_input("Height (m)", 2.4, 5.0, room["height"], key=f"rh_{i}")
                room["flooring"] = col6.selectbox("Flooring", ["tiles","wood","concrete","marble","carpet"], key=f"rfloor_{i}")
                col7, col8 = st.columns(2)
                room["ceiling"] = col7.selectbox("Ceiling", ["flat","hanging","vaulted","exposed","coffered"], key=f"rceil_{i}")
                room["bulbs"] = col8.number_input("Bulbs", 0, 20, room.get("bulbs",2), key=f"rbulbs_{i}")
                room["sockets"] = col8.number_input("Sockets", 0, 20, room.get("sockets",2), key=f"rsock_{i}")
                room["switches"] = col8.number_input("Switches", 0, 20, room.get("switches",1), key=f"rsw_{i}")

                st.markdown("**Furniture**")
                furn = room.get("furniture",[])
                for j, item in enumerate(furn):
                    fcols = st.columns([3,1,1,1,1])
                    item["item"] = fcols[0].text_input("Item", item["item"], key=f"fitem_{i}_{j}")
                    item["w"] = fcols[1].number_input("W",0.1,5.0, item["w"], key=f"fw_{i}_{j}")
                    item["d"] = fcols[2].number_input("D",0.1,5.0, item["d"], key=f"fd_{i}_{j}")
                    item["h"] = fcols[3].number_input("H",0.1,3.0, item["h"], key=f"fh_{i}_{j}")
                    if fcols[4].button("❌", key=f"fdel_{i}_{j}"):
                        furn.pop(j); st.rerun()
                if st.button("➕ Add Furniture", key=f"fadd_{i}"):
                    furn.append({"item":"New","w":1.0,"d":0.5,"h":0.5}); st.rerun()
                if st.button("🗑 Delete Room", key=f"rdel_{i}"):
                    spec["rooms"].pop(i); st.rerun()
                st.markdown("---")
        if st.button("➕ Add New Room"):
            spec["rooms"].append({"name":"New Room","type":"living","width":4.0,"length":4.0,"height":3.0,
                                  "flooring":"wood","ceiling":"flat","bulbs":2,"sockets":2,"switches":1,"furniture":[]})
            st.rerun()

    # ---------- DOORS ----------
    with st.expander("🚪 Doors", expanded=False):
        for i, door in enumerate(spec["doors"]):
            cols = st.columns([2,1,1,1,1,1])
            door["type"] = cols[0].selectbox("Type", ["Main Entrance","Interior Door","Bathroom Door","Sliding Door"],
                                            index=["Main Entrance","Interior Door","Bathroom Door","Sliding Door"].index(door.get("type","Interior Door")),
                                            key=f"dtype_{i}")
            door["width"] = cols[1].number_input("Width (m)", 0.6,2.0, door["width"], key=f"dw_{i}")
            door["height"] = cols[2].number_input("Height (m)", 2.0,3.0, door["height"], key=f"dh_{i}")
            door["wall"] = cols[3].selectbox("Wall", ["north","south","east","west"], key=f"dwall_{i}")
            door["height_above_floor"] = cols[4].number_input("Sill (m)", 0.0,2.0, door.get("height_above_floor",0.0), key=f"dsill_{i}")
            door["material"] = cols[5].selectbox("Material", ["Wood","Steel","Glass","Aluminium"], key=f"dmat_{i}")
            if st.button("🗑", key=f"ddel_{i}"): spec["doors"].pop(i); st.rerun()
            st.markdown("---")
        if st.button("➕ Add Door"):
            spec["doors"].append({"type":"Interior Door","width":0.9,"height":2.1,"wall":"south","height_above_floor":0.0,"material":"Wood"})
            st.rerun()

    # ---------- WINDOWS ----------
    with st.expander("🪟 Windows", expanded=False):
        for i, win in enumerate(spec["windows"]):
            cols = st.columns([2,1,1,1,1,1])
            win["type"] = cols[0].selectbox("Type", ["Sliding","Casement","Fixed","Louvre"], key=f"wtype_{i}")
            win["width"] = cols[1].number_input("Width (m)", 0.6,3.0, win["width"], key=f"ww_{i}")
            win["height"] = cols[2].number_input("Height (m)", 0.6,2.5, win["height"], key=f"wh_{i}")
            win["wall"] = cols[3].selectbox("Wall", ["north","south","east","west"], key=f"wwall_{i}")
            win["height_above_floor"] = cols[4].number_input("Sill (m)", 0.0,2.0, win.get("height_above_floor",0.9), key=f"wsill_{i}")
            win["glazing"] = cols[5].selectbox("Glazing", ["Single","Double","Triple"], key=f"wglaz_{i}")
            if st.button("🗑", key=f"wdel_{i}"): spec["windows"].pop(i); st.rerun()
            st.markdown("---")
        if st.button("➕ Add Window"):
            spec["windows"].append({"type":"Sliding","width":1.2,"height":1.2,"wall":"north","height_above_floor":0.9,"glazing":"Double"})
            st.rerun()

    # ---------- MEP & ORIENTATION ----------
    with st.expander("🌬️ MEP, Sun & Wind", expanded=False):
        spec["hvac"] = st.selectbox("HVAC System", ["Natural Ventilation","Split AC Units","Central Chilled Water","VRV/VRF System","Hybrid"])
        col1, col2 = st.columns(2)
        spec["orientation"] = col1.selectbox("Sun Orientation (Front)", ["North","South","East","West"])
        spec["wind_direction"] = col2.selectbox("Prevailing Wind Direction", ["North","South","East","West"])
        spec["mep_details"]["plumbing_fixtures_per_floor"] = st.number_input("Plumbing Fixtures per Floor", 1,20, spec["mep_details"]["plumbing_fixtures_per_floor"])
        spec["mep_details"]["electrical_load_per_sqm"] = st.number_input("Electrical Load (VA/m²)", 30,200, spec["mep_details"]["electrical_load_per_sqm"])

    # ---------- SAVE & REPORT ----------
    if st.button("📄 Generate Specification Report"):
        save_spec(spec)
        # build report
        total_area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
        report = f"""
# Architectural Specification – {spec['building_name']}

## General
- Category: {spec['category']}
- Shape: {spec['shape']}
- Floors: {spec['floors']} × {fmt_length(spec['floor_height'], unit)} floor height
- Total height: {fmt_length(spec['floors']*spec['floor_height'], unit)}
- Plot: {fmt_length(spec['plot_length'], unit)} × {fmt_length(spec['plot_width'], unit)}
- Footprint: {fmt_length(spec['overall_length'], unit)} × {fmt_length(spec['overall_width'], unit)}
- Total floor area: {fmt_area(total_area, unit)}

## Grid & Walls
- Grid: {spec['grid']['spacing_x']}m × {spec['grid']['spacing_y']}m, column size {spec['grid']['column_size']}m
- Reference: {spec['grid']['gridline_ref']}
- Exterior: {spec['exterior_wall']} ({spec['plaster_exterior']})
- Interior: {spec['interior_wall']} ({spec['plaster_interior']})

## Rooms ({len(spec['rooms'])})
"""
        for r in spec['rooms']:
            area = r['width']*r['length']
            report += f"- {r['name']} ({r['type']}) {fmt_length(r['width'], unit)} × {fmt_length(r['length'], unit)} × {fmt_length(r['height'], unit)}, Area: {fmt_area(area, unit)}\n"
            report += f"  Floor: {r.get('flooring','wood')}, Ceiling: {r.get('ceiling','flat')}\n"
            report += f"  Bulbs: {r.get('bulbs',0)}, Sockets: {r.get('sockets',0)}, Switches: {r.get('switches',0)}\n"
            if r.get('furniture'):
                report += "  Furniture:\n"
                for f in r['furniture']:
                    report += f"    - {f['item']} ({fmt_length(f['w'], unit)} × {fmt_length(f['d'], unit)} × {fmt_length(f['h'], unit)})\n"
            report += "\n"
        report += f"""
## Doors ({len(spec['doors'])})
"""
        for d in spec['doors']:
            report += f"- {d['type']} {fmt_length(d['width'], unit)} × {fmt_length(d['height'], unit)}, Wall: {d.get('wall','south')}, Sill: {fmt_length(d.get('height_above_floor',0), unit)}, Material: {d.get('material','Wood')}\n"
        report += f"""
## Windows ({len(spec['windows'])})
"""
        for w in spec['windows']:
            report += f"- {w['type']} {fmt_length(w['width'], unit)} × {fmt_length(w['height'], unit)}, Wall: {w.get('wall','north')}, Sill: {fmt_length(w.get('height_above_floor',0.9), unit)}, Glazing: {w.get('glazing','Double')}\n"
        report += f"""
## MEP & Environment
- HVAC: {spec['hvac']}
- Plumbing fixtures/floor: {spec['mep_details']['plumbing_fixtures_per_floor']}
- Electrical load: {spec['mep_details']['electrical_load_per_sqm']} VA/m²
- Sun orientation: {spec['orientation']}
- Wind direction: {spec['wind_direction']}

## East African Material Costs (approximate)
"""
        for mat in EA_MATERIALS:
            cost_ssp = get_ea_cost(mat, "South Sudan", 1)
            report += f"- {mat}: {cost_ssp:,.0f} SSP (South Sudan)\n"
        report += "\n---\n*Generated by RANDOM Architectural Studio*\n"
        st.text_area("Specification Report", report, height=500)
        st.download_button("📥 Download JSON", json.dumps(spec, indent=2), file_name=f"{spec['building_name'] or 'spec'}.json")
        add_xp(uname,20); st.session_state.user_data=get_user(uname)

elif page == "Architecture Spaces":
    st.title("🏛️ Architecture – Spaces & Layouts")
    for room in spec["rooms"]:
        with st.expander(room["name"]):
            st.json(room)

elif page == "Engineering":
    st.title("⚙️ Engineering – Foundations & Structure")
    spec["soil_type"] = st.selectbox("Soil Type", ["Clay","Sand","Rock","Silt","Gravel"])
    spec["foundation"] = st.selectbox("Foundation Type", ["Strip Foundation","Raft Foundation","Pile Foundation"])
    spec["foundation_depth"] = st.number_input("Foundation Depth (m)", 0.5,20.0, spec["foundation_depth"])
    spec["column_type"] = st.text_input("Column Type", spec.get("column_type","RC Rectangular 300x300mm"))
    spec["beam_type"] = st.text_input("Beam Type", spec.get("beam_type","RC 230x300mm"))
    st.success("Engineering parameters updated.")

elif page == "Construction":
    st.title("🚧 Construction – Materials, Labour & Schedule")
    spec["labour_rate_per_day"] = st.number_input("Labour Rate (USD/day)", 5.0,100.0, spec.get("labour_rate_per_day",15.0))
    area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
    total_cost = area * 1500
    st.metric("Estimated Total Construction Cost (USD)", f"${total_cost:,.0f}")
    months = spec["floors"] * 4
    st.write(f"Rough schedule: **{months} months**")
    st.info("Visit Materials & Cost for detailed East African pricing with SSP.")

elif page == "Ram Assistant":
    st.title("🤖 AI Assistant – Ram")
    st.markdown("Ram generates floorplans, checks standards, estimates costs, and more.")
    user_query = st.text_area("Ask Ram:")
    if st.button("Ask"):
        answer = ram_advisor(user_query, spec)
        st.success(answer)
    st.caption("Try: 'generate floorplan', 'estimate cost', 'check standards', 'suggest materials'")

elif page == "Roofing":
    st.title("🏠 Roofing Design")
    spec["roof_type"] = st.selectbox("Roof Type", ["Flat","Pitched","Gable","Hip","Mansard","Gambrel","Butterfly"])
    spec["roof_material"] = st.selectbox("Roof Material", ["Concrete Tiles","Clay Tiles","Metal Sheets","Thatch","Green Roof","Slate"])
    spec["roof_pitch"] = st.slider("Roof Pitch (degrees)", 0, 60, spec.get("roof_pitch",30))
    st.success("Roofing parameters updated.")

elif page == "Materials & Cost":
    st.title("💰 East African Material Costs (including SSP)")
    country = st.selectbox("Country", list(EA_COUNTRIES.keys()))
    material = st.selectbox("Material", list(EA_MATERIALS.keys()))
    quantity = st.number_input("Quantity", 1.0, 10000.0, 1.0)
    cost = get_ea_cost(material, country, quantity)
    curr = EA_COUNTRIES[country]
    st.metric(f"Cost in {curr}", f"{cost:,.0f}")
    st.dataframe(pd.DataFrame(EA_MATERIALS).T)

elif page == "Diagnostics":
    st.title("🔍 Structural Diagnostics")
    cols_x = int(spec["overall_length"] / spec["grid"]["spacing_x"]) + 1
    cols_y = int(spec["overall_width"] / spec["grid"]["spacing_y"]) + 1
    total_cols = cols_x * cols_y * spec["floors"]
    total_beams = (cols_x*(cols_y-1) + cols_y*(cols_x-1)) * spec["floors"]
    area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
    alerts = []
    if total_cols < 16: alerts.append("🔴 Column density too low")
    if total_beams / max(1,total_cols) < 1.9: alerts.append("🔵 Beam‑column ratio imbalance")
    if not alerts: alerts = ["🟢 Design stable"]
    for a in alerts: st.write(a)
    st.table(pd.DataFrame([
        {"Item":"Concrete","Qty":f"{total_cols*2.6:.1f} m³"},
        {"Item":"Steel Rebar","Qty":f"{total_beams*0.48:.2f} MT"},
        {"Item":"CMU Blocks","Qty":f"{int(area*42):,} units"}
    ]))

elif page == "Saved Specs":
    st.title("📋 Saved Specifications")
    for s in load_specs():
        with st.expander(f"{s.get('building_name','Unnamed')} – {s.get('id','')}"):
            st.json(s)

elif page == "Settings":
    st.title("⚙️ Settings")
    if st.button("Delete All Saved Specs"):
        SPEC_FILE.write_text("[]")
        st.success("Cleared.")

st.markdown('<div class="footer">AI Powered · Data Driven · Secure · Scalable</div>', unsafe_allow_html=True)
