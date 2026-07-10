# ============================================================
# RANDOM – Single‑Project AEC Studio (Fixed Materials & Cost)
# ============================================================
import streamlit as st
import json, uuid, hashlib, math, random, base64
from pathlib import Path
from datetime import datetime
import pandas as pd

# ---------- CONFIG ----------
st.set_page_config(page_title="RANDOM Studio", page_icon="⚡", layout="wide")

# ---------- VERCEL SPEED INSIGHTS ----------
# Inject Vercel Speed Insights for performance monitoring
speed_insights_script = """
<script type="module">
import { injectSpeedInsights } from 'https://cdn.jsdelivr.net/npm/@vercel/speed-insights@1/dist/index.mjs';
injectSpeedInsights({
    framework: 'streamlit',
    debug: false
});
</script>
"""
st.html(speed_insights_script, unsafe_allow_javascript=True)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "users.json"
PRICES_FILE = DATA_DIR / "material_prices.json"
XP_PER_LEVEL = 100

if not PRICES_FILE.exists():
    default_prices = {
        "Cement (50kg bag)": {"USD":8,"UGX":29000,"KES":1100,"TZS":20000,"RWF":9000,"SSP":12000},
        "Steel Rebar (ton)": {"USD":800,"UGX":2900000,"KES":110000,"TZS":2000000,"RWF":900000,"SSP":1200000},
        "Concrete Blocks (1000 units)": {"USD":250,"UGX":900000,"KES":34000,"TZS":600000,"RWF":270000,"SSP":375000},
        "Timber (m³)": {"USD":300,"UGX":1100000,"KES":41000,"TZS":750000,"RWF":330000,"SSP":450000},
        "Roofing Sheets (per m²)": {"USD":5,"UGX":18000,"KES":680,"TZS":12000,"RWF":5500,"SSP":7500},
        "Tiles (per m²)": {"USD":12,"UGX":43000,"KES":1600,"TZS":30000,"RWF":13500,"SSP":18000},
        "Paint (per litre)": {"USD":4,"UGX":14500,"KES":550,"TZS":10000,"RWF":4500,"SSP":6000},
        "Glass (per m²)": {"USD":25,"UGX":90000,"KES":3400,"TZS":65000,"RWF":28000,"SSP":37500},
    }
    PRICES_FILE.write_text(json.dumps(default_prices, indent=2))

# ---------- THEMES ----------
THEMES = {
    "Warm Amber": {
        "bg_gradient": "radial-gradient(circle at top right, #2d1b34, #0f0f1a 60%)",
        "sidebar_bg": "linear-gradient(180deg, #1a1025, #0c0714)",
        "btn_gradient": "linear-gradient(135deg, #fbbf24, #f97316)",
        "accent": "#fbbf24",
        "card_bg": "rgba(25,20,40,0.65)",
        "text": "#f5f0eb"
    },
    "Ocean Blue": {
        "bg_gradient": "radial-gradient(circle at top right, #0f2027, #203a43 60%)",
        "sidebar_bg": "linear-gradient(180deg, #0a1a24, #051016)",
        "btn_gradient": "linear-gradient(135deg, #38bdf8, #0ea5e9)",
        "accent": "#38bdf8",
        "card_bg": "rgba(15,30,40,0.65)",
        "text": "#e0f0ff"
    },
    "Emerald Green": {
        "bg_gradient": "radial-gradient(circle at top right, #0a2a1a, #05100a 60%)",
        "sidebar_bg": "linear-gradient(180deg, #0a1f14, #030b06)",
        "btn_gradient": "linear-gradient(135deg, #34d399, #059669)",
        "accent": "#34d399",
        "card_bg": "rgba(10,30,20,0.65)",
        "text": "#e0ffe0"
    },
    "Light Mode": {
        "bg_gradient": "linear-gradient(135deg, #f8f9fa, #e9ecef)",
        "sidebar_bg": "linear-gradient(180deg, #ffffff, #f1f3f5)",
        "btn_gradient": "linear-gradient(135deg, #339af0, #1c7ed6)",
        "accent": "#339af0",
        "card_bg": "rgba(255,255,255,0.85)",
        "text": "#212529"
    }
}

def get_theme_css(theme_name):
    t = THEMES.get(theme_name, THEMES["Warm Amber"])
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;700&display=swap');
.stApp {{ background: {t['bg_gradient']}; font-family: 'Inter', sans-serif; color: {t['text']}; }}
h1,h2,h3,h4,h5,h6 {{ font-family: 'Outfit', sans-serif; font-weight: 700; color: {t['text']}; }}
[data-testid="stSidebar"] {{ background: {t['sidebar_bg']}; border-right: 1px solid rgba(255,255,255,0.08); }}
.stButton>button {{ background: {t['btn_gradient']}; color: #0b0710; border: none; border-radius: 18px; padding: 0.75rem 2.2rem; font-weight: 700; font-family: 'Outfit', sans-serif; letter-spacing: 0.5px; transition: all 0.25s; box-shadow: 0 8px 25px {t['accent']}55; }}
.stButton>button:hover {{ transform: scale(1.03); box-shadow: 0 14px 35px {t['accent']}88; }}
.glass-card {{ background: {t['card_bg']}; backdrop-filter: blur(16px); border-radius: 28px; padding: 1.8rem; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 25px 45px rgba(0,0,0,0.5); }}
.xp-container {{ display: flex; align-items: center; gap: 10px; margin-bottom: 1.2rem; }}
.xp-bar-bg {{ flex: 1; height: 10px; background: #2e2340; border-radius: 6px; overflow: hidden; }}
.xp-bar-fill {{ height: 100%; background: {t['btn_gradient']}; border-radius: 6px; box-shadow: 0 0 10px {t['accent']}; }}
.logo-text {{ font-family: 'Outfit', sans-serif; font-size: 2.4rem; font-weight: 800; background: {t['btn_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }}
</style>
"""

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

# ---------- SESSION INIT ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False; st.session_state.username=None
    st.session_state.user_data=None; st.session_state.page="Dashboard"
    st.session_state.unit_system="Metric"
    st.session_state.theme = "Warm Amber"
    st.session_state.chat_history = []
    st.session_state.spec = {
        "building_name": "Project Name",
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
        "rooms": [
            {"name":"Living Room","type":"living","width":6.0,"length":5.0,"height":3.0,
             "flooring":"wood","ceiling":"flat","bulbs":4,"sockets":6,"switches":2,
             "furniture":[{"item":"Sofa","w":2.0,"d":1.0,"h":0.9}]}
        ],
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

if not load_users():
    create_user("admin","admin123",role="admin")

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        st.markdown("<div class='logo-text' style='text-align:center;margin-top:4rem;'>⚡ RANDOM</div>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#e0d7ff;'>Single‑Project AEC Studio</p>",unsafe_allow_html=True)
        with st.form("auth"):
            uname=st.text_input("Username"); pw=st.text_input("Password",type="password")
            colA,colB=st.columns(2)
            with colA: login_btn=st.form_submit_button("Login")
            with colB: reg_btn=st.form_submit_button("Register")
            if login_btn:
                user=authenticate(uname,pw)
                if user:
                    st.session_state.logged_in=True; st.session_state.username=uname
                    st.session_state.user_data=user
                    st.rerun()
                else: st.error("Invalid credentials")
            if reg_btn:
                if not uname or not pw: st.error("Fill all fields")
                else:
                    try:
                        create_user(uname,pw); st.success("Account created!")
                    except ValueError as e: st.error(str(e))
    st.stop()

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# ---------- SIDEBAR (simplified) ----------
uname=st.session_state.username; user_data=st.session_state.user_data
with st.sidebar:
    st.markdown("<div class='logo-text' style='font-size:1.8rem;'>⚡ RANDOM</div>",unsafe_allow_html=True)
    st.markdown(f"**👤 {uname}**")
    lvl=user_data["level"]; xp=user_data["xp"]; needed=xp_for_level(lvl)
    progress=xp/needed if needed>0 else 1.0
    st.markdown(f"""<div class="xp-container"><span style="font-size:12px;color:#e0d7ff;">LVL {lvl}</span>
    <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{progress*100}%;"></div></div>
    <span style="font-size:10px;color:#9b8ec4;">{xp}/{needed} XP</span></div>""",unsafe_allow_html=True)

    page = st.radio("Navigate", ["Dashboard", "Ram Assistant", "Materials & Cost", "BOQ & Export", "Settings"])
    st.session_state.page = page
    st.divider()
    if user_data.get("role")=="admin":
        with st.expander("🛡️ Admin"):
            for u in load_users():
                if u["username"]!=uname:
                    if st.button(f"🗑 {u['username']}",key=f"del_{u['username']}"):
                        users=load_users(); users.remove(u); save_users(users); st.rerun()
    if st.button("🚪 Logout"):
        for k in ["logged_in","username","user_data","spec","chat_history"]:
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

# ---------- MATERIAL PRICES ----------
def load_prices():
    return json.loads(PRICES_FILE.read_text())
def save_prices(prices):
    PRICES_FILE.write_text(json.dumps(prices, indent=2))
def get_price(material, country):
    prices = load_prices()
    base = prices.get(material, {"USD":0})
    curr = {"Uganda":"UGX","Kenya":"KES","Tanzania":"TZS","Rwanda":"RWF","South Sudan":"SSP"}.get(country, "UGX")
    return base.get(curr, base.get("USD",0))

# ---------- BOQ ----------
def compute_boq(spec):
    items = []
    cols = int(spec["overall_length"]/spec["grid"]["spacing_x"])+1
    rows = int(spec["overall_width"]/spec["grid"]["spacing_y"])+1
    col_vol = cols*rows*spec["floors"]* (spec["grid"]["column_size"]**2)*spec["floor_height"]
    items.append({"item":"Concrete for Columns", "unit":"m³", "qty":round(col_vol,2)})
    beam_len = (cols*(spec["overall_width"])+rows*(spec["overall_length"]))*spec["floors"]
    beam_vol = beam_len*0.23*0.3
    items.append({"item":"Concrete for Beams", "unit":"m³", "qty":round(beam_vol,2)})
    ext_wall_area = 2*(spec["overall_length"]+spec["overall_width"])*spec["floor_height"]*spec["floors"]
    items.append({"item":"Exterior Brickwork", "unit":"m²", "qty":round(ext_wall_area,0)})
    int_wall_area = (len(spec["rooms"])-1)*spec["overall_width"]*spec["floor_height"]*spec["floors"]
    items.append({"item":"Interior Brickwork", "unit":"m²", "qty":round(int_wall_area,0)})
    floor_area = spec["overall_length"]*spec["overall_width"]*spec["floors"]
    items.append({"item":"Floor Tiles", "unit":"m²", "qty":round(floor_area,0)})
    roof_area = spec["overall_length"]*spec["overall_width"]
    items.append({"item":"Roof Sheets", "unit":"m²", "qty":round(roof_area,0)})
    paint_area = ext_wall_area + int_wall_area
    items.append({"item":"Paint (exterior+interior)", "unit":"litre", "qty":round(paint_area*0.1,0)})
    items.append({"item":"Doors", "unit":"pcs", "qty":len(spec["doors"])})
    items.append({"item":"Windows", "unit":"pcs", "qty":len(spec["windows"])})
    glazing_area = sum(w["width"]*w["height"] for w in spec["windows"])
    items.append({"item":"Glass", "unit":"m²", "qty":round(glazing_area,2)})
    return items

# ---------- IFC EXPORT ----------
def compress_guid(guid_str):
    raw_uuid = uuid.UUID(guid_str).bytes
    return base64.b64encode(raw_uuid, b"-_").decode()[:22]

def export_ifc(spec):
    lines = []
    lines.append("ISO-10303-21;")
    lines.append("HEADER;")
    lines.append("FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');")
    lines.append("FILE_NAME('','',(''),(''),'RANDOM','','');")
    lines.append("FILE_SCHEMA(('IFC2X3'));")
    lines.append("ENDSEC;")
    lines.append("DATA;")

    id_counter = 1
    def new_id():
        nonlocal id_counter
        oid = id_counter
        id_counter += 1
        return f"#{oid}"

    proj_id = new_id(); site_id = new_id(); building_id = new_id()
    storey_ids = [new_id() for _ in range(spec["floors"])]
    owner_hist = new_id()
    lines.append(f"{owner_hist}=IFCOWNERHISTORY(#0,#0,$,.ADDED.,$,#0,$,0);")
    units = new_id()
    lines.append(f"{units}=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);")
    lines.append(f"{proj_id}=IFCPROJECT('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},'{spec['building_name']}',$,$,$,$,(#{units}),#0);")
    lines.append(f"{site_id}=IFCSITE('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},'Site',$,$,$,$,$,$,$,$,$,$);")
    lines.append(f"{building_id}=IFCBUILDING('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},'Building',$,$,#{site_id},$,$,$,$);")
    rel_agg = new_id(); rel_agg2 = new_id()
    lines.append(f"{rel_agg}=IFCRELAGGREGATES('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},$,$,#{proj_id},(#{site_id}));")
    lines.append(f"{rel_agg2}=IFCRELAGGREGATES('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},$,$,#{site_id},(#{building_id}));")

    for idx, storey_id in enumerate(storey_ids):
        z = idx * spec["floor_height"]
        placement = new_id()
        lines.append(f"{placement}=IFCLOCALPLACEMENT($,IFCAXIS2PLACEMENT3D(IFCCARTESIANPOINT((0.,0.,{z})),IFCDIRECTION((0.,0.,1.)),IFCDIRECTION((1.,0.,0.))));")
        lines.append(f"{storey_id}=IFCBUILDINGSTOREY('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},'Storey {idx+1}',$,$,{placement},$,$,$);")
        for wall_data in [("north",(0,spec["overall_width"]),(spec["overall_length"],spec["overall_width"])),
                          ("south",(0,0),(spec["overall_length"],0)),
                          ("east",(spec["overall_length"],0),(spec["overall_length"],spec["overall_width"])),
                          ("west",(0,0),(0,spec["overall_width"]))]:
            wall_id = new_id()
            lines.append(f"{wall_id}=IFCWALL('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},'{wall_data[0]} wall',$,$,{storey_id},$,$);")
        slab_id = new_id()
        lines.append(f"{slab_id}=IFCSLAB('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},'Slab',$,$,{storey_id},$,$);")
        for x in range(0, int(spec["overall_length"])+1, int(spec["grid"]["spacing_x"])):
            for y in range(0, int(spec["overall_width"])+1, int(spec["grid"]["spacing_y"])):
                col_id = new_id()
                lines.append(f"{col_id}=IFCCOLUMN('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},'Column',$,$,{storey_id},$,$);")
        for x in range(0, int(spec["overall_length"]), int(spec["grid"]["spacing_x"])):
            for y in range(0, int(spec["overall_width"]), int(spec["grid"]["spacing_y"])):
                beam_id = new_id()
                lines.append(f"{beam_id}=IFCBEAM('{compress_guid(uuid.uuid4().hex)}',#{owner_hist},'Beam',$,$,{storey_id},$,$);")
    lines.append("ENDSEC;")
    lines.append("END-ISO-10303-21;")
    return "\n".join(lines)

# ---------- SMART RAM ----------
def ram_advisor(query, spec, history):
    q = query.lower()
    if "news" in q or "archdaily" in q or "designboom" in q:
        return "🌐 I’ve embedded live streams from ArchDaily & Designboom below. Stay inspired!"
    if "floorplan" in q or "layout" in q:
        return generate_floorplan_text(spec)
    if "cost" in q or "estimate" in q:
        area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
        cost = area * 1500
        return f"💰 Estimated construction cost: ${cost:,.0f} (based on {area:.0f} m² at $1500/m²)."
    if "boq" in q or "bill of quantities" in q:
        items = compute_boq(spec)
        reply = "📋 Bill of Quantities for your project:\n"
        for item in items:
            reply += f"- {item['item']}: {item['qty']} {item['unit']}\n"
        return reply
    if "material" in q:
        return f"🧱 Recommended: {spec['exterior_wall']} for exterior, {spec['interior_wall']} for interior."
    if "schedule" in q:
        return f"⏳ Timeline for {spec['floors']} floors: {spec['floors']*4} – {spec['floors']*6} months."
    if "room" in q and "size" in q:
        rooms_info = "\n".join([f"- {r['name']}: {fmt_length(r['width'], unit)} x {fmt_length(r['length'], unit)}" for r in spec['rooms']])
        return f"Current room sizes:\n{rooms_info}\n\nStandard minimums (East Africa): Living 20m², Bedroom 12m², Bathroom 5m²."
    if "design" in q or "suggestion" in q:
        return ("Based on your grid and shape, consider placing the living room at the front for natural light. "
                "For better ventilation, orient windows towards the prevailing wind direction. "
                "I can generate a floorplan layout if you ask.")
    return "✨ I'm your architectural AI. Ask me about floorplans, BOQ, room sizes, materials, news, or design suggestions."

def generate_floorplan_text(spec, seed=None):
    if seed is not None:
        random.seed(seed)
    rooms = spec["rooms"]
    grid_x = spec["grid"]["spacing_x"]
    grid_y = spec["grid"]["spacing_y"]
    cols = int(spec["overall_length"] / grid_x)
    rows = int(spec["overall_width"] / grid_y)
    if cols<1 or rows<1: return "Grid too small."
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
                    if plan[j][i] != "--": free = False; break
                if not free: break
            if free:
                for i in range(x, x+rw):
                    for j in range(y, y+rl):
                        plan[j][i] = room["name"][:2].center(2)
                placed = True; break
        if not placed:
            for y in range(rows):
                for x in range(cols):
                    if plan[y][x] == "--": plan[y][x] = room["name"][:2].center(2); placed = True; break
                if placed: break
    return "\n".join([" ".join(row) for row in plan])

# ============================================================
# PAGE ROUTING
# ============================================================
page = st.session_state.page
unit = st.session_state.unit_system
spec = st.session_state.spec

if page == "Dashboard":
    st.title(f"⚡ {spec['building_name']}")
    st.markdown("### Unified Architecture · Engineering · Construction Dashboard")

    tab1, tab2, tab3 = st.tabs(["🏛️ Architecture", "⚙️ Engineering", "🚧 Construction"])

    with tab1:
        # (Architecture tab content – identical to previous complete version)
        with st.expander("Project Identity & Shape", expanded=True):
            spec["building_name"] = st.text_input("Project Title", spec["building_name"])
            col1, col2, col3 = st.columns(3)
            spec["category"] = col1.selectbox("Category", ["Residential","Commercial","Industrial"], index=0)
            spec["shape"] = col2.selectbox("Shape", ["Rectangle","L-shape","T-shape","U-shape","Courtyard"], index=0)
            spec["floors"] = col3.slider("Floors", 1, 50, spec["floors"])
            spec["floor_height"] = st.slider("Floor Height (m)", 2.4, 5.0, spec["floor_height"])
            st.caption(f"Total building height: {spec['floors']*spec['floor_height']} m")

        with st.expander("Plot & Footprint"):
            col1, col2 = st.columns(2)
            spec["plot_length"] = col1.number_input("Plot Length (m)", 10.0,500.0, spec["plot_length"])
            spec["plot_width"] = col2.number_input("Plot Width (m)", 10.0,500.0, spec["plot_width"])
            col1, col2, col3, col4 = st.columns(4)
            spec["setback_front"] = col1.number_input("Front Setback (m)", 0.0,50.0, spec["setback_front"])
            spec["setback_back"] = col2.number_input("Rear Setback (m)", 0.0,50.0, spec["setback_back"])
            spec["setback_left"] = col3.number_input("Left Setback (m)", 0.0,50.0, spec["setback_left"])
            spec["setback_right"] = col4.number_input("Right Setback (m)", 0.0,50.0, spec["setback_right"])
            col1, col2 = st.columns(2)
            spec["overall_length"] = col1.number_input("Building Length (m)", 5.0, spec["plot_length"], spec["overall_length"])
            spec["overall_width"] = col2.number_input("Building Width (m)", 5.0, spec["plot_width"], spec["overall_width"])

        with st.expander("Grid & Walls"):
            st.markdown("**Grid System**")
            col1, col2, col3 = st.columns(3)
            spec["grid"]["spacing_x"] = col1.number_input("Col Spacing X (m)", 3.0, 9.0, spec["grid"]["spacing_x"])
            spec["grid"]["spacing_y"] = col2.number_input("Col Spacing Y (m)", 3.0, 9.0, spec["grid"]["spacing_y"])
            spec["grid"]["column_size"] = col3.number_input("Column Size (m)", 0.3, 1.0, spec["grid"]["column_size"])
            spec["grid"]["gridline_ref"] = st.selectbox("Gridline Reference", ["Centerline", "Interior Face", "Exterior Face"],
                                                        index=0 if spec["grid"].get("gridline_ref","Centerline")=="Centerline" else 1)
            st.markdown("**Walls**")
            col1, col2 = st.columns(2)
            spec["exterior_wall"] = col1.selectbox("Exterior Wall Type", 
                                                   ["Cavity Brick (280mm)","Solid Brick (230mm)","Concrete Block (200mm)",
                                                    "AAC Block (200mm)","Timber Frame + Cladding","Steel Frame + Cladding"], index=0)
            spec["plaster_exterior"] = col1.selectbox("Exterior Finish",
                                                      ["Cement Plaster + Paint (20mm)","Gypsum Plaster + Paint (15mm)",
                                                       "Tile Cladding (10mm)","Stone Cladding (30mm)","Exposed Brick (no plaster)"])
            spec["interior_wall"] = col2.selectbox("Interior Partition Type",
                                                   ["Brick Partition (115mm)","Concrete Block (100mm)",
                                                    "Timber Stud + Plasterboard","Glass Partition"], index=0)
            spec["plaster_interior"] = col2.selectbox("Interior Finish",
                                                      ["Gypsum Plaster + Paint (15mm)","Cement Plaster + Paint (20mm)",
                                                       "Tile Cladding (10mm)","Exposed Brick (no plaster)"])

        with st.expander("📐 Floorplan Layout Options", expanded=True):
            st.markdown("Based on your grid, here are three possible arrangements:")
            seeds = [42, 123, 789]
            cols = st.columns(3)
            for idx, seed in enumerate(seeds):
                with cols[idx]:
                    st.markdown(f"**Option {idx+1}**")
                    plan = generate_floorplan_text(spec, seed=seed)
                    st.text(plan)

        with st.expander("🛏️ Rooms & Spaces (Edit Details)", expanded=True):
            for i, room in enumerate(spec["rooms"]):
                with st.container():
                    st.markdown(f"**{room.get('name','Room')} ({room.get('type','living')})**")
                    col1, col2, col3 = st.columns([2,2,1])
                    room["name"] = col1.text_input("Name", room["name"], key=f"rname_{i}")
                    room["type"] = col2.selectbox("Type", ["living","kitchen","dining","master_bedroom","bedroom",
                                                           "bathroom","storage","balcony","corridor"], key=f"rtype_{i}")
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

        with st.expander("🚪 Doors"):
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

        with st.expander("🪟 Windows"):
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

        if st.button("💾 Save Architecture", key="save_arch"):
            st.success("Architecture parameters saved.")

    with tab2:
        col1, col2 = st.columns(2)
        spec["soil_type"] = col1.selectbox("Soil Type", ["Clay","Sand","Rock","Silt","Gravel"], index=0)
        spec["foundation"] = col2.selectbox("Foundation", ["Strip","Raft","Pile"], index=0)
        spec["foundation_depth"] = st.number_input("Foundation Depth (m)", 0.5,20.0, spec["foundation_depth"])
        spec["column_type"] = st.text_input("Column Type", spec.get("column_type","RC 300x300mm"))
        spec["beam_type"] = st.text_input("Beam Type", spec.get("beam_type","RC 230x300mm"))
        spec["roof_type"] = st.selectbox("Roof Type", ["Flat","Pitched","Gable","Hip","Mansard","Gambrel","Butterfly"])
        spec["roof_material"] = st.selectbox("Roof Material", ["Concrete Tiles","Clay Tiles","Metal Sheets","Thatch","Green Roof","Slate"])
        spec["roof_pitch"] = st.slider("Roof Pitch (degrees)", 0, 60, spec.get("roof_pitch",30))
        if st.button("💾 Save Engineering", key="save_eng"):
            st.success("Engineering parameters saved.")

    with tab3:
        labour = st.number_input("Labour Rate (USD/day)", 5,100, spec.get("labour_rate_per_day",15))
        spec["labour_rate_per_day"] = labour
        area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
        est_cost = area * 1500
        st.metric("Est. Construction Cost (USD)", f"${est_cost:,.0f}")
        months = spec["floors"] * 5
        st.write(f"🕒 Schedule: **{months} months** (rough estimate)")

        boq_items = compute_boq(spec)
        total_boq_cost = sum(item["qty"] * get_price(item["item"], spec.get("east_africa_country","Uganda")) for item in boq_items)
        st.markdown("---")
        st.subheader("📋 Live BOQ Cost Summary")
        st.metric(f"Total BOQ Cost ({spec.get('east_africa_country','Uganda')})", f"{total_boq_cost:,.0f}")
        if st.button("💾 Save Construction", key="save_const"):
            st.success("Construction parameters saved.")

elif page == "Ram Assistant":
    st.title("🤖 Creative AI – Ram")
    for chat in st.session_state.chat_history[-5:]:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Ram:** {chat['ram']}")
        st.divider()
    user_query = st.text_area("Ask Ram:", key="ram_input")
    if st.button("Ask Ram"):
        ans = ram_advisor(user_query, spec, [c['user'] for c in st.session_state.chat_history])
        st.session_state.chat_history.append({"user":user_query, "ram":ans})
        st.success(ans)
        if "news" in user_query.lower():
            col1, col2 = st.columns(2)
            with col1: st.components.v1.iframe("https://www.archdaily.com", height=500)
            with col2: st.components.v1.iframe("https://www.designboom.com", height=500)
    if st.button("Clear Chat"):
        st.session_state.chat_history = []

elif page == "Materials & Cost":
    st.title("💰 Live Material Cost Estimation")
    prices = load_prices()
    country = st.selectbox("Country", ["Uganda","Kenya","Tanzania","Rwanda","South Sudan","USD"])
    st.subheader("Update Prices")
    if "price_form_data" not in st.session_state:
        st.session_state.price_form_data = {}
    with st.form("price_update_form"):
        for mat in prices:
            col1, col2 = st.columns([3,1])
            key = f"price_{mat}"
            if key not in st.session_state.price_form_data:
                st.session_state.price_form_data[key] = float(prices[mat].get(country, 0))
            new_price = col2.number_input(mat, value=st.session_state.price_form_data[key], step=1.0, key=key)
        if st.form_submit_button("Update Prices"):
            for mat in prices:
                key = f"price_{mat}"
                prices[mat][country] = st.session_state.price_form_data[key]
            save_prices(prices)
            st.success("Prices updated!")
            st.rerun()
    st.subheader("Current Prices")
    df = pd.DataFrame(prices).T
    st.dataframe(df)

elif page == "BOQ & Export":
    st.title("📋 Bill of Quantities & Export")
    boq_items = compute_boq(spec)
    st.subheader("Bill of Quantities")
    df_boq = pd.DataFrame(boq_items)
    st.table(df_boq)
    prices = load_prices()
    country = spec.get("east_africa_country","Uganda")
    total = 0
    for item in boq_items:
        price = get_price(item["item"], country)
        item["unit_cost"] = price
        item["total_cost"] = price * item["qty"]
        total += item["total_cost"]
    st.subheader("Cost Estimation")
    df_cost = pd.DataFrame(boq_items)
    st.dataframe(df_cost)
    st.metric(f"Total Estimated Cost ({country})", f"{total:,.0f}")
    st.subheader("IFC Export")
    ifc_text = export_ifc(spec)
    st.download_button("📥 Download IFC File", ifc_text, file_name=f"{spec['building_name']}.ifc", mime="text/plain")
    st.subheader("Download Spec as JSON")
    st.download_button("📥 Download Spec JSON", json.dumps(spec, indent=2), file_name=f"{spec['building_name']}.json")

elif page == "Settings":
    st.title("⚙️ Settings")
    unit = st.selectbox("Unit System", ["Metric","Imperial"], index=0 if unit=="Metric" else 1)
    st.session_state.unit_system = unit
    theme = st.selectbox("Design Theme", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme))
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    if st.button("Reset Specification to Default"):
        st.session_state.spec = {
            "building_name": "Project Name",
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
            "rooms": [
                {"name":"Living Room","type":"living","width":6.0,"length":5.0,"height":3.0,
                 "flooring":"wood","ceiling":"flat","bulbs":4,"sockets":6,"switches":2,
                 "furniture":[{"item":"Sofa","w":2.0,"d":1.0,"h":0.9}]}
            ],
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
        st.success("Specification reset to default.")

st.markdown('<div style="text-align:center;padding:1.5rem 0;color:#9b8ec4;font-size:0.8rem;border-top:1px solid rgba(255,255,255,0.05);">⚡ RANDOM · AI Powered · Data Driven · Secure</div>', unsafe_allow_html=True)
