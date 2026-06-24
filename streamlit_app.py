# client/streamlit_app.py

import streamlit as st
import requests

API = "http://localhost:8000"

st.title("🌍 RANDOM AI MULTI-USER SIMULATION")

# -----------------------------
# CONNECT USER
# -----------------------------

if "user_id" not in st.session_state:
    if st.button("Connect to World"):
        res = requests.post(f"{API}/connect").json()
        st.session_state.user_id = res["user_id"]

if "user_id" in st.session_state:
    st.success(f"Connected: {st.session_state.user_id}")

    uid = st.session_state.user_id

    # -------------------------
    # ACTIONS
    # -------------------------

    col1, col2, col3 = st.columns(3)

    if col1.button("Spawn City"):
        r = requests.post(f"{API}/city/{uid}")
        st.json(r.json())

    if col2.button("Create Design"):
        r = requests.post(f"{API}/design/{uid}")
        st.json(r.json())

    if col3.button("Tick World"):
        requests.post(f"{API}/tick")
        st.success("World evolved")

    # -------------------------
    # WORLD VIEW
    # -------------------------

    world = requests.get(f"{API}/world").json()

    st.subheader("🌍 World State")

    st.metric("Users", len(world["users"]))
    st.metric("Cities", len(world["cities"]))
    st.metric("Designs", len(world["designs"]))
    st.metric("Events", len(world["events"]))

    st.json(world)
