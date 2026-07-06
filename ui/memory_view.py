import streamlit as st

def render_memory(mem):
    st.title("🧠 Memory System")
    st.json(mem)
