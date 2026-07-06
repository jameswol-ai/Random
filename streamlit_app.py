# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# V38 STABLE — HARDENED BIM + EVOLUTION ENGINE
# No KeyError / No JSON crash / Safe simulation core
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
    page_title="ARC V38 Stable OS",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# SAFE MEMORY LAYER (CRASH PROOF)
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "evolution": [],
    "logs": []
}

def load_memory():
    if not MEMORY_FILE.exists():
        return DEFAULT_STATE.copy()

    try:
        data = json.loads(MEMORY_FILE.read_text())

        # 🧠 auto-heal missing keys
        for k in DEFAULT_STATE:
            if k not in data:
                data[k] = []

        return data

    except Exception:
        return DEFAULT_STATE.copy()

def save_memory(mem):
    try:
        MEMORY_FILE.write_text(json.dumps(mem, indent=2))
    except:
        pass

def log(mem, msg):
    if "logs" not in mem:
        mem["logs"] = []

    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory(mem)

# init
if "mem" not in st.session_state:
    st.session_state.mem = load_memory()

mem = st.session_state.mem

# =========================================================
# ARCHITECTURE DOMAIN ENGINE
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
# SAFE DESIGN GENERATION
# =========================================================

def generate_design(btype, bedrooms):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": domain(btype),
        "bedrooms": bedrooms,
        "area_sqm": 80 + bedrooms * 18,
        "structure": {
            "columns": random.randint(14, 36),
            "beams": random.randint(28, 72)
        },
        "cost": 0  # ALWAYS INITIALIZED
    }

# =========================================================
# SAFE MUTATION (NO STRUCTURE BREAKS)
# =========================================================

def mutate(d):
    d = json.loads(json.dumps(d))

    d["structure"]["columns"] = max(
        10,
        d["structure"]["columns"] + random.randint(-2, 3)
    )

    d["structure"]["beams"] = max(
        16,
        d["structure"]["beams"] + random.randint(-4, 5)
    )

    # safe cost recalculation ALWAYS
    area = max(1, d["area_sqm"])
    d["cost"] = int(area * random.randint(1200, 2600))

    return d

# =========================================================
# FITNESS ENGINE (SAFE DIVISION ONLY)
# =========================================================

def fitness(d):
    cols = max(1, d["structure"]["columns"])
    beams = max(1, d["structure"]["beams"])

    ratio = beams / cols

    structural = max(0, 100 - abs(ratio - 2.1) * 20)

    cost_per_sqm = d["cost"] / max(1, d["area_sqm"])
    cost_eff = max(0, 100 - abs(cost_per_sqm - 1650) * 0.03)

    complexity = min(100, d["bedrooms"] * 12)

    return {
        "structural": structural,
        "cost": cost_eff,
        "complexity": complexity
    }

def score(f):
    return int(sum(f.values()) / len(f))

# =========================================================
# EVOLUTION ENGINE (STABLE)
# =========================================================

def evolve(btype, bedrooms, gens, pop):
    population = [generate_design(btype, bedrooms) for _ in range(pop)]
    history = []

    for _ in range(gens):
        scored = []

        for d in population:
            f = fitness(d)
            d["fitness"] = f
            d["score"] = score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop // 2)]

        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate(s))

        population = new_pop[:pop]

    return scored[0], history

# =========================================================
# FLOOR PLAN (SAFE)
# =========================================================

def floor_plan(d):
    rooms = [
        {"name": "Living", "w": 6.5, "h": 5.0, "color": "#1e3a8a"},
        {"name": "Kitchen", "w": 4.5, "h": 4.0, "color": "#065f46"}
    ]

    for i in range(d["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4.5 if i == 0 else 4.0,
            "h": 4.0,
            "color": "#4c1d95"
        })

    return rooms

# =========================================================
# RENDER
# =========================================================

def render(plan):
    html = '<div style="display:flex;flex-wrap:wrap;gap:12px;">'
    for r in plan:
        html += f"""
        <div style="padding:12px;background:{r['color']};
        color:white;border-radius:10px;min-width:160px">
        <b>{r['name']}</b><br>{r['w']}m × {r['h']}m
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# UI
# =========================================================

st.sidebar.title("🏗️ ARC V38 SAFE")

page = st.sidebar.radio("Mode", ["Dashboard", "Design Lab", "Memory"])

btype = st.sidebar.selectbox("Type", sum(ARCH.values(), []))
beds = st.sidebar.slider("Bedrooms", 1, 8, 3)
gens = st.sidebar.slider("Generations", 2, 15, 5)
pop = st.sidebar.slider("Population", 4, 20, 8)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🏗️ SYSTEM CORE")

    c1,c2,c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

    if mem["logs"]:
        st.subheader("Recent Logs")
        for l in mem["logs"][-6:]:
            st.caption(f"{l['time']} → {l['msg']}")

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "Design Lab":
    st.title("🧠 ENGINE CORE")

    if st.button("Run Engine"):
        best, hist = evolve(btype, beds, gens, pop)

        best["plan"] = floor_plan(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best": best["id"],
            "score": best["score"]
        })

        log(mem, f"Generated {best['id']}")

        st.session_state.active = best

    if "active" in st.session_state:
        d = st.session_state.active

        st.subheader(f"Project {d['id']}")

        a,b,c = st.columns(3)
        a.metric("Score", d["score"])
        b.metric("Area", d["area_sqm"])
        c.metric("Cost", d["cost"])

        render(d["plan"])

# =========================================================
# MEMORY
# =========================================================

else:
    st.title("🧠 MEMORY CORE")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.mem = DEFAULT_STATE.copy()
        save_memory(st.session_state.mem)
        st.rerun()