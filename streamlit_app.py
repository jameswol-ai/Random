# ============================================================
# RANDOM V51 AI CORE
# AI ARCHITECTURE OPERATING SYSTEM
#
# Single File Streamlit Edition
# Stable Foundation Build
# ============================================================

import streamlit as st
import json
import uuid
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM AI | Architecture Core",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
    """
    <style>
    .main {
        background-color: #0b1020;
    }

    .card {
        background: #151b32;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 15px;
        border: 1px solid #27304d;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        color: white;
    }

    .subtitle {
        color: #9aa7c7;
        font-size: 18px;
    }

    .agent {
        padding: 12px;
        border-radius: 12px;
        background: #10162b;
        margin: 8px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION MEMORY
# ============================================================

if "project" not in st.session_state:

    st.session_state.project = {
        "id": str(uuid.uuid4()),
        "name": "Untitled Project",
        "created": str(datetime.now()),
        "requirements": [],
        "decisions": [],
        "agents": []
    }


if "memory" not in st.session_state:
    st.session_state.memory = []


if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# AI AGENTS
# ============================================================

AGENTS = {

    "Architect Agent": {
        "role": "Spatial design intelligence",
        "status": "Ready"
    },

    "BIM Agent": {
        "role": "Building information modelling",
        "status": "Ready"
    },

    "Structural Agent": {
        "role": "Structural reasoning",
        "status": "Ready"
    },

    "Sustainability Agent": {
        "role": "Environmental analysis",
        "status": "Ready"
    },

    "Cost Agent": {
        "role": "Cost and feasibility analysis",
        "status": "Ready"
    }
}


# ============================================================
# RANDOM AI ENGINE
# ============================================================

def random_ai_command(command):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    result = {
        "time": timestamp,
        "command": command,
        "analysis": []
    }


    if "house" in command.lower():

        result["analysis"] = [

            "Architect Agent: Creating spatial concept",
            "BIM Agent: Defining building elements",
            "Structural Agent: Selecting structural strategy",
            "Sustainability Agent: Evaluating passive design",
            "Cost Agent: Reviewing feasibility"

        ]

    else:

        result["analysis"] = [

            "Architect Agent: Analysing design intent",
            "BIM Agent: Mapping building data",
            "Structural Agent: Checking possibilities",
            "Sustainability Agent: Reviewing performance",
            "Cost Agent: Estimating implications"

        ]


    st.session_state.memory.append(result)

    st.session_state.project["decisions"].append(
        result
    )

    return result



# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="title">
    🧠 RANDOM AI
    </div>

    <div class="subtitle">
    Architecture Intelligence Operating System
    </div>
    """,
    unsafe_allow_html=True
)


st.write("")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🏗️ Project")

    project_name = st.text_input(
        "Project Name",
        st.session_state.project["name"]
    )

    st.session_state.project["name"] = project_name


    st.divider()

    st.header("AI Core")

    st.write(
        "Version: RANDOM V51"
    )

    st.write(
        "Mode: Architecture Intelligence"
    )



# ============================================================
# DASHBOARD
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="card">

        <h3>📁 Project</h3>

        {st.session_state.project["name"]}

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="card">

        <h3>🧠 Memory</h3>

        {len(st.session_state.memory)}
        decisions stored

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="card">

        <h3>🤖 Agents</h3>

        5 active

        </div>
        """,
        unsafe_allow_html=True
    )



# ============================================================
# AGENT PANEL
# ============================================================

st.subheader("🤖 AI Agent Network")


for agent, data in AGENTS.items():

    st.markdown(
        f"""
        <div class="agent">

        <b>{agent}</b><br>

        {data["role"]}

        <br>

        Status: {data["status"]}

        </div>
        """,
        unsafe_allow_html=True
    )



# ============================================================
# COMMAND CENTER
# ============================================================

st.subheader("💬 RANDOM AI Command Center")


command = st.chat_input(
    "Describe a building, design problem, or analysis task..."
)


if command:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": command
        }
    )


    response = random_ai_command(command)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )



for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.chat_message("user").write(
            msg["content"]
        )

    else:

        with st.chat_message("assistant"):

            st.write(
                "RANDOM AI analysis:"
            )

            for item in msg["content"]["analysis"]:

                st.write(
                    "• " + item
                )



# ============================================================
# MEMORY VIEW
# ============================================================

st.divider()

st.subheader("📚 Design Reasoning Memory")


if st.session_state.memory:

    st.json(
        st.session_state.memory
    )

else:

    st.info(
        "No design decisions recorded yet."
    )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "RANDOM V51 AI CORE | Architecture Intelligence Platform"
)
