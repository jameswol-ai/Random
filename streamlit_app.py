# ============================================================
# RANDOM V56.0 AI BIM STUDIO
# Parametric Architecture + BIM Intelligence Engine
#
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import uuid
import json
import re

from datetime import datetime
from dataclasses import dataclass, field, asdict


# ============================================================
# OPTIONAL VISUALIZATION
# ============================================================

try:
    import plotly.graph_objects as go
    PLOTLY = True

except Exception:
    PLOTLY = False



# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="RANDOM AI BIM Studio V56",

    page_icon="🏛️",

    layout="wide"

)



# ============================================================
# BIM OBJECT MODEL
# ============================================================


@dataclass
class BIMElement:

    id:str

    type:str

    name:str



@dataclass
class Space(BIMElement):

    area:float

    x:float

    y:float

    width:float

    depth:float

    height:float=3000



@dataclass
class Wall(BIMElement):

    x1:float

    y1:float

    x2:float

    y2:float

    thickness:float=200

    height:float=3000



@dataclass
class Opening(BIMElement):

    width:float

    height:float

    x:float

    y:float



@dataclass
class Column(BIMElement):

    size:str="300x300mm"

    material:str="Reinforced Concrete"



@dataclass
class BIMProject:


    id:str = field(
        default_factory=lambda:
        str(uuid.uuid4())
    )


    created:str = field(
        default_factory=lambda:
        str(datetime.now())
    )


    name:str="AI Residence"


    spaces:list=field(
        default_factory=list
    )


    walls:list=field(
        default_factory=list
    )


    openings:list=field(
        default_factory=list
    )


    columns:list=field(
        default_factory=list
    )


    structure:dict=field(
        default_factory=dict
    )


    cost:dict=field(
        default_factory=dict
    )



# ============================================================
# AI ARCHITECT ASSISTANT
# ============================================================


def analyse_design_brief(text):

    text=text.lower()


    bedrooms=3

    bathrooms=2


    bed_match=re.search(
        r"(\d+)\s*bedroom",
        text
    )


    bath_match=re.search(
        r"(\d+)\s*bathroom",
        text
    )


    if bed_match:

        bedrooms=int(
            bed_match.group(1)
        )


    if bath_match:

        bathrooms=int(
            bath_match.group(1)
        )


    features=[]


    keywords={

        "courtyard":
        "Internal Courtyard",

        "solar":
        "Solar Roof",

        "pool":
        "Swimming Pool",

        "garage":
        "Vehicle Garage",

        "office":
        "Home Office"

    }


    for key,value in keywords.items():

        if key in text:

            features.append(value)



    style="Modern"


    if "tropical" in text:

        style="Tropical Modern"


    if "luxury" in text:

        style="Luxury Contemporary"



    return {

        "bedrooms":bedrooms,

        "bathrooms":bathrooms,

        "style":style,

        "features":features

    }



# ============================================================
# PARAMETRIC ARCHITECTURAL GENERATOR
# ============================================================


def generate_spaces(config):


    spaces=[]


    spaces.append(

        Space(

            "RM001",

            "Space",

            "Living Room",

            35,

            0,

            0,

            7,

            5

        )

    )


    spaces.append(

        Space(

            "RM002",

            "Space",

            "Kitchen",

            18,

            7,

            0,

            4,

            4

        )

    )


    spaces.append(

        Space(

            "RM003",

            "Space",

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


        spaces.append(

            Space(

                f"RM-B{i+1}",

                "Space",

                f"Bedroom {i+1}",

                16,

                (i%3)*4,

                10+(i//3)*4,

                4,

                4

            )

        )


    return spaces



# ============================================================
# WALL GENERATOR
# ============================================================


def generate_walls(spaces):


    walls=[]


    counter=1


    for room in spaces:


        walls.extend([


            Wall(

                f"W{counter}",

                "Wall",

                f"{room.name} North Wall",

                room.x,

                room.y,

                room.x+room.width,

                room.y

            ),


            Wall(

                f"W{counter+1}",

                "Wall",

                f"{room.name} East Wall",

                room.x+room.width,

                room.y,

                room.x+room.width,

                room.y+room.depth

            )

        ])


        counter+=2



    return walls



# ============================================================
# OPENING GENERATOR
# ============================================================


def generate_openings():


    return [

        Opening(

            "D001",

            "Door",

            "Entrance Door",

            1200,

            2400,

            2,

            0

        ),


        Opening(

            "WIN001",

            "Window",

            "Living Window",

            1500,

            1200,

            5,

            5

        )

    ]



# ============================================================
# STRUCTURE GENERATOR
# ============================================================


def generate_structure():


    columns=[]


    for x in range(5):

        for y in range(5):

            columns.append(

                Column(

                    f"C{x}{y}",

                    "Column",

                    f"Grid {x+1}-{y+1}"

                )

            )


    return {

        "columns":columns,

        "system":
        "Reinforced Concrete Frame"

    }
