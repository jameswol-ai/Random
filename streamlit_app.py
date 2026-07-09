# ============================================================
# RANDOM – AI Architectural Specification Studio
# Combined: Auth, XP, Full Spec Form, Diagnostics, Saved Specs
# ============================================================
import streamlit as st, json, uuid, hashlib, math
from pathlib import Path
from datetime import datetime
import pandas as pd

# ---------- CONFIG ----------
st.set_page_config(page_title="RANDOM Studio", page_icon="⚡", layout="wide")
DATA_DIR = Path("data"); DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "users.json"
XP_PER_LEVEL = 100
SPEC_FILE = DATA_DIR / "specs.json"
if not SPEC_FILE.exists():
    SPEC_FILE.write_text("[]")

# ---------- NEW LOGO & THEME ----------
st.markdown("""
<style>
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
    page = st.radio("Go to",["Specification Studio","Diagnostics","Saved Specs","Settings"])
    st.session_state.page=page
    st.divider()
    if user_data.get("role")=="admin":
        with st.expander("🛡️ Admin"):
            for u in load_users():
                if u["username"]!=uname:
                    if st.button(f"🗑 {u['username']}",key=f"del_{u['username']}"):
                        users=load_users(); users.remove(u); save_users(users); st.rerun()
    st.markdown("### 📁 Recent Projects")
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
# ARCHITECTURAL SPECIFICATION LOGIC
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

WALL_MATERIALS = {
    "Cavity Brick (280mm)": 280,
    "Solid Brick (230mm)": 230,
    "Concrete Block (200mm)": 200,
    "AAC Block (200mm)": 200,
    "Timber Frame + Cladding": 150,
    "Steel Frame + Cladding": 150,
}

INTERIOR_WALLS = {
    "Brick Partition (115mm)": 115,
    "Concrete Block (100mm)": 100,
    "Timber Stud + Plasterboard": 90,
    "Glass Partition": 12,
}

PLASTER_FINISHES = [
    "Cement Plaster + Paint (20mm)",
    "Gypsum Plaster + Paint (15mm)",
    "Tile Cladding (10mm)",
    "Stone Cladding (30mm)",
    "Exposed Brick (no plaster)",
]

FOUNDATION_TYPES = {
    "Strip Foundation": {"min_depth": 0.8, "width_factor": 1.0},
    "Raft Foundation": {"depth": 0.3, "reinforcement": "heavy"},
    "Pile Foundation": {"min_depth": 5.0, "diameter": 0.6},
}

HVAC_SYSTEMS = [
    "Natural Ventilation",
    "Split AC Units",
    "Central Chilled Water",
    "VRV/VRF System",
    "Hybrid (Natural + Mechanical)",
]

SUNLIGHT_ORIENTATIONS = ["North", "South", "East", "West"]

def save_spec(spec):
    data = json.loads(SPEC_FILE.read_text())
    spec["id"] = str(uuid.uuid4())[:8].upper()
    spec["created"] = datetime.now().isoformat()
    data.append(spec)
    SPEC_FILE.write_text(json.dumps(data, indent=2))

def load_specs():
    return json.loads(SPEC_FILE.read_text())

def structural_review(spec):
    # Estimate column/beam counts from grid
    cols_x = int(spec["overall_length"] / spec["grid"]["spacing_x"]) + 1
    cols_y = int(spec["overall_width"] / spec["grid"]["spacing_y"]) + 1
    total_cols = cols_x * cols_y * spec["floors"]
    total_beams = (cols_x * (cols_y-1) + cols_y * (cols_x-1)) * spec["floors"]
    area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
    cost = area * 1650  # rough cost estimate
    alerts = []
    if total_cols < 16:
        alerts.append("🔴 Column density too low.")
    if cost / area > 2300:
        alerts.append("🟡 Cost efficiency threshold exceeded.")
    if total_beams / total_cols < 1.9:
        alerts.append("🔵 Beam-column ratio imbalance.")
    if not alerts:
        alerts = ["🟢 Design structurally stable."]
    return alerts, total_cols, total_beams, area, cost

def material_takeoffs(spec, total_cols, total_beams, area):
    return [
        {"item": "High-Performance Concrete", "qty": f"{total_cols * 2.6:.1f} m³"},
        {"item": "Tensile Steel Rebar", "qty": f"{total_beams * 0.48:.2f} MT"},
        {"item": "CMU Blocks", "qty": f"{int(area * 42):,} units"},
        {"item": "Dead Load Base", "qty": f"{int(total_cols * 13.2):,} kN"}
    ]

# ---------- DEFAULT SPEC ----------
if "spec" not in st.session_state:
    st.session_state.spec = {
        "building_name": "",
        "floors": 2,
        "floor_height": 3.0,
        "overall_length": 20.0,
        "overall_width": 15.0,
        "grid": {"spacing_x": 6.0, "spacing_y": 6.0, "column_size": 0.4},
        "exterior_wall": list(WALL_MATERIALS.keys())[0],
        "interior_wall": list(INTERIOR_WALLS.keys())[0],
        "plaster_exterior": PLASTER_FINISHES[0],
        "plaster_interior": PLASTER_FINISHES[1],
        "foundation": list(FOUNDATION_TYPES.keys())[0],
        "foundation_depth": 1.2,
        "flooring": "tiles",
        "ceiling": "flat",
        "rooms": [{"name":"Living Room","type":"living","width":6.0,"length":5.0,"height":3.0,"flooring":"wood","ceiling":"flat"}],
        "doors": [],
        "windows": [],
        "stairs": {"count": 1, "type": "U-shaped", "width": 1.2},
        "lifts": {"count": 1, "type": "Passenger", "capacity": 8},
        "hvac": HVAC_SYSTEMS[0],
        "orientation": "South",
        "mep_details": {"plumbing_fixtures_per_floor": 4, "electrical_load_per_sqm": 50},
    }

# ============================================================
# PAGE ROUTING
# ============================================================
page = st.session_state.page

if page == "Specification Studio":
    st.title("⚡ RANDOM – Architectural Spec Studio")
    with st.form("spec_form"):
        st.header("Building Information")
        col1, col2 = st.columns(2)
        spec = st.session_state.spec
        spec["building_name"] = col1.text_input("Project Name", spec["building_name"])
        spec["floors"] = col2.slider("Number of Floors", 1, 30, spec["floors"])
        spec["floor_height"] = st.slider("Floor‑to‑Floor Height (m)", 2.4, 5.0, spec["floor_height"])
        col1, col2 = st.columns(2)
        spec["overall_length"] = col1.number_input("Building Length (m)", 5.0, 100.0, spec["overall_length"])
        spec["overall_width"] = col2.number_input("Building Width (m)", 5.0, 100.0, spec["overall_width"])

        st.subheader("Grid System")
        col1, col2 = st.columns(2)
        spec["grid"]["spacing_x"] = col1.number_input("Column Spacing X (m)", 3.0, 9.0, spec["grid"]["spacing_x"])
        spec["grid"]["spacing_y"] = col2.number_input("Column Spacing Y (m)", 3.0, 9.0, spec["grid"]["spacing_y"])
        spec["grid"]["column_size"] = st.number_input("Column Size (m)", 0.3, 1.0, spec["grid"]["column_size"])

        st.subheader("Wall Construction")
        col1, col2 = st.columns(2)
        spec["exterior_wall"] = col1.selectbox("Exterior Wall Type", list(WALL_MATERIALS.keys()),
                                              index=list(WALL_MATERIALS.keys()).index(spec["exterior_wall"]))
        spec["plaster_exterior"] = col1.selectbox("Exterior Finish", PLASTER_FINISHES)
        spec["interior_wall"] = col2.selectbox("Interior Wall Type", list(INTERIOR_WALLS.keys()),
                                              index=list(INTERIOR_WALLS.keys()).index(spec["interior_wall"]))
        spec["plaster_interior"] = col2.selectbox("Interior Finish", PLASTER_FINISHES)

        st.subheader("Foundation")
        col1, col2 = st.columns(2)
        spec["foundation"] = col1.selectbox("Foundation Type", list(FOUNDATION_TYPES.keys()))
        spec["foundation_depth"] = col2.number_input("Foundation Depth (m)", 0.3, 15.0, spec["foundation_depth"])

        st.subheader("Flooring & Ceiling (Defaults)")
        spec["flooring"] = st.selectbox("Global Flooring", ["tiles","wood","concrete","marble","carpet"])
        spec["ceiling"] = st.selectbox("Global Ceiling Type", ["flat","hanging","vaulted","exposed","coffered"])

        st.subheader("Rooms & Spaces")
        for i, room in enumerate(spec["rooms"]):
            cols = st.columns([3,2,1,1,1,1,1])
            room["name"] = cols[0].text_input("Room Name", room["name"], key=f"rname_{i}")
            room["type"] = cols[1].selectbox("Type", list(ROOM_STANDARDS.keys()), 
                                            index=list(ROOM_STANDARDS.keys()).index(room["type"]) if room["type"] in ROOM_STANDARDS else 0,
                                            key=f"rtype_{i}")
            room["width"] = cols[2].number_input("W(m)", 1.0, 20.0, room["width"], key=f"rw_{i}")
            room["length"] = cols[3].number_input("L(m)", 1.0, 20.0, room["length"], key=f"rl_{i}")
            room["height"] = cols[4].number_input("H(m)", 2.4, 5.0, room["height"], key=f"rh_{i}")
            room["flooring"] = cols[5].selectbox("Floor", ["tiles","wood","concrete","marble","carpet"], 
                                                index=0 if room.get("flooring")=="wood" else 0, key=f"rfloor_{i}")
            room["ceiling"] = cols[6].selectbox("Ceil", ["flat","hanging","vaulted","exposed","coffered"],
                                                index=0 if room.get("ceiling")=="flat" else 0, key=f"rceil_{i}")
            if st.button("❌", key=f"rdel_{i}"):
                spec["rooms"].pop(i)
                st.rerun()
        col_add, _ = st.columns(2)
        if col_add.button("➕ Add Room"):
            spec["rooms"].append({"name":"New Room","type":"living","width":4.0,"length":4.0,"height":3.0,"flooring":"wood","ceiling":"flat"})
            st.rerun()

        st.subheader("Doors & Windows")
        st.markdown("**Doors**")
        for i, door in enumerate(spec["doors"]):
            cols = st.columns([2,1,1,1,1])
            door["type"] = cols[0].selectbox("Type", ["Main Entrance","Interior Door","Bathroom Door","Sliding Door"],
                                            index=["Main Entrance","Interior Door","Bathroom Door","Sliding Door"].index(door.get("type","Interior Door")),
                                            key=f"dtype_{i}")
            door["width"] = cols[1].number_input("Width (m)", 0.6, 2.0, door.get("width",0.9), key=f"dw_{i}")
            door["height"] = cols[2].number_input("Height (m)", 2.0, 3.0, door.get("height",2.1), key=f"dh_{i}")
            door["material"] = cols[3].selectbox("Material", ["Wood","Steel","Glass","Aluminium"],
                                                index=0, key=f"dmat_{i}")
            if cols[4].button("❌", key=f"ddel_{i}"):
                spec["doors"].pop(i); st.rerun()
        if st.button("➕ Add Door"):
            spec["doors"].append({"type":"Interior Door","width":0.9,"height":2.1,"material":"Wood"})
            st.rerun()

        st.markdown("**Windows**")
        for i, win in enumerate(spec["windows"]):
            cols = st.columns([2,1,1,1,1])
            win["type"] = cols[0].selectbox("Type", ["Sliding","Casement","Fixed","Louvre"],
                                           index=0, key=f"wtype_{i}")
            win["width"] = cols[1].number_input("Width (m)", 0.6, 3.0, win.get("width",1.2), key=f"ww_{i}")
            win["height"] = cols[2].number_input("Height (m)", 0.6, 2.5, win.get("height",1.2), key=f"wh_{i}")
            win["glazing"] = cols[3].selectbox("Glazing", ["Single","Double","Triple"],
                                              index=1, key=f"wglaz_{i}")
            if cols[4].button("❌", key=f"wdel_{i}"):
                spec["windows"].pop(i); st.rerun()
        if st.button("➕ Add Window"):
            spec["windows"].append({"type":"Sliding","width":1.2,"height":1.2,"glazing":"Double"})
            st.rerun()

        st.subheader("Circulation (Stairs / Lifts)")
        col1, col2 = st.columns(2)
        spec["stairs"]["count"] = col1.number_input("Number of Staircases", 0, 4, spec["stairs"]["count"])
        spec["stairs"]["type"] = col1.selectbox("Stair Type", ["Straight","U-shaped","L-shaped","Spiral"])
        spec["stairs"]["width"] = col1.number_input("Stair Width (m)", 0.9, 2.5, spec["stairs"]["width"])
        spec["lifts"]["count"] = col2.number_input("Number of Lifts", 0, 6, spec["lifts"]["count"])
        spec["lifts"]["type"] = col2.selectbox("Lift Type", ["Passenger","Goods","Stretcher"])
        spec["lifts"]["capacity"] = col2.number_input("Capacity (persons)", 4, 26, spec["lifts"]["capacity"])

        st.subheader("MEP & HVAC")
        spec["hvac"] = st.selectbox("HVAC System", HVAC_SYSTEMS)
        col1, col2 = st.columns(2)
        spec["mep_details"]["plumbing_fixtures_per_floor"] = col1.number_input("Plumbing Fixtures / Floor", 1, 20, spec["mep_details"]["plumbing_fixtures_per_floor"])
        spec["mep_details"]["electrical_load_per_sqm"] = col2.number_input("Electrical Load (VA/m²)", 30, 200, spec["mep_details"]["electrical_load_per_sqm"])

        st.subheader("Sunlight Orientation")
        spec["orientation"] = st.selectbox("Building Orientation (Front Facade)", SUNLIGHT_ORIENTATIONS)

        submitted = st.form_submit_button("⚡ Generate Full Specification")
        if submitted:
            # Save to library
            save_spec(spec)
            # Show report
            total_area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
            report = f"""
# Architectural Specification – {spec['building_name'] or 'Unnamed Project'}

## General
- Floors: {spec['floors']}
- Floor height: {spec['floor_height']} m
- Total height: {spec['floors'] * spec['floor_height']:.1f} m
- Building footprint: {spec['overall_length']}m (L) x {spec['overall_width']}m (W)
- Total floor area: {total_area:.0f} m²

## Grid System
- Column grid: {spec['grid']['spacing_x']}m x {spec['grid']['spacing_y']}m
- Column size: {spec['grid']['column_size']}m

## Walls
- Exterior: {spec['exterior_wall']} (thickness {WALL_MATERIALS[spec['exterior_wall']]}mm)
  Finish: {spec['plaster_exterior']}
- Interior partitions: {spec['interior_wall']} (thickness {INTERIOR_WALLS[spec['interior_wall']]}mm)
  Finish: {spec['plaster_interior']}

## Foundation
- Type: {spec['foundation']}
- Depth: {spec['foundation_depth']} m
- Details: {json.dumps(FOUNDATION_TYPES[spec['foundation']])}

## Rooms ({len(spec['rooms'])})
"""
            for r in spec['rooms']:
                area = r['width'] * r['length']
                report += f"- {r['name']} ({r['type']}): {r['width']}m x {r['length']}m, Area: {area:.1f} m², Height: {r['height']}m, Flooring: {r['flooring']}, Ceiling: {r['ceiling']}\n"

            report += f"""
## Doors ({len(spec['doors'])})
"""
            for d in spec['doors']:
                report += f"- {d['type']}: {d['width']}m x {d['height']}m, Material: {d['material']}\n"

            report += f"""
## Windows ({len(spec['windows'])})
"""
            for w in spec['windows']:
                report += f"- {w['type']}: {w['width']}m x {w['height']}m, Glazing: {w['glazing']}\n"

            report += f"""
## Circulation
- Stairs: {spec['stairs']['count']} x {spec['stairs']['type']} ({spec['stairs']['width']}m wide)
- Lifts: {spec['lifts']['count']} x {spec['lifts']['type']} ({spec['lifts']['capacity']} persons)

## MEP / HVAC
- HVAC System: {spec['hvac']}
- Plumbing fixtures per floor: {spec['mep_details']['plumbing_fixtures_per_floor']}
- Electrical load: {spec['mep_details']['electrical_load_per_sqm']} VA/m² (approx {total_area * spec['mep_details']['electrical_load_per_sqm']:.0f} VA total)

## Sunlight Orientation
- Building faces {spec['orientation']}. (For {spec['orientation']} orientation, maximize glazing on {'South' if spec['orientation']=='North' else 'North' if spec['orientation']=='South' else 'appropriate'} side.)

---
*Generated by RANDOM Architectural Studio*
"""
            st.text_area("Specification Report", report, height=400)
            st.success("Specification saved to library.")
            st.download_button("📥 Download JSON", json.dumps(spec, indent=2), file_name=f"{spec['building_name'] or 'spec'}.json")
            add_xp(uname, 20)
            st.session_state.user_data = get_user(uname)

elif page == "Diagnostics":
    st.title("🔍 Structural Diagnostics & Material Takeoffs")
    spec = st.session_state.spec
    if not spec["building_name"]:
        st.info("Please fill in the specification first.")
    else:
        alerts, cols, beams, area, cost = structural_review(spec)
        st.subheader(f"Diagnostics for {spec['building_name']}")
        st.markdown("### Structural Review")
        for a in alerts:
            st.write(a)
        st.markdown("### Material Quantity Estimates")
        df = pd.DataFrame(material_takeoffs(spec, cols, beams, area))
        st.table(df)

elif page == "Saved Specs":
    st.title("📋 Saved Specifications")
    specs = load_specs()
    if not specs:
        st.info("No saved specifications.")
    else:
        for s in specs:
            with st.expander(f"{s.get('building_name','Unnamed')} – {s.get('id','')} (created {s.get('created','')[:10]})"):
                st.json(s)

elif page == "Settings":
    st.title("⚙️ Settings")
    st.info("Units: Metric (SI) – all dimensions in metres.")
    if st.button("Delete All Saved Specs"):
        SPEC_FILE.write_text("[]")
        st.success("Cleared.")

st.markdown('<div class="footer">AI Powered · Data Driven · Secure · Scalable</div>', unsafe_allow_html=True)
