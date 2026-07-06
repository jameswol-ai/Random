# ============================================================
# RANDOM AI BIM STUDIO V56
# Parametric Architecture + BIM Intelligence Engine
#
# streamlit_app.py
# ============================================================

import streamlit as st
import uuid
import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime


# ============================================================
# OPTIONAL VISUALIZATION
# ============================================================

try:
    import plotly.graph_objects as go
    PLOTLY = True
except Exception:
    PLOTLY = False



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM AI BIM Studio V56",
    page_icon="🏛️",
    layout="wide"
)



# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

.main{
background:#070b18;
}

.hero{

background:
linear-gradient(
135deg,
#111936,
#070b18
);

padding:35px;
border-radius:25px;
border:1px solid #263252;

}


.logo{

font-size:45px;
font-weight:900;

}


.subtitle{

color:#aab7d8;
font-size:18px;

}


.card{

background:#11182d;
padding:20px;
border-radius:20px;
border:1px solid #263252;

}


.metric{

font-size:35px;
font-weight:900;
color:#8ea2ff;

}

</style>

""",
unsafe_allow_html=True)



# ============================================================
# BIM DATA MODEL
# ============================================================


@dataclass
class Room:

    name:str
    width:float
    depth:float
    x:float
    y:float


    def area(self):

        return round(
            self.width*self.depth,
            2
        )



@dataclass
class Wall:

    id:str
    x1:float
    y1:float
    x2:float
    y2:float
    height:float=3



@dataclass
class Opening:

    id:str
    type:str
    width:float
    height:float
    x:float
    y:float



@dataclass
class BIMProject:


    name:str

    id:str=field(
        default_factory=lambda:
        str(uuid.uuid4())
    )


    created:str=field(
        default_factory=lambda:
        str(datetime.now())
    )


    rooms:list=field(
        default_factory=list
    )

    walls:list=field(
        default_factory=list
    )

    openings:list=field(
        default_factory=list
    )

    cost:dict=field(
        default_factory=dict
    )



# ============================================================
# AI ARCHITECT ASSISTANT
# ============================================================


def interpret_brief(text):

    text=text.lower()


    bedrooms=3

    bathrooms=2


    match=re.search(
        r"(\d+)\s*bedroom",
        text
    )


    if match:

        bedrooms=int(
            match.group(1)
        )


    match=re.search(
        r"(\d+)\s*bathroom",
        text
    )


    if match:

        bathrooms=int(
            match.group(1)
        )


    return {

        "bedrooms":bedrooms,

        "bathrooms":bathrooms,

        "courtyard":
        "courtyard" in text,

        "luxury":
        "luxury" in text,

        "solar":
        "solar" in text

    }



# ============================================================
# BIM GENERATOR
# ============================================================


def create_rooms(config):


    rooms=[]


    rooms.append(

        Room(
            "Living Room",
            7,
            5,
            0,
            0
        )

    )


    rooms.append(

        Room(
            "Kitchen",
            4,
            4,
            7,
            0
        )

    )


    rooms.append(

        Room(
            "Dining",
            4,
            4,
            7,
            4
        )

    )


    for i in range(
        config["bedrooms"]
    ):

        rooms.append(

            Room(

                f"Bedroom {i+1}",

                4,

                4,

                (i%3)*4,

                10+(i//3)*4

            )

        )


    return rooms



def create_walls(rooms):

    walls=[]

    count=1


    for r in rooms:


        walls.extend([


        Wall(
            f"W{count}",
            r.x,
            r.y,
            r.x+r.width,
            r.y
        ),


        Wall(
            f"W{count+1}",
            r.x+r.width,
            r.y,
            r.x+r.width,
            r.y+r.depth
        ),


        Wall(
            f"W{count+2}",
            r.x+r.width,
            r.y+r.depth,
            r.x,
            r.y+r.depth
        ),


        Wall(
            f"W{count+3}",
            r.x,
            r.y+r.depth,
            r.x,
            r.y
        )

        ])


        count+=4


    return walls



def create_openings():

    return [

        Opening(
            "D001",
            "Door",
            1,
            2.1,
            2,
            0
        ),

        Opening(
            "WIN001",
            "Window",
            1.5,
            1.2,
            5,
            5
        )

    ]



# ============================================================
# COST ENGINE
# ============================================================


def calculate_cost(project):


    area=sum(
        r.area()
        for r in project.rooms
    )


    return {

        "Floor Area m2":
        round(area,2),

        "Concrete m3":
        round(area*0.25,2),

        "Steel Tonnes":
        round(area*0.04,2),

        "Estimated USD":
        round(area*700,2)

    }



# ============================================================
# SESSION
# ============================================================


if "project" not in st.session_state:

    st.session_state.project = BIMProject(
        "AI Residence"
    )


project=st.session_state.project



# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<div class="logo">
🏛️ RANDOM AI BIM STUDIO V56
</div>

<div class="subtitle">
AI Architecture • Parametric BIM • Digital Construction
</div>

</div>

""",
unsafe_allow_html=True)



# ============================================================
# SIDEBAR
# ============================================================


with st.sidebar:


    st.header(
        "🤖 AI Architect"
    )


    project.name=st.text_input(
        "Project Name",
        project.name
    )


    brief=st.text_area(

        "Design Brief",

"""
Luxury tropical modern villa,
4 bedroom,
courtyard,
solar roof
"""

    )


    if st.button(
        "🚀 Generate BIM Model"
    ):


        config=interpret_brief(
            brief
        )


        project.rooms=create_rooms(
            config
        )


        project.walls=create_walls(
            project.rooms
        )


        project.openings=create_openings()


        project.cost=calculate_cost(
            project
        )


        st.success(
            "BIM Generated"
        )


    st.divider()


    st.download_button(

        "📦 Export BIM JSON",

        json.dumps(
            asdict(project),
            indent=2
        ),

        "random_bim.json"

    )


# ============================================================
# METRICS
# ============================================================


c1,c2,c3,c4=st.columns(4)


data=[

(c1,"Rooms",len(project.rooms)),

(c2,"Walls",len(project.walls)),

(c3,"Openings",len(project.openings)),

(c4,"Area",
sum(r.area() for r in project.rooms))

]


for col,title,value in data:

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
# FLOOR PLAN
# ============================================================


st.subheader(
"📐 AI Generated Floor Plan"
)


if PLOTLY:


    fig=go.Figure()


    for wall in project.walls:


        fig.add_shape(

            type="line",

            x0=wall.x1,

            y0=wall.y1,

            x1=wall.x2,

            y1=wall.y2,

            line=dict(
                width=5
            )

        )


    for room in project.rooms:


        fig.add_annotation(

            x=room.x+room.width/2,

            y=room.y+room.depth/2,

            text=room.name,

            showarrow=False

        )


    fig.update_layout(

        height=650,

        title="RANDOM AI Parametric Plan"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


else:

    st.warning(
        "Install plotly for visualization"
    )



# ============================================================
# BIM TREE
# ============================================================


tab1,tab2,tab3=st.tabs(
[
"🧱 BIM Objects",
"💰 Cost",
"🤖 AI Notes"
]
)


with tab1:

    st.json(
        asdict(project)
    )



with tab2:

    for k,v in project.cost.items():

        st.metric(
            k,
            v
        )



with tab3:


    st.info(

"""
AI Recommendations

• Improve daylight orientation
• Add passive ventilation
• Optimize structural grid
• Reserve roof for solar panels

Architecture engine ready for IFC integration.

"""

    )



st.caption(
"RANDOM AI BIM STUDIO V56 | Parametric Architecture Intelligence"
)
