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

# ============================================================
# FITNESS ANALYSIS ENGINE
# ============================================================


def calculate_fitness(design):

    structural_ratio = (

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
                structural_ratio - 2.1
            )
            *
            22
        )

    )



    cost_per_sqm = (

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
                cost_per_sqm - 1650
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
        9

    )



    return {


        "structural_integrity":

        structural_score,


        "cost_efficiency":

        cost_score,


        "spatial_complexity":

        spatial_score

    }




def calculate_score(fitness):

    return int(

        sum(
            fitness.values()
        )

        /

        len(fitness)

    )





# ============================================================
# EVOLUTIONARY DESIGN LOOP
# ============================================================


def run_evolutionary_loop(

        building_type,

        bedrooms,

        generations,

        population_size

):


    population=[

        generate_base_design(
            building_type,
            bedrooms
        )

        for _ in range(population_size)

    ]


    history=[]



    for generation in range(generations):


        scored=[]



        for design in population:


            fitness=calculate_fitness(
                design
            )


            design["fitness"]=fitness


            design["score"]=calculate_score(
                fitness
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



        survivors=scored[

            :

            max(
                2,
                population_size//2
            )

        ]



        next_generation=[]



        for parent in survivors:


            next_generation.append(
                parent
            )


            next_generation.append(

                mutate_design(
                    parent
                )

            )



        population=next_generation[

            :

            population_size

        ]



    return scored[0], history





# ============================================================
# PARAMETRIC FLOOR PLAN SYNTHESIS
# ============================================================


def generate_floor_plan(design):


    rooms=[


        {

        "name":
        "Grand Living Lounge",

        "w":
        6.5,

        "h":
        5.0,

        "color":
        "#1e3a8a"

        },


        {

        "name":
        "Culinary Kitchen",

        "w":
        4.5,

        "h":
        4.0,

        "color":
        "#064e3b"

        },


        {

        "name":
        "Central Powder Room",

        "w":
        3.0,

        "h":
        2.5,

        "color":
        "#78350f"

        }

    ]



    for i in range(

        design["bedrooms"]

    ):


        rooms.append(

            {


            "name":

            (

            "Master Suite"

            if i == 0

            else

            f"Bedroom {i+1}"

            ),


            "w":

            4.5,


            "h":

            4.0,


            "color":

            "#4c1d95"


            }

        )



    return rooms





# ============================================================
# BLUEPRINT HTML RENDERER
# ============================================================


def render_native_blueprint(plan):


    st.markdown(
        "### 🗺️ Generative Spatial Layout"
    )


    canvas="<div class='arc-blueprint-canvas'>"



    for room in plan:


        canvas += f"""

        <div class="arc-room-module"
        style="background:{room['color']}">

        <div style="
        font-size:1.15rem;
        font-weight:700;
        ">

        {room['name']}

        </div>


        <div class="room-meta">

        📐 {room['w']}m × {room['h']}m

        </div>


        </div>

        """



    canvas += "</div>"



    st.markdown(

        canvas,

        unsafe_allow_html=True

    )





# ============================================================
# STRUCTURAL DIAGNOSTICS
# ============================================================


def run_structural_review(design):


    alerts=[]



    if design["structure"]["columns"] < 16:

        alerts.append(

            "🔴 Column density low. Review structural grid."

        )



    if (

        design["cost"]

        /

        design["area_sqm"]

        >

        2300

    ):

        alerts.append(

            "🟡 Cost efficiency threshold exceeded."

        )



    if (

        design["structure"]["beams"]

        /

        design["structure"]["columns"]

        <

        1.9

    ):

        alerts.append(

            "🔵 Beam-column ratio requires review."

        )



    if not alerts:

        alerts.append(

            "🟢 Design structurally stable."

        )



    return alerts





# ============================================================
# MATERIAL INTELLIGENCE
# ============================================================


def calculate_material_takeoffs(design):


    return [


        {

        "Material":

        "High Performance Concrete",

        "Quantity":

        f"{design['structure']['columns']*2.6:.1f} m³"

        },


        {

        "Material":

        "Steel Reinforcement",

        "Quantity":

        f"{design['structure']['beams']*0.48:.2f} MT"

        },


        {

        "Material":

        "CMU Blocks",

        "Quantity":

        f"{int(design['area_sqm']*42):,} units"

        },


        {

        "Material":

        "Dead Load Estimate",

        "Quantity":

        f"{int(design['structure']['columns']*13.2):,} kN"

        }

    ]

# ============================================================
# STREAMLIT WORKSPACE
# ============================================================


st.sidebar.title(
    "📐 RANDOM AI Architecture Studio"
)



page = st.sidebar.radio(

    "Workspace",

    [

        "📊 Dashboard",

        "🧬 Evolution Lab",

        "🏛️ Blueprint Viewer",

        "🧱 Structural Intelligence",

        "💰 Cost & Materials",

        "🧠 Memory Core",

        "📦 Export"

    ]

)



ARCH_FLAT = sum(
    ARCH_DOMAINS.values(),
    []
)



building_type = st.sidebar.selectbox(

    "Architectural Typology",

    ARCH_FLAT

)



bedrooms = st.sidebar.slider(

    "Spatial Modules",

    1,

    8,

    3

)



generations = st.sidebar.slider(

    "Evolution Generations",

    2,

    20,

    6

)



population = st.sidebar.slider(

    "Population Size",

    4,

    30,

    10

)




# ============================================================
# DASHBOARD
# ============================================================


if page == "📊 Dashboard":


    st.title(
        "📐 RANDOM AI Studio Dashboard"
    )


    c1,c2,c3 = st.columns(3)


    c1.metric(

        "Stored Projects",

        len(
            mem["projects"]
        )

    )


    c2.metric(

        "Generated Designs",

        len(
            mem["designs"]
        )

    )


    c3.metric(

        "Evolution Cycles",

        len(
            mem["evolution"]
        )

    )



    st.divider()


    st.subheader(
        "System Telemetry"
    )


    if mem["logs"]:


        for log in reversed(

            mem["logs"][-10:]

        ):

            st.caption(

                f"{log['time']} | {log['msg']}"

            )


    else:

        st.info(
            "No system events recorded."
        )





# ============================================================
# EVOLUTION LAB
# ============================================================


elif page == "🧬 Evolution Lab":


    st.title(
        "🧬 Generative Architecture Evolution"
    )



    if st.button(

        "🚀 Start Evolution Pipeline",

        type="primary"

    ):


        with st.spinner(

            "Evolving architectural DNA..."

        ):


            best,history = run_evolutionary_loop(

                building_type,

                bedrooms,

                generations,

                population

            )



            best["plan"] = generate_floor_plan(

                best

            )


            mem["designs"].append(

                best

            )



            mem["evolution"].append(

                {

                "id":
                str(uuid.uuid4())[:6],


                "design":
                best["id"],


                "score":
                best["score"],


                "time":
                datetime.now().isoformat()

                }

            )



            st.session_state.active_design = best


            st.session_state.active_history = history



            log_event(

                f"Generated design {best['id']}"

            )



            save_memory()




    if st.session_state.active_design:


        design = st.session_state.active_design



        st.subheader(

            f"⚡ Design DNA {design['id']}"

        )



        a,b,c = st.columns(3)



        a.metric(

            "Fitness Score",

            design["score"]

        )


        b.metric(

            "Floor Area",

            f"{design['area_sqm']} m²"

        )


        c.metric(

            "Estimated Cost",

            f"${design['cost']:,}"

        )



        st.line_chart(

            st.session_state.active_history

        )





# ============================================================
# BLUEPRINT VIEWER
# ============================================================


elif page == "🏛️ Blueprint Viewer":


    st.title(
        "🏛️ Parametric Spatial Blueprint"
    )



    if st.session_state.active_design:


        render_native_blueprint(

            st.session_state.active_design["plan"]

        )


    else:

        st.info(

            "Generate a design first."

        )





# ============================================================
# STRUCTURAL INTELLIGENCE
# ============================================================


elif page == "🧱 Structural Intelligence":


    st.title(

        "🧱 Structural Diagnostics"

    )


    if st.session_state.active_design:


        design = st.session_state.active_design


        for alert in run_structural_review(design):

            st.write(alert)



        st.json(

            design["fitness"]

        )


    else:

        st.info(

            "No active design."

        )





# ============================================================
# COST & MATERIALS
# ============================================================


elif page == "💰 Cost & Materials":


    st.title(

        "💰 Material Intelligence"

    )



    if st.session_state.active_design:


        design = st.session_state.active_design



        st.metric(

            "Estimated Construction Cost",

            f"${design['cost']:,}"

        )



        st.table(

            calculate_material_takeoffs(

                design

            )

        )



    else:

        st.info(

            "Generate a design first."

        )





# ============================================================
# MEMORY CORE
# ============================================================


elif page == "🧠 Memory Core":


    st.title(

        "🧠 Architecture Memory Repository"

    )


    st.json(

        mem

    )



    if st.button(

        "Reset Memory"

    ):


        st.session_state.memory = DEFAULT_STATE.copy()


        st.session_state.active_design = None


        st.session_state.active_history = []



        save_memory()


        st.success(

            "Memory cleared"

        )


        st.rerun()





# ============================================================
# EXPORT
# ============================================================


# ============================================================
# EXPORT
# ============================================================


elif page == "📦 Export":


    st.title(

        "📦 Project Export Hub"

    )


    if st.session_state.active_design:


        export_data = json.dumps(

            st.session_state.active_design,

            indent=4

        )


        st.download_button(

            label="⬇️ Download Design JSON",

            data=export_data,

            file_name="random_design.json",

            mime="application/json"

        )


        st.subheader(

            "Preview"

        )


        st.json(

            st.session_state.active_design

        )


    else:


        st.info(

            "Generate a design before exporting."

        )





# ============================================================
# FOOTER
# ============================================================


st.caption(

    "RANDOM AI Architecture Intelligence Engine | Evolutionary Spatial Synthesis"

)
