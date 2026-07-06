# =============================
# ARC STUDIO V15
# AEC + BIM + EVOLUTION ENGINE CORE
# =============================

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
    page_title="Arc Studio V15 - AEC Engine",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "bim_models": [],
    "logs": [],
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(st.session_state.memory, f, indent=2)

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory

# =========================================================
# AEC BIM DATA MODEL (NEW CORE ADDITION)
# =========================================================

def create_bim_model(design):
    """Turns raw design into BIM-like structured object"""

    floors = design.get("floors", 1)
    bedrooms = design.get("bedrooms", 1)

    bim = {
        "project_id": design["id"],
        "architecture": {
            "floors": floors,
            "rooms": design.get("rooms", []),
            "typology": design.get("type", "Unknown")
        },
        "structure": {
            "columns": random.randint(20, 80),
            "beams": random.randint(40, 160),
            "slabs": floors,
            "foundation": "Raft Foundation"
        },
        "mep": {
            "water_system": "Pressurized Network",
            "electrical": "3-phase distribution",
            "fire_system": "Sprinkler + Hydrant",
            "drainage": "Gravity + Pump Assist"
        },
        "hvac": {
            "system": "VRF / Central Chiller Hybrid",
            "air_handling_units": random.randint(1, floors),
            "cooling_load_kw": random.randint(50, 500),
            "zones": floors * 2
        },
        "cost_model": {
            "structure_cost": 0,
            "mep_cost": 0,
            "hvac_cost": 0,
            "total": 0
        }
    }

    return bim

# =========================================================
# AEC COST ENGINE (NEW)
# =========================================================

def calculate_costs(bim):
    base_structure = bim["structure"]["columns"] * 1200
    base_mep = bim["architecture"]["floors"] * 15000
    base_hvac = bim["hvac"]["cooling_load_kw"] * 300

    total = base_structure + base_mep + base_hvac

    bim["cost_model"] = {
        "structure_cost": base_structure,
        "mep_cost": base_mep,
        "hvac_cost": base_hvac,
        "total": total
    }

    return bim

# =========================================================
# GENETIC ENGINE (SIMPLIFIED V15 CORE)
# =========================================================

def generate_design():
    return {
        "id": str(uuid.uuid4())[:8],
        "type": random.choice(["Residential", "Commercial", "Industrial"]),
        "floors": random.randint(1, 20),
        "bedrooms": random.randint(1, 6),
        "rooms": ["Living", "Kitchen", "Bath", "Flex"],
        "area": random.randint(80, 2000)
    }

def evolve_design(d):
    d = json.loads(json.dumps(d))
    d["floors"] = max(1, d["floors"] + random.randint(-1, 3))
    d["area"] += random.randint(-50, 120)
    return d

def run_evolution(n=10):
    population = [generate_design() for _ in range(n)]
    best = population[0]

    for p in population:
        if p["area"] > best["area"]:
            best = p

    return best

# =========================================================
# BIM PIPELINE (NEW CORE FEATURE)
# =========================================================

def build_full_bim(design):
    bim = create_bim_model(design)
    bim = calculate_costs(bim)
    return bim

import plotly.graph_objects as go

# =========================================================
# 2D FLOOR PLAN ENGINE (SIMPLIFIED BIM DRAWING LAYER)
# =========================================================

def generate_2d_plan(design):
    rooms = design.get("rooms", ["Living", "Kitchen", "Bath", "Bedroom"])

    layout = []
    x, y = 0, 0

    for i, room in enumerate(rooms):
        w = random.randint(3, 6)
        h = random.randint(3, 6)

        layout.append({
            "name": room,
            "x": x,
            "y": y,
            "w": w,
            "h": h
        })

        x += w + 1
        if x > 10:
            x = 0
            y += h + 1

    return layout


def draw_2d_plan(layout):
    fig = go.Figure()

    for r in layout:
        fig.add_shape(
            type="rect",
            x0=r["x"],
            y0=r["y"],
            x1=r["x"] + r["w"],
            y1=r["y"] + r["h"],
            line=dict(color="white"),
            fillcolor="rgba(0,150,255,0.3)"
        )

        fig.add_annotation(
            x=r["x"] + r["w"]/2,
            y=r["y"] + r["h"]/2,
            text=r["name"],
            showarrow=False,
            font=dict(color="white", size=10)
        )

    fig.update_layout(
        title="2D BIM Floor Plan",
        paper_bgcolor="black",
        plot_bgcolor="black",
        height=600
    )

    return fig


# =========================================================
# 3D BUILDING ENGINE (BIM MASSING MODEL)
# =========================================================

def generate_3d_model(design):
    floors = design.get("floors", 1)

    x, y, z = [], [], []

    for f in range(floors):
        x.extend([0, 10, 10, 0, 0])
        y.extend([0, 0, 10, 10, 0])
        z.extend([f, f, f, f, f])

    return x, y, z


def draw_3d_model(design):
    x, y, z = generate_3d_model(design)

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=dict(color="cyan", width=5)
            )
        ]
    )

    fig.update_layout(
        title="3D BIM Building Massing",
        scene=dict(
            xaxis=dict(title="X"),
            yaxis=dict(title="Y"),
            zaxis=dict(title="Floors")
        ),
        paper_bgcolor="black",
        height=600
    )

    return fig


# =========================================================
# AI COPILOT (RULE-BASED ENGINE V1)
# =========================================================

def ai_copilot(command, design, bim):
    cmd = command.lower()

    if "cost" in cmd:
        return f"💰 Total cost is {bim['cost_model']['total']:,}. Reduce floors or MEP systems to optimize."

    if "reduce cost" in cmd:
        return "⚡ Suggestion: reduce HVAC load and structural columns by 10–15%."

    if "increase floors" in cmd:
        return "🏗️ Structural check: safe to increase up to +3 floors with current system."

    if "hvac" in cmd:
        return f"🌬 HVAC system uses {bim['hvac']['system']} with {bim['hvac']['cooling_load_kw']} kW load."

    if "optimize" in cmd:
        return "🧠 Optimization: balance structural density and HVAC zoning for efficiency gain."

    return "🤖 Command not recognized. Try: cost, hvac, optimize, reduce cost, increase floors"


# =========================================================
# STREAMLIT UI EXTENSION
# =========================================================

st.sidebar.markdown("## 🧠 AI Copilot")
user_prompt = st.sidebar.text_input("Ask Arc AI (cost, hvac, optimize...)")

# =========================================================
# MAIN UI TABS EXTENSION
# =========================================================

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if st.session_state.active_design:

    design = st.session_state.active_design
    bim = build_full_bim(design)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏗 BIM Dashboard",
        "📐 2D Floor Plan",
        "🏙 3D Model",
        "🤖 AI Copilot"
    ])

    # -------------------------
    # BIM DASHBOARD
    # -------------------------
    with tab1:
        st.subheader("BIM Model Overview")
        st.json(bim)

    # -------------------------
    # 2D FLOOR PLAN
    # -------------------------
    with tab2:
        layout = generate_2d_plan(design)
        fig = draw_2d_plan(layout)
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # 3D MODEL
    # -------------------------
    with tab3:
        fig3d = draw_3d_model(design)
        st.plotly_chart(fig3d, use_container_width=True)

    # -------------------------
    # AI COPILOT
    # -------------------------
    with tab4:
        st.subheader("Arc AI Copilot Response")

        if user_prompt:
            response = ai_copilot(user_prompt, design, bim)
            st.success(response)
        else:
            st.info("Ask something like: 'reduce cost' or 'optimize hvac'")

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# =========================================================
# STRUCTURAL ENGINE (LOAD + ELEMENT SIMULATION)
# =========================================================

def structural_engine(bim):
    floors = bim["architecture"]["floors"]

    return {
        "load_per_column": round(random.uniform(120, 450), 2),
        "beam_stress_index": round(random.uniform(0.4, 0.9), 2),
        "slab_thickness_mm": 150 + floors * 5,
        "structural_efficiency": round(random.uniform(65, 95), 2)
    }


# =========================================================
# MEP NETWORK ENGINE (GRAPH MODEL)
# =========================================================

def generate_mep_graph():
    G = nx.Graph()

    nodes = [
        "Main Water Tank",
        "Pump Room",
        "Distribution Line",
        "Bathrooms",
        "Kitchens",
        "Drainage System",
        "Electrical Panel",
        "Lighting Circuits",
        "Fire System",
        "Backup Generator"
    ]

    for n in nodes:
        G.add_node(n)

    edges = [
        ("Main Water Tank", "Pump Room"),
        ("Pump Room", "Distribution Line"),
        ("Distribution Line", "Bathrooms"),
        ("Distribution Line", "Kitchens"),
        ("Drainage System", "Bathrooms"),
        ("Electrical Panel", "Lighting Circuits"),
        ("Electrical Panel", "Backup Generator"),
        ("Fire System", "Pump Room"),
        ("Fire System", "Distribution Line")
    ]

    G.add_edges_from(edges)

    return G


def draw_mep_graph(G):
    plt.figure(figsize=(6, 4))
    pos = nx.spring_layout(G)

    nx.draw(G, pos,
            with_labels=True,
            node_color="skyblue",
            node_size=1500,
            font_size=8)

    st.pyplot(plt)


# =========================================================
# HVAC ZONING ENGINE
# =========================================================

def hvac_zoning(bim):
    floors = bim["architecture"]["floors"]

    zones = []

    for f in range(floors):
        zones.append({
            "floor": f + 1,
            "zone_type": random.choice(["Cooling Zone", "Heating Zone", "Mixed Zone"]),
            "airflow_cfm": random.randint(800, 5000),
            "temperature_target": random.randint(18, 26)
        })

    return zones


# =========================================================
# BOQ (BILL OF QUANTITIES ENGINE)
# =========================================================

def generate_boq(bim):
    area = bim["architecture"].get("floors", 1) * 120

    boq = [
        {"Item": "Concrete", "Qty": area * 0.8, "Unit": "m³"},
        {"Item": "Steel Reinforcement", "Qty": area * 0.12, "Unit": "tons"},
        {"Item": "Masonry Blocks", "Qty": area * 20, "Unit": "pcs"},
        {"Item": "Plastering", "Qty": area * 2.5, "Unit": "m²"},
        {"Item": "Paint", "Qty": area * 3.0, "Unit": "m²"},
        {"Item": "Electrical Wiring", "Qty": area * 8, "Unit": "m"},
        {"Item": "Plumbing Pipes", "Qty": area * 5, "Unit": "m"},
        {"Item": "HVAC Ducting", "Qty": area * 4, "Unit": "m"}
    ]

    return pd.DataFrame(boq)


# =========================================================
# COST BREAKDOWN ANALYTICS
# =========================================================

def cost_breakdown(bim):
    return pd.DataFrame([
        ["Structure", bim["cost_model"]["structure_cost"]],
        ["MEP", bim["cost_model"]["mep_cost"]],
        ["HVAC", bim["cost_model"]["hvac_cost"]],
        ["Contingency (10%)", bim["cost_model"]["total"] * 0.1],
        ["TOTAL", bim["cost_model"]["total"] * 1.1]
    ], columns=["Category", "Cost"])


# =========================================================
# ATTACH ENGINE TO ACTIVE BIM
# =========================================================

def enrich_bim(bim):
    bim["structure_analysis"] = structural_engine(bim)
    bim["hvac_zones"] = hvac_zoning(bim)
    bim["mep_graph"] = generate_mep_graph()
    return bim


# =========================================================
# UI EXTENSION (NEW TABS)
# =========================================================

if st.session_state.active_design:

    design = st.session_state.active_design
    bim = build_full_bim(design)
    bim = enrich_bim(bim)

    tabA, tabB, tabC, tabD = st.tabs([
        "⚙️ Structural",
        "🔌 MEP",
        "🌬 HVAC",
        "💰 Costing"
    ])

    # -------------------------
    # STRUCTURAL
    # -------------------------
    with tabA:
        st.subheader("Structural Analysis")
        st.json(bim["structure_analysis"])

    # -------------------------
    # MEP
    # -------------------------
    with tabB:
        st.subheader("MEP Network Diagram")
        draw_mep_graph(bim["mep_graph"])

    # -------------------------
    # HVAC
    # -------------------------
    with tabC:
        st.subheader("HVAC Zoning")
        st.dataframe(pd.DataFrame(bim["hvac_zones"]))

    # -------------------------
    # COSTING
    # -------------------------
    with tabD:
        st.subheader("Bill of Quantities (BOQ)")
        st.dataframe(generate_boq(bim))

        st.subheader("Cost Breakdown")
        st.dataframe(cost_breakdown(bim))


import pandas as pd
from datetime import timedelta

# =========================================================
# 🌍 SUSTAINABILITY ENGINE (CARBON + MATERIAL IMPACT)
# =========================================================

def sustainability_model(bim):
    area = bim["architecture"]["floors"] * 120

    carbon = {
        "concrete_kgCO2": area * 320,
        "steel_kgCO2": area * 180,
        "glass_kgCO2": area * 90,
        "total_kgCO2": 0
    }

    carbon["total_kgCO2"] = sum([
        carbon["concrete_kgCO2"],
        carbon["steel_kgCO2"],
        carbon["glass_kgCO2"]
    ])

    return carbon


# =========================================================
# 📆 CONSTRUCTION TIMELINE SIMULATION ENGINE
# =========================================================

def construction_timeline(bim):
    floors = bim["architecture"]["floors"]

    base_days = 120
    complexity_factor = floors * 18

    phases = [
        {"phase": "Site Preparation", "days": 15},
        {"phase": "Foundation Works", "days": 30},
        {"phase": "Structural Frame", "days": base_days + complexity_factor},
        {"phase": "MEP Installation", "days": 45 + floors * 5},
        {"phase": "Finishing Works", "days": 60},
        {"phase": "Commissioning", "days": 20}
    ]

    start = pd.Timestamp.today()

    timeline = []

    for p in phases:
        end = start + timedelta(days=p["days"])
        timeline.append({
            "Phase": p["phase"],
            "Duration (days)": p["days"],
            "Start": start.date(),
            "End": end.date()
        })
        start = end

    return pd.DataFrame(timeline)


# =========================================================
# 📦 EXPORT ENGINE (JSON / BIM SNAPSHOT)
# =========================================================

def export_bim_snapshot(bim):
    return {
        "project_id": bim["id"],
        "architecture": bim["architecture"],
        "structure_analysis": bim.get("structure_analysis", {}),
        "hvac": bim.get("hvac_zones", []),
        "cost": bim["cost_model"],
        "sustainability": sustainability_model(bim)
    }


# =========================================================
# 🌳 BIM TREE EXPLORER (HIERARCHICAL VIEW)
# =========================================================

def build_bim_tree(bim):
    tree = {
        "Project": {
            "ID": bim["id"],
            "Type": bim["type"],
            "Floors": bim["architecture"]["floors"],
            "Rooms": len(bim.get("rooms", []))
        },
        "Systems": {
            "Structure": bim.get("structure_analysis", {}),
            "HVAC Zones": len(bim.get("hvac_zones", [])),
            "MEP Nodes": len(list(bim.get("mep_graph", []).nodes)) if bim.get("mep_graph") else 0
        },
        "Economics": {
            "Total Cost": bim["cost_model"]["total"],
            "Cost per m²": bim["cost_model"]["total"] / max(1, bim["architecture"]["floors"] * 120)
        }
    }

    return tree


# =========================================================
# 🧠 BIM INTELLIGENCE SUMMARY PANEL
# =========================================================

def bim_summary(bim):
    carbon = sustainability_model(bim)
    timeline = construction_timeline(bim)

    return {
        "carbon_footprint_tons": carbon["total_kgCO2"] / 1000,
        "estimated_duration_days": int(timeline["Duration (days)"].sum()),
        "efficiency_index": round(
            (bim["structure_analysis"]["structural_efficiency"] if "structure_analysis" in bim else 75) * 0.9,
            2
        )
    }


# =========================================================
# 🧩 UI EXTENSION: FINAL BIM DASHBOARD LAYER
# =========================================================

if st.session_state.active_design:

    design = st.session_state.active_design
    bim = build_full_bim(design)
    bim = enrich_bim(bim)

    st.markdown("---")
    st.subheader("🧠 BIM Intelligence Command Center")

    col1, col2, col3 = st.columns(3)

    summary = bim_summary(bim)

    col1.metric("🌍 Carbon Footprint (tons CO₂)", summary["carbon_footprint_tons"])
    col2.metric("📆 Project Duration (days)", summary["estimated_duration_days"])
    col3.metric("⚡ Efficiency Index", summary["efficiency_index"])

    tab1, tab2, tab3 = st.tabs([
        "🌍 Sustainability",
        "📆 Timeline",
        "📦 Export / BIM Snapshot"
    ])

    # -------------------------
    # 🌍 SUSTAINABILITY
    # -------------------------
    with tab1:
        st.subheader("Carbon Emissions Breakdown")
        st.json(sustainability_model(bim))

    # -------------------------
    # 📆 TIMELINE
    # -------------------------
    with tab2:
        st.subheader("Construction Timeline Simulation")
        st.dataframe(construction_timeline(bim))

    # -------------------------
    # 📦 EXPORT
    # -------------------------
    with tab3:
        st.subheader("BIM Export Snapshot")
        st.json(export_bim_snapshot(bim))

        st.subheader("BIM Tree Explorer")
        st.json(build_bim_tree(bim))


import re

# =========================================================
# 🧠 NATURAL LANGUAGE DESIGN PARSER
# =========================================================

def parse_design_prompt(prompt: str):
    prompt = prompt.lower()

    floors = int(re.search(r"(\d+)\s*floor", prompt).group(1)) if re.search(r"(\d+)\s*floor", prompt) else 2

    if "hospital" in prompt:
        btype = "Medical Clinic"
    elif "office" in prompt:
        btype = "Boutique Office"
    elif "factory" in prompt or "industrial" in prompt:
        btype = "Distribution Warehouse"
    elif "hotel" in prompt:
        btype = "Hotel Resort"
    else:
        btype = "Modern Apartment"

    bedrooms = 1 if "commercial" in prompt else min(6, floors + 1)

    return {
        "floors": floors,
        "type": btype,
        "bedrooms": bedrooms
    }


# =========================================================
# 🧠 AI ARCHITECT AGENT
# =========================================================

def architect_agent(spec):
    return {
        "design_logic": f"Spatial zoning optimized for {spec['type']}",
        "layout_strategy": "Central circulation core with radial room distribution",
        "risk_notes": "Check vertical load transfer continuity across floors"
    }


# =========================================================
# 🧠 STRUCTURAL ENGINEER AGENT
# =========================================================

def structural_agent(spec):
    return {
        "frame_system": "Reinforced concrete moment frame",
        "column_grid": f"{4 + spec['floors']}m spacing",
        "recommendation": "Increase beam depth on upper floors for load balance"
    }


# =========================================================
# 🧠 MEP ENGINEER AGENT
# =========================================================

def mep_agent(spec):
    return {
        "hvac_strategy": "Zoned variable air volume (VAV)",
        "plumbing": "Vertical riser core with horizontal distribution",
        "electrical": "Redundant looped distribution network"
    }


# =========================================================
# 🧠 COST ENGINEER AGENT
# =========================================================

def cost_agent(spec):
    base = spec["floors"] * 120 * 1800

    return {
        "estimated_cost": base,
        "cost_driver": "MEP systems and structural reinforcement",
        "optimization_tip": "Reduce glazing ratio to lower HVAC load"
    }


# =========================================================
# 🧠 COPILOT ORCHESTRATOR (MULTI-AGENT SYSTEM)
# =========================================================

def copilot_engine(prompt):
    spec = parse_design_prompt(prompt)

    return {
        "input_spec": spec,
        "architect": architect_agent(spec),
        "structural": structural_agent(spec),
        "mep": mep_agent(spec),
        "cost": cost_agent(spec)
    }


# =========================================================
# 🧠 BIM AUTO-GENERATOR FROM PROMPT
# =========================================================

def generate_bim_from_prompt(prompt):
    spec = parse_design_prompt(prompt)

    design = {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": spec["type"],
        "architecture": {
            "floors": spec["floors"]
        },
        "rooms": [],
        "cost_model": {
            "structure_cost": spec["floors"] * 50000,
            "mep_cost": spec["floors"] * 30000,
            "hvac_cost": spec["floors"] * 20000,
            "total": spec["floors"] * 120000
        }
    }

    return design


# =========================================================
# 🎛️ COPILOT UI PANEL
# =========================================================

st.markdown("---")
st.subheader("🧠 AI Copilot Command Center")

user_prompt = st.text_input(
    "Describe your building (e.g. '3 floor hospital with emergency wing')"
)

if user_prompt:
    result = copilot_engine(user_prompt)
    bim = generate_bim_from_prompt(user_prompt)
    bim = enrich_bim(bim)

    tab1, tab2, tab3 = st.tabs([
        "🧠 AI Design Reasoning",
        "🏗 BIM Auto-Generation",
        "💰 Cost Intelligence"
    ])

    # -------------------------
    # 🧠 REASONING
    # -------------------------
    with tab1:
        st.subheader("Multi-Agent Design Intelligence")

        st.json(result)

    # -------------------------
    # 🏗 BIM OUTPUT
    # -------------------------
    with tab2:
        st.subheader("Generated BIM Model")

        st.json(bim)

    # -------------------------
    # 💰 COST
    # -------------------------
    with tab3:
        st.subheader("Cost Breakdown")

        st.json(result["cost"])
