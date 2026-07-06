# ============================================================
# RANDOM V55.1 AI BIM STUDIO
# Parametric Architecture + BIM Intelligence Engine
#
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import uuid
from datetime import datetime


# Optional visualization
try:
    import plotly.graph_objects as go
    PLOTLY = True
except Exception:
    PLOTLY = False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RANDOM AI BIM Studio V55.1",
    page_icon="🏛️",
    layout="wide"
)


# ============================================================
# RANDOM AI VISUAL SYSTEM
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

color:#aab7d8;

font-size:20px;

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

background:#4255ff;

color:white;

height:45px;

border-radius:14px;

font-weight:800;

width:100%;

}

</style>

""",
unsafe_allow_html=True
)



# ============================================================
# UNIT CONVERSION ENGINE
# ============================================================

def mm_to_inches(mm):

    return mm / 25.4



def mm_to_feet_inches(mm):

    inches = mm_to_inches(mm)

    feet = int(inches // 12)

    remaining = round(
        inches % 12,
        1
    )

    return f"{feet}'-{remaining}\""



def m_to_feet_inches(m):

    total_inches = m * 39.3701

    feet = int(total_inches // 12)

    inches = round(
        total_inches % 12,
        1
    )

    return f"{feet}'-{inches}\""



def sqm_to_sqft(area):

    return round(
        area * 10.7639,
        2
    )



def show_length(
    mm,
    mode
):

    metric = f"{mm} mm"

    imperial = mm_to_feet_inches(mm)


    if mode == "Metric":

        return metric


    if mode == "Imperial":

        return imperial


    return f"{metric} ({imperial})"



def show_area(
    area,
    mode
):

    metric = f"{area} m²"

    imperial = (
        f"{sqm_to_sqft(area)} ft²"
    )


    if mode == "Metric":

        return metric


    if mode == "Imperial":

        return imperial


    return f"{metric} ({imperial})"



# ============================================================
# BIM DATABASE
# ============================================================

if "bim" not in st.session_state:

    st.session_state.bim = {

        "id":
        str(uuid.uuid4()),


        "created":
        str(datetime.now()),


        "project":
        "AI Residence",


        "units":
        "Dual",


        "levels":
        [],


        "spaces":
        [],


        "walls":
        [],


        "doors":
        [],


        "windows":
        [],


        "grid":
        [],


        "columns":
        [],


        "beams":
        [],


        "foundation":
        {},


        "roof":
        {},


        "cost":
        {}

    }



# ============================================================
# ARCHITECTURAL GENERATORS
# ============================================================

def generate_spaces(
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
        "name":"Balcony",
        "area":10
        },

        {
        "name":"Laundry",
        "area":8
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



def generate_walls():

    return [

        {
        "id":"W001",
        "length":6000,
        "height":3000,
        "thickness":200
        },


        {
        "id":"W002",
        "length":5000,
        "height":3000,
        "thickness":200
        }

    ]



def generate_doors():

    return [

        {
        "id":"D001",
        "type":"Entrance",
        "width":1200,
        "height":2400
        },


        {
        "id":"D002",
        "type":"Internal",
        "width":900,
        "height":2100
        }

    ]



def generate_windows():

    return [

        {
        "id":"WIN001",
        "width":1500,
        "height":1200
        }

    ]
