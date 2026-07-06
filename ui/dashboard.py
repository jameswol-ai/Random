import streamlit as st

def render_dashboard(mem):
    st.title("📐 Control Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Evolution Runs", len(mem["evolution"]))

    st.markdown("---")

    for log in mem["logs"][-6:]:
        st.caption(f"{log['time']} — {log['msg']}")