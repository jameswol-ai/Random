# ============================================================
# RANDOM AI BIM STUDIO V56
# Parametric Architecture + BIM Intelligence Engine
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import uuid
import json
import re

from dataclasses import dataclass, field, asdict
from datetime import datetime


# ============================================================
# OPTIONAL LIBRARIES
# ============================================================

try:
    import plotly.graph_objects as go
    PLOTLY = True
except:
    PLOTLY = False


try:
    import pyvista as pv
    from stpyvista import stpyvista
    PVISTA = True
except:
    PVISTA = False



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

font-size:48px;
font-weight:900;

}


.subtitle{

color:#aab7d8;

}


.card{

background:#11182d;

padding:20px;

border-radius:18px;

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
class Space:

    id:str

    name:str

    area:float

    x:float

    y:float

    width:float

    depth:float

    height:float=3



@dataclass
class Wall:

    id:str

    x1:float

    y1:float

    x2:float

    y2:float

    thickness:float=0.2

    height:float=3



@dataclass
class Opening:

    id:str

    type:str

    x:float

    y:float

    width:float

    height:float



@dataclass
class Column:

    id:str

    x:float

    y:float

    size:str="300x300"



@dataclass
class BIMProject:

    id:str=field(
        default_factory=lambda:
        str(uuid.uuid4())
    )

    created:str=field(
        default_factory=lambda:
        str(datetime.now())
    )

    name:str="AI Residence"

    spaces:list=field(default_factory=list)

    walls:list=field(default_factory=list)

    openings:list=field(default_factory=list)

    columns:list=field(default_factory=list)

    cost:dict=field(default_factory=dict)





# ============================================================
# AI ARCHITECT
# ============================================================


def analyse_brief(text):

    text=text.lower()


    bedrooms=3

    bathrooms=2


    b=re.search(
        r"(\d+)\s*bedroom",
        text
    )


    if b:
        bedrooms=int(b.group(1))


    b=re.search(
        r"(\d+)\s*bathroom",
        text
    )


    if b:
        bathrooms=int(b.group(1))


    features=[]


    for key in [
        "courtyard",
        "solar",
        "pool",
        "garage"
    ]:

        if key in text:
            features.append(key)



    return {

        "bedrooms":bedrooms,

        "bathrooms":bathrooms,

        "features":features

    }




# ============================================================
# BIM GENERATOR
# ============================================================


def generate_spaces(config):

    rooms=[]


    rooms.append(

        Space(
            "RM001",
            "Living Room",
            35,
            0,
            0,
            7,
            5
        )

    )


    rooms.append(

        Space(
            "RM002",
            "Kitchen",
            18,
            7,
            0,
            4,
            4
        )

    )


    rooms.append(

        Space(
            "RM003",
            "Dining",
            16,
            7,
            4,
            4,
            4
        )

    )


    for i in range(
        config["bedrooms"]
    ):

        rooms.append(

            Space(

                f"RM{i+4}",

                f"Bedroom {i+1}",

                16,

                (i%3)*4,

                10+(i//3)*4,

                4,

                4

            )

        )


    return rooms




def generate_walls(spaces):

    walls=[]

    count=1


    for r in spaces:


        walls.append(

            Wall(

                f"W{count}",

                r.x,

                r.y,

                r.x+r.width,

                r.y

            )

        )


        walls.append(

            Wall(

                f"W{count+1}",

                r.x+r.width,

                r.y,

                r.x+r.width,

                r.y+r.depth

            )

        )


        count+=2


    return walls




def generate_columns():

    columns=[]


    for x in range(5):

        for y in range(5):

            columns.append(

                Column(

                    f"C{x}{y}",

                    x*5,

                    y*5

                )

            )


    return columns




def generate_openings():

    return [

        Opening(
            "D001",
            "Door",
            2,
            0,
            1.2,
            2.4
        ),

        Opening(
            "WIN001",
            "Window",
            5,
            5,
            1.5,
            1.2
        )

    ]





# ============================================================
# COST
# ============================================================


def calculate_cost(project):

    area=sum(
        x.area
        for x in project.spaces
    )


    return {

        "Floor Area m2":
        round(area,2),

        "Concrete m3":
        round(area*0.25,2),

        "Steel tonnes":
        round(area*0.04,2),

        "Estimated USD":
        round(area*700,2)

    }





# ============================================================
# SESSION
# ============================================================


if "project" not in st.session_state:

    st.session_state.project=BIMProject()



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

AI Architecture • BIM Intelligence • Parametric Design

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

        "Building Brief",

"""
Luxury tropical villa,
4 bedroom,
courtyard,
solar roof
"""

    )


    if st.button(
        "🚀 Generate BIM"
    ):


        config=analyse_brief(
            brief
        )


        project.spaces=generate_spaces(
            config
        )


        project.walls=generate_walls(
            project.spaces
        )


        project.columns=generate_columns()


        project.openings=generate_openings()


        project.cost=calculate_cost(
            project
        )


        st.success(
            "BIM Generated"
        )





# ============================================================
# METRICS
# ============================================================


c1,c2,c3,c4=st.columns(4)


for col,title,value in [

(c1,"ROOMS",len(project.spaces)),

(c2,"WALLS",len(project.walls)),

(c3,"COLUMNS",len(project.columns)),

(c4,"AREA",
sum(x.area for x in project.spaces))

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
# TABS
# ============================================================


tabs=st.tabs(

[
"📐 Floor Plan",
"🏢 3D BIM",
"🧱 Objects",
"💰 Cost",
"📦 Export"

]

)



# ============================================================
# FLOOR PLAN
# ============================================================


with tabs[0]:


    if PLOTLY:


        fig=go.Figure()


        for w in project.walls:


            fig.add_shape(

                type="line",

                x0=w.x1,

                y0=w.y1,

                x1=w.x2,

                y1=w.y2,

                line=dict(width=5)

            )


        for r in project.spaces:


            fig.add_annotation(

                x=r.x+r.width/2,

                y=r.y+r.depth/2,

                text=r.name,

                showarrow=False

            )


        st.plotly_chart(
            fig,
            use_container_width=True
        )




# ============================================================
# 3D VIEWER
# ============================================================


with tabs[1]:


    st.subheader(
        "3D BIM Preview"
    )


    if PVISTA:


        plotter=pv.Plotter()


        for w in project.walls:


            length=((w.x2-w.x1)**2+
                    (w.y2-w.y1)**2)**0.5


            mesh=pv.Box(

                bounds=(

                0,

                length,

                0,

                w.thickness,

                0,

                w.height

                )

            )


            plotter.add_mesh(mesh)



        plotter.camera_position="iso"


        stpyvista(
            plotter,
            height=600
        )


    else:

        st.info(
            "Install pyvista and stpyvista for 3D"
        )





# ============================================================
# BIM OBJECTS
# ============================================================


with tabs[2]:


    st.json(

        {

        "Spaces":
        [
            asdict(x)
            for x in project.spaces
        ],

        "Walls":
        [
            asdict(x)
            for x in project.walls
        ],

        "Columns":
        [
            asdict(x)
            for x in project.columns
        ]

        }

    )




# ============================================================
# COST
# ============================================================


with tabs[3]:


    for k,v in project.cost.items():

        st.metric(
            k,
            v
        )




# ============================================================
# EXPORT
# ============================================================


with tabs[4]:


    data=json.dumps(

        asdict(project),

        indent=2

    )


    st.download_button(

        "📦 Download BIM JSON",

        data,

        "random_bim.json"

    )


    st.info(

"""
IFC Export Framework Ready

Future integration:
- ifcopenshell
- Revit
- Archicad
- Blender BIM

"""

    )



st.caption(
"RANDOM AI BIM STUDIO V56 | Parametric Architecture Intelligence"
)
