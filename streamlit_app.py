# ============================================================
# RANDOM – AI Architectural Specification Studio
# Full features: AI Assistant Ram, Layouts, Metric/Imperial, Plot, etc.
# ============================================================
import streamlit as st
import json, uuid, hashlib, math, random, textwrap
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

# ---------- UNIT CONVERTER ----------
IMPERIAL_LENGTH = 3.28084   # m -> ft
IMPERIAL_AREA = 10.7639

def convert_length(val, to_imperial=False):
    return val * IMPERIAL_LENGTH if to_imperial else val

def convert_area(val, to_imperial=False):
    return val * IMPERIAL_AREA if to_imperial else val

def fmt_length(val, unit='Metric'):
    if unit == 'Imperial':
        return f"{val*IMPERIAL_LENGTH:.1f} ft"
    return f"{val:.2f} m"

def fmt_area(val, unit='Metric'):
    if unit == 'Imperial':
        return f"{val*IMPERIAL_AREA:.0f} ft²"
    return f"{val:.1f} m²"

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
    st.session_state.page="Specification Studio"
    st.session_state.unit_system="Metric"

if not load_users():
    create_user("admin","admin123",role="admin")

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        st.markdown("<div class='logo-text' style='text-align:center;margin-top:4rem;'>⚡ RANDOM</div>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#94a3b8;'>AI Architectural Design Studio</p>",unsafe_allow_html=True)
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
    page = st.radio("Go to",["Specification Studio", "Layout Options", "AI Assistant Ram", "Diagnostics", "Saved Specs", "Settings"])
    st.session_state.page=page
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

# ============================================================
# ARCHITECTURAL DATA
# ============================================================
ROOM_STANDARDS = {
    "living": {"min_area":20, "min_width":4.0, "min_height":2.4},
    "kitchen": {"min_area":10, "min_width":2.4, "min_height":2.4},
    "dining": {"min_area":12, "min_width":3.0, "min_height":2.4},
    "master_bedroom": {"min_area":18, "min_width":4.0, "min_height":2.4},
    "bedroom": {"min_area":12, "min_width":3.0, "min_height":2.4},
    "bathroom": {"min_area":5, "min_width":2.0, "min_height":2.4},
    "storage": {"min_area":3, "min_width":1.5, "min_height":2.4},
    "balcony": {"min_area":4, "min_width":1.5, "min_height":2.7},
    "corridor": {"min_width":1.2, "min_height":2.4},
}
WALL_MATERIALS = {"Cavity Brick (280mm)":280,"Solid Brick (230mm)":230,"Concrete Block (200mm)":200,"AAC Block (200mm)":200,"Timber Frame + Cladding":150,"Steel Frame + Cladding":150}
INTERIOR_WALLS = {"Brick Partition (115mm)":115,"Concrete Block (100mm)":100,"Timber Stud + Plasterboard":90,"Glass Partition":12}
PLASTER_FINISHES = ["Cement Plaster + Paint (20mm)","Gypsum Plaster + Paint (15mm)","Tile Cladding (10mm)","Stone Cladding (30mm)","Exposed Brick (no plaster)"]
FOUNDATION_TYPES = {"Strip Foundation":{"min_depth":0.8},"Raft Foundation":{"depth":0.3},"Pile Foundation":{"min_depth":5.0,"diameter":0.6}}
HVAC_SYSTEMS = ["Natural Ventilation","Split AC Units","Central Chilled Water","VRV/VRF System","Hybrid"]
ORIENTATIONS = ["North","South","East","West"]

# ---------- SPEC SAVING ----------
def save_spec(spec):
    data = json.loads(SPEC_FILE.read_text())
    spec["id"] = str(uuid.uuid4())[:8].upper()
    spec["created"] = datetime.now().isoformat()
    data.append(spec)
    SPEC_FILE.write_text(json.dumps(data, indent=2))

def load_specs():
    return json.loads(SPEC_FILE.read_text())

# ---------- DIAGNOSTICS ----------
def structural_review(spec):
    cols_x = int(spec["overall_length"] / spec["grid"]["spacing_x"]) + 1
    cols_y = int(spec["overall_width"] / spec["grid"]["spacing_y"]) + 1
    total_cols = cols_x * cols_y * spec["floors"]
    total_beams = (cols_x*(cols_y-1) + cols_y*(cols_x-1)) * spec["floors"]
    area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
    alerts = []
    if total_cols < 16: alerts.append("🔴 Column density too low")
    if total_beams / max(1,total_cols) < 1.9: alerts.append("🔵 Beam-column ratio imbalance")
    if not alerts: alerts = ["🟢 Design structurally stable"]
    return alerts, total_cols, total_beams, area

def material_takeoffs(total_cols, total_beams, area):
    return [
        {"item":"Concrete","qty":f"{total_cols*2.6:.1f} m³"},
        {"item":"Steel Rebar","qty":f"{total_beams*0.48:.2f} MT"},
        {"item":"CMU Blocks","qty":f"{int(area*42):,} units"},
        {"item":"Dead Load","qty":f"{int(total_cols*13.2):,} kN"}
    ]

# ---------- AI ASSISTANT RAM ----------
def ram_advisor(query: str, spec: dict) -> str:
    """Simple rule‑based advisor that uses the current specification context."""
    q = query.lower()
    if "cost" in q or "estimate" in q:
        area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
        cost = area * 1500  # rough $/m²
        return f"Estimated construction cost: ${cost:,.0f} (based on {area:.0f} m² at $1500/m²)."
    if "schedule" in q or "timeline" in q:
        return f"For a {spec['floors']}-storey building, a realistic timeline is {spec['floors']*4} – {spec['floors']*6} months."
    if "material" in q:
        return f"Common materials: {spec['exterior_wall']} for exterior, {spec['interior_wall']} for interior. Consider using {spec['plaster_exterior']} for finish."
    if "size" in q and "room" in q:
        return "Minimum room sizes per standards: Living 20 m², Bedroom 12 m², Bathroom 5 m². I can adjust your rooms accordingly."
    return "I can help with cost estimates, material suggestions, scheduling, and size advice. Please be more specific."

# ---------- DEFAULT SPEC ----------
if "spec" not in st.session_state:
    st.session_state.spec = {
        "building_name": "",
        "plot_length": 30.0,
        "plot_width": 25.0,
        "setback_front": 5.0,
        "setback_back": 3.0,
        "setback_left": 2.0,
        "setback_right": 2.0,
        "floors": 2,
        "floor_height": 3.0,
        "overall_length": 20.0,
        "overall_width": 15.0,
        "grid": {"spacing_x":6.0,"spacing_y":6.0,"column_size":0.4},
        "exterior_wall": list(WALL_MATERIALS.keys())[0],
        "interior_wall": list(INTERIOR_WALLS.keys())[0],
        "plaster_exterior": PLASTER_FINISHES[0],
        "plaster_interior": PLASTER_FINISHES[1],
        "foundation": list(FOUNDATION_TYPES.keys())[0],
        "foundation_depth": 1.2,
        "flooring": "tiles",
        "ceiling": "flat",
        "rooms": [{"name":"Living Room","type":"living","width":6.0,"length":5.0,"height":3.0,"flooring":"wood","ceiling":"flat",
                   "bulbs":4,"sockets":6,"furniture":[{"item":"Sofa","w":2.0,"d":1.0,"h":0.9},{"item":"Coffee Table","w":1.2,"d":0.6,"h":0.5}]}],
        "doors": [{"type":"Main Entrance","width":1.0,"height":2.1,"wall":"south","height_above_floor":0.0,"material":"Wood"}],
        "windows": [{"type":"Sliding","width":1.5,"height":1.2,"wall":"north","height_above_floor":0.9,"glazing":"Double"}],
        "stairs":{"count":1,"type":"U-shaped","width":1.2},
        "lifts":{"count":0,"type":"Passenger","capacity":8},
        "hvac": HVAC_SYSTEMS[0],
        "orientation": "South",
        "wind_direction": "North",
        "mep_details":{"plumbing_fixtures_per_floor":4,"electrical_load_per_sqm":50},
    }

# ============================================================
# PAGE ROUTING
# ============================================================
page = st.session_state.page
unit = st.session_state.unit_system
to_imperial = unit == "Imperial"

if page == "Specification Studio":
    st.title("⚡ RANDOM – Specification Studio")
    spec = st.session_state.spec

    # AI quick‑generate
    st.markdown("### 🤖 Quick Generate (AI)")
    ai_desc = st.text_input("Describe your building (e.g., '3‑bedroom house with balcony')")
    if st.button("Generate"):
        # simple AI as before
        desc = ai_desc.lower()
        if "house" in desc or "villa" in desc:
            spec["building_name"] = "Residential House"
            spec["rooms"] = [
                {"name":"Living Room","type":"living","width":6,"length":5,"height":3,"flooring":"wood","ceiling":"flat","bulbs":4,"sockets":6,"furniture":[]},
                {"name":"Kitchen","type":"kitchen","width":4,"length":4,"height":3,"flooring":"tiles","ceiling":"flat","bulbs":2,"sockets":4,"furniture":[]},
                {"name":"Master Bedroom","type":"master_bedroom","width":5,"length":4,"height":3,"flooring":"wood","ceiling":"flat","bulbs":3,"sockets":5,"furniture":[{"item":"King Bed","w":2.0,"d":2.0,"h":1.2}]},
                {"name":"Bathroom","type":"bathroom","width":2,"length":2,"height":3,"flooring":"tiles","ceiling":"flat","bulbs":2,"sockets":2,"furniture":[]}
            ]
            if "3 bed" in desc: spec["rooms"].append({"name":"Bedroom 2","type":"bedroom","width":4,"length":3,"height":3,"flooring":"wood","ceiling":"flat","bulbs":2,"sockets":3,"furniture":[]})
            if "balcony" in desc: spec["rooms"].append({"name":"Balcony","type":"balcony","width":3,"length":2,"height":2.7,"flooring":"tiles","ceiling":"flat","bulbs":1,"sockets":1,"furniture":[]})
            spec["doors"] = [{"type":"Main Entrance","width":1.0,"height":2.1,"wall":"south","height_above_floor":0,"material":"Wood"}]
            spec["windows"] = [{"type":"Sliding","width":1.5,"height":1.2,"wall":"north","height_above_floor":0.9,"glazing":"Double"}]
        add_xp(uname,5); st.session_state.user_data=get_user(uname)
        st.rerun()

    # Editable specification fields
    col1, col2 = st.columns(2)
    spec["building_name"] = col1.text_input("Project Name", spec["building_name"])
    spec["floors"] = col2.slider("Number of Floors", 1, 30, spec["floors"])
    spec["floor_height"] = st.slider("Floor Height (m)", 2.4, 5.0, spec["floor_height"])

    st.subheader("Plot & Setbacks")
    c1,c2,c3,c4 = st.columns(4)
    spec["plot_length"] = c1.number_input("Plot Length (m)", 10.0,200.0, spec["plot_length"])
    spec["plot_width"] = c2.number_input("Plot Width (m)", 10.0,200.0, spec["plot_width"])
    spec["setback_front"] = c3.number_input("Front Setback (m)", 0.0,20.0, spec["setback_front"])
    spec["setback_back"] = c4.number_input("Rear Setback (m)", 0.0,20.0, spec["setback_back"])
    spec["setback_left"] = st.number_input("Left Setback (m)", 0.0,20.0, spec["setback_left"])
    spec["setback_right"] = st.number_input("Right Setback (m)", 0.0,20.0, spec["setback_right"])

    st.subheader("Building Footprint")
    c1,c2 = st.columns(2)
    spec["overall_length"] = c1.number_input("Length (m)", 5.0, spec["plot_length"], spec["overall_length"])
    spec["overall_width"] = c2.number_input("Width (m)", 5.0, spec["plot_width"], spec["overall_width"])

    st.subheader("Grid System")
    c1,c2,c3 = st.columns(3)
    spec["grid"]["spacing_x"] = c1.number_input("Col Spacing X (m)", 3.0,9.0, spec["grid"]["spacing_x"])
    spec["grid"]["spacing_y"] = c2.number_input("Col Spacing Y (m)", 3.0,9.0, spec["grid"]["spacing_y"])
    spec["grid"]["column_size"] = c3.number_input("Column Size (m)", 0.3,1.0, spec["grid"]["column_size"])

    st.subheader("Walls & Finishes")
    c1,c2 = st.columns(2)
    spec["exterior_wall"] = c1.selectbox("Exterior Wall", list(WALL_MATERIALS.keys()), index=list(WALL_MATERIALS.keys()).index(spec["exterior_wall"]))
    spec["plaster_exterior"] = c1.selectbox("Exterior Finish", PLASTER_FINISHES)
    spec["interior_wall"] = c2.selectbox("Interior Partition", list(INTERIOR_WALLS.keys()), index=list(INTERIOR_WALLS.keys()).index(spec["interior_wall"]))
    spec["plaster_interior"] = c2.selectbox("Interior Finish", PLASTER_FINISHES)

    st.subheader("Foundation")
    c1,c2 = st.columns(2)
    spec["foundation"] = c1.selectbox("Type", list(FOUNDATION_TYPES.keys()))
    spec["foundation_depth"] = c2.number_input("Depth (m)", 0.3,15.0, spec["foundation_depth"])

    st.subheader("Flooring & Ceiling Defaults")
    spec["flooring"] = st.selectbox("Global Flooring", ["tiles","wood","concrete","marble","carpet"])
    spec["ceiling"] = st.selectbox("Global Ceiling", ["flat","hanging","vaulted","exposed","coffered"])

    # ROOMS
    st.subheader("Rooms & Spaces")
    for i, room in enumerate(spec["rooms"]):
        with st.expander(f"{room.get('name','Room')} ({room.get('type','living')})"):
            cols = st.columns([3,2,1,1,1,1,1])
            room["name"] = cols[0].text_input("Name", room["name"], key=f"rname_{i}")
            room["type"] = cols[1].selectbox("Type", list(ROOM_STANDARDS.keys()), index=list(ROOM_STANDARDS.keys()).index(room["type"]) if room["type"] in ROOM_STANDARDS else 0, key=f"rtype_{i}")
            room["width"] = cols[2].number_input("W(m)", 1.0,20.0, room["width"], key=f"rw_{i}")
            room["length"] = cols[3].number_input("L(m)", 1.0,20.0, room["length"], key=f"rl_{i}")
            room["height"] = cols[4].number_input("H(m)", 2.4,5.0, room["height"], key=f"rh_{i}")
            room["flooring"] = cols[5].selectbox("Floor", ["tiles","wood","concrete","marble","carpet"], index=0 if room.get("flooring")=="wood" else 0, key=f"rfloor_{i}")
            room["ceiling"] = cols[6].selectbox("Ceil", ["flat","hanging","vaulted","exposed","coffered"], index=0 if room.get("ceiling")=="flat" else 0, key=f"rceil_{i}")
            room["bulbs"] = st.number_input("Bulbs", 0,20, room.get("bulbs",2), key=f"rbulbs_{i}")
            room["sockets"] = st.number_input("Sockets", 0,20, room.get("sockets",2), key=f"rsock_{i}")
            # furniture list
            st.markdown("**Furniture**")
            furn = room.get("furniture",[])
            for j, item in enumerate(furn):
                fc = st.columns([3,1,1,1,1])
                item["item"] = fc[0].text_input("Item", item["item"], key=f"fitem_{i}_{j}")
                item["w"] = fc[1].number_input("W",0.1,5.0, item["w"], key=f"fw_{i}_{j}")
                item["d"] = fc[2].number_input("D",0.1,5.0, item["d"], key=f"fd_{i}_{j}")
                item["h"] = fc[3].number_input("H",0.1,3.0, item["h"], key=f"fh_{i}_{j}")
                if fc[4].button("❌", key=f"fdel_{i}_{j}"):
                    furn.pop(j); st.rerun()
            if st.button("➕ Furniture", key=f"fadd_{i}"):
                furn.append({"item":"New","w":1.0,"d":0.5,"h":0.5})
                st.rerun()
            if st.button("🗑 Delete Room", key=f"rdel_{i}"):
                spec["rooms"].pop(i); st.rerun()
    if st.button("➕ Add Room"):
        spec["rooms"].append({"name":"New Room","type":"living","width":4.0,"length":4.0,"height":3.0,"flooring":"wood","ceiling":"flat","bulbs":2,"sockets":2,"furniture":[]})
        st.rerun()

    # DOORS
    st.subheader("Doors")
    for i, door in enumerate(spec["doors"]):
        with st.expander(f"Door {i+1} ({door.get('type','')})"):
            cols = st.columns([2,1,1,1,1,1])
            door["type"] = cols[0].selectbox("Type", ["Main Entrance","Interior Door","Bathroom Door","Sliding Door"],
                                            index=["Main Entrance","Interior Door","Bathroom Door","Sliding Door"].index(door.get("type","Interior Door")), key=f"dtype_{i}")
            door["width"] = cols[1].number_input("Width (m)", 0.6,2.0, door["width"], key=f"dw_{i}")
            door["height"] = cols[2].number_input("Height (m)", 2.0,3.0, door["height"], key=f"dh_{i}")
            door["wall"] = cols[3].selectbox("Wall", ["north","south","east","west"], index=0 if door.get("wall","south")=="north" else 1, key=f"dwall_{i}")
            door["height_above_floor"] = cols[4].number_input("Sill Height (m)", 0.0,2.0, door.get("height_above_floor",0.0), key=f"dsill_{i}")
            door["material"] = cols[5].selectbox("Material", ["Wood","Steel","Glass","Aluminium"], index=0, key=f"dmat_{i}")
            if st.button("🗑 Delete", key=f"ddel_{i}"): spec["doors"].pop(i); st.rerun()
    if st.button("➕ Add Door"):
        spec["doors"].append({"type":"Interior Door","width":0.9,"height":2.1,"wall":"south","height_above_floor":0.0,"material":"Wood"})
        st.rerun()

    # WINDOWS
    st.subheader("Windows")
    for i, win in enumerate(spec["windows"]):
        with st.expander(f"Window {i+1} ({win.get('type','')})"):
            cols = st.columns([2,1,1,1,1,1])
            win["type"] = cols[0].selectbox("Type", ["Sliding","Casement","Fixed","Louvre"], index=0, key=f"wtype_{i}")
            win["width"] = cols[1].number_input("Width (m)", 0.6,3.0, win["width"], key=f"ww_{i}")
            win["height"] = cols[2].number_input("Height (m)", 0.6,2.5, win["height"], key=f"wh_{i}")
            win["wall"] = cols[3].selectbox("Wall", ["north","south","east","west"], index=0 if win.get("wall","north")=="north" else 1, key=f"wwall_{i}")
            win["height_above_floor"] = cols[4].number_input("Sill Height (m)", 0.0,2.0, win.get("height_above_floor",0.9), key=f"wsill_{i}")
            win["glazing"] = cols[5].selectbox("Glazing", ["Single","Double","Triple"], index=1, key=f"wglaz_{i}")
            if st.button("🗑 Delete", key=f"wdel_{i}"): spec["windows"].pop(i); st.rerun()
    if st.button("➕ Add Window"):
        spec["windows"].append({"type":"Sliding","width":1.2,"height":1.2,"wall":"north","height_above_floor":0.9,"glazing":"Double"})
        st.rerun()

    # Circulation
    st.subheader("Circulation (Stairs / Lifts)")
    c1,c2 = st.columns(2)
    spec["stairs"]["count"] = c1.number_input("Staircases", 0,4, spec["stairs"]["count"])
    spec["stairs"]["type"] = c1.selectbox("Stair Type", ["Straight","U-shaped","L-shaped","Spiral"])
    spec["stairs"]["width"] = c1.number_input("Stair Width (m)", 0.9,2.5, spec["stairs"]["width"])
    spec["lifts"]["count"] = c2.number_input("Lifts", 0,6, spec["lifts"]["count"])
    spec["lifts"]["type"] = c2.selectbox("Lift Type", ["Passenger","Goods","Stretcher"])
    spec["lifts"]["capacity"] = c2.number_input("Capacity (pers)", 4,26, spec["lifts"]["capacity"])

    # MEP & orientation
    st.subheader("MEP, Sun & Wind")
    spec["hvac"] = st.selectbox("HVAC System", HVAC_SYSTEMS)
    c1,c2 = st.columns(2)
    spec["mep_details"]["plumbing_fixtures_per_floor"] = c1.number_input("Plumbing Fixtures/Floor", 1,20, spec["mep_details"]["plumbing_fixtures_per_floor"])
    spec["mep_details"]["electrical_load_per_sqm"] = c2.number_input("Electrical Load (VA/m²)", 30,200, spec["mep_details"]["electrical_load_per_sqm"])
    spec["orientation"] = st.selectbox("Sun Orientation (Front Facade)", ORIENTATIONS)
    spec["wind_direction"] = st.selectbox("Prevailing Wind Direction", ORIENTATIONS)

    # Save & Report
    if st.button("💾 Save Specification & Show Report"):
        save_spec(spec)
        # Build detailed report
        def build_report(spec, unit_sys):
            u = unit_sys
            report = f"# Architectural Specification – {spec['building_name']}\n\n"
            report += f"## General\n- Floors: {spec['floors']}\n- Floor height: {fmt_length(spec['floor_height'], u)}\n"
            report += f"- Plot: {fmt_length(spec['plot_length'], u)} x {fmt_length(spec['plot_width'], u)}\n"
            report += f"- Building footprint: {fmt_length(spec['overall_length'], u)} x {fmt_length(spec['overall_width'], u)}\n"
            total_area = spec['overall_length'] * spec['overall_width'] * spec['floors']
            report += f"- Total floor area: {fmt_area(total_area, u)}\n"
            report += f"- Orientation: {spec['orientation']}, Wind: {spec['wind_direction']}\n\n"
            report += f"## Rooms ({len(spec['rooms'])})\n"
            for r in spec['rooms']:
                area = r['width'] * r['length']
                report += f"### {r['name']} ({r['type']})\n"
                report += f"- Size: {fmt_length(r['width'], u)} x {fmt_length(r['length'], u)} x {fmt_length(r['height'], u)}\n"
                report += f"- Area: {fmt_area(area, u)}\n"
                report += f"- Flooring: {r.get('flooring','wood')}, Ceiling: {r.get('ceiling','flat')}\n"
                report += f"- Bulbs: {r.get('bulbs',0)}, Sockets: {r.get('sockets',0)}\n"
                if r.get('furniture'):
                    report += "- Furniture:\n"
                    for f in r['furniture']:
                        report += f"  - {f['item']} ({fmt_length(f['w'], u)} x {fmt_length(f['d'], u)} x {fmt_length(f['h'], u)})\n"
                report += "\n"
            report += f"## Doors ({len(spec['doors'])})\n"
            for d in spec['doors']:
                report += f"- {d['type']}: {fmt_length(d['width'], u)} x {fmt_length(d['height'], u)}, Wall: {d.get('wall','south')}, Sill: {fmt_length(d.get('height_above_floor',0), u)}, Material: {d.get('material','Wood')}\n"
            report += f"\n## Windows ({len(spec['windows'])})\n"
            for w in spec['windows']:
                report += f"- {w['type']}: {fmt_length(w['width'], u)} x {fmt_length(w['height'], u)}, Wall: {w.get('wall','north')}, Sill: {fmt_length(w.get('height_above_floor',0.9), u)}, Glazing: {w.get('glazing','Double')}\n"
            report += f"\n## MEP/HVAC\n- HVAC: {spec['hvac']}\n- Plumbing/floor: {spec['mep_details']['plumbing_fixtures_per_floor']}\n- Electrical: {spec['mep_details']['electrical_load_per_sqm']} VA/m²\n"
            return report

        report = build_report(spec, unit)
        st.text_area("Report", report, height=500)
        st.download_button("📥 Download JSON", json.dumps(spec, indent=2), file_name=f"{spec['building_name'] or 'spec'}.json")
        add_xp(uname,20); st.session_state.user_data=get_user(uname)

elif page == "Layout Options":
    st.title("🗺️ Grid‑Based Layout Options")
    spec = st.session_state.spec
    grid_x = spec["grid"]["spacing_x"]
    grid_y = spec["grid"]["spacing_y"]
    cols_x = int(spec["overall_length"] / grid_x)
    cols_y = int(spec["overall_width"] / grid_y)
    # generate three random room assignments to grid cells
    st.write(f"Based on your grid ({grid_x}m x {grid_y}m), building footprint {spec['overall_length']}m x {spec['overall_width']}m gives {cols_x}x{cols_y} bays.")
    for option in range(3):
        st.subheader(f"Option {option+1}")
        # create a simple text grid
        grid = [["  " for _ in range(cols_x)] for _ in range(cols_y)]
        room_types = list(spec["rooms"])
        # fill grid with room names
        for room in room_types:
            # place room randomly in available cells
            placed = False
            for attempt in range(10):
                rw = int(max(1, room["width"]/grid_x))
                rl = int(max(1, room["length"]/grid_y))
                x = random.randint(0, cols_x - rw)
                y = random.randint(0, cols_y - rl)
                # check if cells free
                free = True
                for i in range(x, x+rw):
                    for j in range(y, y+rl):
                        if grid[j][i] != "  ":
                            free = False
                if free:
                    for i in range(x, x+rw):
                        for j in range(y, y+rl):
                            grid[j][i] = room["name"][:2].center(2)
                    placed = True
                    break
            if not placed:
                # just place at first available
                for y in range(cols_y):
                    for x in range(cols_x):
                        if grid[y][x] == "  ":
                            grid[y][x] = room["name"][:2].center(2)
                            break
                    else: continue
                    break
        # render grid
        st.text("\n".join([" ".join(row) for row in grid]))

elif page == "AI Assistant Ram":
    st.title("🤖 AI Assistant – Ram")
    st.markdown("Ask Ram about sizes, materials, cost, scheduling, or anything related to your current specification.")
    user_query = st.text_area("Your question:")
    if st.button("Ask Ram"):
        answer = ram_advisor(user_query, st.session_state.spec)
        st.success(answer)
    st.info("Example queries: 'What is the estimated cost?', 'How long will construction take?', 'Suggest materials for exterior walls'.")

elif page == "Diagnostics":
    st.title("🔍 Structural Diagnostics & Material Takeoffs")
    spec = st.session_state.spec
    if not spec["building_name"]:
        st.info("Please fill in the specification first.")
    else:
        alerts, cols, beams, area = structural_review(spec)
        st.subheader(f"Diagnostics for {spec['building_name']}")
        st.markdown("### Structural Review")
        for a in alerts: st.write(a)
        st.markdown("### Material Quantity Estimates")
        df = pd.DataFrame(material_takeoffs(cols, beams, area))
        st.table(df)

elif page == "Saved Specs":
    st.title("📋 Saved Specifications")
    specs = load_specs()
    if not specs:
        st.info("No saved specifications.")
    else:
        for s in specs:
            with st.expander(f"{s.get('building_name','Unnamed')} – {s.get('id','')}"):
                st.json(s)

elif page == "Settings":
    st.title("⚙️ Settings")
    st.info("Units: choose Metric or Imperial in the sidebar.")
    if st.button("Delete All Saved Specs"):
        SPEC_FILE.write_text("[]")
        st.success("Cleared.")

st.markdown('<div class="footer">AI Powered · Data Driven · Secure · Scalable</div>', unsafe_allow_html=True)
