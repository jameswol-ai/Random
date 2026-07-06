# ============================================================
# RANDOM V51 AI DESIGN STUDIO + BIM CORE
# Single File Streamlit Edition
#
# AI Architecture Intelligence Engine
# ============================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime


# ============================================================
# OPTIONAL PLOTLY
# ============================================================

try:
    import plotly.graph_objects as go
except Exception:
    go = None


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM V51 AI Design Studio",
    page_icon="🏗️",
    layout="wide"
)


MEMORY_FILE = Path(
    "random_v51_memory.json"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
"""
<style>

.stApp{
background:
linear-gradient(
135deg,
#020617,
#111827,
#1e293b
);
color:white;
}


.hero{

padding:40px;
border-radius:30px;
background:
linear-gradient(
135deg,
rgba(37,99,235,.5),
rgba(124,58,237,.5)
);
text-align:center;

}


.card{

background:
rgba(255,255,255,.08);

padding:20px;

border-radius:20px;

border:
1px solid rgba(255,255,255,.15);

}


.agent{

background:
rgba(16,185,129,.2);

padding:15px;

border-radius:15px;

margin:8px;

}


</style>
""",
unsafe_allow_html=True
)


# ============================================================
# MEMORY
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

        "projects":[],
        "history":[]

    }



def save_memory():

    MEMORY_FILE.write_text(
        json.dumps(
            st.session_state.memory,
            indent=2
        )
    )



if "memory" not in st.session_state:

    st.session_state.memory = load_memory()



if "project" not in st.session_state:

    st.session_state.project = None



# ============================================================
# BIM OBJECT ENGINE
# ============================================================


def create_bim_object(
        object_type,
        name
):

    return {

        "id":
        str(uuid.uuid4())[:8],

        "type":
        object_type,

        "name":
        name,

        "material":
        random.choice(
            [
                "Concrete",
                "Steel",
                "Timber",
                "Glass"
            ]
        ),

        "created":
        datetime.now().isoformat()

    }



def create_space(
        name,
        floor
):

    return {

        "id":
        str(uuid.uuid4())[:6],

        "name":
        name,

        "floor":
        floor,

        "area":
        random.randint(
            15,
            100
        ),

        "objects":[

            create_bim_object(
                "Wall",
                "Boundary Wall"
            ),

            create_bim_object(
                "Door",
                "Entrance Door"
            )

        ]

    }



def create_floor(level):

    rooms=[

        "Lobby",
        "Office",
        "Meeting Room",
        "Core",
        "Services"

    ]


    return {

        "level":
        level,

        "height":
        3.5,

        "spaces":[

            create_space(
                r,
                level
            )

            for r in rooms

        ]

    }


# ============================================================
# AI AGENTS
# ============================================================


def architect_agent(prompt):

    return {

        "agent":
        "Architect AI",

        "building":

        random.choice(

            [
            "Smart Office Tower",
            "Eco Residential Complex",
            "Research Campus",
            "Mixed Use Development"
            ]

        ),

        "concept":

        "Adaptive human-centred architecture",

        "confidence":

        random.randint(
            85,
            99
        )

    }



def structural_agent():

    return {

        "agent":
        "Structural AI",

        "system":

        random.choice(

            [
            "Reinforced Concrete Frame",
            "Steel Frame",
            "Composite System"

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



def sustainability_agent():

    return {

        "energy":

        random.randint(
            80,
            98
        ),

        "strategy":

        random.choice(

            [
            "Solar optimisation",
            "Passive ventilation",
            "Green roof",
            "Water recycling"

            ]

        )

    }



def compliance_agent():

    return {

        "fire":
        "PASS",

        "accessibility":
        "PASS",

        "score":
        random.randint(
            85,
            99
        )

    }


# ============================================================
# BIM GENERATOR
# ============================================================


def generate_project(prompt):


    floors=random.randint(
        3,
        15
    )


    project={

        "id":
        str(uuid.uuid4())[:8],

        "prompt":
        prompt,

        "date":
        datetime.now().isoformat(),


        "architecture":
        architect_agent(prompt),


        "floors":[

            create_floor(i)

            for i in range(floors)

        ],


        "structure":
        structural_agent(),


        "sustainability":
        sustainability_agent(),


        "compliance":
        compliance_agent(),


        "evolution":

        random.randint(
            70,
            95
        )

    }


    return project


# ============================================================
# HEADER
# ============================================================


st.markdown(

"""
<div class="hero">

<h1>🏗️ RANDOM V51</h1>

<h2>AI DESIGN STUDIO + BIM CORE</h2>

<p>
Imagine → Generate → Analyse → Evolve
</p>

</div>
""",

unsafe_allow_html=True

)


# ============================================================
# COPILOT
# ============================================================


st.subheader(
"🤖 BIM Copilot"
)


prompt=st.text_area(
"Describe your building",
placeholder=
"Example: Sustainable 20 floor innovation tower"
)


if st.button(
"🚀 Generate AI Building"
):

    if prompt:

        project=generate_project(
            prompt
        )

        st.session_state.project=project

        st.session_state.memory["projects"].append(
            project
        )

        st.session_state.memory["history"].append(
            datetime.now().isoformat()
        )

        save_memory()

        st.success(
            "AI BIM model created"
        )
