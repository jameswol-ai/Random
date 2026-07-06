# ============================================================
# RANDOM V54 BIM VISUALIZATION STUDIO
#
# AI Architecture + BIM Intelligence Engine
#
# Streamlit Single File Edition
# ============================================================

import streamlit as st
import uuid
from datetime import datetime

try:
    import plotly.graph_objects as go
    PLOTLY = True
except Exception:
    PLOTLY = False


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM AI BIM Studio",
    page_icon="🏛️",
    layout="wide"
)


# ============================================================
# UI DESIGN
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
border:1px solid #27304d;

}

.logo {

font-size:55px;
font-weight:900;

}

.subtitle {

color:#aab6d8;
font-size:20px;

}


.card {

background:#11182d;
padding:20px;
border-radius:18px;
border:1px solid #27304d;

}


.metric {

font-size:35px;
font-weight:900;
color:#8fa7ff;

}


.stButton button {

background:#4255ff;
color:white;

height:45px;

border-radius:15px;

font-weight:bold;

width:100%;

}

</style>

""",
unsafe_allow_html=True
)



# ============================================================
# DATA MODEL
# ============================================================

if "project" not in st.session_state:

    st.session_state.project = {

        "id":str(uuid.uuid4()),

        "created":
        str(datetime.now()),

        "spaces":[],
        "walls":[],
        "doors":[],
        "windows":[],
        "columns":[],
        "beams":[],
        "grid":[],
        "foundation":{},
        "roof":{},
        "cost":{}

    }



# ============================================================
# GENERATORS
# ============================================================

def create_spaces(bedrooms,bathrooms):

    spaces=[

        ("Living Room",35),
        ("Kitchen",18),
        ("Dining",16),
        ("Corridor",12),
        ("Laundry",8),
        ("Balcony",10)

    ]

    for i in range(bedrooms):

        spaces.append(
            (
            f"Bedroom {i+1}",
            16
            )
        )


    for i in range(bathrooms):

        spaces.append(
            (
            f"Bathroom {i+1}",
            6
            )
        )


    return [

        {
        "name":n,
        "area":a
        }

        for n,a in spaces

    ]



def create_walls():

    return [

        {
        "id":"W01",
        "length":"6000mm",
        "height":"3000mm",
        "thickness":"200mm"
        },

        {
        "id":"W02",
        "length":"5000mm",
        "height":"3000mm",
        "thickness":"200mm"
        }

    ]



def create_doors():

    return [

        {
        "id":"D01",
        "type":"Internal Door",
        "size":"900x2100mm"
        },

        {
        "id":"D02",
        "type":"Entrance Door",
        "size":"1200x2400mm"
        }

    ]



def create_windows():

    return [

        {
        "id":"WIN01",
        "size":"1500x1200mm",
        "sill":"900mm"
        },

        {
        "id":"WIN02",
        "size":"1200x1200mm",
        "sill":"900mm"
        }

    ]



def create_grid(spacing):

    grid=[]

    letters=["A","B","C","D"]

    for row in letters:

        for number in range(1,5):

            grid.append(

            {
            "grid":
            f"{row}{number}",

            "spacing":
            spacing

            }

            )

    return grid



def create_structure():

    return {

    "Columns":
    "300x300mm Reinforced Concrete",

    "Beams":
    "250x450mm Reinforced Concrete",

    "Slab":
    "150mm Concrete Slab"

    }



def create_cost(area):

    return {

    "Floor Area":
    f"{area} m²",

    "Concrete":
    f"{area*0.25:.2f} m³",

    "Steel":
    f"{area*0.04:.2f} tonnes",

    "Flooring":
    f"{area} m²",

    "Estimated Cost":
    f"${area*600:,.0f}"

    }



# ============================================================
# HEADER
# ============================================================

st.markdown(

"""

<div class="hero">

<div class="logo">

🏛️ RANDOM AI BIM STUDIO

</div>

<div class="subtitle">

Architecture Intelligence • Parametric BIM • Automated Documentation

</div>

</div>

""",

unsafe_allow_html=True

)



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🏠 Building Parameters")


    project_name=st.text_input(
        "Project Name",
        "AI Residence"
    )


    bedrooms=st.slider(
        "Bedrooms",
        1,
        10,
        4
    )


    bathrooms=st.slider(
        "Bathrooms",
        1,
        8,
        3
    )


    floors=st.slider(
        "Floors",
        1,
        5,
        2
    )


    grid_spacing=st.selectbox(
        "Structural Grid",
        [
        1,
        1.5,
        3
        ]
    )


    generate=st.button(
        "🚀 GENERATE BIM MODEL"
    )



# ============================================================
# BUILD GENERATION
# ============================================================

if generate:


    spaces=create_spaces(
        bedrooms,
        bathrooms
    )


    area=sum(
        s["area"]
        for s in spaces
    )


    st.session_state.project.update(

    {

    "name":project_name,

    "spaces":spaces,

    "walls":create_walls(),

    "doors":create_doors(),

    "windows":create_windows(),

    "grid":create_grid(grid_spacing),

    "columns":
    ["A1","A2","B1","B2"],

    "beams":
    ["Beam B01","Beam B02"],

    "foundation":
    {
    "type":"Pad Foundation",
    "depth":"1200mm"
    },

    "roof":
    {
    "type":"Pitched Roof",
    "pitch":"30 degrees"
    },

    "cost":
    create_cost(area)

    }

    )

    st.success(
        "RANDOM BIM Model Generated"
    )



# ============================================================
# DASHBOARD
# ============================================================

p=st.session_state.project


c1,c2,c3,c4=st.columns(4)


for col,title,value in [

(c1,"Rooms",len(p["spaces"])),

(c2,"Walls",len(p["walls"])),

(c3,"Openings",
len(p["doors"])+len(p["windows"])),

(c4,"Grid Points",
len(p["grid"]))

]:

    col.markdown(

    f"""

<div class="card">

<h3>{title}</h3>

<div class="metric">
{value}
</div>

</div>

""",

unsafe_allow_html=True

)



# ============================================================
# OUTPUT TABS
# ============================================================

tabs=st.tabs(

[
"📐 Floor Plan",
"🏠 Elevation",
"✂️ Section",
"🧱 BIM",
"📊 Schedules",
"💰 Cost"

]

)



with tabs[0]:

    st.subheader(
        "Generated Floor Plan"
    )


    if PLOTLY:

        fig=go.Figure()


        for i,room in enumerate(p["spaces"]):

            fig.add_shape(

            type="rect",

            x0=i*5,
            y0=0,
            x1=i*5+4,
            y1=4

            )

            fig.add_annotation(

            x=i*5+2,
            y=2,
            text=room["name"]

            )


        fig.update_layout(
            height=500,
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



with tabs[1]:

    st.subheader(
        "Elevation Generator"
    )

    st.write(
        "Front elevation data"
    )

    st.json(

    {
    "Floors":floors,
    "Height":"3000mm/floor",
    "Roof":"30 degree pitch"

    }

    )



with tabs[2]:

    st.subheader(
        "Building Section"
    )

    st.json(

    {

    "Foundation depth":"1200mm",

    "Floor slab":"150mm",

    "Ceiling height":"3000mm"

    }

    )



with tabs[3]:

    st.subheader(
        "BIM Objects"
    )

    st.json(p)



with tabs[4]:

    st.subheader(
        "Schedules"
    )


    st.write("Room Schedule")

    st.json(
        p["spaces"]
    )


    st.write("Door Schedule")

    st.json(
        p["doors"]
    )


    st.write("Window Schedule")

    st.json(
        p["windows"]
    )



with tabs[5]:

    st.subheader(
        "Cost Intelligence"
    )

    st.json(
        p["cost"]
    )



st.caption(
"RANDOM V54 BIM VISUALIZATION STUDIO | AI Architecture Engine"
)
