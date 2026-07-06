# ============================================================
# RANDOM V1 REBORN
# AI ARCHITECTURE INTELLIGENCE STUDIO
# Single File Streamlit Foundation
# ============================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# ============================================================
# OPTIONAL DEPENDENCIES
# ============================================================

try:
    import plotly.graph_objects as go
except Exception:
    go = None

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Random AI Architecture Studio",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")


# ============================================================
# BEAUTIFUL UI STYLE
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
    linear-gradient(
        135deg,
        #0b1020,
        #111827,
        #1f2937
    );
    color:white;
}

h1,h2,h3 {
    color:#ffffff;
}

.hero {
    padding:35px;
    border-radius:25px;
    background:
    linear-gradient(
        135deg,
        rgba(59,130,246,0.35),
        rgba(139,92,246,0.35)
    );
    text-align:center;
    margin-bottom:25px;
}

.card {
    background:
    rgba(255,255,255,0.08);
    padding:20px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.15);
    margin-bottom:15px;
}

.metric {
    font-size:32px;
    font-weight:bold;
}

.agent {
    padding:15px;
    border-radius:15px;
    background:
    rgba(16,185,129,0.15);
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# MEMORY ENGINE
# ============================================================

DEFAULT_MEMORY = {
    "projects": [],
    "designs": [],
    "logs": []
}


def load_memory():

    if MEMORY_FILE.exists():

        try:
            return json.loads(
                MEMORY_FILE.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:
            pass

    return DEFAULT_MEMORY.copy()



def save_memory():

    MEMORY_FILE.write_text(
        json.dumps(
            st.session_state.memory,
            indent=2
        ),
        encoding="utf-8"
    )



def log_event(message):

    st.session_state.memory["logs"].append(
        {
            "time":
            datetime.now().isoformat(),

            "message":
            message
        }
    )

    save_memory()



if "memory" not in st.session_state:
    st.session_state.memory = load_memory()


if "design" not in st.session_state:
    st.session_state.design = None


# ============================================================
# AI DESIGN ENGINE
# ============================================================

def generate_design():

    return {

        "id":
        str(uuid.uuid4())[:8].upper(),

        "building_type":
        random.choice(
            [
                "Smart Residence",
                "Office Tower",
                "Research Center",
                "Eco Campus"
            ]
        ),

        "floors":
        random.randint(2,15),

        "area":
        random.randint(200,5000),

        "rooms":
        [
            "Lobby",
            "Living Space",
            "Workspace",
            "Kitchen",
            "Services"
        ],

        "created":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

    }


# ============================================================
# BIM FOUNDATION
# ============================================================

def create_bim(design):

    return {

        "building":
            design["building_type"],

        "geometry":
        {
            "floors":
            design["floors"],

            "gross_area":
            design["area"]
        },

        "structure":
        {
            "columns":
            design["floors"] * 12,

            "beams":
            design["floors"] * 25
        },

        "mep":
        {
            "hvac_load":
            design["area"] * 0.08,

            "power_load":
            design["area"] * 0.05
        },

        "materials":
        [
            "Concrete",
            "Steel",
            "Glass"
        ]

    }


# ============================================================
# VISUALIZATION
# ============================================================

def draw_plan(design):

    if go is None:

        st.warning(
            "Plotly unavailable"
        )

        return


    fig = go.Figure()


    x = 0

    for room in design["rooms"]:

        fig.add_shape(

            type="rect",

            x0=x,
            y0=0,

            x1=x+5,
            y1=5

        )


        fig.add_annotation(

            x=x+2.5,

            y=2.5,

            text=room,

            showarrow=False

        )

        x += 6


    fig.update_layout(
        height=400,
        template="plotly_dark"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



def draw_3d(design):

    if go is None:

        return


    floors = design["floors"]


    fig = go.Figure()


    for floor in range(floors):

        fig.add_trace(

            go.Mesh3d(

                x=[0,10,10,0],

                y=[0,0,10,10],

                z=[
                    floor,
                    floor,
                    floor,
                    floor
                ],

                opacity=0.25

            )

        )


    fig.update_layout(
        height=500,
        template="plotly_dark"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# AI COPILOT
# ============================================================

def ai_assistant(question,bim):

    q = question.lower()


    if "cost" in q:

        return (
            "Preliminary cost analysis: "
            "optimize structure and materials."
        )


    if "energy" in q:

        return (
            "Energy strategy: improve "
            "orientation, glazing and insulation."
        )


    if "structure" in q:

        return (
            f"Structural system contains "
            f"{bim['structure']['columns']} columns."
        )


    return (
        "AI analysis complete. "
        "Try asking about cost, energy, "
        "or structure."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
"""
<div class="hero">

<h1>🏗️ RANDOM</h1>

<h2>AI Architecture Intelligence Studio</h2>

<p>
Generative Design • BIM • AI Agents • Future Digital Twin
</p>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🧠 Random Control"
)


if st.sidebar.button(
    "✨ Generate New Building"
):

    st.session_state.design = generate_design()

    st.session_state.memory["designs"].append(
        st.session_state.design
    )

    log_event(
        "New AI design generated"
    )


# ============================================================
# DASHBOARD
# ============================================================


design = st.session_state.design


c1,c2,c3 = st.columns(3)


with c1:

    st.markdown(
    f"""
    <div class="card">

    <div class="metric">
    {len(st.session_state.memory["designs"])}
    </div>

    AI Designs

    </div>
    """,
    unsafe_allow_html=True
    )


with c2:

    st.markdown(
    """
    <div class="card">

    <div class="metric">
    ONLINE
    </div>

    AI Core

    </div>
    """,
    unsafe_allow_html=True
    )


with c3:

    st.markdown(
    """
    <div class="card">

    <div class="metric">
    V1
    </div>

    Reborn Engine

    </div>
    """,
    unsafe_allow_html=True
    )



# ============================================================
# MAIN WORKSPACE
# ============================================================


if design:


    bim = create_bim(design)


    st.subheader(
        "🏢 Active AI Generated Project"
    )


    st.json(design)



    tabs = st.tabs(
        [
            "BIM",
            "2D Plan",
            "3D Model",
            "AI Agents"
        ]
    )


    with tabs[0]:

        st.json(bim)



    with tabs[1]:

        draw_plan(design)



    with tabs[2]:

        draw_3d(design)



    with tabs[3]:

        agents = [

            "🏛 Architect AI",

            "📐 Structural AI",

            "🌬 MEP AI",

            "🌱 Sustainability AI",

            "💰 Cost AI"

        ]


        for agent in agents:

            st.markdown(
            f"""
            <div class="agent">

            {agent}

            <br>
            Status: Active

            </div>
            """,
            unsafe_allow_html=True
            )



    st.divider()


    st.subheader(
        "🤖 Random AI Copilot"
    )


    question = st.text_input(
        "Ask Random"
    )


    if question:

        st.success(
            ai_assistant(
                question,
                bim
            )
        )


else:

    st.info(
        "Create your first AI building concept using the sidebar."
    )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Random V1 Reborn | AI Architecture Intelligence Foundation"
)
