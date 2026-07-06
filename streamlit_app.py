# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE — V39
# Architect Brain + Physics Layer + BIM Export Core
# Stable Streamlit OS (Production Hardened)
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
    page_title="ARC V39 OS",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# SAFE MEMORY LOADER (FIXES JSONDecodeError CRASH)
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": [],
    "bim_exports": []
}

def safe_load_memory():
    if not MEMORY_FILE.exists():
        return DEFAULT_STATE.copy()

    try:
        raw = MEMORY_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return DEFAULT_STATE.copy()
        return json.loads(raw)
    except Exception:
        return DEFAULT_STATE.copy()

def save_memory():
    try:
        MEMORY_FILE.write_text(
            json.dumps(st.session_state.memory, indent=2),
            encoding="utf-8"
        )
    except Exception:
        pass

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# init
if "memory" not in st.session_state:
    st.session_state.memory = safe_load_memory()

if "active" not in st.session_state:
    st.session_state.active = None

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE BRAIN (DOMAIN ENGINE)
# =========================================================

ARCH = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}

def domain(t):
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
        "domain": domain(btype),
        "floors": floors,
        "bedrooms": bedrooms,
        "area_sqm": 80 + (floors * 55) + (bedrooms * 18),
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(25, 80),
            "slabs": floors
        },
        "materials": {
            "concrete_grade": random.choice(["C25", "C30", "C35"]),
            "steel_grade": random.choice(["S275", "S355"])
        }
    }

def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] = max(10, d["structure"]["columns"] + random.randint(-3, 4))
    d["structure"]["beams"] = max(20, d["structure"]["beams"] + random.randint(-5, 6))
    return d

# =========================================================
# PHYSICS ENGINE (LOAD + STABILITY SIMULATION)
# =========================================================

def physics_check(d):
    col = d["structure"]["columns"]
    beam = d["structure"]["beams"]
    floors = d["structure"]["slabs"]

    load_factor = (beam / max(1, col)) * floors

    stress = min(100, load_factor * 12)
    stability = max(0, 100 - abs(load_factor - 2.2) * 30)

    return {
        "load_factor": round(load_factor, 2),
        "stress_index": round(stress, 2),
        "stability_score": int(stability)
    }

# =========================================================
# COST ENGINE (EAST AFRICA BASED APPROX)
# =========================================================

def cost_engine(d):
    sqm = d["area_sqm"]

    base_rate = random.choice([
        450, 500, 600, 700  # USD/m² simplified EA band
    ])

    structure_multiplier = 1 + (d["structure"]["slabs"] * 0.08)

    total = sqm * base_rate * structure_multiplier

    return {
        "rate_per_sqm": base_rate,
        "total_cost_usd": int(total)
    }

# =========================================================
# BIM EXPORT ENGINE (IFC-LIKE STRUCTURE)
# =========================================================

def bim_export(d):
    export = {
        "IFC_CLASS": "IFCSITE_SIM",
        "project_id": d["id"],
        "geometry": {
            "floors": d["floors"],
            "area": d["area_sqm"]
        },
        "structural": d["structure"],
        "materials": d["materials"],
        "timestamp": datetime.now().isoformat()
    }

    mem["bim_exports"].append(export)
    save_memory()

    return export

# =========================================================
# FITNESS + AI BRAIN SCORE
# =========================================================

def score(d, phys):
    stability = phys["stability_score"]
    stress_penalty = max(0, 100 - phys["stress_index"])

    return int((stability * 0.6) + (stress_penalty * 0.4))

# =========================================================
# EVOLUTION LOOP
# =========================================================

def evolve(btype, floors, bedrooms, gen=6, pop=8):
    popu = [generate_design(btype, floors, bedrooms) for _ in range(pop)]
    history = []

    for _ in range(gen):
        scored = []

        for d in popu:
            phys = physics_check(d)
            d["physics"] = phys
            d["score"] = score(d, phys)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop // 2)]
        popu = survivors + [mutate(random.choice(survivors)) for _ in survivors]
        popu = popu[:pop]

    return scored[0], history

# =========================================================
# SIMPLE FLOOR SYSTEM
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

# =========================================================
# UI RENDER
# =========================================================

def render(plan):
    html = '<div style="display:flex;gap:12px;flex-wrap:wrap;padding:12px;background:#0b0f1a;border-radius:12px;">'
    for r in plan:
        html += f"""
        <div style="background:{r['color']};padding:12px;border-radius:10px;color:white;min-width:140px">
            <b>{r['name']}</b><br>
            {r['w']} × {r['h']}
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏗️ ARC V39 OS")

page = st.sidebar.radio("Mode", ["Dashboard", "Design Lab", "BIM Export", "Memory"])

btype = st.sidebar.selectbox("Building Type", sum(ARCH.values(), []))
floors = st.sidebar.slider("Floors", 1, 5, 2)
bedrooms = st.sidebar.slider("Bedrooms", 1, 8, 3)
gens = st.sidebar.slider("Generations", 3, 12, 6)
pop = st.sidebar.slider("Population", 4, 16, 8)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏗️ ARC CONTROL BRAIN")

    c1, c2, c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("BIM Models", len(mem["bim_exports"]))
    c3.metric("Evolution Runs", len(mem["evolution"]))

    st.subheader("System Logs")
    for l in mem["logs"][-6:]:
        st.caption(f"{l['time']} — {l['msg']}")

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "Design Lab":
    st.title("🧠 ARCHITECT + ENGINEER AI")

    if st.button("Run AI Evolution Engine"):
        best, hist = evolve(btype, floors, bedrooms, gens, pop)

        best["plan"] = floor_plan(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best": best["id"],
            "score": best["score"]
        })

        st.session_state.active = best
        log(f"Generated {best['id']}")

    if st.session_state.active:
        d = st.session_state.active

        st.subheader(f"Design {d['id']}")

        phys = d["physics"]
        cost = cost_engine(d)

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", d["score"])
        c2.metric("Stability", phys["stability_score"])
        c3.metric("Cost (USD)", cost["total_cost_usd"])

        tab1, tab2 = st.tabs(["2D Plan", "Physics"])

        with tab1:
            render(d["plan"])

        with tab2:
            st.json(phys)

# =========================================================
# BIM EXPORT
# =========================================================

elif page == "BIM Export":
    st.title("🏗️ BIM EXPORT SYSTEM")

    if st.session_state.active:
        d = st.session_state.active
        export = bim_export(d)

        st.success("BIM model generated")

        st.json(export)
    else:
        st.info("Run a design first.")

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 MEMORY CORE")

    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active = None
        save_memory()
        st.rerun()