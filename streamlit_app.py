import streamlit as st
import uuid

from config import DEFAULT_STATE
from memory.store import load_memory, save_memory
from memory.logger import log_event

from core.engine import run_evolutionary_loop
from visualization.blueprint_renderer import render_blueprint
from analytics.diagnostics import (
    run_structural_review,
    calculate_material_takeoffs
)

st.set_page_config(page_title="Random Studio Engine", layout="wide")

# ---------------- MEMORY ----------------
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

mem = st.session_state.memory


# ---------------- SIDEBAR ----------------
st.sidebar.title("📐 Arc Studio")

page = st.sidebar.radio(
    "Workspace",
    ["Dashboard Control", "Design Synthesis Lab", "Memory Repositories"]
)

# Config
with st.sidebar.expander("Configure Engine"):
    all_types = ["Luxury Villa", "Modern Apartment", "Townhouse",
                 "Boutique Office", "Corporate Hub"]

    design_type = st.selectbox("Typology", all_types)
    bedrooms = st.slider("Bedrooms", 1, 8, 3)
    generations = st.slider("Generations", 2, 20, 6)
    pop = st.slider("Population", 4, 30, 10)


# ---------------- DASHBOARD ----------------
if page == "Dashboard Control":
    st.title("📐 Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Evolution Runs", len(mem["evolution"]))


# ---------------- LAB ----------------
elif page == "Design Synthesis Lab":
    st.title("🌍 Design Lab")

    if st.button("Run Evolution Engine", type="primary"):

        best, trend = run_evolutionary_loop(
            design_type,
            bedrooms,
            generations,
            pop,
            lambda: str(uuid.uuid4())[:8].upper()
        )

        best["plan"] = [
            {"name": "Living", "w": 5, "h": 4, "color": "#1e3a8a"}
        ]

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best": best["id"],
            "score": best["score"]
        })

        st.session_state.active = best
        st.session_state.trend = trend

        log_event(mem, f"Generated design {best['id']}")
        save_memory(mem)

    if "active" in st.session_state:
        d = st.session_state.active

        st.metric("Score", d["score"])
        st.metric("Area", d["area_sqm"])
        st.metric("Cost", d["cost"])

        render_blueprint(d["plan"])

        st.subheader("Diagnostics")
        for a in run_structural_review(d):
            st.write(a)

        st.subheader("Materials")
        st.table(calculate_material_takeoffs(d))


# ---------------- MEMORY ----------------
elif page == "Memory Repositories":
    st.title("🧠 Memory")

    st.json(mem)

    if st.button("Reset Memory"):
        st.session_state.memory = DEFAULT_STATE.copy()
        save_memory(st.session_state.memory)
        st.rerun()