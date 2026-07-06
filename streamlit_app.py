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

# ============================================================
# SIDEBAR CONTROL PANEL
# ============================================================

with st.sidebar:

    st.header("🏗️ BIM GENERATOR")


    project_name = st.text_input(
        "Project Name",
        "AI Residence"
    )


    bedrooms = st.slider(
        "Bedrooms",
        1,
        12,
        4
    )


    bathrooms = st.slider(
        "Bathrooms",
        1,
        10,
        3
    )


    floors = st.slider(
        "Number of Floors",
        1,
        5,
        2
    )


    units = st.selectbox(
        "Unit System",
        [
            "Metric",
            "Imperial"
        ]
    )


    grid_spacing = st.selectbox(
        "Structural Grid Spacing",
        [
            1,
            1.5,
            3
        ]
    )


    generate = st.button(
        "🚀 GENERATE BIM HOUSE"
    )



# ============================================================
# BUILDING GENERATION
# ============================================================

if generate:


    spaces = create_spaces(
        bedrooms,
        bathrooms
    )


    area = sum(
        x["area"]
        for x in spaces
    )


    opening_data = create_openings()


    st.session_state.bim.update(

    {


    "project":
    project_name,


    "units":
    units,


    "levels":

    [

        {
        "level":"Ground Floor",
        "height":"3000mm"
        },

        {
        "level":"First Floor",
        "height":"3000mm"
        }

    ][:floors],


    "spaces":
    spaces,


    "walls":
    create_walls(),


    "doors":
    opening_data["doors"],


    "windows":
    opening_data["windows"],


    "grid":
    create_grid(
        grid_spacing
    ),


    "columns":
    create_structure()["columns"],


    "beams":
    create_structure()["beams"],


    "foundation":

    {

    "system":
    "Reinforced Concrete Pad Foundation",

    "depth":
    "1200mm",

    "material":
    "Concrete C25"

    },


    "roof":

    {

    "type":
    "Pitched Roof",

    "pitch":
    "30 degrees",

    "covering":
    "Metal Roofing"

    },


    "cost":

    {

    "Floor Area":
    f"{area} m²",

    "Concrete":
    f"{area*0.25:.2f} m³",

    "Steel":
    f"{area*0.04:.2f} tonnes",

    "Estimated Cost":
    f"${area*650:,.0f}"

    }

    }


    )


    st.success(
        "🏛️ RANDOM AI created BIM model"
    )



# ============================================================
# DASHBOARD METRICS
# ============================================================

bim = st.session_state.bim


a,b,c,d = st.columns(4)


metrics = [

    (
    a,
    "ROOMS",
    len(bim["spaces"])
    ),

    (
    b,
    "WALLS",
    len(bim["walls"])
    ),

    (
    c,
    "OPENINGS",
    len(bim["doors"])
    +
    len(bim["windows"])
    ),

    (
    d,
    "GRID",
    len(bim["grid"])
    )

]


for col,title,value in metrics:

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
# BIM VIEWER TABS
# ============================================================

tabs = st.tabs(

[
"📐 Floor Plan",
"🏠 Elevation",
"✂️ Section",
"🧱 BIM Objects",
"📊 Reports"

]

)



# ============================================================
# FLOOR PLAN VIEW
# ============================================================

with tabs[0]:


    st.subheader(
        "Architectural Floor Plan"
    )


    if PLOTLY:


        fig = go.Figure()


        # Walls

        for wall in bim["walls"]:


            fig.add_shape(

                type="line",

                x0=wall["start"][0],

                y0=wall["start"][1],

                x1=wall["end"][0],

                y1=wall["end"][1],

                line=dict(width=8)

            )


        # Grid

        for point in bim["grid"]:


            fig.add_annotation(

                x=point["x"],

                y=point["y"],

                text=point["axis"],

                showarrow=False

            )


        fig.update_layout(

            height=600,

            showlegend=False,

            xaxis_title="Meters",

            yaxis_title="Meters"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:

        st.info(
            "Install plotly for drawing visualization"
        )



# ============================================================
# ELEVATION
# ============================================================

with tabs[1]:

    st.subheader(
        "Front Elevation"
    )


    st.json(

    {

    "Levels":
    len(bim["levels"]),

    "Floor Height":
    "3000mm",

    "Roof":
    bim["roof"]

    }

    )



# ============================================================
# SECTION
# ============================================================

with tabs[2]:

    st.subheader(
        "Building Section"
    )


    st.json(

    {

    "Foundation":
    bim["foundation"],

    "Slab":
    "150mm RC",

    "Ceiling":
    "Gypsum System",

    "Roof":
    bim["roof"]

    }

    )



# ============================================================
# BIM OBJECT DATABASE
# ============================================================

with tabs[3]:


    st.subheader(
        "BIM Object Tree"
    )


    st.json(

    {

    "Spaces":
    bim["spaces"],

    "Walls":
    bim["walls"],

    "Doors":
    bim["doors"],

    "Windows":
    bim["windows"],

    "Columns":
    bim["columns"],

    "Beams":
    bim["beams"]

    }

    )

# ============================================================
# IMPERIAL CONVERSION ENGINE
# ============================================================

def meters_to_feet_inches(meters):

    total_inches = meters * 39.3701

    feet = int(total_inches // 12)

    inches = round(total_inches % 12, 1)

    return f"{feet}'-{inches}\""



def mm_to_feet_inches(mm):

    inches = mm / 25.4

    feet = int(inches // 12)

    remaining_inches = round(inches % 12, 1)

    return f"{feet}'-{remaining_inches}\""
