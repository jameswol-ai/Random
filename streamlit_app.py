# ============================================================
# RANDOM V2
# AI DESIGN STUDIO
# Copilot Driven Architecture Intelligence Engine
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime


# ============================================================
# OPTIONAL IMPORTS
# ============================================================

try:
    import plotly.graph_objects as go
except Exception:
    go = None


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Random V2 AI Design Studio",
    page_icon="🏗️",
    layout="wide"
)


MEMORY_FILE = Path(
    "random_v2_memory.json"
)


# ============================================================
# VISUAL DESIGN
# ============================================================

st.markdown(
"""
<style>

.stApp {
background:
linear-gradient(
120deg,
#050816,
#111827,
#1e293b
);
color:white;
}


.hero {

padding:40px;
border-radius:30px;

background:
linear-gradient(
135deg,
rgba(37,99,235,.4),
rgba(124,58,237,.4)
);

text-align:center;

}


.card {

background:
rgba(255,255,255,.08);

border-radius:20px;

padding:20px;

border:
1px solid rgba(255,255,255,.15);

margin:10px;

}


.agent {

background:
rgba(16,185,129,.15);

border-radius:15px;

padding:15px;

}


.metric {

font-size:35px;

font-weight:bold;

}


</style>

""",
unsafe_allow_html=True
)



# ============================================================
# MEMORY
# ============================================================


def load_memory():

    if MEMORY_FILE.exists():

        try:
            return json.loads(
                MEMORY_FILE.read_text()
            )

        except:
            pass


    return {
        "projects":[],
        "history":[]
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
# AI AGENTS
# ============================================================


def architect_ai(prompt):

    return {

        "building":
        random.choice(
            [
                "Modern Residence",
                "Smart Office",
                "Eco Campus",
                "Innovation Hub"
            ]
        ),

        "spaces":
        [
            "Entrance",
            "Living Area",
            "Work Area",
            "Kitchen",
            "Services"
        ],

        "concept":
        "Human-centered spatial design"
    }



def structural_ai():

    return {

        "system":
        random.choice(
            [
                "Concrete Frame",
                "Steel Frame",
                "Hybrid Structure"
            ]
        ),

        "columns":
        random.randint(20,80)

    }



def sustainability_ai():

    return {

        "energy_score":
        random.randint(70,98),

        "strategy":
        random.choice(
            [
                "Passive ventilation",
                "Solar optimization",
                "Green roof strategy"
            ]
        )

    }



def cost_ai(area):

    return {

        "estimate":
        area * random.randint(
            900,
            1600
        )

    }



def generate_project(prompt):


    architecture = architect_ai(prompt)

    area = random.randint(
        250,
        5000
    )


    return {

        "id":
        str(uuid.uuid4())[:8],


        "prompt":
        prompt,


        "architecture":
        architecture,


        "structure":
        structural_ai(),


        "sustainability":
        sustainability_ai(),


        "cost":
        cost_ai(area),


        "area":
        area,


        "floors":
        random.randint(
            1,
            15
        ),


        "created":
        datetime.now().isoformat()

    }



# ============================================================
# VISUALIZATION
# ============================================================


def floor_plan(project):

    if go is None:

        st.warning(
            "Plotly unavailable"
        )

        return


    fig = go.Figure()


    x=0


    for room in project["architecture"]["spaces"]:

        fig.add_shape(

            type="rect",

            x0=x,

            y0=0,

            x1=x+5,

            y1=5

        )


        fig.add_annotation(

            x=x+2.5,

            y=2.5,

            text=room,

            showarrow=False

        )


        x +=6



    fig.update_layout(
        height=400,
        template="plotly_dark"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



def building_3d(project):


    if go is None:

        return


    fig=go.Figure()


    height = project["floors"]


    fig.add_trace(

        go.Mesh3d(

            x=[
                0,10,10,0
            ],

            y=[
                0,0,10,10
            ],

            z=[
                0,0,height,height
            ],

            opacity=.5

        )

    )


    fig.update_layout(
        height=500,
        template="plotly_dark"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ============================================================
# HEADER
# ============================================================


st.markdown(
"""
<div class="hero">

<h1>🏗️ RANDOM V2</h1>

<h2>AI Architecture Design Studio</h2>

<p>
Imagine → Generate → Analyze → Evolve
</p>

</div>
""",
unsafe_allow_html=True
)



# ============================================================
# COPILOT
# ============================================================


st.subheader(
"🤖 Random Copilot"
)


prompt = st.text_area(

"Describe your building idea",

placeholder=
"Example: Design a sustainable family house with a courtyard"

)



if st.button(
"✨ Generate AI Concept"
):

    if prompt:

        st.session_state.project = generate_project(
            prompt
        )


        st.session_state.memory["history"].append(
            st.session_state.project
        )


        save_memory()


        st.success(
            "AI Design Concept Generated"
        )



# ============================================================
# PROJECT OUTPUT
# ============================================================


project = st.session_state.project



if project:


    st.divider()


    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Area",
        f"{project['area']} m²"
    )


    c2.metric(
        "Floors",
        project["floors"]
    )


    c3.metric(
        "Energy Score",
        project["sustainability"]["energy_score"]
    )


    c4.metric(
        "AI Status",
        "ACTIVE"
    )


    tabs = st.tabs(
        [
            "🏢 Concept",
            "📐 Plan",
            "🌆 3D",
            "🧠 Agents"
        ]
    )


    with tabs[0]:

        st.json(project)



    with tabs[1]:

        floor_plan(project)



    with tabs[2]:

        building_3d(project)



    with tabs[3]:


        agents=[

            "🏛 Architect AI",

            "📐 Structural AI",

            "🌱 Sustainability AI",

            "💰 Cost AI"

        ]


        for a in agents:

            st.markdown(
            f"""
            <div class="agent">

            {a}

            <br>

            Analysis Complete

            </div>
            """,
            unsafe_allow_html=True
            )


else:

    st.info(
        "Describe your project idea above to start Random Copilot."
    )



# ============================================================
# FOOTER
# ============================================================

st.caption(
"Random V2 | AI Design Studio | Architecture Intelligence Engine"
        )
