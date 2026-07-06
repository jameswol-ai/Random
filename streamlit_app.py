# ============================================================
# RANDOM AI BIM STUDIO V56
# DASHBOARD UI
# ============================================================


# ============================================================
# HEADER
# ============================================================

st.markdown(
"""
<div class="hero">

<div class="logo">
🏛️ RANDOM AI BIM STUDIO V56
</div>

<div class="subtitle">

Artificial Intelligence • Parametric Architecture • BIM Intelligence

</div>

</div>

""",
unsafe_allow_html=True
)



# ============================================================
# SESSION INITIALIZATION
# ============================================================


if "project" not in st.session_state:

    st.session_state.project = BIMProject(
        name="AI Residence"
    )



project = st.session_state.project



# ============================================================
# SIDEBAR AI DESIGN CONTROL
# ============================================================


with st.sidebar:


    st.header(
        "🧠 AI ARCHITECT"
    )


    project.name = st.text_input(

        "Project Name",

        project.name

    )


    brief = st.text_area(

        "Describe the building",

"""
Luxury tropical villa,
4 bedroom,
large windows,
open kitchen,
modern architecture
"""

    )


    floors = st.slider(

        "Building Floors",

        1,

        10,

        2

    )


    generate = st.button(

        "🚀 GENERATE AI BIM MODEL",

        use_container_width=True

    )


    st.divider()


    st.subheader(
        "Export Center"
    )


    export_json = st.button(
        "📦 Export BIM JSON"
    )


    export_ifc = st.button(
        "🏢 Export IFC"
    )



# ============================================================
# AI GENERATION PIPELINE
# ============================================================


if generate:


    parameters = analyze_brief(
        brief
    )


    project.rooms = generate_rooms(
        parameters
    )


    project.walls = generate_walls(
        project.rooms
    )


    project.openings = generate_openings()


    project.levels = [

        {
        "name":
        f"Level {i+1}",

        "height":
        3

        }

        for i in range(floors)

    ]


    project.cost = calculate_cost(
        project
    )


    st.success(
        "🏛️ AI BIM model generated successfully"
    )



# ============================================================
# TOP METRIC PANEL
# ============================================================


col1,col2,col3,col4 = st.columns(4)



metrics=[

(
col1,
"ROOMS",
len(project.rooms)
),

(
col2,
"WALL ELEMENTS",
len(project.walls)
),

(
col3,
"OPENINGS",
len(project.openings)
),

(
col4,
"FLOOR AREA",
f"{sum(r.area for r in project.rooms):.1f} m²"
)

]



for col,title,value in metrics:


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
# MAIN DASHBOARD GRID
# ============================================================


left,right = st.columns(
[2,1]
)



# ============================================================
# BIM MODEL PREVIEW PANEL
# ============================================================


with left:


    st.subheader(
        "🏗️ Parametric BIM Model"
    )


    tabs = st.tabs(

    [

    "📐 Floor Plan",

    "🧱 BIM Objects",

    "📊 Schedules"

    ]

    )



    with tabs[0]:


        st.info(
            "Floor plan renderer connected to geometry engine"
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

                x=
                room.x+
                room.width/2,


                y=
                room.y+
                room.depth/2,


                text=
                room.name,


                showarrow=False

                )


            fig.update_layout(

            height=650,

            title=
            "AI Generated Architectural Plan",

            xaxis_title=
            "Meters",

            yaxis_title=
            "Meters",

            )


            st.plotly_chart(

                fig,

                use_container_width=True

            )



    with tabs[1]:


        st.subheader(
            "BIM Object Tree"
        )


        st.json(

        {

        "Rooms":
        [
            asdict(r)
            for r in project.rooms
        ],


        "Walls":
        [
            asdict(w)
            for w in project.walls
        ],


        "Openings":
        [
            asdict(o)
            for o in project.openings
        ]

        }

        )



    with tabs[2]:


        st.subheader(
            "Quantity Schedules"
        )


        for room in project.rooms:


            st.write(

            f"""
**{room.name}**

Dimensions:
{room.width:.1f}m × {room.depth:.1f}m

Area:
{room.area:.1f}m²

"""

            )



# ============================================================
# AI ASSISTANT PANEL
# ============================================================


with right:


    st.subheader(
        "🤖 BIM Intelligence"
    )


    st.markdown(

"""
<div class="card">

<h3>
AI Recommendations
</h3>


<ul>

<li>Increase north glazing for daylight</li>

<li>Reduce corridor circulation waste</li>

<li>Consider rainwater harvesting</li>

<li>Optimize structural grid spacing</li>

</ul>


</div>

""",

unsafe_allow_html=True

)



    st.subheader(
        "📈 Project Status"
    )


    status=[

    ("Geometry","🟢 Complete"),

    ("Architecture","🟢 Generated"),

    ("Structure","🟡 Pending"),

    ("Cost","🟢 Calculated"),

    ("IFC Export","⚪ Ready")

    ]


    for item,state in status:


        st.write(
            f"**{item}:** {state}"
        )



# ============================================================
# COST INTELLIGENCE
# ============================================================


st.divider()


st.subheader(
    "💰 AI Cost Intelligence"
)



cost_col1,cost_col2,cost_col3 = st.columns(3)



if project.cost:


    cost_items=list(
        project.cost.items()
    )


    for i,(name,value) in enumerate(cost_items):


        [
        cost_col1,
        cost_col2,
        cost_col3
        ][i%3].metric(

            name,

            value

        )
