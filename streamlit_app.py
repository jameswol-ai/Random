# streamlit_app.py

import streamlit as st
from core import memory, registry
import importlib
import os

st.set_page_config(page_title="RANDOM AI SYSTEM V1", layout="wide")

mem = memory.load()

# -------------------------------
# LOAD PLUGINS
# -------------------------------

def load_plugins():
    plugin_files = [
        "modules.design_engine",
        "modules.city_engine",
        "modules.knowledge_engine"
    ]

    for p in plugin_files:
        mod = importlib.import_module(p)
        name = p.split(".")[-1]
        registry.register(name, mod.run)

load_plugins()

# -------------------------------
# UI
# -------------------------------

st.title("🧠 RANDOM AI SYSTEM V1")

menu = st.sidebar.selectbox("Modules", [
    "Dashboard",
    "Design Engine",
    "City Engine",
    "Knowledge Engine"
] + registry.list_engines())

# -------------------------------
# DASHBOARD
# -------------------------------

if menu == "Dashboard":
    st.metric("Cities", len(mem["cities"]))
    st.metric("Designs", len(mem["designs"]))
    st.metric("Knowledge", len(mem["knowledge"]))
    st.metric("Engines", len(registry.list_engines()))

# -------------------------------
# DESIGN
# -------------------------------

elif menu == "Design Engine":
    if st.button("Generate Design"):
        result = registry.get("design_engine")(mem)
        memory.save(mem)
        st.json(result)

# -------------------------------
# CITY
# -------------------------------

elif menu == "City Engine":
    if st.button("Spawn City"):
        result = registry.get("city_engine")(mem)
        memory.save(mem)
        st.json(result)

# -------------------------------
# KNOWLEDGE
# -------------------------------

elif menu == "Knowledge Engine":
    text = st.text_input("Knowledge")

    if st.button("Store"):
        result = registry.get("knowledge_engine")(mem, text)
        memory.save(mem)
        st.success(result)

# -------------------------------
# DYNAMIC ENGINE VIEW
# -------------------------------

elif menu in registry.list_engines():
    st.subheader(f"Engine: {menu}")

    if st.button("Run Engine"):
        result = registry.get(menu)(mem)
        memory.save(mem)
        st.json(result)
