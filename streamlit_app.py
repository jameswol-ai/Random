# ============================================================
# RANDOM V51.1 AI DESIGN STUDIO + BIM CORE
# FIXED SINGLE FILE STREAMLIT EDITION
# ============================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime


# ============================================================
# OPTIONAL LIBRARIES
# ============================================================

try:
    import plotly.graph_objects as go
except Exception:
    go = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM V51 BIM CORE",
    page_icon="🏗️",
    layout="wide"
)


MEMORY_FILE = Path(
    "random_memory.json"
)


# ============================================================
# SESSION INITIALIZATION
# ============================================================

if "memory" not in st.session_state:
    st.session_state.memory = {
        "projects": [],
        "history": []
    }


if "project" not in st.session_state:
    st.session_state.project = None



# ============================================================
# MEMORY FUNCTIONS
# ============================================================

def load_memory():

    if MEMORY_FILE.exists():

        try:
            return json.loads(
                MEMORY_FILE.read_text()
            )

        except Exception:
            pass

    return {
        "projects": [],
        "history": []
    }



def save_memory():

    try:

        MEMORY_FILE.write_text(
            json.dumps(
                st.session_state.memory,
                indent=2
            )
        )

    except Exception:
        pass



if not st.session_state.memory["projects"]:

    st.session_state.memory = load_memory()



# ============================================================
# STYLE
# ============================================================

st.markdown(
"""
<style>

.stApp {

background:
linear-gradient(
135deg,
#020617,
#111827,
#1e293b
);

}


.hero {

padding:40px;
border-radius:25px;

background:
linear-gradient(
135deg,
rgba(37,99,235,.5),
rgba(124,58,237,.5)
);

text-align:center;

}


.agent {

padding:15px;
margin:8px;
border-radius:15px;

background:
rgba(16,185,129,.2);

}

</style>
""",
unsafe_allow_html=True
)



# ============================================================
# BIM GENERATORS
# ============================================================

def create_object(kind):

    return {

        "id":
        str(uuid.uuid4())[:8],

        "type":
        kind,

        "material":
        random.choice(
            [
                "Concrete",
                "Steel",
                "Glass",
                "Timber"
            ]
        )

    }



def create_space(name, floor):

    return {

        "name": name,

        "floor": floor,

        "area":
        random.randint(
            20,
            120
        ),

        "objects":

        [
            create_object("Wall"),
            create_object("Door"),
            create_object("Window")
        ]

    }



def create_floor(level):

    names = [

        "Lobby",
        "Office",
        "Meeting",
        "Services",
        "Core"

    ]

    return {

        "level": level,

        "spaces":

        [
            create_space(
                n,
                level
            )

            for n in names

        ]

    }



# ============================================================
# AI AGENTS
# ============================================================

def architect_ai(prompt):

    return {

        "building":

        random.choice(

            [
                "Smart Tower",
                "Eco Campus",
                "Mixed Use Hub",
                "Innovation Centre"
            ]

        ),

        "concept":
        "Adaptive intelligent architecture"

    }



def structure_ai():

    return {

        "system":

        random.choice(

            [
                "Concrete Frame",
                "Steel Frame",
                "Composite Structure"
            ]

        ),

        "grid":

        random.choice(
            [
                5,
                6,
                7.5
            ]
        )

    }



def sustainability_ai():

    return {

        "score":
        random.randint(
            80,
            98
        ),

        "strategy":
        random.choice(
            [
                "Solar",
                "Passive Cooling",
                "Green Roof"
            ]
        )

    }



# ============================================================
# PROJECT ENGINE
# ============================================================

def generate_project(prompt):

    floors=random.randint(
        3,
        12
    )


    return {

        "id":
        str(uuid.uuid4())[:8],

        "prompt":
        prompt,

        "created":
        datetime.now().isoformat(),

        "architecture":
        architect_ai(prompt),

        "floors":

        [
            create_floor(i)
            for i in range(floors)
        ],

        "structure":
        structure_ai(),

        "sustainability":
        sustainability_ai()

    }



# ============================================================
# VISUALS
# ============================================================

def floor_plan(project):

    if go is None:
        st.info("Plotly not installed")
        return


    fig=go.Figure()

    x=0


    for room in project["floors"][0]["spaces"]:

        fig.add_shape(

            type="rect",

            x0=x,

            y0=0,

            x1=x+8,

            y1=6

        )


        fig.add_annotation(

            x=x+4,

            y=3,

            text=room["name"],

            showarrow=False

        )


        x+=10


    fig.update_layout(
        template="plotly_dark",
        height=450
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ============================================================
# UI
# ============================================================


st.markdown(

"""
<div class="hero">

<h1>🏗️ RANDOM V51.1 BIM CORE</h1>

<h3>AI Architecture Intelligence Engine</h3>

</div>
""",

unsafe_allow_html=True

)



prompt=st.text_area(
"Describe your building"
)



if st.button(
"🚀 Generate BIM"
):

    if prompt.strip():

        new_project=generate_project(prompt)

        st.session_state.project=new_project

        st.session_state.memory["projects"].append(
            new_project
        )

        st.session_state.memory["history"].append(
            datetime.now().isoformat()
        )

        save_memory()

        st.success(
            "BIM project created"
        )


# ============================================================
# DISPLAY
# ============================================================

project=st.session_state.project


if project:


    c1,c2,c3=st.columns(3)


    c1.metric(
        "Building",
        project["architecture"]["building"]
    )


    c2.metric(
        "Floors",
        len(project["floors"])
    )


    c3.metric(
        "Energy",
        f"{project['sustainability']['score']}%"
    )


    tab1,tab2,tab3=st.tabs(
        [
            "🏢 Explorer",
            "📐 Plan",
            "🧠 AI"
        ]
    )


    with tab1:

        for floor in project["floors"]:

            with st.expander(
                f"Floor {floor['level']}"
            ):

                for room in floor["spaces"]:

                    st.write(
                        room["name"],
                        room["area"],
                        "m²"
                    )


    with tab2:

        floor_plan(project)


    with tab3:

        st.write(
            project["architecture"]
        )

        st.write(
            project["structure"]
        )

        st.write(
            project["sustainability"]
        )


else:

    st.info(
        "Enter a project description to activate RANDOM AI."
    )



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "🧠 RANDOM MEMORY"
    )

    st.metric(
        "Projects",
        len(
            st.session_state.memory["projects"]
        )
    )


st.caption(
"RANDOM V51.1 | Fixed BIM Core"
)
