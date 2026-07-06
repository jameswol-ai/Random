# ============================================================
# RANDOM V50 BIM CORE
# AI ARCHITECTURE + BIM INTELLIGENCE ENGINE
# Single File Streamlit Edition
#
# V2 AI Design Studio upgraded into BIM Core
# ============================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime


# ============================================================
# OPTIONAL VISUALIZATION
# ============================================================

try:
    import plotly.graph_objects as go
except Exception:
    go = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Random V50 BIM Core",
    page_icon="🏗️",
    layout="wide"
)


MEMORY_FILE = Path(
    "random_v50_memory.json"
)


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
"""
<style>

.stApp {

background:
linear-gradient(
120deg,
#030712,
#111827,
#1e293b
);

color:white;

}


.hero {

padding:45px;

border-radius:30px;

background:
linear-gradient(
135deg,
rgba(37,99,235,.45),
rgba(124,58,237,.45)
);

text-align:center;

}


.card {

background:
rgba(255,255,255,.08);

padding:20px;

border-radius:20px;

border:
1px solid rgba(255,255,255,.15);

}


.agent {

background:
rgba(16,185,129,.18);

padding:15px;

border-radius:15px;

margin:10px 0;

}


</style>
""",
unsafe_allow_html=True
)



# ============================================================
# MEMORY SYSTEM
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
# BIM OBJECT GENERATORS
# ============================================================


def create_space(name, floor):

    return {

        "id":
        str(uuid.uuid4())[:6],

        "name":
        name,

        "floor":
        floor,

        "type":
        "space",

        "area":
        random.randint(12,80)

    }



def create_floor(number):

    rooms = [

        "Lobby",

        "Office",

        "Meeting Room",

        "Core",

        "Services"

    ]


    return {

        "level":
        number,

        "height":
        3.5,


        "spaces":

        [

            create_space(
                r,
                number
            )

            for r in rooms

        ]

    }



def create_structure():

    grid = random.choice(

        [

            5,

            6,

            7.5

        ]

    )


    columns = []


    for x in range(4):

        for y in range(4):

            columns.append(

                {

                "id":
                f"C{x}{y}",

                "x":
                x*grid,

                "y":
                y*grid

                }

            )


    return {

        "system":
        random.choice(

            [

            "Reinforced Concrete Frame",

            "Steel Frame",

            "Composite Structure"

            ]

        ),


        "grid_spacing":
        grid,


        "columns":
        columns

    }



# ============================================================
# AI AGENTS
# ============================================================


def architect_ai(prompt):

    return {

        "building_type":

        random.choice(

            [

            "Smart Office Tower",

            "Eco Residential Complex",

            "Innovation Campus",

            "Mixed Use Building"

            ]

        ),


        "concept":

        "Human-centred adaptive architecture",


        "spaces":

        [

        "Entrance",

        "Public Zone",

        "Work Zone",

        "Service Zone"

        ]

    }



def structural_ai():

    return create_structure()



def sustainability_ai():

    return {

        "energy_score":

        random.randint(
            75,
            98
        ),


        "strategy":

        random.choice(

            [

            "Passive ventilation",

            "Solar optimisation",

            "Green roof",

            "Water reuse"

            ]

        )

    }



def compliance_ai():

    return {

        "fire":

        "Checked",


        "accessibility":

        "Checked",


        "safety_score":

        random.randint(
            80,
            99
        )

    }


# ============================================================
# BIM PROJECT GENERATOR
# ============================================================


def generate_bim_project(prompt):


    floors = random.randint(
        3,
        15
    )


    building = {

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

            for i in range(
                floors
            )

        ],


        "structure":
        structural_ai(),


        "sustainability":
        sustainability_ai(),


        "compliance":
        compliance_ai(),


        "area":
        floors *
        random.randint(
            300,
            900
        )

    }


    return building
