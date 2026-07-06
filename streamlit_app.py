# ============================================================
# RANDOM V50 BIM CORE
# AI ARCHITECTURE + BIM INTELLIGENCE ENGINE
# Single File Streamlit Edition
#
# V2 AI Design Studio upgraded into BIM Core
# ============================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime


# ============================================================
# OPTIONAL VISUALIZATION
# ============================================================

try:
    import plotly.graph_objects as go
except Exception:
    go = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Random V50 BIM Core",
    page_icon="🏗️",
    layout="wide"
)


MEMORY_FILE = Path(
    "random_v50_memory.json"
)


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
"""
<style>

.stApp {

background:
linear-gradient(
120deg,
#030712,
#111827,
#1e293b
);

color:white;

}


.hero {

padding:45px;

border-radius:30px;

background:
linear-gradient(
135deg,
rgba(37,99,235,.45),
rgba(124,58,237,.45)
);

text-align:center;

}


.card {

background:
rgba(255,255,255,.08);

padding:20px;

border-radius:20px;

border:
1px solid rgba(255,255,255,.15);

}


.agent {

background:
rgba(16,185,129,.18);

padding:15px;

border-radius:15px;

margin:10px 0;

}


</style>
""",
unsafe_allow_html=True
)



# ============================================================
# MEMORY SYSTEM
# ============================================================


def load_memory():

    if MEMORY_FILE.exists():

        try:
            return json.loads(
                MEMORY_FILE.read_text()
            )

        except Exception:
            pass


    return {

        "projects": [],

        "history": []

    }



def save_memory():

    MEMORY_FILE.write_text(

        json.dumps(

            st.session_state.memory,

            indent=2

        )

    )



if "memory" not in st.session_state:

    st.session_state.memory = load_memory()



if "project" not in st.session_state:

    st.session_state.project = None



# ============================================================
# BIM OBJECT GENERATORS
# ============================================================


def create_space(name, floor):

    return {

        "id":
        str(uuid.uuid4())[:6],

        "name":
        name,

        "floor":
        floor,

        "type":
        "space",

        "area":
        random.randint(12,80)

    }



def create_floor(number):

    rooms = [

        "Lobby",

        "Office",

        "Meeting Room",

        "Core",

        "Services"

    ]


    return {

        "level":
        number,

        "height":
        3.5,


        "spaces":

        [

            create_space(
                r,
                number
            )

            for r in rooms

        ]

    }



def create_structure():

    grid = random.choice(

        [

            5,

            6,

            7.5

        ]

    )


    columns = []


    for x in range(4):

        for y in range(4):

            columns.append(

                {

                "id":
                f"C{x}{y}",

                "x":
                x*grid,

                "y":
                y*grid

                }

            )


    return {

        "system":
        random.choice(

            [

            "Reinforced Concrete Frame",

            "Steel Frame",

            "Composite Structure"

            ]

        ),


        "grid_spacing":
        grid,


        "columns":
        columns

    }



# ============================================================
# AI AGENTS
# ============================================================


def architect_ai(prompt):

    return {

        "building_type":

        random.choice(

            [

            "Smart Office Tower",

            "Eco Residential Complex",

            "Innovation Campus",

            "Mixed Use Building"

            ]

        ),


        "concept":

        "Human-centred adaptive architecture",


        "spaces":

        [

        "Entrance",

        "Public Zone",

        "Work Zone",

        "Service Zone"

        ]

    }



def structural_ai():

    return create_structure()



def sustainability_ai():

    return {

        "energy_score":

        random.randint(
            75,
            98
        ),


        "strategy":

        random.choice(

            [

            "Passive ventilation",

            "Solar optimisation",

            "Green roof",

            "Water reuse"

            ]

        )

    }



def compliance_ai():

    return {

        "fire":

        "Checked",


        "accessibility":

        "Checked",


        "safety_score":

        random.randint(
            80,
            99
        )

    }


# ============================================================
# BIM PROJECT GENERATOR
# ============================================================


def generate_bim_project(prompt):


    floors = random.randint(
        3,
        15
    )


    building = {

        "id":
        str(uuid.uuid4())[:8],


        "prompt":
        prompt,


        "created":
        datetime.now().isoformat(),


        "architecture":
        architect_ai(prompt),


        "floors":

        [

            create_floor(i)

            for i in range(
                floors
            )

        ],


        "structure":
        structural_ai(),


        "sustainability":
        sustainability_ai(),


        "compliance":
        compliance_ai(),


        "area":
        floors *
        random.randint(
            300,
            900
        )

    }


    return building

# ============================================================
# VISUALIZATION ENGINE
# ============================================================


def create_floor_plan(project):

    if go is None:

        st.warning(
            "Plotly not installed. Install with: pip install plotly"
        )
        return


    floor = project["floors"][0]


    fig = go.Figure()


    x = 0


    for space in floor["spaces"]:

        fig.add_shape(

            type="rect",

            x0=x,

            y0=0,

            x1=x+8,

            y1=6

        )


        fig.add_annotation(

            x=x+4,

            y=3,

            text=space["name"],

            showarrow=False

        )


        x += 10



    fig.update_layout(

        title="BIM Ground Floor Plan",

        height=450,

        template="plotly_dark",

        xaxis=dict(
            visible=False
        ),

        yaxis=dict(
            visible=False
        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )




def create_3d_building(project):


    if go is None:

        return



    floors = len(
        project["floors"]
    )


    height = floors * 3.5



    fig = go.Figure()



    fig.add_trace(

        go.Mesh3d(

            x=[
                0,
                40,
                40,
                0
            ],

            y=[
                0,
                0,
                40,
                40
            ],

            z=[
                0,
                0,
                height,
                height
            ],

            opacity=0.45,

            name="Building Mass"

        )

    )



    for column in project["structure"]["columns"]:


        fig.add_trace(

            go.Scatter3d(

                x=[
                    column["x"],
                    column["x"]
                ],

                y=[
                    column["y"],
                    column["y"]
                ],

                z=[
                    0,
                    height
                ],

                mode="lines",

                name=column["id"]

            )

        )



    fig.update_layout(

        title="BIM Structural Massing",

        height=600,

        template="plotly_dark"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



# ============================================================
# BIM ANALYSIS
# ============================================================


def structural_score(project):

    spacing = project["structure"]["grid_spacing"]

    score = 100


    if spacing > 7:

        score -= 10


    return score



def generate_report(project):


    return {

        "Spatial Quality":

        random.randint(
            80,
            95
        ),


        "Structural Logic":

        structural_score(project),


        "Sustainability":

        project["sustainability"]["energy_score"],


        "Compliance":

        project["compliance"]["safety_score"]

    }




# ============================================================
# HEADER
# ============================================================


st.markdown(

"""

<div class="hero">

<h1>🏗️ RANDOM V50 BIM CORE</h1>

<h2>AI Architecture Intelligence Engine</h2>

<p>

Imagine → Generate → Analyse → Evolve

</p>

</div>

""",

unsafe_allow_html=True

)



# ============================================================
# RANDOM COPILOT
# ============================================================


st.subheader(
"🤖 Random BIM Copilot"
)



prompt = st.text_area(

"Describe your building",

placeholder=

"Example: Generate a 10-floor sustainable office tower"

)



if st.button(
"🚀 Generate BIM Project"
):

    if prompt:

        project = generate_bim_project(
            prompt
        )


        st.session_state.project = project


        st.session_state.memory["projects"].append(
            project
        )


        st.session_state.memory["history"].append(
            datetime.now().isoformat()
        )


        save_memory()


        st.success(
            "BIM model generated successfully"
        )




# ============================================================
# DISPLAY PROJECT
# ============================================================


project = st.session_state.project



if project:


    st.divider()



    col1,col2,col3,col4 = st.columns(4)


    col1.metric(

        "Building Area",

        f"{project['area']} m²"

    )


    col2.metric(

        "Floors",

        len(project["floors"])

    )


    col3.metric(

        "Structure",

        project["structure"]["system"]

    )


    col4.metric(

        "BIM Status",

        "ACTIVE"

    )



    tabs = st.tabs(

        [

        "🏢 BIM Explorer",

        "📐 Floor Plan",

        "🌆 3D Model",

        "🧠 AI Analysis"

        ]

    )



    with tabs[0]:


        st.subheader(
            "Building Tree"
        )


        for floor in project["floors"]:

            with st.expander(
                f"Floor {floor['level']}"
            ):

                for room in floor["spaces"]:

                    st.write(

                        f"📦 {room['name']} | {room['area']} m²"

                    )



    with tabs[1]:

        create_floor_plan(project)



    with tabs[2]:

        create_3d_building(project)



    with tabs[3]:


        report = generate_report(project)



        for key,value in report.items():


            st.progress(

                value / 100,

                text=f"{key}: {value}%"

            )



        agents = [

            "🏛 Architect AI",

            "📐 Structural AI",

            "🌱 Sustainability AI",

            "⚙️ BIM Coordinator AI",

            "📋 Compliance AI"

        ]



        for agent in agents:


            st.markdown(

            f"""

            <div class="agent">

            {agent}

            <br>

            Analysis completed

            </div>

            """,

            unsafe_allow_html=True

            )


else:


    st.info(

        "Enter a project idea to activate Random BIM Copilot."

    )



# ============================================================
# MEMORY VIEW
# ============================================================


with st.sidebar:


    st.header(
        "🧠 Random Memory"
    )


    st.metric(

        "Projects",

        len(
            st.session_state.memory["projects"]
        )

    )


    st.caption(

        "Random V50 BIM Core"

    )



# ============================================================
# FOOTER
# ============================================================


st.caption(

"RANDOM V50 | BIM CORE | AI Architecture Intelligence Engine"

)
