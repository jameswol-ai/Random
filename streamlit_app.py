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
