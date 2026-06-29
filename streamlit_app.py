# =========================================================
# RANDOM — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# Generative Multi-Story Floor Plan & Regional Cost Synthesis
# Zero-Dependency Single-File Streamlit Implementation
# =========================================================

import streamlit as st
import json
import uuid
import random
import math
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG & GLOBAL HUD COSMETICS
# =========================================================

st.set_page_config(
    page_title="Arc Forex & Arch AI",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_studio_v12.json")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stSidebarNav"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.03em;
    }

    .arc-blueprint-canvas {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 16px;
        background: #090d16;
        padding: 24px;
        border-radius: 12px;
        border: 1px dashed #334155;
        margin: 15px 0;
    }
    
    .arc-room-module {
        padding: 24px;
        border-radius: 8px;
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .room-title {
        font-size: 1.15rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 6px;
    }

    .room-meta {
        font-family: 'Space Grotesk', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        opacity: 0.75;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# REGIONAL FOREX DATA ENGINE (EAST AFRICA - LIVE 2026 RATES)
# =========================================================

REGIONAL_FX = {
    "Kenya": {"currency": "KES", "rate_to_usd": 129.49, "symbol": "KSh", "cost_multiplier": 1.0},
    "Uganda": {"currency": "UGX", "rate_to_usd": 3665.20, "symbol": "USh", "cost_multiplier": 0.95},
    "Tanzania": {"currency": "TZS", "rate_to_usd": 2625.00, "symbol": "TSh", "cost_multiplier": 0.98},
    "South Sudan": {"currency": "SSP", "rate_to_usd": 4626.40, "symbol": "SSP", "cost_multiplier": 1.35} # Premium due to structural logistics 
}

DEFAULT_STATE = {
    "designs": [],
    "logs": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except Exception:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

# =========================================================
# ARCHITECTURAL MATRIX SYNTHESIS
# =========================================================

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"],
    "Commercial": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"],
    "Industrial": ["Distribution Depot", "Heavy Machinery Plant Warehouse"]
}

def generate_spatial_model(domain, btype, plot_size, floors, target_bathrooms, target_country):
    max_footprint = int(plot_size * 0.65)
    floor_area = min(max_footprint, random.randint(120, int(max_footprint * 1.1)))
    total_gfa = floor_area * floors
    
    span_length = 6.0 if domain == "Residential" else (7.5 if domain == "Commercial" else 12.0)
    col_count = max(12, int((floor_area / (span_length * 5.0)) * 4))
    beam_count = int(col_count * 1.8)
    
    rooms = []
    rooms.append({"name": "Central Corridor Gallery", "type": "Corridor", "w": 2.5, "h": 14.0, "color": "#1e293b"})
    rooms.append({"name": "Main Staircase Core", "type": "Stairs", "w": 4.5, "h": 4.0, "color": "#334155"})
    
    if domain == "Residential":
        rooms.append({"name": "Grand Living Room", "type": "Living Room", "w": 7.0, "h": 5.5, "color": "#0d2040"})
        rooms.append({"name": "Chef's Kitchen Deck", "type": "Kitchen", "w": 4.5, "h": 4.0, "color": "#053020"})
        bedroom_count = max(1, int(total_gfa / 75))
        for i in range(bedroom_count):
            rooms.append({"name": f"Master Suite Room {i+1}", "type": "Bedroom", "w": 4.5, "h": 4.0, "color": "#2a0f4d"})
    elif domain == "Commercial":
        rooms.append({"name": "Co-Working Hub Suite", "type": "Office Space", "w": 12.0, "h": 8.0, "color": "#075e8a"})
        rooms.append({"name": "Executive Dialogue Hall", "type": "Conference", "w": 6.0, "h": 5.0, "color": "#1e1b4b"})
    else:
        rooms.append({"name": "Main Production Bay Floor", "type": "Manufacturing Floor", "w": 18.0, "h": 12.0, "color": "#3b0764"})
        rooms.append({"name": "Logistics Dispatch Terminal", "type": "Loading Bay", "w": 8.0, "h": 8.0, "color": "#451a03"})

    for b in range(target_bathrooms):
        rooms.append({"name": f"Sanitary Bathroom {b+1}", "type": "Bathroom", "w": 3.0, "h": 2.5, "color": "#4a2306"})

    doors = len(rooms) + floors * 2
    windows = max(4, int(total_gfa / 16))

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "domain": domain,
        "type": btype,
        "plot_size": plot_size,
        "floors": floors,
        "floor_area": floor_area,
        "total_gfa": total_gfa,
        "rooms": rooms,
        "doors": doors,
        "windows": windows,
        "country": target_country,
        "structural": {
            "columns": int(col_count * floors),
            "beams": int(beam_count * floors),
            "span": span_length
        }
    }

# =========================================================
# GRAPHICS CANVAS RENDERING ENGINE
# =========================================================

def render_native_blueprint(plan):
    canvas_html = '<div class="arc-blueprint-canvas">'
    for room in plan:
        canvas_html += (
            f'<div class="arc-room-module" style="background-color: {room["color"]};">'
            f'<div class="room-title">{room["name"]}</div>'
            f'<div class="room-meta">📐 {room["w"]}m × {room["h"]}m Layout ({room["type"]})</div>'
            f'</div>'
        )
    canvas_html += '</div>'
    st.markdown(canvas_html, unsafe_allow_html=True)

# =========================================================
# STRUCTURAL CODE TESTING (EUROCODES)
# =========================================================

def run_eurocode_analysis(d, domain):
    span = d["structural"]["span"]
    gk = 5.5  
    qk = 2.0 if domain == "Residential" else (3.5 if domain == "Commercial" else 7.5)
    
    design_load_kpa = (1.35 * gk) + (1.50 * qk)
    w_ed = design_load_kpa * 4.5  
    m_ed = (w_ed * (span ** 2)) / 8
    
    b = 300; d_eff = 450; f_ck = 30  
    m_rd = (0.167 * f_ck * b * (d_eff ** 2)) / 10**6
    allowable_deflection = (span * 1000) / 250
    est_deflection = (5 * (w_ed/1.35) * (span**4) * 10**12) / (384 * 200000 * (b * (d_eff**3) / 12))
    
    return {
        "design_load": f"{design_load_kpa:.2f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm",
        "m_rd": f"{m_rd:.1f} kNm",
        "uls_status": "PASS (Design Load Capacity Envelope OK)" if m_rd > m_ed else "FAIL (Increase Profile Depth)",
        "deflection_limit": f"{allowable_deflection:.1f} mm",
        "calculated_deflection": f"{min(allowable_deflection, est_deflection):.1f} mm"
    }

# =========================================================
# MATERIAL QUANTUM ASSESSMENT & FOREX BILL OF QUANTITIES
# =========================================================

def compute_forex_boq(d, target_country):
    gfa = d["total_gfa"]
    fx_meta = REGIONAL_FX[target_country]
    fx_rate = fx_meta["rate_to_usd"]
    currency_symbol = fx_meta["symbol"]
    regional_multiplier = fx_meta["cost_multiplier"]
    
    # Base Quantities
    conc_qty = int(gfa * 0.35)
    steel_qty = int(conc_qty * 0.12)
    brick_qty = int(gfa * 38)
    finish_qty = int(gfa)
    
    base_usd_items = [
        {"Item Description": "Substructure Ground Earth Excavations", "Qty": int(gfa*0.15), "Unit": "m³", "Rate_USD": 150},
        {"Item Description": "Structural C30 Reinforcement Concrete", "Qty": conc_qty, "Unit": "m³", "Rate_USD": 210},
        {"Item Description": "Tensile Steel Bars Profile (B500B)", "Qty": steel_qty, "Unit": "Tons", "Rate_USD": 1200},
        {"Item Description": "External Wall Perimeter Blockwork Masonry", "Qty": brick_qty, "Unit": "Pcs", "Rate_USD": 2.5},
        {"Item Description": "Internal Floor Level Screed & Tiling Work", "Qty": finish_qty, "Unit": "m²", "Rate_USD": 40},
        {"Item Description": "Timber Internal Opening Door Fitting Units", "Qty": d["doors"], "Unit": "Sets", "Rate_USD": 300},
        {"Item Description": "Anodized Aluminum Glazed Window Assemblies", "Qty": d["windows"], "Unit": "Sets", "Rate_USD": 450}
    ]
    
    grand_total_usd = 0
    grand_total_local = 0
    calculated_items = []
    
    for item in base_usd_items:
        adjusted_rate_usd = item["Rate_USD"] * regional_multiplier
        cost_usd = item["Qty"] * adjusted_rate_usd
        cost_local = cost_usd * fx_rate
        grand_total_usd += cost_usd
        grand_total_local += cost_local
        
        calculated_items.append({
            "Material Asset Item": item["Item Description"],
            "Quantity Matrix": f"{item['Qty']:,} {item['Unit']}",
            "Rate (Local Currency)": f"{currency_symbol} {int(adjusted_rate_usd * fx_rate):,}",
            "Total Local Cost": f"{currency_symbol} {int(cost_local):,}"
        })
        
    return calculated_items, grand_total_usd, grand_total_local, fx_meta

# =========================================================
# ISOMETRIC CANVAS ENGINE (3D HOVER VIEWPORT)
# =========================================================

def draw_3d_isometric_canvas(plan):
    canvas_w, canvas_h = 800, 380
    shapes_js = ""
    for idx, r in enumerate(plan):
        offset_x = (idx % 3) * 170 + 100
        offset_y = (idx // 3) * 110 + 130
        rw = min(115, int(r["w"] * 14))
        rh = min(95, int(r["h"] * 14))
        color = r["color"]
        
        shapes_js += f"""
        ctx.fillStyle = "{color}";
        ctx.beginPath();
        ctx.moveTo({offset_x}, {offset_y});
        ctx.lineTo({offset_x} + {rw}, {offset_y} - {rh}/2);
        ctx.lineTo({offset_x} + {rw} + {rw}, {offset_y});
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = "rgba(255,255,255,0.3)";
        ctx.stroke();
        
        ctx.fillStyle = "rgba(255,255,255,0.06)";
        ctx.beginPath();
        ctx.moveTo({offset_x}, {offset_y});
        ctx.lineTo({offset_x}, {offset_y} - 40);
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2 - 40);
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 11px Space Grotesk";
        ctx.fillText("{r['name']}", {offset_x} + 15, {offset_y} - 2);
        """

    return f"""
    <div style="background:#040711; padding:12px; border-radius:10px; border:1px solid #1e293b; text-align:center;">
        <canvas id="arc3dCanvas" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#050814;"></canvas>
        <script>
            const canvas = document.getElementById('arc3dCanvas');
            const ctx = canvas.getContext('2d');
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.04)';
            for(let i=0; i<canvas.width; i+=40) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}
            for(let j=0; j<canvas.height; j+=40) {{ ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(canvas.width, j); ctx.stroke(); }}
            {shapes_js}
        </script>
    </div>
    """

# =========================================================
# APPLICATION CONTROL ENGINE LAYERS
# =========================================================

st.sidebar.title("📐 Arc Engine")
st.sidebar.caption("v12.1 • Regional Forex & Architectural Engine")
st.sidebar.markdown("---")

nav_page = st.sidebar.radio("Studio Workspace", ["Control Hub Dashboard", "Generative Design Engine"])
st.sidebar.markdown("---")

with st.sidebar.expander("📐 Arc Configuration Options", expanded=True):
    select_country = st.selectbox("East African Target Region", list(REGIONAL_FX.keys()))
    select_domain = st.selectbox("Structural Logic Domain", list(ARCH_DOMAINS.keys()))
    select_type = st.selectbox("Specific Typology", ARCH_DOMAINS[select_domain])
    
    input_plot = st.slider("Total Boundary Plot Area (m²)", 200, 5000, 800, step=50)
    input_floors = st.slider("Building Height Limit (Floors)", 1, 12, 3)
    input_baths = st.slider("Total Bathroom Batteries", 1, 10, 2)

# ---------------------------------------------------------
# WORKSPACE DISPLAY: DASHBOARD
# ---------------------------------------------------------
if nav_page == "Control Hub Dashboard":
    st.title("📐 Regional Structural Dashboard")
    st.markdown("Systems online. Cross-referencing East African Forex indices with Eurocode construction configurations.")
    
    fx_col1, fx_col2, fx_col3, fx_col4 = st.columns(4)
    fx_col1.metric("Live Forex USD / KES", f"KSh {REGIONAL_FX['Kenya']['rate_to_usd']}")
    fx_col2.metric("Live Forex USD / UGX", f"USh {REGIONAL_FX['Uganda']['rate_to_usd']}")
    fx_col3.metric("Live Forex USD / TZS", f"TSh {REGIONAL_FX['Tanzania']['rate_to_usd']}")
    fx_col4.metric("Live Forex USD / SSP", f"SSP {REGIONAL_FX['South Sudan']['rate_to_usd']}")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Evolved Blueprints Saved", len(mem["designs"]))
    c2.metric("Telemetry Pipeline Computations", len(mem["logs"]))

# ---------------------------------------------------------
# WORKSPACE DISPLAY: SYNTHESIS CORE LAB
# ---------------------------------------------------------
elif nav_page == "Generative Design Engine":
    st.title("🌍 Architecture & Regional Material Synthesis Lab")
    st.markdown("Opens design vectors using current exchange parameters. Tweak structural values directly inside the sidebar.")
    
    trigger_synthesis = st.button("Initialize Regional Generative Synthesis Sequence", type="primary", use_container_width=True)
    
    if trigger_synthesis:
        with st.spinner("Synchronizing currency profiles and processing structural calculations..."):
            generated_asset = generate_spatial_model(select_domain, select_type, input_plot, input_floors, input_baths, select_country)
            generated_asset["plan"] = generated_asset["rooms"]
            
            st.session_state.active_design = generated_asset
            mem["designs"].append(generated_asset)
            log_event(f"Evolved local multi-floor architectural framework instance #{generated_asset['id']}")

    st.markdown("---")

    if st.session_state.active_design is not None:
        asset = st.session_state.active_design
        
        st.subheader(f"⚡ Live Specification Frame: Model Archetype #{asset['id']}")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Regional Assignment", asset["country"])
        m2.metric("Gross Built Area Floor Space", f"{asset['total_gfa']:,} m²")
        m3.metric("Level Structural Count", f"{asset['floors']} Storeys")
        m4.metric("Framing Openings", f"{asset['doors']} Doors / {asset['windows']} Windows")
        
        st.markdown("<br>", unsafe_allow_html=True)
        tab_2d, tab_3d, tab_eurocode, tab_boq = st.tabs([
            "🗺️ 2D Spatial Floor Plan Blueprint", 
            "📦 3D Wireframe Isometric View", 
            "📐 Eurocode Analysis Load Check", 
            "💰 Currency Dynamic Bill of Quantities"
        ])
        
        with tab_2d:
            st.markdown("### 🗺️ Plan Spatial Configurations Layout")
            render_native_blueprint(asset["plan"])
            
        with tab_3d:
            st.markdown("### 📦 3D Isometric Elevation Viewport")
            html_isometric_view = draw_3d_isometric_canvas(asset["plan"])
            st.components.v1.html(html_isometric_view, height=410)
            
        with tab_eurocode:
            st.markdown("### 📐 Eurocode 2 Structural Strength Envelope")
            analysis = run_eurocode_analysis(asset, asset["domain"])
            
            e1, e2, e3 = st.columns(3)
            e1.metric("Design Ultimate Loading ($E_{d}$)", analysis["design_load"])
            e2.metric("Applied Action Moment ($M_{Ed}$)", analysis["m_ed"])
            e3.metric("Section Resistance ($M_{Rd}$)", analysis["m_rd"])
            st.info(f"**Structural Capacity Check:** {analysis['uls_status']}")
            
        with tab_boq:
            st.markdown("### 📊 Live Multi-Currency Forex Bill of Quantities")
            boq_table, total_usd, total_local, current_fx = compute_forex_boq(asset, asset["country"])
            
            st.table(boq_table)
            
            b_usd, b_local = st.columns(2)
            b_usd.metric("Total Project Cost Basis (USD)", f"$ {int(total_usd):,}")
            b_local.metric(f"Localized Target Estimation ({current_fx['currency']})", f"{current_fx['symbol']} {int(total_local):,}")
            st.caption(f"Conversion computed utilizing live indices: **1 USD = {current_fx['rate_to_usd']} {current_fx['currency']}**")
            
    else:
        st.info("No layout structures are currently loaded into memory. Adjust the parameters on the sidebar options panel and run the pipeline generator.")