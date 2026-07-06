# ============================================================
# RANDOM V52 HYBRID ARCHITECTURE ENGINE
# AI HOUSE GENERATOR + BIM FOUNDATION
#
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import uuid
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM V52 Architecture AI",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
"""
<style>

.main {
background:#0b1020;
}

.card {
background:#151b32;
padding:20px;
border-radius:15px;
margin:10px 0;
}

h1,h2,h3 {
color:white;
}

</style>
""",
unsafe_allow_html=True
)



# ============================================================
# SESSION DATA
# ============================================================

if "model" not in st.session_state:

    st.session_state.model = {
        "id":str(uuid.uuid4()),
        "created":str(datetime.now()),
        "rooms":[],
        "grid":[],
        "structure":{},
        "cost":{}
    }



# ============================================================
# CONVERSION
# ============================================================

def metric_to_imperial(value):

    return round(value * 3.28084,2)



# ============================================================
# GRID ENGINE
# ============================================================

def generate_grid(spacing, size_x, size_y):

    grid=[]

    x=0

    while x <= size_x:

        y=0

        while y <= size_y:

            grid.append(
                {
                    "x":round(x,2),
                    "y":round(y,2)
                }
            )

            y+=spacing

        x+=spacing

    return grid



# ============================================================
# SPACE ENGINE
# ============================================================

def generate_house(
    bedrooms,
    bathrooms
):

    spaces=[

        {
        "name":"Living Room",
        "area":30
        },

        {
        "name":"Kitchen",
        "area":15
        },

        {
        "name":"Dining",
        "area":15
        },

        {
        "name":"Corridor",
        "area":10
        },

        {
        "name":"Balcony",
        "area":8
        }

    ]


    for i in range(bedrooms):

        spaces.append(
            {
            "name":f"Bedroom {i+1}",
            "area":16
            }
        )


    for i in range(bathrooms):

        spaces.append(
            {
            "name":f"Bathroom {i+1}",
            "area":6
            }
        )


    return spaces



# ============================================================
# COST ENGINE
# ============================================================

def calculate_cost(area):

    rate = 500

    return {

        "Floor Area m2":area,

        "Concrete Estimate m3":
        round(area*0.25,2),

        "Floor Finish m2":
        area,

        "Estimated Construction Cost USD":
        area*rate

    }



# ============================================================
# HEADER
# ============================================================

st.title(
"🧠 RANDOM V52"
)

st.subheader(
"Hybrid Architecture + BIM Intelligence Engine"
)



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🏠 House Parameters")


    floors=st.number_input(
        "Number of Floors",
        1,
        10,
        2
    )


    bedrooms=st.number_input(
        "Bedrooms",
        1,
        20,
        4
    )


    bathrooms=st.number_input(
        "Bathrooms",
        1,
        20,
        3
    )


    unit=st.selectbox(
        "Unit System",
        [
            "Metric",
            "Imperial"
        ]
    )


    grid_spacing=st.selectbox(
        "Grid Spacing",
        [
            1,
            1.5,
            3
        ]
    )


    generate=st.button(
        "Generate House"
    )



# ============================================================
# GENERATION
# ============================================================

if generate:

    rooms=generate_house(
        bedrooms,
        bathrooms
    )


    grid=generate_grid(
        grid_spacing,
        18,
        15
    )


    area=sum(
        r["area"]
        for r in rooms
    )


    st.session_state.model["rooms"]=rooms

    st.session_state.model["grid"]=grid


    st.session_state.model["structure"]={

        "Columns":
        "300x300 mm Reinforced Concrete",

        "Beams":
        "250x450 mm Reinforced Concrete",

        "Foundation":
        "Pad Foundation System",

        "Roof":
        "Pitched Roof 30 degrees",

        "Ceiling":
        "Gypsum Board System"

    }


    st.session_state.model["cost"]=calculate_cost(
        area
    )


    st.success(
        "RANDOM generated building model"
    )



# ============================================================
# DASHBOARD
# ============================================================

c1,c2,c3=st.columns(3)


with c1:

    st.markdown(
    f"""
    <div class="card">

    🏠 Spaces

    <h2>
    {len(st.session_state.model["rooms"])}
    </h2>

    </div>
    """,
    unsafe_allow_html=True
    )


with c2:

    st.markdown(
    f"""
    <div class="card">

    📐 Grid Points

    <h2>
    {len(st.session_state.model["grid"])}
    </h2>

    </div>
    """,
    unsafe_allow_html=True
    )


with c3:

    st.markdown(
    """
    <div class="card">

    🧱 BIM Status

    <h2>
    Active
    </h2>

    </div>
    """,
    unsafe_allow_html=True
    )



# ============================================================
# OUTPUTS
# ============================================================

tab1,tab2,tab3,tab4=st.tabs(
[
"🏠 Spaces",
"📐 Grid",
"🏗 Structure",
"💰 Cost"
]
)



with tab1:

    st.json(
        st.session_state.model["rooms"]
    )



with tab2:

    st.write(
        "Grid spacing:",
        grid_spacing,
        "m"
    )

    st.json(
        st.session_state.model["grid"]
    )



with tab3:

    st.json(
        st.session_state.model["structure"]
    )



with tab4:

    st.json(
        st.session_state.model["cost"]
    )



# ============================================================
# FOOTER
# ============================================================

st.caption(
"RANDOM V52 Hybrid Architecture Engine | AI + BIM Foundation"
)
