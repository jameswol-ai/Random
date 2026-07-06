# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# Multi-Agent Architecture Council OS
# Streamlit Entry Point
# =========================================================

import streamlit as st

from core.memory import load_memory, save_memory, log_event, DEFAULT_STATE
from engine.evolution import run_evolution
from engine.planner import generate_floor_plan
from ui.dashboard import render_dashboard
from ui.memory_view import render_memory
from ui.components import render_blueprint
from plugins.council.council_orchestrator import ArchitectureCouncil

from datetime import datetime
import uuid

# =========================================================
# INIT STATE
# =========================================================

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "ui_state" not in st.session_state:
    st.session_state.ui_state = {
        "active_design": None,
        "history": [],
        "type": "Luxury Villa",
        "bedrooms": 3,
        "gens": 6,
        "pop": 10
    }

mem = st.session_state.memory
state = st.session_state.ui_state

# =========================================================
# SIDEBAR CONTROL
# =========================================================

st.sidebar.title("📐 Arc Studio — Council OS")

page = st.sidebar.radio(
    "Workspace",
    ["Dashboard", "Design Lab", "Memory"]
)

state["type"] = st.sidebar.selectbox(
    "Typology",
    ["Luxury Villa", "Modern Apartment", "Townhouse"]
)

state["bedrooms"] = st.sidebar.slider("Bedrooms", 1, 8, 3)
state["gens"] = st.sidebar.slider("Generations", 2, 20, 6)
state["pop"] = st.sidebar.slider("Population", 4, 30, 10)

# =========================================================
# COUNCIL INITIALIZATION
# =========================================================

council = ArchitectureCouncil()

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    render_dashboard(mem)

# =========================================================
# DESIGN LAB (EVOLUTION + COUNCIL JUDGMENT)
# =========================================================

elif page == "Design Lab":
    st.title("🌍 Architecture Council Laboratory")

    run = st.button("Run Council Evolution Engine", type="primary")

    if run:
        best, history = run_evolution(
            state["type"],
            state["bedrooms"],
            state["gens"],
            state["pop"]
        )

        best["plan"] = generate_floor_plan(best)

        # 🧠 COUNCIL FINAL EVALUATION
        best["council"] = council.evaluate(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best": best["id"],
            "score": best["score"],
            "time": datetime.now().isoformat()
        })

        state["active_design"] = best
        state["history"] = history

        log_event(mem, f"Council evaluated design {best['id']}")

    # =====================================================
    # ACTIVE DESIGN VIEW
    # =====================================================

    if state["active_design"]:
        d = state["active_design"]

        st.subheader(f"🏛️ Design {d['id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Final Score", d["score"])
        c2.metric("Area", d["area_sqm"])
        c3.metric("Cost", d["cost"])

        st.markdown("---")

        tab1, tab2, tab3 = st.tabs([
            "🗺️ Blueprint",
            "🏛️ Council Review",
            "📊 Evolution"
        ])

        # -------------------------
        # BLUEPRINT
        # -------------------------
        with tab1:
            render_blueprint(d["plan"])

        # -------------------------
        # COUNCIL PANEL
        # -------------------------
        with tab2:
            st.subheader("🏛️ Architecture Council Verdict")

            council_report = d.get("council", None)

            if council_report:
                st.metric("Council Score", council_report["final_score"])
                st.success(council_report["verdict"])

                st.markdown("### Agent Reports")

                for r in council_report["agent_reports"]:
                    st.markdown(f"""
**{r['agent']}**
- Score: `{r['score']}`
- Notes: {r['notes']}
                    """)

        # -------------------------
        # EVOLUTION CHART
        # -------------------------
        with tab3:
            st.subheader("Genetic Convergence")
            st.line_chart(state["history"])

    else:
        st.info("Run the Council Engine to generate a design.")

# =========================================================
# MEMORY VIEW
# =========================================================

elif page == "Memory":
    render_memory(mem)

    st.markdown("---")

    if st.button("Reset System Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.ui_state = {
            "active_design": None,
            "history": [],
            "type": "Luxury Villa",
            "bedrooms": 3,
            "gens": 6,
            "pop": 10
        }

        save_memory()
        st.rerun()