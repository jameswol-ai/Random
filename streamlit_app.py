# ============================================================
# RANDOM AI ARCHITECTURE INTELLIGENCE ENGINE
# V52 BIM STUDIO CORE
#
# Evolutionary Spatial Layout Synthesis
# AI Assisted Architecture + BIM Intelligence
# Single File Streamlit Edition
# ============================================================


import streamlit as st
import json
import uuid
import random

from pathlib import Path
from datetime import datetime


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================


st.set_page_config(
    page_title="RANDOM AI BIM Studio",
    page_icon="📐",
    layout="wide"
)


MEMORY_FILE = Path("random_memory.json")



# ============================================================
# RANDOM AI VISUAL SYSTEM
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

letter-spacing:-0.03em;

}



[data-testid="stSidebar"] {

background:
linear-gradient(
180deg,
#090d16,
#111827
);

}



.random-header {

background:
linear-gradient(
135deg,
#111827,
#1e3a8a
);

padding:25px;

border-radius:20px;

color:white;

margin-bottom:25px;

}



.random-card {

background:
rgba(255,255,255,0.05);

padding:20px;

border-radius:16px;

border:

1px solid
rgba(255,255,255,0.12);

}



.arc-blueprint-canvas {


display:flex;

flex-wrap:wrap;

gap:16px;


background:

#090d16;


padding:25px;


border-radius:18px;


border:

1px dashed #475569;


}



.arc-room-module {


min-width:220px;


padding:22px;


border-radius:14px;


color:white;


transition:
0.25s;


box-shadow:

0 15px 30px rgba(0,0,0,.35);


}



.arc-room-module:hover {


transform:

translateY(-6px);


}



.room-meta {


opacity:.75;


font-size:.85rem;


margin-top:10px;


}



</style>

""",
unsafe_allow_html=True
)



# ============================================================
# MEMORY CORE
# ============================================================


DEFAULT_STATE = {


    "projects": [],


    "designs": [],


    "logs": [],


    "evolution": [],


    "version":

    "V52 BIM CORE"

}





def load_memory():

    if MEMORY_FILE.exists():

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


            for key in DEFAULT_STATE:

                if key not in data:

                    data[key] = DEFAULT_STATE[key]


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

            "timestamp":
            datetime.now().isoformat(),


            "message":
            message

        }

    )


    save_memory()





# ============================================================
# SESSION ENGINE
# ============================================================


if "memory" not in st.session_state:

    st.session_state.memory = load_memory()



if "active_design" not in st.session_state:

    st.session_state.active_design = None



if "active_history" not in st.session_state:

    st.session_state.active_history = []



if "unit_system" not in st.session_state:

    st.session_state.unit_system = "Metric"



mem = st.session_state.memory





# ============================================================
# UNIT CONVERSION SYSTEM
# ============================================================


def convert_area(value):

    if st.session_state.unit_system == "Imperial":

        return f"{value * 10.7639:.1f} ft²"


    if st.session_state.unit_system == "Dual":

        return (

            f"{value:.1f} m² | "

            f"{value * 10.7639:.1f} ft²"

        )


    return f"{value:.1f} m²"





def convert_length(value):

    if st.session_state.unit_system == "Imperial":

        return f"{value * 3.28084:.2f} ft"


    if st.session_state.unit_system == "Dual":

        return (

            f"{value:.2f} m | "

            f"{value * 3.28084:.2f} ft"

        )


    return f"{value:.2f} m"

# ============================================================
# ARCHITECTURAL KNOWLEDGE DOMAINS
# ============================================================


ARCH_DOMAINS = {


    "Residential":

    [

        "Luxury Villa",

        "Modern Apartment",

        "Townhouse"

    ],



    "Commercial":

    [

        "Boutique Office",

        "Corporate Hub",

        "Hotel Resort",

        "Medical Clinic"

    ],



    "Industrial":

    [

        "Distribution Warehouse",

        "Advanced Manufacturing Plant"

    ]

}





def get_domain(building_type):

    for domain, types in ARCH_DOMAINS.items():

        if building_type in types:

            return domain


    return "Unknown"





# ============================================================
# AI DESIGN GENETICS ENGINE
# ============================================================


def generate_base_design(
        building_type,
        spatial_modules
):


    rooms = (

        [

            "Living Core",

            "Kitchen Hub",

            "Primary Service Zone"

        ]

        +

        [

            "Adaptive Flex Module"

        ]

        *

        random.randint(1,3)

    )


    base_area = (

        120

        +

        spatial_modules * 18

    )



    design = {


        "id":

        str(uuid.uuid4())[:8].upper(),



        "type":

        building_type,



        "domain":

        get_domain(building_type),



        "modules":

        spatial_modules,



        "rooms":

        rooms,



        "area_sqm":

        base_area,



        "structure":

        {


            "columns":

            random.randint(
                14,
                40
            ),



            "beams":

            random.randint(
                30,
                90
            )

        },



        "cost":

        0

    }


    return design





# ============================================================
# GENETIC MUTATION
# ============================================================


def mutate_design(design):


    child = json.loads(

        json.dumps(design)

    )



    child["structure"]["columns"] += random.randint(
        -2,
        4
    )



    child["structure"]["columns"] = max(

        10,

        child["structure"]["columns"]

    )



    child["structure"]["beams"] += random.randint(
        -5,
        8
    )



    child["structure"]["beams"] = max(

        16,

        child["structure"]["beams"]

    )



    if random.random() > 0.5:


        child["rooms"].append(

            "AI Generated Adaptive Space"

        )


        child["area_sqm"] += 20



    child["cost"] = int(

        child["area_sqm"]

        *

        random.randint(
            1400,
            2600
        )

    )


    return child





# ============================================================
# FITNESS INTELLIGENCE
# ============================================================


def calculate_fitness(design):


    beam_ratio = (

        design["structure"]["beams"]

        /

        max(
            1,
            design["structure"]["columns"]
        )

    )



    structural_score = max(

        0,

        100 -

        int(

            abs(
                beam_ratio - 2.2
            )

            *

            20

        )

    )



    cost_ratio = (

        design["cost"]

        /

        max(
            1,
            design["area_sqm"]
        )

    )



    cost_score = max(

        0,

        100 -

        int(

            abs(
                cost_ratio - 1800
            )

            *

            0.04

        )

    )



    spatial_score = min(

        100,

        len(
            design["rooms"]
        )

        *

        10

    )



    return {


        "structural":

        structural_score,



        "economic":

        cost_score,



        "spatial":

        spatial_score

    }





def calculate_score(metrics):

    return int(

        sum(
            metrics.values()
        )

        /

        len(metrics)

    )





# ============================================================
# EVOLUTION PIPELINE
# ============================================================


def run_evolution(

        building_type,

        modules,

        generations,

        population_size

):


    population = [

        generate_base_design(
            building_type,
            modules
        )

        for _ in range(population_size)

    ]


    history = []



    for cycle in range(generations):


        scored = []



        for design in population:


            design["fitness"] = calculate_fitness(
                design
            )


            design["score"] = calculate_score(

                design["fitness"]

            )


            scored.append(design)



        scored.sort(

            key=lambda x:

            x["score"],

            reverse=True

        )



        history.append(

            scored[0]["score"]

        )



        survivors = scored[

            :

            max(
                2,
                population_size // 2
            )

        ]



        next_population = []



        for parent in survivors:


            next_population.append(

                parent

            )


            next_population.append(

                mutate_design(
                    parent
                )

            )



        population = next_population[

            :

            population_size

        ]



    return scored[0], history





# ============================================================
# PARAMETRIC BIM SPACE GENERATOR
# ============================================================


def generate_floor_plan(design):


    rooms = [

        {

            "name":

            "Central Living Atrium",

            "width":

            6.5,

            "height":

            5.5,

            "color":

            "#1e40af"

        },


        {

            "name":

            "Smart Kitchen Hub",

            "width":

            4.5,

            "height":

            4.0,

            "color":

            "#047857"

        },


        {

            "name":

            "Service Core",

            "width":

            3.0,

            "height":

            3.0,

            "color":

            "#92400e"

        }

    ]



    for i in range(

        design["modules"]

    ):


        rooms.append(

            {

                "name":

                f"Spatial Module {i+1}",


                "width":

                4.2,


                "height":

                4.0,


                "color":

                "#6b21a8"

            }

        )



    return rooms





# ============================================================
# BIM BLUEPRINT RENDERER
# ============================================================


def render_blueprint(plan):


    st.markdown(

        "### 🏛️ AI Generated Spatial Blueprint"

    )



    html = (

        "<div class='arc-blueprint-canvas'>"

    )



    for room in plan:


        html += f"""

        <div class="arc-room-module"

        style="background:{room['color']}">


        <b>

        {room['name']}

        </b>


        <div class="room-meta">

        📐 {room['width']}m × {room['height']}m

        </div>


        </div>

        """



    html += "</div>"



    st.markdown(

        html,

        unsafe_allow_html=True

    )
