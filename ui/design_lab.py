import streamlit as st
from engine.evolution import run_evolution
from engine.planner import generate_floor_plan
from ui.components import render_blueprint

def render_design_lab(mem, log_event, state):
    st.title("🌍 Design Lab")

    run = st.button("Run Evolution Engine", type="primary")

    if run:
        best, history = run_evolution(
            state["type"],
            state["bedrooms"],
            state["gens"],
            state["pop"]
        )

        best["plan"] = generate_floor_plan(best)

        mem["designs"].append(best)
        state["active"] = best
        state["history"] = history

        log_event(mem, f"Generated {best['id']}")

    if state["active"]:
        d = state["active"]

        st.subheader(f"Design {d['id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", d["score"])
        c2.metric("Area", d["area_sqm"])
        c3.metric("Cost", d["cost"])

        render_blueprint(d["plan"])