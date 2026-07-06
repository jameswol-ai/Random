# =========================================================
# RANDOM V12
# Architecture Intelligence OS - Frontend Shell
# =========================================================

import streamlit as st
import uuid
import random
from datetime import datetime

from core.memory import load_memory, save_memory, log_event

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random AIOS",
    page_icon="🏗️",
    layout="wide"
)

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
# STYLE (lightweight upgrade)
# =========================================================

st.markdown("""
<style>
    .title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .card {
        padding: 16px;
        border-radius: 12px;
        background: #0f172a;
        color: white;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

page = st.sidebar.radio(
    "Random AIOS",
    [
        "🏠 Dashboard",
        "🧪 Design Lab",
        "📊 Analytics",
        "🧠 Memory",
        "⚙ Settings"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Random V12 • Modular AI Architecture System")

# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":
    st.markdown("<div class='title'>🏗️ Random AIOS Dashboard</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Projects", len(mem["projects"]))
    col2.metric("Designs", len(mem["designs"]))
    col3.metric("Evolutions", len(mem["evolution"]))

    st.markdown("### 🧠 System Activity")

    logs = mem.get("logs", [])[-8:]
    if logs:
        for l in reversed(logs):
            st.write(f"⏱ {l['time'][11:19]} → {l['msg']}")
    else:
        st.info("No system activity yet.")

# =========================================================
# DESIGN LAB (CORE ENGINE ENTRY POINT)
# =========================================================

elif page == "🧪 Design Lab":
    st.markdown("<div class='title'>🧪 AI Design Laboratory</div>", unsafe_allow_html=True)

    btype = st.selectbox(
        "Building Type",
        ["Luxury Villa", "Modern Apartment", "Townhouse", "Office Hub", "Clinic"]
    )

    bedrooms = st.slider("Spatial Modules", 1, 8, 3)
    generations = st.slider("AI Generations", 2, 15, 6)
    population = st.slider("Population Size", 4, 20, 10)

    run = st.button("🚀 Run Evolution Engine", use_container_width=True)

    # =====================================================
    # SIMPLE GENERATOR (placeholder for future AI agents)
    # =====================================================

    def generate_design():
        base_area = random.randint(120, 450)

        return {
            "id": str(uuid.uuid4())[:8].upper(),
            "type": btype,
            "bedrooms": bedrooms,
            "area_sqm": base_area,
            "score": random.randint(60, 98),
            "cost": base_area * random.randint(1200, 2500),
            "rooms": ["Living", "Kitchen", "Bath"] + ["Bedroom"] * bedrooms,
            "structure": {
                "columns": random.randint(14, 32),
                "beams": random.randint(25, 70)
            }
        }

    # =====================================================
    # EVOLUTION LOOP
    # =====================================================

    def run_evolution(population_size):
        population_set = [generate_design() for _ in range(population_size)]
        best = max(population_set, key=lambda x: x["score"])
        history = [d["score"] for d in population_set]
        return best, history

    if run:
        with st.spinner("Running AI architectural evolution..."):
            best, history = run_evolution(population)

            st.session_state.active_design = best
            st.session_state.active_history = history

            mem["designs"].append(best)
            mem["evolution"].append({
                "id": str(uuid.uuid4())[:6],
                "best": best["id"],
                "score": best["score"],
                "time": datetime.now().isoformat()
            })

            log_event(mem, f"Generated design {best['id']}")

    # =====================================================
    # OUTPUT
    # =====================================================

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.markdown("### 🏗 Best Design Output")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", d["score"])
        c2.metric("Area", f"{d['area_sqm']} m²")
        c3.metric("Cost", f"${d['cost']:,}")

        st.markdown("### 🧱 Structural Summary")
        st.json(d["structure"])

# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":
    st.markdown("### 📊 Evolution Trends")

    if st.session_state.active_history:
        st.line_chart(st.session_state.active_history)
    else:
        st.info("Run a design simulation first.")

# =========================================================
# MEMORY VIEW
# =========================================================

elif page == "🧠 Memory":
    st.markdown("### 🧠 System Memory")

    st.json(mem)

    if st.button("🧹 Reset Memory"):
        st.session_state.memory = {
            "projects": [],
            "designs": [],
            "logs": [],
            "evolution": []
        }
        save_memory(st.session_state.memory)
        st.rerun()

# =========================================================
# SETTINGS
# =========================================================

elif page == "⚙ Settings":
    st.markdown("### ⚙ System Settings")

    st.info("Future: kernel configuration, agent toggles, plugin system, BIM export, multi-agent orchestration.")