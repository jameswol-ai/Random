import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import uuid

from src.auth import login_page
from src.memory import load_memory, save_memory, DEFAULT_MEMORY
from src.knowledge_base import ARCHITECTURE_TYPES
from src.design_generator import generate_design, generate_concepts
from src.evolution import evolve_design_multi, pareto_front
from src.rendering_2d import generate_floor_plan
from src.rendering_3d import build_3d_stacked_figure
from src.ifc_export import export_ifc
from src.gltf_export import design_to_glb
from src.room_editor import render_room_editor
from src.utils import add_xp, get_user, load_users, save_users, xp_for_level

# ---- Page config ----
st.set_page_config(page_title="RANDOM V4", page_icon="🏗️", layout="wide")

# ---- Dark theme CSS ----
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, .stApp { background: #0f1117; font-family: 'Inter', sans-serif; color: #e2e8f0; }
h1, h2, h3, h4, h5, .stTitle, .stHeader { font-weight: 600; color: #f1f5f9; }
[data-testid="stSidebar"] { background: #16181d; border-right: 1px solid #1e293b; }
.glass-card { background: rgba(30,41,59,0.6); backdrop-filter: blur(12px); border-radius: 16px; padding: 1.5rem; border: 1px solid #334155; box-shadow: 0 8px 32px rgba(0,0,0,0.4); margin-bottom: 1.5rem; }
.banner { background: linear-gradient(135deg, #1a2a3a, #0f172a); padding: 2rem 2.5rem; border-radius: 24px; color: white; margin-bottom: 2rem; border: 1px solid #334155; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
.metric-box { background: rgba(30,41,59,0.8); border-radius: 12px; padding: 0.8rem 1rem; border-left: 4px solid #22c55e; }
.concept-item { background: rgba(30,41,59,0.4); border-radius: 10px; padding: 0.75rem 1rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; }
.concept-score { background: rgba(34,197,94,0.15); padding: 0.25rem 1rem; border-radius: 20px; font-weight: 700; color: #4ade80; }
.agent-box { background: rgba(30,41,59,0.5); border-radius: 14px; padding: 1rem; text-align: center; border: 1px solid #334155; }
.agent-name { font-weight: 600; color: #94a3b8; font-size: 0.85rem; }
.agent-score { font-size: 2rem; font-weight: 700; color: #f1f5f9; }
.agent-sub { font-size: 0.7rem; color: #64748b; }
.stButton > button { background: #22c55e; color: #0f172a; border: none; border-radius: 12px; padding: 0.6rem 1.8rem; font-weight: 600; transition: all 0.2s; }
.stButton > button:hover { background: #16a34a; color: white; box-shadow: 0 8px 20px rgba(34,197,94,0.3); }
.xp-container { display: flex; align-items: center; gap: 10px; margin-bottom: 1rem; }
.xp-bar-bg { flex: 1; height: 8px; background: #1e293b; border-radius: 4px; overflow: hidden; }
.xp-bar-fill { height: 100%; background: #22c55e; border-radius: 4px; }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# ---- Session init ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.memory = DEFAULT_MEMORY.copy()
    st.session_state.page = "Dashboard"
    st.session_state.generated_concepts = []
    st.session_state.unit_system = "Metric"
    st.session_state.all_final_designs = []

# Auto-create admin
from pathlib import Path
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "random_users.json"
if not load_users():
    from src.utils import create_user
    create_user("admin", "admin123", role="admin")

# ---- Login / Logout ----
if not st.session_state.logged_in:
    login_page()
    st.stop()

username = st.session_state.username
user_data = st.session_state.user_data
memory = st.session_state.memory

# ---- Sidebar ----
with st.sidebar:
    st.markdown("### 🏗️ RANDOM V4")
    st.markdown(f"**👤 {username}**")
    lvl = user_data.get("level", 1)
    xp = user_data.get("xp", 0)
    needed = xp_for_level(lvl)
    progress = xp / needed if needed > 0 else 1.0
    st.markdown(f"""
    <div class="xp-container">
        <span style="font-size:12px; color:#94a3b8;">LVL {lvl}</span>
        <div class="xp-bar-bg">
            <div class="xp-bar-fill" style="width:{progress*100}%;"></div>
        </div>
        <span style="font-size:10px; color:#64748b;">{xp}/{needed} XP</span>
    </div>
    """, unsafe_allow_html=True)
    
    nav = st.radio("Navigation", [
        "Dashboard", "Random Copilot", "Concepts", "Comparison",
        "2D Plans", "Room Editor", "3D Viewer", "Reports", "Memory", "Settings"
    ])
    st.session_state.page = nav
    st.divider()
    
    # Admin panel
    if user_data.get("role") == "admin":
        with st.expander("🛡️ Admin Panel"):
            users = load_users()
            for u in users:
                cols = st.columns([3,1])
                cols[0].write(f"**{u['username']}** (Lvl {u['level']})")
                if u["username"] != username:
                    if cols[1].button("🗑️", key=f"del_{u['username']}"):
                        users.remove(u)
                        save_users(users)
                        st.rerun()
                else:
                    cols[1].write("you")
    
    st.markdown("### 📁 PROJECT MEMORY")
    for proj in memory["projects"][-5:]:
        col1, col2 = st.columns([3,2])
        col1.markdown(f"**{proj['name']}**")
        col2.markdown(f"<span style='color:#64748b;font-size:0.8rem;'>{proj['date']}</span>", unsafe_allow_html=True)
    
    if st.button("➕ New Project", use_container_width=True):
        new_name = f"Project {len(memory['projects'])+1}"
        memory["projects"].append({"name": new_name, "date": datetime.now().strftime("%b %d, %Y")})
        save_memory(username, memory)
        st.rerun()
    
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        save_memory(username, memory)
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_data = None
        st.session_state.memory = DEFAULT_MEMORY.copy()
        st.session_state.generated_concepts = []
        st.rerun()

# ---- Page routing ----
page = st.session_state.page

if page == "Dashboard":
    # ... (use the same dashboard as V4 but import from modules)
    st.markdown('<div class="banner"><h1>Welcome back, Architect</h1><p>Create. Evolve. Perfect.</p></div>', unsafe_allow_html=True)
    if not st.session_state.generated_concepts:
        with st.spinner("Generating 5 unique design concepts..."):
            st.session_state.generated_concepts = generate_concepts(5)
            leveled_up = add_xp(username, 10)
            st.session_state.user_data = get_user(username)
            if leveled_up:
                st.balloons()
    # ... rest of dashboard code ...
    # Best design view, 2D/3D preview, agent scores

elif page == "Random Copilot":
    # ... copilot page using evolve_design_multi, Pareto front ...
    pass

# ... etc. for all pages ...

# You can copy the page logic directly from the V4 single-file version, now calling functions from src.

# ---- Footer ----
st.markdown('<div style="text-align:center;padding:1.5rem 0;color:#64748b;font-size:0.8rem;border-top:1px solid #1e293b;"><span>AI Powered</span> · <span>Data Driven</span> · <span>Secure</span> · <span>Scalable</span></div>', unsafe_allow_html=True)
