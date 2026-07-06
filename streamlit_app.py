# ============================================================
# RANDOM AI BIM STUDIO V53
#
# AI Architecture + BIM Intelligence Engine
# Evolutionary Spatial Synthesis
# Single File Streamlit Edition
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
    page_title="RANDOM AI BIM Studio",
    page_icon="📐",
    layout="wide"
)


MEMORY_FILE = Path(
    "random_bim_memory.json"
)



# ============================================================
# VISUAL SYSTEM
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



[data-testid="stSidebar"] {

background:
linear-gradient(
180deg,
#050816,
#111827
);

}



.random-banner {

background:
linear-gradient(
135deg,
#111827,
#2563eb
);

padding:30px;

border-radius:22px;

color:white;

margin-bottom:25px;

}



.random-card {

background:
rgba(255,255,255,0.06);

border-radius:18px;

padding:20px;

border:
1px solid rgba(255,255,255,0.15);

}



.blueprint {

display:flex;

flex-wrap:wrap;

gap:16px;

background:#070b14;

padding:25px;

border-radius:20px;

border:
1px dashed #475569;

}



.room {

padding:22px;

min-width:220px;

border-radius:15px;

color:white;

box-shadow:
0 15px 35px rgba(0,0,0,.3);

}



.small {

opacity:.75;

font-size:.85rem;

}


</style>

""",
unsafe_allow_html=True
)



# ============================================================
# MEMORY CORE
# ============================================================


DEFAULT_MEMORY = {

    "version":
    "V53 BIM STUDIO",


    "projects":
    [],


    "designs":
    [],


    "evolution":
    [],


    "logs":
    []

}





def load_memory():

    if MEMORY_FILE.exists():

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data=json.load(f)


            for key in DEFAULT_MEMORY:

                if key not in data:

                    data[key]=DEFAULT_MEMORY[key]


            return data


        except Exception:

            return DEFAULT_MEMORY.copy()


    return DEFAULT_MEMORY.copy()




def save_memory():

    try:

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                st.session_state.memory,
                f,
                indent=4
            )


    except Exception:

        pass




def log_event(text):

    st.session_state.memory["logs"].append(

        {

            "time":
            datetime.now().isoformat(),

            "event":
            text

        }

    )

    save_memory()





# ============================================================
# SESSION ENGINE
# ============================================================


if "memory" not in st.session_state:

    st.session_state.memory = load_memory()



if "active_design" not in st.session_state:

    st.session_state.active_design=None



if "history" not in st.session_state:

    st.session_state.history=[]



if "unit_system" not in st.session_state:

    st.session_state.unit_system="Metric"



memory = st.session_state.memory





# ============================================================
# UNIT SYSTEM
# ============================================================


def area_display(value):


    if st.session_state.unit_system=="Imperial":

        return f"{value*10.7639:.1f} ft²"



    if st.session_state.unit_system=="Dual":

        return (

            f"{value:.1f} m² | "

            f"{value*10.7639:.1f} ft²"

        )


    return f"{value:.1f} m²"




def length_display(value):


    if st.session_state.unit_system=="Imperial":

        return f"{value*3.28084:.2f} ft"



    if st.session_state.unit_system=="Dual":

        return (

            f"{value:.2f} m | "

            f"{value*3.28084:.2f} ft"

        )


    return f"{value:.2f} m"





# ============================================================
# ARCHITECTURAL KNOWLEDGE BASE
# ============================================================


ARCHITECTURE_TYPES = {


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

"Manufacturing Facility"

]

}





def get_domain(name):


    for domain,items in ARCHITECTURE_TYPES.items():

        if name in items:

            return domain


    return "General"





# ============================================================
# AI DESIGN DNA GENERATOR
# ============================================================


def generate_design(
        building,
        modules
):


    rooms = [

        "Living Core",

        "Kitchen Intelligence Hub",

        "Service Zone"

    ]



    for i in range(

        random.randint(1,3)

    ):

        rooms.append(

            "Adaptive AI Module"

        )



    return {


        "id":

        str(uuid.uuid4())[:8].upper(),



        "building":

        building,



        "domain":

        get_domain(building),



        "modules":

        modules,



        "rooms":

        rooms,



        "area":

        120 + modules*20,



        "structure":

        {

            "columns":

            random.randint(15,40),


            "beams":

            random.randint(35,90)

        },



        "cost":

        0

    }





# ============================================================
# MUTATION ENGINE
# ============================================================


def mutate(design):


    child=json.loads(

        json.dumps(design)

    )


    child["structure"]["columns"] += random.randint(
        -2,4
    )


    child["structure"]["beams"] += random.randint(
        -5,8
    )


    child["structure"]["columns"]=max(
        10,
        child["structure"]["columns"]
    )


    child["structure"]["beams"]=max(
        15,
        child["structure"]["beams"]
    )


    if random.random()>0.5:

        child["rooms"].append(

            "Generated Spatial Intelligence Zone"

        )

        child["area"]+=20



    child["cost"]=int(

        child["area"]

        *

        random.randint(
            1500,
            2600
        )

    )


    return child

# ============================================================
# FITNESS INTELLIGENCE ENGINE
# ============================================================


def evaluate_design(design):


    ratio = (

        design["structure"]["beams"]

        /

        max(
            1,
            design["structure"]["columns"]
        )

    )


    structural = max(

        0,

        100 -

        int(
            abs(
                ratio - 2.2
            )
            *
            20
        )

    )



    if design["cost"] == 0:

        economic = 80


    else:

        cost_rate = (

            design["cost"]

            /

            design["area"]

        )


        economic = max(

            0,

            100 -

            int(
                abs(
                    cost_rate - 1800
                )
                *
                0.04
            )

        )



    spatial = min(

        100,

        len(
            design["rooms"]
        )
        *
        12

    )



    return {


        "Structural Score":

        structural,


        "Economic Score":

        economic,


        "Spatial Score":

        spatial

    }





def total_score(metrics):


    return int(

        sum(
            metrics.values()
        )

        /

        len(metrics)

    )





# ============================================================
# EVOLUTIONARY BIM ENGINE
# ============================================================


def evolve_design(

        building,

        modules,

        generations,

        population_size

):


    population = [

        generate_design(
            building,
            modules
        )

        for _ in range(population_size)

    ]



    history=[]



    for generation in range(generations):


        evaluated=[]


        for design in population:


            design["fitness"] = evaluate_design(
                design
            )


            design["score"] = total_score(

                design["fitness"]

            )


            evaluated.append(design)



        evaluated.sort(

            key=lambda x:x["score"],

            reverse=True

        )



        history.append(

            evaluated[0]["score"]

        )



        survivors = evaluated[

            :

            max(
                2,
                population_size//2
            )

        ]



        next_population=[]



        for parent in survivors:


            next_population.append(

                parent

            )


            next_population.append(

                mutate(parent)

            )



        population = next_population[

            :

            population_size

        ]



    return evaluated[0], history





# ============================================================
# BIM SPACE GENERATOR
# ============================================================


def create_bim_plan(design):


    spaces=[


        {

        "name":
        "Central Living Atrium",

        "width":
        7,

        "height":
        5,

        "color":
        "#2563eb"

        },


        {

        "name":
        "AI Kitchen Hub",

        "width":
        5,

        "height":
        4,

        "color":
        "#059669"

        },


        {

        "name":
        "Service Core",

        "width":
        3,

        "height":
        3,

        "color":
        "#d97706"

        }

    ]



    for i in range(

        design["modules"]

    ):


        spaces.append(

            {

# ============================================================
# PROJECT SUMMARY
# ============================================================


def project_summary(design):

    return {

        "Design ID":
        design["id"],

        "Building Type":
        design["building"],

        "Domain":
        design["domain"],

        "Area":
        area_display(
            design["area"]
        ),

        "Modules":
        design["modules"],

        "Fitness":
        design.get(
            "score",
            0
        )

    }





# ============================================================
# APPLICATION HEADER
# ============================================================


st.markdown(

"""
<div class="random-banner">

<h1>
📐 RANDOM AI BIM STUDIO V53
</h1>

<p>
Evolutionary Architecture • BIM Intelligence • Generative Spatial Design
</p>

</div>
""",

unsafe_allow_html=True

)




# ============================================================
# SIDEBAR CONTROL PANEL
# ============================================================


with st.sidebar:


    st.title(
        "⚙️ Studio Controls"
    )


    st.session_state.unit_system = st.selectbox(

        "Unit System",

        [

            "Metric",

            "Imperial",

            "Dual"

        ]

    )



    building = st.selectbox(

        "Architectural Typology",

        sum(
            ARCHITECTURE_TYPES.values(),
            []
        )

    )



    modules = st.slider(

        "Spatial Modules",

        1,

        10,

        4

    )



    generations = st.slider(

        "AI Evolution Cycles",

        2,

        30,

        8

    )



    population = st.slider(

        "Population",

        4,

        40,

        12

    )





# ============================================================
# MAIN TABS
# ============================================================


tabs = st.tabs(

[

"🏠 Dashboard",

"🧬 Evolution Lab",

"🏛️ BIM Viewer",

"🧱 Structural AI",

"💰 Cost + Materials",

"🌱 Sustainability",

"🧠 Memory Core",

"📦 Export"

]

)





# ============================================================
# DASHBOARD
# ============================================================


with tabs[0]:


    st.subheader(
        "System Dashboard"
    )


    c1,c2,c3 = st.columns(3)


    c1.metric(

        "Stored Designs",

        len(
            memory["designs"]
        )

    )


    c2.metric(

        "Evolution Runs",

        len(
            memory["evolution"]
        )

    )


    c3.metric(

        "System Version",

        "V53"

    )


    st.divider()


    st.info(

        "Generate a design in the Evolution Lab."

    )





# ============================================================
# EVOLUTION LAB
# ============================================================


with tabs[1]:


    st.subheader(

        "🧬 AI Evolution Laboratory"

    )



    if st.button(

        "🚀 Generate BIM Design",

        type="primary"

    ):


        with st.spinner(

            "Evolving architectural DNA..."

        ):


            design
           
