# ============================================================
# RANDOM AI BIM STUDIO V56
# Parametric Architecture + BIM Intelligence Engine
#
# streamlit_app.py
#
# Single File Edition
# ============================================================

import streamlit as st
import uuid
import json
import math
from dataclasses import dataclass, asdict, field
from datetime import datetime


# ============================================================
# OPTIONAL LIBRARIES
# ============================================================

try:
    import plotly.graph_objects as go
    PLOTLY = True
except Exception:
    PLOTLY = False


try:
    import pyvista as pv
    PYVISTA = True
except Exception:
    PYVISTA = False



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RANDOM AI BIM Studio V56",
    page_icon="🏛️",
    layout="wide"
)



# ============================================================
# STYLE SYSTEM
# ============================================================

st.markdown("""

<style>

body{
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

font-size:20px;

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

""", unsafe_allow_html=True)



# ============================================================
# BIM DATA MODEL
# ============================================================


@dataclass
class BIMRoom:

    name:str

    width:float

    depth:float

    x:float

    y:float


    @property
    def area(self):

        return round(
            self.width*self.depth,
            2
        )



@dataclass
class BIMWall:

    id:str

    x1:float

    y1:float

    x2:float

    y2:float

    height:float=3.0

    thickness:float=0.2



@dataclass
class BIMOpening:

    id:str

    type:str

    x:float

    y:float

    width:float

    height:float



@dataclass
class BIMProject:


    name:str

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


    levels:list=field(
        default_factory=lambda:
        [
            {
            "name":"Ground Floor",
            "height":3
            }
        ]
    )


    materials:dict=field(
        default_factory=dict
    )


    cost:dict=field(
        default_factory=dict
    )


    id:str=field(
        default_factory=lambda:
        str(uuid.uuid4())
    )



# ============================================================
# AI BRIEF GENERATOR
# ============================================================


def analyze_brief(text):

    text=text.lower()


    bedrooms=3

    bathrooms=2


    if "4 bedroom" in text:
        bedrooms=4

    elif "5 bedroom" in text:
        bedrooms=5


    if "luxury" in text:

        size_multiplier=1.4

    else:

        size_multiplier=1


    return {

        "bedrooms":bedrooms,

        "bathrooms":bathrooms,

        "size_multiplier":
        size_multiplier

    }



# ============================================================
# PARAMETRIC ARCHITECTURE GENERATOR
# ============================================================


def generate_rooms(parameters):


    rooms=[]


    scale=parameters["size_multiplier"]


    rooms.append(

        BIMRoom(
            "Living Room",
            7*scale,
            5*scale,
            0,
            0
        )

    )


    rooms.append(

        BIMRoom(
            "Kitchen",
            4*scale,
            4*scale,
            7*scale,
            0
        )

    )


    rooms.append(

        BIMRoom(
            "Dining",
            4*scale,
            4*scale,
            7*scale,
            4*scale
        )

    )


    for i in range(parameters["bedrooms"]):

        rooms.append(

            BIMRoom(

                f"Bedroom {i+1}",

                4*scale,

                4*scale,

                (i%2)*4*scale,

                7*scale+(i//2)*4*scale

            )

        )


    return rooms



def generate_walls(rooms):

    walls=[]

    counter=1


    for room in rooms:

        x=room.x

        y=room.y


        walls.extend(

        [

        BIMWall(
            f"W{counter}",
            x,
            y,
            x+room.width,
            y
        ),

        BIMWall(
            f"W{counter+1}",
            x+room.width,
            y,
            x+room.width,
            y+room.depth
        ),

        BIMWall(
            f"W{counter+2}",
            x+room.width,
            y+room.depth,
            x,
            y+room.depth
        ),

        BIMWall(
            f"W{counter+3}",
            x,
            y+room.depth,
            x,
            y
        )

        ]

        )


        counter+=4


    return walls



def generate_openings():

    return [

        BIMOpening(
            "D001",
            "Door",
            2,
            0,
            1,
            2.1
        ),

        BIMOpening(
            "WIN001",
            "Window",
            5,
            5,
            1.5,
            1.2
        )

    ]



# ============================================================
# COST ENGINE
# ============================================================


def calculate_cost(project):


    area=sum(
        room.area
        for room in project.rooms
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
