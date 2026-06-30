# =========================================================
# ARC — ARCHITECTURAL INTELLECT ENGINE (BIM-UPGRADED)
# Generative Spatial + Structural Synthesis Core
# =========================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="ARC BIM Engine V11",
    page_icon="🏢",
    layout="wide"
)

MEMORY_FILE = Path("arc_studio_v11.json")

# =========================================================
# STYLE (LIGHT BIM UI UPGRADE)
# =========================================================

st.markdown("""
<style>
html, body {
    font-family: 'Arial';
    background: #050814;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.arc-blueprint-canvas {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 12px;
    padding: 20px;
    border-radius: 12px;
    background: rgba(255,255,255,0.02);
}

.arc-room-module {
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #1e293b;
    transition: 0.2s;
}

.arc-room-module:hover {
    transform: translateY(-2px);
    border-color: #38bdf8;
}

.room-title {
    font-weight: bold;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM (SAFE BIM STATE)
# =========================================================

DEFAULT_STATE = {"designs": [], "logs": []}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# init session
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory

# =========================================================
# ARCH TYPES (BIM DOMAINS)
# =========================================================

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment"],
    "Commercial": ["Office Block", "Clinic Center"],
    "Industrial": ["Warehouse", "Factory"]
}

# =========================================================
# BIM ELEMENT GENERATION (IMPROVED)
# =========================================================

def uid(prefix):
    return f"{prefix}-{str(uuid.uuid4())[:8]}"

def generate_spatial_model(domain, btype, plot_size, floors, baths):

    max_fp = int(plot_size * 0.65)
    floor_area = random.randint(120, max_fp)
    total_gfa = floor_area * floors

    span = {"Residential": 6.0, "Commercial": 7.5, "Industrial": 12.0}[domain]

    col_count = max(12, floor_area // 30)
    beam_count = int(col_count * 1.8)

    rooms = []

    # CORE
    rooms.append({
        "id": uid("RM"),
        "name": "Lobby Core",
        "type": "Core",
        "w": 3,
        "h": 8,
        "color": "#1e293b"
    })

    # TYPOLOGY LOGIC
    if domain == "Residential":
        bedrooms = max(1, total_gfa // 140)
        for i in range(bedrooms):
            rooms.append({
                "id": uid("RM"),
                "name": f"Bedroom {i+1}",
                "type": "Room",
                "w": 4,
                "h": 4,
                "color": "#2a0f4d"
            })

    elif domain == "Commercial":
        rooms.append({
            "id": uid("RM"),
            "name": "Office Floor Plate",
            "type": "Work",
            "w": 10,
            "h": 8,
            "color": "#075e8a"
        })

    else:
        rooms.append({
            "id": uid("RM"),
            "name": "Industrial Hall",
            "type": "Industrial",
            "w": 14,
            "h": 10,
            "color": "#3b0764"
        })

    # SERVICE ELEMENTS
    for i in range(baths):
        rooms.append({
            "id": uid("RM"),
            "name": f"Bath {i+1}",
            "type": "Service",
            "w": 3,
            "h": 2,
            "color": "#4a2306"
        })

    return {
        "id": uid("PRJ"),
        "domain": domain,
        "type": btype,
        "plot_size": plot_size,
        "floors": floors,
        "total_gfa": total_gfa,
        "rooms": rooms,
        "doors": len(rooms),
        "windows": max(4, int(total_gfa / 25)),
        "structural": {
            "columns": col_count * floors,
            "beams": beam_count * floors,
            "span": span
        }
    }

# =========================================================
# FLOOR PLAN
# =========================================================

def generate_floor_plan(d):
    return d["rooms"]

# =========================================================
# RENDER ENGINE (BIM GRID)
# =========================================================

def render(plan):

    st.markdown("### 🧱 BIM Floor Assembly View")

    html = '<div class="arc-blueprint-canvas">'

    for r in plan:
        html += f"""
        <div class="arc-room-module" style="background:{r['color']}">
            <div class="room-title">{r['name']}</div>
            <div>{r['w']}m × {r['h']}m</div>
            <div style="opacity:0.6;font-size:12px">{r['type']}</div>
            <div style="opacity:0.5;font-size:11px">ID: {r['id']}</div>
        </div>
        """

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# EUROCODE ENGINE (STABILIZED)
# =========================================================

def eurocode(d):

    span = d["structural"]["span"]

    gk = 5.5
    qk = 2.0 if d["domain"] == "Residential" else 3.5

    load = (1.35 * gk) + (1.5 * qk)
    w_ed = load * 4.5

    m_ed = (w_ed * span ** 2) / 8

    m_rd = (0.167 * 30 * 300 * (450 ** 2)) / 1e6

    return {
        "MEd": round(m_ed, 2),
        "MRd": round(m_rd, 2),
        "UTILIZATION": round(m_ed / max(m_rd, 1), 2),
        "STATUS": "PASS" if m_rd > m_ed else "FAIL"
    }

# =========================================================
# UI
# =========================================================

st.sidebar.title("ARC BIM V11")
page = st.sidebar.radio("Mode", ["Dashboard", "Generate"])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🏢 ARC BIM CONTROL DASHBOARD")

    c1, c2 = st.columns(2)

    c1.metric("Design Models", len(mem["designs"]))
    c2.metric("System Logs", len(mem["logs"]))

    st.markdown("---")
    st.subheader("Recent Activity")

    for log in reversed(mem["logs"][-6:]):
        st.caption(f"{log['time'][11:19]} → {log['msg']}")

# =========================================================
# GENERATION
# =========================================================

elif page == "Generate":

    st.title("🏗 BIM GENERATION CORE")

    domain = st.selectbox("Domain", list(ARCH_DOMAINS.keys()))
    btype = st.selectbox("Typology", ARCH_DOMAINS[domain])

    plot = st.slider("Plot Size (m²)", 200, 3000, 800)
    floors = st.slider("Floors", 1, 10, 3)
    baths = st.slider("Bathrooms", 1, 6, 2)

    if st.button("Generate BIM Model"):

        asset = generate_spatial_model(domain, btype, plot, floors, baths)
        asset["plan"] = generate_floor_plan(asset)

        mem["designs"].append(asset)
        log_event("BIM model generated")

        st.success("Model Generated Successfully")

        # SUMMARY
        st.subheader("📦 Model Summary")
        st.json({
            "ID": asset["id"],
            "Domain": asset["domain"],
            "Floors": asset["floors"],
            "GFA": asset["total_gfa"],
            "Elements": len(asset["rooms"])
        })

        # FLOOR PLAN
        st.subheader("🧱 Floor Plan")
        render(asset["plan"])

        # EUROCODE
        st.subheader("📐 Structural Check")
        st.json(eurocode(asset))
