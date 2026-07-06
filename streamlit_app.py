# ============================================================
# RANDOM V55 REAL BIM ENGINE
# AI ARCHITECTURE + PARAMETRIC BIM STUDIO
#
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import uuid
import math
from datetime import datetime

try:
    import plotly.graph_objects as go
    PLOTLY = True
except Exception:
    PLOTLY = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM AI BIM Studio V55",
    page_icon="🏛️",
    layout="wide"
)


# ============================================================
# VISUAL SYSTEM
# ============================================================

st.markdown(
"""
<style>

.main {
background:#070b18;
}

.hero {

background:
linear-gradient(
135deg,
#111936,
#080d20
);

padding:35px;
border-radius:25px;

border:1px solid #263252;

}


.logo {

font-size:52px;
font-weight:900;

}


.subtitle {

font-size:20px;
color:#aab7d8;

}


.card {

background:#11182d;

padding:20px;

border-radius:18px;

border:1px solid #263252;

}


.metric {

font-size:34px;

font-weight:900;

color:#8ea2ff;

}


.stButton button {

height:45px;

width:100%;

border-radius:14px;

background:#4255ff;

color:white;

font-weight:800;

border:none;

}


</style>
""",
unsafe_allow_html=True
)


# ============================================================
# PROJECT MEMORY
# ============================================================

if "bim" not in st.session_state:

    st.session_state.bim = {

        "project":
        "Untitled Residence",

        "id":
        str(uuid.uuid4()),

        "created":
        str(datetime.now()),

        "units":
        "Metric",

        "levels":[],

        "spaces":[],

        "walls":[],

        "doors":[],

        "windows":[],

        "grid":[],

        "columns":[],

        "beams":[],

        "foundation":{},

        "roof":{},

        "cost":{}

    }


# ============================================================
# UNIT FUNCTIONS
# ============================================================

def meters_to_feet(value):

    return round(value * 3.28084,2)


def mm_to_inches(value):

    return round(value / 25.4,2)



# ============================================================
# AI SPACE GENERATOR
# ============================================================

def create_spaces(
    bedrooms,
    bathrooms
):

    spaces = [

        {
        "name":"Living Room",
        "area":35
        },

        {
        "name":"Kitchen",
        "area":18
        },

        {
        "name":"Dining",
        "area":16
        },

        {
        "name":"Corridor",
        "area":12
        },

        {
        "name":"Laundry",
        "area":8
        },

        {
        "name":"Balcony",
        "area":10
        }

    ]


    for i in range(bedrooms):

        spaces.append(

            {
            "name":
            f"Bedroom {i+1}",

            "area":
            16
            }

        )


    for i in range(bathrooms):

        spaces.append(

            {
            "name":
            f"Bathroom {i+1}",

            "area":
            6
            }

        )


    return spaces



# ============================================================
# BIM GEOMETRY ENGINE
# ============================================================

def create_grid(
    spacing
):

    grid=[]

    axes=[
        "A",
        "B",
        "C",
        "D",
        "E"
    ]


    for a in axes:

        for number in range(1,6):

            grid.append(

                {
                "axis":
                f"{a}{number}",

                "spacing":
                spacing,

                "x":
                number*spacing,

                "y":
                axes.index(a)*spacing

                }

            )

    return grid



def create_walls():

    return [

        {
        "id":"W001",
        "start":[0,0],
        "end":[12,0],
        "thickness":200,
        "height":3000
        },

        {
        "id":"W002",
        "start":[12,0],
        "end":[12,10],
        "thickness":200,
        "height":3000
        }

    ]



def create_openings():

    return {

        "doors":[

            {
            "id":"D001",
            "width":900,
            "height":2100,
            "type":"Entrance"
            }

        ],

        "windows":[

            {
            "id":"WIN001",
            "width":1500,
            "height":1200,
            "sill":900
            }

        ]

    }



def create_structure():

    return {

        "columns":

        [

        {
        "id":"C1",
        "grid":"A1",
        "size":"300x300mm"
        },

        {
        "id":"C2",
        "grid":"A2",
        "size":"300x300mm"
        }

        ],


        "beams":

        [

        {
        "id":"B1",
        "span":"6m",
        "size":"250x450mm"
        }

        ]

    }



# ============================================================
# HEADER
# ============================================================

st.markdown(

"""
<div class="hero">

<div class="logo">

🏛️ RANDOM AI BIM STUDIO V55

</div>

<div class="subtitle">

AI Architecture • Parametric BIM • Automated Documentation

</div>

</div>

""",

unsafe_allow_html=True
)
