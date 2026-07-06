# =========================================================
# RANDOM V12+ CORE
# Architecture Intelligence OS - Unified Engine
# =========================================================

import streamlit as st
import uuid
import random
import json
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random AIOS",
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
    "logs": [],
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory(mem):
    try:
        MEMORY_FILE.write_text(json.dumps(mem, indent=2), encoding="utf-8")
    except Exception:
        pass

def log_event(mem, msg):
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory(mem)

# =========================================================
# SESSION STATE
# =========================================================

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if "active_history" not in st.session_state:
    st.session_state.active_history = []

mem = st.session_state.memory

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>
    .title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 12px;
    }
    .card {
        padding: 14px;
        border-radius: 12px;
        background: #0f172a;
        color: white;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# CORE EVOLUTION ENGINE
# =========================================================

ARCH_TYPES = ["Luxury Villa", "Modern Apartment", "Townhouse", "Office Hub", "Clinic"]

def generate_design(btype, bedrooms):
    base_area = random.randint(120, 500)

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "bedrooms": bedrooms,
        "area_sqm": base_area,
        "score": random.randint(60, 100),
        "cost": base_area * random.randint(1200, 2600),
        "rooms": ["Living", "Kitchen", "Bath"] + ["Bedroom"] * bedrooms,
        "structure": {
            "columns": random.randint(14, 40),
            "beams": random.randint(20, 80)
        }
    }

def run_evolution(pop_size):
    population = [generate_design(random.choice(ARCH_TYPES), random.randint(1, 5)) for _ in range(pop_size)]
    best = max(population, key=lambda x: x["score"])
    history = sorted([p["score"] for p in population])
    return best, history

# =========================================================
# SIDEBAR NAV
# =========================================================

page = st.sidebar.radio(
    "Random AIOS",
    ["🏠 Dashboard", "🧪 Design Lab", "📊 Analytics", "🧠 Memory", "⚙ Settings"]
)

st.sidebar.caption("Random V12+ Unified Engine")

# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":
    st.markdown("<div class='title'>🏗 Random AIOS Control Core</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Evolution Runs", len(mem["evolution"]))

    st.markdown("### 🧠 System Logs")
    logs = mem["logs"][-6:]
    if logs:
        for l in reversed(logs):
            st.write(f"⏱ {l['time'][11:19]} → {l['msg']}")
    else:
        st.info("No activity yet.")

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "🧪 Design Lab":
    st.markdown("<div class='title'>🧪 Evolution Design Engine</div>", unsafe_allow_html=True)

    btype = st.selectbox("Building Type", ARCH_TYPES)
    bedrooms = st.slider("Spatial Modules", 1, 8, 3)
    population = st.slider("Population Size", 4, 20, 10)

    if st.button("🚀 Run Evolution Engine", use_container_width=True):
        with st.spinner("Evolving architectural genomes..."):
            best, history = run_evolution(population)

            st.session_state.active_design = best
            st.session_state.active_history = history

            mem["designs"].append(best)
            mem["evolution"].append({
                "id": str(uuid.uuid4())[:6],
                "best_id": best["id"],
                "score": best["score"],
                "time": datetime.now().isoformat()
            })

            log_event(mem, f"Generated design {best['id']}")

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.markdown("### 🏗 Best Design Output")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", d["score"])
        c2.metric("Area", f"{d['area_sqm']} m²")
        c3.metric("Cost", f"${d['cost']:,}")

        st.markdown("### 🧱 Structure")
        st.json(d["structure"])

# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":
    st.markdown("### 📊 Evolution Curve")

    if st.session_state.active_history:
        st.line_chart(st.session_state.active_history)
    else:
        st.info("Run evolution first.")

# =========================================================
# MEMORY
# =========================================================

elif page == "🧠 Memory":
    st.markdown("### 🧠 System Memory")

    st.json(mem)

    if st.button("🧹 Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        save_memory(st.session_state.memory)
        st.rerun()

# =========================================================
# SETTINGS
# =========================================================

elif page == "⚙ Settings":
    st.markdown("### ⚙ System Settings")
    st.info("Future: multi-agent plugins, BIM export, structural AI simulation layer.")