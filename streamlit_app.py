# ============================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# Evolutionary Spatial Layout Synthesis & Diagnostics
# Zero Dependency Streamlit Edition
# ============================================================

import streamlit as st
import json
import uuid
import random

from pathlib import Path
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Random Studio Engine",
    page_icon="📐",
    layout="wide"
)


MEMORY_FILE = Path("arc_memory.json")


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Space+Grotesk:wght@400;700'
);


html, body {

font-family:
'Plus Jakarta Sans',
sans-serif;

}


h1,h2,h3,h4 {

font-family:
'Space Grotesk',
sans-serif;

}


.arc-blueprint-canvas {

display:flex;
flex-wrap:wrap;
gap:16px;

background:#090d16;

padding:24px;

border-radius:12px;

border:1px dashed #334155;

}


.arc-room-module {

min-width:220px;

padding:20px;

border-radius:12px;

color:white;

border:1px solid rgba(255,255,255,.15);

}


.room-meta {

font-size:.85rem;

opacity:.75;

margin-top:8px;

}

</style>

""",
unsafe_allow_html=True
)



# ============================================================
# MEMORY SYSTEM
# ============================================================


DEFAULT_STATE = {

    "projects": [],

    "designs": [],

    "logs": [],

    "evolution": []

}



def load_memory():

    if MEMORY_FILE.exists():

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data=json.load(file)

                return data


        except Exception:

            return DEFAULT_STATE.copy()


    return DEFAULT_STATE.copy()



def save_memory():

    try:

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                st.session_state.memory,
                file,
                indent=4
            )

    except Exception:

        pass



def log_event(message):

    st.session_state.memory["logs"].append(

        {

            "time":
            datetime.now().isoformat(),

            "msg":
            message

        }

    )

    save_memory()



# ============================================================
# SESSION INITIALIZATION
# ============================================================


if "memory" not in st.session_state:

    st.session_state.memory = load_memory()



if "active_design" not in st.session_state:

    st.session_state.active_design=None



if "active_history" not in st.session_state:

    st.session_state.active_history=[]



mem = st.session_state.memory




# ============================================================
# ARCHITECTURAL DOMAINS
# ============================================================


ARCH_DOMAINS={

"Residential":[

    "Luxury Villa",

    "Modern Apartment",

    "Townhouse"

],


"Commercial":[

    "Boutique Office",

    "Corporate Hub",

    "Hotel Resort",

    "Medical Clinic"

],


"Industrial":[

    "Distribution Warehouse",

    "Advanced Manufacturing Plant"

]

}



def get_domain(building_type):

    for domain,types in ARCH_DOMAINS.items():

        if building_type in types:

            return domain


    return "Unknown"





# ============================================================
# DESIGN GENERATION ENGINE
# ============================================================


def generate_base_design(
        building_type,
        bedrooms
):


    core_rooms=(

        [

            "Living Room",

            "Gourmet Kitchen",

            "Primary Bathroom"

        ]

        +

        [

            "Flex Space"

        ] * random.randint(1,3)

    )



    area = (

        65

        +

        44

        +

        9

        +

        bedrooms * 18

    )



    return {


        "id":
        str(uuid.uuid4())[:8].upper(),


        "type":
        building_type,


        "domain":
        get_domain(building_type),


        "bedrooms":
        bedrooms,


        "rooms":
        core_rooms,


        "area_sqm":
        area,


        "structure":

        {

            "columns":
            random.randint(14,36),


            "beams":
            random.randint(28,72)

        },


        "cost":
        0


    }




# ============================================================
# MUTATION ENGINE
# ============================================================


def mutate_design(design):

    d=json.loads(
        json.dumps(design)
    )


    d["structure"]["columns"] = max(

        10,

        d["structure"]["columns"]

        +

        random.randint(-2,4)

    )



    d["structure"]["beams"] = max(

        16,

        d["structure"]["beams"]

        +

        random.randint(-4,6)

    )



    if random.random()>0.5:

        d["rooms"].append(
            "Adaptive Modular Terracing"
        )

        d["area_sqm"] += 20



    d["cost"] = int(

        d["area_sqm"]

        *

        random.randint(
            1300,
            2500
        )

    )


    return d
