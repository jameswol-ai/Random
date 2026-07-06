# ============================================================
# RANDOM V53 AI BUILDER
# Parametric Architecture + BIM Core
#
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import uuid
from datetime import datetime

try:
    import plotly.graph_objects as go
    PLOTLY = True
except:
    PLOTLY = False


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM AI Builder",
    page_icon="🏛️",
    layout="wide"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
"""
<style>

.main {
background:#070b18;
}

.hero {

background:#111a33;
padding:30px;
border-radius:25px;
border:1px solid #27304d;

}

.logo {

font-size:50px;
font-weight:900;

}

.subtitle {

color:#a8b4d8;

}

.card {

background:#11182d;
padding:20px;
border-radius:18px;
border:1px solid #27304d;

}

.big {

font-size:32px;
font-weight:800;
color:#8fa7ff;

}


.stButton button {

border-radius:15px;
height:45px;

background:#4155ff;
color:white;

font-weight:bold;

}

</style>

""",
unsafe_allow_html=True
)



# ============================================================
# BUILDING DATABASE
# ============================================================

if "model" not in st.session_state:

    st.session_state.model = {

        "id":str(uuid.uuid4()),

        "created":str(datetime.now()),

        "spaces":[],
        "walls":[],
        "doors":[],
        "windows":[],
        "grid":[],
        "structure":{},
        "roof":{},
        "foundation":{},
        "cost":{}

    }



# ============================================================
# GENERATORS
# ============================================================

def generate_spaces(bedrooms,bathrooms):

    spaces=[]

    base=[

        ("Living Room",30),
        ("Kitchen",15),
        ("Dining",15),
        ("Corridor",12),
        ("Laundry",8),
        ("Balcony",10)

    ]

    for name,area in base:

        spaces.append(
            {
            "name":name,
            "area":area
            }
        )


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



def generate_openings():

    return {

    "doors":[

        {
        "id":"D01",
        "size":"900x2100mm"
        }

    ],

    "windows":[

        {
        "id":"WIN01",
        "size":"1500x1200mm"
        }

    ]

    }



def generate_grid(spacing):

    grid=[]

    for x in range(6):

        for y in range(6):

            grid.append(

            {
            "axis_x":x*spacing,
            "axis_y":y*spacing
            }

            )

    return grid



def generate_structure():

    return {

    "columns":
    "300x300mm RC Columns",

    "beams":
    "250x450mm RC Beams",

    "slab":
    "150mm Reinforced Concrete Slab"

    }



def calculate_cost(area):

    return {

    "Area":
    f"{area} m²",

    "Concrete":
    f"{round(area*0.25,2)} m³",

    "Steel":
    f"{round(area*0.04,2)} tonnes",

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
🏛️ RANDOM AI BUILDER
</div>

<div class="subtitle">

Parametric Architecture • BIM • Structural Intelligence

</div>

</div>

""",

unsafe_allow_html=True

)



# ============================================================
# CONTROL PANEL
# ============================================================

with st.sidebar:

    st.header("🏠 Building Generator")


    bedrooms=st.slider(
        "Bedrooms",
        1,10,4
    )

    bathrooms=st.slider(
        "Bathrooms",
        1,8,3
    )

    floors=st.number_input(
        "Floors",
        1,
        5,
        2
    )


    spacing=st.selectbox(

        "Grid Spacing",

        [
        1,
        1.5,
        3
        ]

    )


    generate=st.button(
        "🚀 GENERATE BIM HOUSE"
    )


if generate:

    spaces=generate_spaces(
        bedrooms,
        bathrooms
    )

    st.session_state.model["spaces"]=spaces

    st.session_state.model["walls"]=generate_walls()

    openings=generate_openings()

    st.session_state.model["doors"]=openings["doors"]

    st.session_state.model["windows"]=openings["windows"]

    st.session_state.model["grid"]=generate_grid(
        spacing
    )

    st.session_state.model["structure"]=generate_structure()


    st.session_state.model["foundation"]={

        "type":
        "Pad Foundation",

        "depth":
        "1200mm"

    }


    st.session_state.model["roof"]={

        "type":
        "Pitched Roof",

        "pitch":
        "30 degrees"

    }


    area=sum(
        x["area"]
        for x in spaces
    )


    st.session_state.model["cost"]=calculate_cost(area)


    st.success(
        "RANDOM AI created BIM model"
    )



# ============================================================
# DASHBOARD
# ============================================================

spaces=len(
st.session_state.model["spaces"]
)

objects=(

len(st.session_state.model["walls"])

+

len(st.session_state.model["doors"])

+

len(st.session_state.model["windows"])

)



a,b,c,d=st.columns(4)


for col,title,value in [

(a,"SPACES",spaces),

(b,"BIM OBJECTS",objects),

(c,"GRID",len(st.session_state.model["grid"])),

(d,"ENGINE","ONLINE")

]:

    col.markdown(

    f"""

    <div class="card">

    <h3>{title}</h3>

    <div class="big">
    {value}
    </div>

    </div>

    """,

    unsafe_allow_html=True

    )



# ============================================================
# OUTPUTS
# ============================================================

tab1,tab2,tab3,tab4,tab5=st.tabs(

[
"🏠 Architecture",
"📐 Grid",
"🧱 BIM",
"🏗 Structure",
"💰 Cost"
]

)



with tab1:

    st.json(
        st.session_state.model["spaces"]
    )


    if PLOTLY:

        fig=go.Figure()


        for i,room in enumerate(
            st.session_state.model["spaces"]
        ):

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
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



with tab2:

    st.json(
        st.session_state.model["grid"]
    )



with tab3:

    st.write("Walls")

    st.json(
        st.session_state.model["walls"]
    )

    st.write("Doors")

    st.json(
        st.session_state.model["doors"]
    )

    st.write("Windows")

    st.json(
        st.session_state.model["windows"]
    )



with tab4:

    st.json(
        st.session_state.model["structure"]
    )

    st.json(
        st.session_state.model["foundation"]
    )

    st.json(
        st.session_state.model["roof"]
    )



with tab5:

    st.json(
        st.session_state.model["cost"]
    )



st.caption(
"RANDOM V53 AI BUILDER | Parametric Architecture Intelligence"
)
