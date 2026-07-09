import streamlit as st
from src.auth import login_page
from src.memory import load_memory, save_memory, DEFAULT_MEMORY
from src.utils import add_xp, get_user, load_users, create_user
from pathlib import Path

st.set_page_config(page_title="RANDOM V4", page_icon="🏗️", layout="wide")

# Session init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.memory = DEFAULT_MEMORY.copy()
    st.session_state.generated_concepts = []
    st.session_state.unit_system = "Metric"
    st.session_state.all_final_designs = []

# Auto-create admin if no users
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "random_users.json"
if not USER_FILE.exists() or not load_users():
    create_user("admin", "admin123", role="admin")

if not st.session_state.logged_in:
    login_page()
else:
    # Load memory
    username = st.session_state.username
    st.session_state.memory = load_memory(username)
    # The sidebar and navigation are built inside each page
    # We'll use a multipage app: each page is in pages/ folder
