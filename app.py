import os, json, uuid, hashlib, math, random, base64
from datetime import datetime
from pathlib import Path
from flask import Flask, session, request, render_template_string, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change_me_in_production_123!")

# ---------- In‑memory data (resets on cold start) ----------
USERS = {}
PRICES = {
    "Cement (50kg bag)": {"USD":8,"UGX":29000,"KES":1100,"TZS":20000,"RWF":9000,"SSP":12000},
    "Steel Rebar (ton)": {"USD":800,"UGX":2900000,"KES":110000,"TZS":2000000,"RWF":900000,"SSP":1200000},
    "Concrete Blocks (1000 units)": {"USD":250,"UGX":900000,"KES":34000,"TZS":600000,"RWF":270000,"SSP":375000},
    "Timber (m³)": {"USD":300,"UGX":1100000,"KES":41000,"TZS":750000,"RWF":330000,"SSP":450000},
    "Roofing Sheets (per m²)": {"USD":5,"UGX":18000,"KES":680,"TZS":12000,"RWF":5500,"SSP":7500},
    "Tiles (per m²)": {"USD":12,"UGX":43000,"KES":1600,"TZS":30000,"RWF":13500,"SSP":18000},
    "Paint (per litre)": {"USD":4,"UGX":14500,"KES":550,"TZS":10000,"RWF":4500,"SSP":6000},
    "Glass (per m²)": {"USD":25,"UGX":90000,"KES":3400,"TZS":65000,"RWF":28000,"SSP":37500},
}
XP_PER_LEVEL = 100

DEFAULT_SPEC = {
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

if "admin" not in USERS:
    USERS["admin"] = {"password_hash": hashlib.sha256(("admin123"+"rand_salt").encode()).hexdigest(),
                      "role":"admin","level":1,"xp":0,"badges":[],
                      "created": datetime.now().isoformat()}

# ---------- Helpers ----------
def hash_password(pw):
    return hashlib.sha256((pw+"rand_salt").encode()).hexdigest()

def get_user(uname):
    return USERS.get(uname)

def authenticate(uname, pw):
    u = get_user(uname)
    if u and u["password_hash"] == hash_password(pw):
        return u
    return None

def create_user(uname, pw, role="user"):
    if uname in USERS:
        return False, "Username exists"
    USERS[uname] = {
        "password_hash": hash_password(pw),
        "role": role,
        "level": 1,
        "xp": 0,
        "badges": [],
        "created": datetime.now().isoformat()
    }
    return True, "User created"

def add_xp(uname, amount):
    user = USERS.get(uname)
    if not user:
        return False
    user["xp"] += amount
    while user["xp"] >= XP_PER_LEVEL * user["level"]:
        user["xp"] -= XP_PER_LEVEL * user["level"]
        user["level"] += 1
    return True

def compute_boq(spec):
    items = []
    cols = int(spec["overall_length"] / spec["grid"]["spacing_x"]) + 1
    rows = int(spec["overall_width"] / spec["grid"]["spacing_y"]) + 1
    col_vol = cols * rows * spec["floors"] * (spec["grid"]["column_size"]**2) * spec["floor_height"]
    items.append({"item":"Concrete for Columns", "unit":"m³", "qty":round(col_vol,2)})
    beam_len = (cols * spec["overall_width"] + rows * spec["overall_length"]) * spec["floors"]
    beam_vol = beam_len * 0.23 * 0.3
    items.append({"item":"Concrete for Beams", "unit":"m³", "qty":round(beam_vol,2)})
    ext_wall_area = 2 * (spec["overall_length"] + spec["overall_width"]) * spec["floor_height"] * spec["floors"]
    items.append({"item":"Exterior Brickwork", "unit":"m²", "qty":round(ext_wall_area,0)})
    int_wall_area = (len(spec["rooms"]) - 1) * spec["overall_width"] * spec["floor_height"] * spec["floors"]
    items.append({"item":"Interior Brickwork", "unit":"m²", "qty":round(int_wall_area,0)})
    floor_area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
    items.append({"item":"Floor Tiles", "unit":"m²", "qty":round(floor_area,0)})
    roof_area = spec["overall_length"] * spec["overall_width"]
    items.append({"item":"Roof Sheets", "unit":"m²", "qty":round(roof_area,0)})
    paint_area = ext_wall_area + int_wall_area
    items.append({"item":"Paint (exterior+interior)", "unit":"litre", "qty":round(paint_area*0.1,0)})
    items.append({"item":"Doors", "unit":"pcs", "qty":len(spec["doors"])})
    items.append({"item":"Windows", "unit":"pcs", "qty":len(spec["windows"])})
    glazing_area = sum(w["width"]*w["height"] for w in spec["windows"])
    items.append({"item":"Glass", "unit":"m²", "qty":round(glazing_area,2)})
    return items

def get_price(material, country):
    base = PRICES.get(material, {"USD":0})
    curr = {"Uganda":"UGX","Kenya":"KES","Tanzania":"TZS","Rwanda":"RWF","South Sudan":"SSP"}.get(country, "UGX")
    return base.get(curr, base.get("USD",0))

def export_ifc(spec):
    lines = [
        "ISO-10303-21;",
        "HEADER;",
        "FILE_DESCRIPTION((''),'2;1');",
        "FILE_NAME('','',(''),(''),'','','');",
        "FILE_SCHEMA(('IFC2X3'));",
        "ENDSEC;",
        "DATA;",
        "#1=IFCPROJECT('0yj$xKATr2DB8z9k8I$LEl',#0,'Project',$,$,$,$,$,#0);",
        "ENDSEC;",
        "END-ISO-10303-21;"
    ]
    return "\n".join(lines)

THEME_CSS = {
    "Warm Amber": """
        :root {
            --bg-gradient: radial-gradient(circle at top right, #2d1b34, #0f0f1a 60%);
            --sidebar-bg: linear-gradient(180deg, #1a1025, #0c0714);
            --btn-gradient: linear-gradient(135deg, #fbbf24, #f97316);
            --accent: #fbbf24;
            --card-bg: rgba(25,20,40,0.65);
            --text: #f5f0eb;
        }
    """,
    "Ocean Blue": """
        :root {
            --bg-gradient: radial-gradient(circle at top right, #0f2027, #203a43 60%);
            --sidebar-bg: linear-gradient(180deg, #0a1a24, #051016);
            --btn-gradient: linear-gradient(135deg, #38bdf8, #0ea5e9);
            --accent: #38bdf8;
            --card-bg: rgba(15,30,40,0.65);
            --text: #e0f0ff;
        }
    """,
    "Emerald Green": """
        :root {
            --bg-gradient: radial-gradient(circle at top right, #0a2a1a, #05100a 60%);
            --sidebar-bg: linear-gradient(180deg, #0a1f14, #030b06);
            --btn-gradient: linear-gradient(135deg, #34d399, #059669);
            --accent: #34d399;
            --card-bg: rgba(10,30,20,0.65);
            --text: #e0ffe0;
        }
    """,
    "Light Mode": """
        :root {
            --bg-gradient: linear-gradient(135deg, #f8f9fa, #e9ecef);
            --sidebar-bg: linear-gradient(180deg, #ffffff, #f1f3f5);
            --btn-gradient: linear-gradient(135deg, #339af0, #1c7ed6);
            --accent: #339af0;
            --card-bg: rgba(255,255,255,0.85);
            --text: #212529;
        }
    """
}

# ---------- Flask Routes ----------
@app.route("/login", methods=["GET","POST"])
def login():
    if "user" in session:
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        uname = request.form.get("username","")
        pw = request.form.get("password","")
        action = request.form.get("action")
        if action == "register":
            if not uname or not pw:
                error = "Fill all fields"
            else:
                success, msg = create_user(uname, pw)
                if success:
                    session["user"] = uname
                    session["spec"] = DEFAULT_SPEC.copy()
                    session["projects"] = []
                    return redirect(url_for("index"))
                else:
                    error = msg
        else:
            user = authenticate(uname, pw)
            if user:
                session["user"] = uname
                session["spec"] = DEFAULT_SPEC.copy()
                session["projects"] = []
                return redirect(url_for("index"))
            else:
                error = "Invalid credentials"
    return render_template_string(LOGIN_HTML, error=error)

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    # Ensure projects list exists
    if "projects" not in session:
        session["projects"] = []
    return render_template_string(INDEX_HTML,
                                  user=session["user"],
                                  user_data=USERS[session["user"]],
                                  spec=session.get("spec", DEFAULT_SPEC),
                                  projects=session.get("projects", []),
                                  theme=session.get("theme","Warm Amber"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/update_spec", methods=["POST"])
def update_spec():
    if "user" not in session:
        return "Unauthorized", 401
    spec = session.get("spec", DEFAULT_SPEC)
    for key in ["building_name","floors","overall_length","overall_width"]:
        val = request.form.get(key)
        if val is not None:
            try:
                if key == "building_name":
                    spec[key] = val
                else:
                    spec[key] = float(val)
            except:
                pass
    session["spec"] = spec
    return redirect(url_for("index"))

@app.route("/update_theme", methods=["POST"])
def update_theme():
    if "user" not in session:
        return "Unauthorized", 401
    theme = request.form.get("theme","Warm Amber")
    if theme in THEME_CSS:
        session["theme"] = theme
    return redirect(url_for("index"))

@app.route("/ram_chat", methods=["POST"])
def ram_chat():
    if "user" not in session:
        return "Unauthorized", 401
    query = request.form.get("query","")
    spec = session.get("spec", DEFAULT_SPEC)
    resp = f"Ram says: I'm still learning. You asked: {query}"
    if "boq" in query.lower():
        items = compute_boq(spec)
        resp = "📋 Bill of Quantities:\n" + "\n".join([f"{i['item']}: {i['qty']} {i['unit']}" for i in items])
    elif "cost" in query.lower():
        area = spec["overall_length"] * spec["overall_width"] * spec["floors"]
        resp = f"Estimated cost: ${area*1500:,.0f}"
    return resp

@app.route("/download/ifc")
def download_ifc():
    spec = session.get("spec", DEFAULT_SPEC)
    ifc = export_ifc(spec)
    response = make_response(ifc)
    response.headers["Content-Disposition"] = f"attachment; filename={spec.get('building_name','project')}.ifc"
    response.mimetype = "text/plain"
    return response

@app.route("/download/spec")
def download_spec():
    spec = session.get("spec", DEFAULT_SPEC)
    json_str = json.dumps(spec, indent=2)
    response = make_response(json_str)
    response.headers["Content-Disposition"] = f"attachment; filename={spec.get('building_name','project')}_spec.json"
    response.mimetype = "application/json"
    return response

# ---------- New Project Routes ----------
@app.route("/save_project", methods=["POST"])
def save_project():
    if "user" not in session:
        return "Unauthorized", 401
    name = request.form.get("project_name","").strip()
    if not name:
        return "Project name required", 400
    projects = session.get("projects", [])
    # Check if name already exists
    for p in projects:
        if p["name"] == name:
            # Update existing project
            p["spec"] = session.get("spec", DEFAULT_SPEC).copy()
            p["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            session["projects"] = projects
            return redirect(url_for("index"))
    # New project
    projects.append({
        "name": name,
        "spec": session.get("spec", DEFAULT_SPEC).copy(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    session["projects"] = projects
    return redirect(url_for("index"))

@app.route("/load_project/<path:name>")
def load_project(name):
    if "user" not in session:
        return "Unauthorized", 401
    projects = session.get("projects", [])
    for p in projects:
        if p["name"] == name:
            session["spec"] = p["spec"].copy()
            return redirect(url_for("index"))
    return "Project not found", 404

@app.route("/delete_project/<path:name>")
def delete_project(name):
    if "user" not in session:
        return "Unauthorized", 401
    projects = session.get("projects", [])
    projects = [p for p in projects if p["name"] != name]
    session["projects"] = projects
    return redirect(url_for("index"))

# ---------- HTML Templates ----------
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RANDOM Studio - Login</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body { background: #0f0f1a; font-family: 'Outfit', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .login-card { background: rgba(25,20,40,0.8); backdrop-filter: blur(16px); border-radius: 28px; padding: 3rem; border: 1px solid rgba(255,255,255,0.1); width: 100%; max-width: 400px; }
    .logo-text { font-size: 2.4rem; font-weight: 800; background: linear-gradient(135deg, #fbbf24, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; text-align: center; }
    input { width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; background: rgba(0,0,0,0.4); color: white; font-size: 1rem; }
    button { width: 100%; padding: 0.75rem; background: linear-gradient(135deg, #fbbf24, #f97316); border: none; border-radius: 18px; font-weight: 700; color: #0b0710; cursor: pointer; margin-top: 0.5rem; }
    .error { color: #f87171; margin-bottom: 1rem; }
  </style>
</head>
<body>
  <div class="login-card">
    <div class="logo-text">⚡ RANDOM</div>
    <p style="text-align:center; color:#e0d7ff;">Single‑Project AEC Studio</p>
    {% if error %}<div class="error">{{ error }}</div>{% endif %}
    <form method="post">
      <input type="text" name="username" placeholder="Username" required>
      <input type="password" name="password" placeholder="Password" required>
      <div style="display:flex; gap:10px;">
        <button type="submit" name="action" value="login">Login</button>
        <button type="submit" name="action" value="register">Register</button>
      </div>
    </form>
  </div>
</body>
</html>
"""

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RANDOM Studio</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    {% if theme and theme in ['Warm Amber','Ocean Blue','Emerald Green','Light Mode'] %}
    {{ theme_css[theme] | safe }}
    {% else %}
    {{ theme_css['Warm Amber'] | safe }}
    {% endif %}
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', sans-serif; background: var(--bg-gradient); color: var(--text); display: flex; min-height: 100vh; overflow-x: hidden; }
    .sidebar {
      width: 280px;
      background: var(--sidebar-bg);
      padding: 2rem 1.5rem;
      border-right: 1px solid rgba(255,255,255,0.08);
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      transition: transform 0.3s ease;
      position: fixed; top: 0; left: 0; bottom: 0; z-index: 999;
    }
    .sidebar.collapsed { transform: translateX(-100%); }
    .main {
      margin-left: 280px;
      flex: 1;
      padding: 2rem;
      transition: margin-left 0.3s ease;
      min-height: 100vh;
    }
    .sidebar.collapsed + .main { margin-left: 0; }
    .hamburger {
      display: none;
      position: fixed;
      top: 1rem; left: 1rem;
      z-index: 1001;
      background: var(--btn-gradient);
      border: none;
      width: 40px; height: 40px;
      border-radius: 8px;
      color: #0b0710;
      font-size: 1.5rem;
      cursor: pointer;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .overlay {
      display: none;
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.5);
      z-index: 998;
    }
    .overlay.active { display: block; }
    @media (max-width: 768px) {
      .sidebar { transform: translateX(-100%); }
      .sidebar.open { transform: translateX(0); }
      .main { margin-left: 0; }
      .hamburger { display: flex; }
    }
    .logo-text { font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; background: var(--btn-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .nav-btn {
      background: transparent; border: none;
      color: var(--text); padding: 0.75rem;
      text-align: left; font-size: 1rem;
      border-radius: 12px; cursor: pointer;
      transition: background 0.2s;
    }
    .nav-btn:hover, .nav-btn.active { background: rgba(255,255,255,0.1); }
    .glass-card {
      background: var(--card-bg); backdrop-filter: blur(16px);
      border-radius: 28px; padding: 1.8rem; margin-bottom: 2rem;
      border: 1px solid rgba(255,255,255,0.1);
      box-shadow: 0 25px 45px rgba(0,0,0,0.5);
    }
    button.primary {
      background: var(--btn-gradient); color: #0b0710;
      border: none; border-radius: 18px;
      padding: 0.75rem 2rem; font-weight: 700;
      cursor: pointer; font-family: 'Outfit', sans-serif;
    }
    .tab { background: rgba(255,255,255,0.05); border: none; color: var(--text); padding: 0.75rem 1.5rem; border-radius: 12px 12px 0 0; cursor: pointer; }
    .tab.active { background: var(--card-bg); }
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    .xp-container { display: flex; align-items: center; gap: 10px; margin-bottom: 1.2rem; }
    .xp-bar-bg { flex: 1; height: 10px; background: #2e2340; border-radius: 6px; overflow: hidden; }
    .xp-bar-fill { height: 100%; background: var(--btn-gradient); border-radius: 6px; box-shadow: 0 0 10px var(--accent); }
    input, select, textarea { background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; color: white; padding: 0.5rem; width: 100%; margin-bottom: 0.5rem; }
    .project-list { display: flex; flex-direction: column; gap: 0.5rem; }
    .project-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 12px; }
    .project-item button { background: transparent; border: 1px solid rgba(255,255,255,0.2); color: var(--text); padding: 0.3rem 0.8rem; border-radius: 8px; cursor: pointer; margin-left: 0.5rem; }
  </style>
</head>
<body>
  <!-- Hamburger (mobile) -->
  <button class="hamburger" id="hamburgerBtn" onclick="toggleSidebar()">☰</button>
  <div class="overlay" id="overlay" onclick="closeSidebar()"></div>

  <div class="sidebar" id="sidebar">
    <div class="logo-text">⚡ RANDOM</div>
    <div><strong>👤 {{ user }}</strong></div>
    <div class="xp-container">
      <span style="font-size:12px;">LVL {{ user_data.level }}</span>
      <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{{ (user_data.xp / (user_data.level * 100)) * 100 if user_data.level else 0 }}%;"></div></div>
      <span style="font-size:10px;">{{ user_data.xp }}/{{ user_data.level * 100 }} XP</span>
    </div>
    <button class="nav-btn active" onclick="showPage('dashboard'); closeSidebar()">📊 Dashboard</button>
    <button class="nav-btn" onclick="showPage('ram'); closeSidebar()">🤖 Ram Assistant</button>
    <button class="nav-btn" onclick="showPage('materials'); closeSidebar()">💰 Materials & Cost</button>
    <button class="nav-btn" onclick="showPage('boq'); closeSidebar()">📋 BOQ & Export</button>
    <button class="nav-btn" onclick="showPage('projects'); closeSidebar()">📁 Projects</button>
    <button class="nav-btn" onclick="showPage('settings'); closeSidebar()">⚙️ Settings</button>
    <div style="margin-top: auto;">
      <a href="/logout"><button class="primary" style="width:100%;">🚪 Logout</button></a>
    </div>
  </div>

  <div class="main" id="mainContent">
    <!-- Dashboard Page -->
    <div id="page-dashboard" class="page active">
      <h1>⚡ {{ spec.building_name }}</h1>
      <div style="display:flex; gap:10px; margin-bottom:20px;">
        <button class="tab active" onclick="switchTab(event, 'arch')">🏛️ Architecture</button>
        <button class="tab" onclick="switchTab(event, 'eng')">⚙️ Engineering</button>
        <button class="tab" onclick="switchTab(event, 'const')">🚧 Construction</button>
      </div>
      <div id="tab-arch" class="tab-content active">
        <div class="glass-card">
          <h3>Project Identity & Shape</h3>
          <form method="post" action="/update_spec">
            <label>Project Title</label>
            <input type="text" name="building_name" value="{{ spec.building_name }}">
            <label>Floors</label>
            <input type="number" name="floors" value="{{ spec.floors }}">
            <label>Building Length (m)</label>
            <input type="number" name="overall_length" value="{{ spec.overall_length }}" step="0.1">
            <label>Building Width (m)</label>
            <input type="number" name="overall_width" value="{{ spec.overall_width }}" step="0.1">
            <button type="submit" class="primary">Save Architecture</button>
          </form>
        </div>
        <div class="glass-card">
          <h3>Rooms</h3>
          {% for room in spec.rooms %}
          <div>{{ room.name }} ({{ room.type }}) - {{ room.width }}x{{ room.length }} m</div>
          {% endfor %}
        </div>
      </div>
      <div id="tab-eng" class="tab-content">
        <div class="glass-card">
          <h3>Structural</h3>
          <p>Foundation: {{ spec.foundation }} (Depth: {{ spec.foundation_depth }} m)</p>
          <p>Columns: {{ spec.column_type }}, Beams: {{ spec.beam_type }}</p>
        </div>
      </div>
      <div id="tab-const" class="tab-content">
        <div class="glass-card">
          <h3>Construction Cost</h3>
          <p>Estimated cost: ${{ (spec.overall_length * spec.overall_width * spec.floors * 1500) | int }}</p>
          <p>Schedule: {{ spec.floors * 5 }} months</p>
        </div>
      </div>
    </div>

    <!-- Ram Assistant Page -->
    <div id="page-ram" class="page" style="display:none;">
      <h1>🤖 Creative AI – Ram</h1>
      <div class="glass-card">
        <div id="chat-history"></div>
        <textarea id="ram-input" rows="2" placeholder="Ask Ram..."></textarea>
        <button class="primary" onclick="sendRamQuery()">Ask Ram</button>
      </div>
    </div>

    <!-- Materials & Cost Page -->
    <div id="page-materials" class="page" style="display:none;">
      <h1>💰 Material Prices</h1>
      <table class="glass-card" style="width:100%; border-collapse:collapse;">
        <tr><th>Material</th><th>USD</th><th>UGX</th><th>KES</th></tr>
        {% for mat, prices in prices.items() %}
        <tr><td>{{ mat }}</td><td>{{ prices.USD }}</td><td>{{ prices.UGX }}</td><td>{{ prices.KES }}</td></tr>
        {% endfor %}
      </table>
    </div>

    <!-- BOQ & Export Page -->
    <div id="page-boq" class="page" style="display:none;">
      <h1>📋 Bill of Quantities</h1>
      {% set boq = compute_boq(spec) %}
      <table class="glass-card" style="width:100%;">
        <tr><th>Item</th><th>Unit</th><th>Quantity</th></tr>
        {% for item in boq %}
        <tr><td>{{ item.item }}</td><td>{{ item.unit }}</td><td>{{ item.qty }}</td></tr>
        {% endfor %}
      </table>
      <div style="display:flex; gap:10px; margin-top:20px;">
        <a href="/download/ifc"><button class="primary">📥 Download IFC</button></a>
        <a href="/download/spec"><button class="primary">📥 Download Spec JSON</button></a>
      </div>
    </div>

    <!-- NEW Projects Page -->
    <div id="page-projects" class="page" style="display:none;">
      <h1>📁 Saved Projects</h1>
      <div class="glass-card">
        <h3>Save Current Project</h3>
        <form method="post" action="/save_project" style="display:flex; gap:10px;">
          <input type="text" name="project_name" placeholder="Project name" value="{{ spec.building_name }}" style="flex:1;">
          <button type="submit" class="primary">Save</button>
        </form>
      </div>
      <div class="glass-card">
        <h3>Your Projects</h3>
        <div class="project-list">
          {% if projects %}
            {% for project in projects %}
            <div class="project-item">
              <span>{{ project.name }} <small style="color:var(--accent)">({{ project.date }})</small></span>
              <div>
                <a href="/load_project/{{ project.name }}"><button>Load</button></a>
                <a href="/delete_project/{{ project.name }}"><button>Delete</button></a>
              </div>
            </div>
            {% endfor %}
          {% else %}
            <p>No saved projects yet.</p>
          {% endif %}
        </div>
      </div>
    </div>

    <!-- Settings Page -->
    <div id="page-settings" class="page" style="display:none;">
      <h1>⚙️ Settings</h1>
      <form method="post" action="/update_theme">
        <label>Theme</label>
        <select name="theme" onchange="this.form.submit()">
          <option value="Warm Amber" {{ 'selected' if theme=='Warm Amber' }}>Warm Amber</option>
          <option value="Ocean Blue" {{ 'selected' if theme=='Ocean Blue' }}>Ocean Blue</option>
          <option value="Emerald Green" {{ 'selected' if theme=='Emerald Green' }}>Emerald Green</option>
          <option value="Light Mode" {{ 'selected' if theme=='Light Mode' }}>Light Mode</option>
        </select>
      </form>
    </div>
  </div>

  <script>
    // Sidebar toggle (mobile & desktop)
    function toggleSidebar() {
      const sidebar = document.getElementById('sidebar');
      const overlay = document.getElementById('overlay');
      sidebar.classList.toggle('open');
      overlay.classList.toggle('active');
    }
    function closeSidebar() {
      document.getElementById('sidebar').classList.remove('open');
      document.getElementById('overlay').classList.remove('active');
    }

    // Page switching
    function showPage(pageId) {
      document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
      const pageEl = document.getElementById('page-' + pageId);
      if (pageEl) pageEl.style.display = 'block';
      // Update active nav button
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      const clickedBtn = event.target;
      if (clickedBtn.classList.contains('nav-btn')) clickedBtn.classList.add('active');
    }

    // Dashboard tabs
    function switchTab(e, tabName) {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      e.target.classList.add('active');
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      document.getElementById('tab-' + tabName).classList.add('active');
    }

    // Ram chat
    async function sendRamQuery() {
      const query = document.getElementById('ram-input').value;
      const resp = await fetch('/ram_chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'query=' + encodeURIComponent(query)
      });
      const text = await resp.text();
      document.getElementById('chat-history').innerHTML += `<p><strong>You:</strong> ${query}</p><p><strong>Ram:</strong> ${text}</p>`;
      document.getElementById('ram-input').value = '';
    }

    // Close sidebar on window resize to avoid mobile menu stuck open
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) {
        closeSidebar();
      }
    });
  </script>
</body>
</html>
"""

# ---------- Make template variables available ----------
@app.context_processor
def inject_globals():
    return dict(
        theme_css=THEME_CSS,
        prices=PRICES,
        compute_boq=compute_boq
    )

# Vercel auto‑detects the Flask app