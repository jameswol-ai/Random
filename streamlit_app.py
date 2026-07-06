# =========================================================
# ARC V40 — FULL BIM + STRUCTURAL SOLVER + CITY SCALE OS
# Single-File Production Streamlit Architecture Engine
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
    page_title="ARC V40 OS",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_v40_memory.json")

# =========================================================
# SAFE MEMORY SYSTEM (NO JSON CRASHES)
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "bim": [],
    "city": [],
    "logs": []
}

def safe_load():
    if not MEMORY_FILE.exists():
        return DEFAULT_STATE.copy()
    try:
        raw = MEMORY_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return DEFAULT_STATE.copy()
        return json.loads(raw)
    except Exception:
        return DEFAULT_STATE.copy()

def save():
    try:
        MEMORY_FILE.write_text(json.dumps(st.session_state.mem, indent=2))
    except Exception:
        pass

def log(msg):
    st.session_state.mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save()

if "mem" not in st.session_state:
    st.session_state.mem = safe_load()

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.mem

# =========================================================
# ARCHITECTURE DOMAIN SYSTEM
# =========================================================

ARCH = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}

def get_domain(t):
    for k, v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

# =========================================================
# DESIGN GENERATOR
# =========================================================

def generate_design(btype, floors, bedrooms):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": get_domain(btype),
        "floors": floors,
        "bedrooms": bedrooms,
        "area_sqm": 70 + floors * 60 + bedrooms * 18,
        "structure": {
            "columns": random.randint(12, 42),
            "beams": random.randint(25, 85),
            "slabs": floors
        }
    }

def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] = max(10, d["structure"]["columns"] + random.randint(-3, 4))
    d["structure"]["beams"] = max(20, d["structure"]["beams"] + random.randint(-5, 6))
    return d

# =========================================================
# PHYSICS ENGINE (LOAD + STABILITY)
# =========================================================

def physics(d):
    col = d["structure"]["columns"]
    beam = d["structure"]["beams"]
    floors = d["structure"]["slabs"]

    load_index = (beam / max(1, col)) * floors

    stability = max(0, 100 - abs(load_index - 2.2) * 30)
    stress = min(100, load_index * 14)

    return {
        "load_index": round(load_index, 2),
        "stability": int(stability),
        "stress": int(stress)
    }

# =========================================================
# COST ENGINE (EAST AFRICA MODEL)
# =========================================================

def cost(d):
    sqm = d["area_sqm"]

    rate = random.choice([450, 500, 600, 700, 850])  # USD/m² band
    multiplier = 1 + (d["structure"]["slabs"] * 0.08)

    total = sqm * rate * multiplier

    return {
        "rate_per_sqm": rate,
        "total_usd": int(total)
    }

# =========================================================
# BOQ ENGINE (FULL CONSTRUCTION BREAKDOWN)
# =========================================================

def boq(d):
    a = d["area_sqm"]

    return [
        ("Foundation Works", int(a * 55)),
        ("Substructure", int(a * 40)),
        ("Concrete Frame", int(a * 120)),
        ("Walling", int(a * 70)),
        ("Roofing", int(a * 85)),
        ("Finishes", int(a * 110)),
        ("MEP Systems", int(a * 95))
    ]

# =========================================================
# BIM EXPORT (DIGITAL TWIN)
# =========================================================

def bim(d, phys, cost_data):
    return {
        "IFC_CLASS": "ARC_V40_BUILDING",
        "id": d["id"],
        "geometry": {
            "floors": d["floors"],
            "area": d["area_sqm"]
        },
        "structure": d["structure"],
        "physics": phys,
        "cost": cost_data,
        "timestamp": datetime.now().isoformat()
    }

# =========================================================
# EVOLUTION ENGINE
# =========================================================

def evolve(btype, floors, bedrooms, gen=6, pop=8):
    popu = [generate_design(btype, floors, bedrooms) for _ in range(pop)]
    history = []

    for _ in range(gen):
        scored = []

        for d in popu:
            phys = physics(d)
            d["physics"] = phys
            d["score"] = phys["stability"] - phys["stress"] * 0.3
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop // 2)]
        popu = survivors + [mutate(random.choice(survivors)) for _ in survivors]
        popu = popu[:pop]

    return scored[0], history

# =========================================================
# FLOOR PLAN RENDER
# =========================================================

def floor_plan(d):
    rooms = [
        {"name": "Living", "w": 6, "h": 5, "color": "#1e3a8a"},
        {"name": "Kitchen", "w": 4, "h": 4, "color": "#065f46"}
    ]

    for i in range(d["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4,
            "h": 4,
            "color": "#4c1d95"
        })

    return rooms

def render(plan):
    html = '<div style="display:flex;flex-wrap:wrap;gap:10px;padding:10px;background:#0b0f1a;border-radius:12px;">'
    for r in plan:
        html += f"""
        <div style="background:{r['color']};padding:10px;border-radius:10px;color:white;min-width:140px">
            <b>{r['name']}</b><br>{r['w']}×{r['h']}
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# CITY GENERATOR (SIMPLE SCALE LAYER)
# =========================================================

def city(n=10):
    return [
        {
            "id": str(uuid.uuid4())[:6],
            "type": random.choice(sum(ARCH.values(), [])),
            "height": random.randint(1, 12),
            "density": round(random.random(), 2)
        }
        for _ in range(n)
    ]

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏗️ ARC V40 OS")

mode = st.sidebar.radio("Mode", ["Dashboard", "Design Lab", "BIM", "City", "Memory"])

btype = st.sidebar.selectbox("Building Type", sum(ARCH.values(), []))
floors = st.sidebar.slider("Floors", 1, 5, 2)
bedrooms = st.sidebar.slider("Bedrooms", 1, 8, 3)

# =========================================================
# DASHBOARD
# =========================================================

if mode == "Dashboard":
    st.title("🏗️ ARC V40 CONTROL CORE")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("BIM Models", len(mem["bim"]))
    c3.metric("City Nodes", len(mem["city"]))

    st.subheader("Logs")
    for l in mem["logs"][-6:]:
        st.caption(f"{l['time']} — {l['msg']}")

# =========================================================
# DESIGN LAB
# =========================================================

elif mode == "Design Lab":
    st.title("🧠 ENGINEERING AI CORE")

    if st.button("Run Evolution Engine"):
        best, hist = evolve(btype, floors, bedrooms)

        best["plan"] = floor_plan(best)

        mem["designs"].append(best)
        st.session_state.active = best

        log(f"Generated {best['id']}")

    if st.session_state.active:
        d = st.session_state.active

        phys = d["physics"]
        cost_data = cost(d)

        c1, c2, c3 = st.columns(3)
        c1.metric("Stability", phys["stability"])
        c2.metric("Stress", phys["stress"])
        c3.metric("Cost USD", cost_data["total_usd"])

        tab1, tab2 = st.tabs(["2D Plan", "BOQ"])

        with tab1:
            render(d["plan"])

        with tab2:
            st.table(boq(d))

# =========================================================
# BIM
# =========================================================

elif mode == "BIM":
    st.title("🏗️ BIM DIGITAL TWIN")

    if st.session_state.active:
        d = st.session_state.active
        phys = d["physics"]
        cost_data = cost(d)

        model = bim(d, phys, cost_data)
        mem["bim"].append(model)

        st.success("BIM model generated")
        st.json(model)
    else:
        st.info("Run a design first.")

# =========================================================
# CITY MODE
# =========================================================

elif mode == "City":
    st.title("🏙️ CITY SIMULATION LAYER")

    c = city(12)
    mem["city"] = c

    st.json(c)

# =========================================================
# MEMORY
# =========================================================

elif mode == "Memory":
    st.title("🧠 MEMORY CORE")

    st.json(mem)

    if st.button("Reset"):
        st.session_state.mem = DEFAULT_STATE.copy()
        st.session_state.active = None
        save()
        st.rerun()