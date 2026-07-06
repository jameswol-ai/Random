# ============================================================
# RANDOM V52.2 AI ARCHITECTURE STUDIO
#
# Hybrid Architecture + BIM Intelligence Engine
# Streamlit Edition
# ============================================================

import streamlit as st
import uuid
from datetime import datetime


# ============================================================
# OPTIONAL VISUALIZATION
# ============================================================

try:
    import plotly.graph_objects as go
    PLOTLY = True
except:
    PLOTLY = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM AI Studio",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# VISUAL DESIGN SYSTEM
# ============================================================

st.markdown(
"""
<style>

body {
background:#070b18;
}

.main {
background:#070b18;
}


/* Header */

.hero {

background:
linear-gradient(
135deg,
#111a33,
#0b1020
);

padding:35px;
border-radius:25px;

border:
1px solid #27304d;

margin-bottom:25px;

}


.logo {

font-size:55px;
font-weight:900;

background:
linear-gradient(
90deg,
#ffffff,
#8fa7ff
);

-webkit-background-clip:text;
color:transparent;

}


.tagline {

color:#aab4d6;
font-size:20px;

}



/* Cards */

.card {

background:#11182d;

padding:20px;

border-radius:20px;

border:
1px solid #27304d;

height:130px;

}


.card h3 {

color:#ffffff;

}


.value {

font-size:35px;

font-weight:800;

color:#8fa7ff;

}



/* Buttons */

.stButton button {

width:100%;

height:45px;

border-radius:15px;

background:
linear-gradient(
90deg,
#344cff,
#6677ff
);

color:white;

font-weight:700;

border:none;

}


.stButton button:hover {

transform:scale(1.02);

}



/* Tabs */

.stTabs [data-baseweb="tab"] {

font-size:16px;

font-weight:700;

}



</style>

""",
unsafe_allow_html=True
)



# ============================================================
# SESSION MODEL
# ============================================================

if "building" not in st.session_state:

    st.session_state.building = {

        "id":str(uuid.uuid4()),

        "date":str(datetime.now()),

        "rooms":[],

        "grid":[],

        "structure":{},

        "cost":{}

    }



# ============================================================
# ENGINES
# ============================================================

def create_spaces(bedrooms,bathrooms):

    spaces=[

        ("Living Room",35),

        ("Kitchen",18),

        ("Dining",18),

        ("Entrance Hall",8),

        ("Corridor",12),

        ("Balcony",10),

        ("Laundry",8)

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
        "name":x[0],
        "area":x[1]
        }

        for x in spaces

    ]



def create_grid(spacing):

    points=[]

    for x in range(0,6):

        for y in range(0,6):

            points.append(

                {
                "grid_x":x*spacing,
                "grid_y":y*spacing
                }

            )

    return points



def cost_engine(area):

    return {

    "Floor Area":f"{area} m²",

    "Concrete":
    f"{round(area*0.25,2)} m³",

    "Steel":
    f"{round(area*0.035,2)} tonnes",

    "Flooring":
    f"{area} m²",

    "Estimated Cost":
    f"${area*550:,.0f}"

    }




# ============================================================
# HERO
# ============================================================

st.markdown(
"""

<div class="hero">

<div class="logo">
🏛️ RANDOM AI
</div>

<div class="tagline">

Architecture Intelligence Studio  
<br>
AI Design • BIM • Cost • Documentation

</div>

</div>

""",
unsafe_allow_html=True
)



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Architecture_icon.svg/512px-Architecture_icon.svg.png",
        width=120
    )


    st.header("🏠 Design Controls")


    bedrooms=st.slider(
        "Bedrooms",
        1,10,4
    )


    bathrooms=st.slider(
        "Bathrooms",
        1,8,3
    )


    floors=st.slider(
        "Floors",
        1,5,2
    )


    grid=st.selectbox(

        "Structural Grid",

        [
        1,
        1.5,
        3
        ]

    )


    if st.button(
        "🚀 GENERATE BUILDING"
    ):


        rooms=create_spaces(
            bedrooms,
            bathrooms
        )


        area=sum(
            r["area"]
            for r in rooms
        )


        st.session_state.building["rooms"]=rooms

        st.session_state.building["grid"]=create_grid(grid)


        st.session_state.building["structure"]={

            "Columns":
            "300x300 mm RC",

            "Beams":
            "250x450 mm RC",

            "Foundation":
            "Pad Foundation",

            "Roof":
            "30° Pitch Roof",

            "Ceiling":
            "Gypsum Ceiling"

        }


        st.session_state.building["cost"]=cost_engine(area)


        st.success(
            "Building Generated"
        )



# ============================================================
# DASHBOARD
# ============================================================

rooms=len(
    st.session_state.building["rooms"]
)


gridpoints=len(
    st.session_state.building["grid"]
)



a,b,c,d=st.columns(4)


for col,title,value in [

(a,"ROOMS",rooms),

(b,"GRID POINTS",gridpoints),

(c,"BIM OBJECTS",rooms*4),

(d,"STATUS","READY")

]:


    col.markdown(

    f"""

    <div class="card">

    <h3>{title}</h3>

    <div class="value">
    {value}
    </div>

    </div>

    """,

    unsafe_allow_html=True

    )



# ============================================================
# TABS
# ============================================================

tab1,tab2,tab3,tab4=st.tabs(

[
"🏠 Floor Plan",
"📐 Grid",
"🏗 BIM",
"💰 Cost"
]

)



with tab1:

    st.subheader(
        "Generated Spaces"
    )


    st.json(
        st.session_state.building["rooms"]
    )



    if PLOTLY:

        fig=go.Figure()


        for i,r in enumerate(
            st.session_state.building["rooms"]
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

                text=r["name"]

            )


        fig.update_layout(
            height=500,
            showlegend=False
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



with tab2:

    st.subheader(
        "Structural Grid System"
    )

    st.json(
        st.session_state.building["grid"]
    )



with tab3:

    st.subheader(
        "BIM Intelligence"
    )


    st.json(
        st.session_state.building["structure"]
    )



with tab4:

    st.subheader(
        "Cost Intelligence"
    )


    st.json(
        st.session_state.building["cost"]
    )



# ============================================================
# FOOTER
# ============================================================

st.caption(
"RANDOM V52.2 | AI Architecture Operating System"
)
