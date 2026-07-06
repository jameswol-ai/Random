# ============================================================
# DESIGN EVOLUTION ENGINE
# ============================================================


def evolve_design(project):

    mutation = {

        "id":
        str(uuid.uuid4())[:6],

        "change":

        random.choice(

            [
            "Improved spatial circulation",
            "Optimised structural grid",
            "Added sustainability features",
            "Improved daylight strategy",
            "Enhanced public spaces"
            ]

        ),

        "score":

        random.randint(
            85,
            99
        )

    }


    project["evolution_result"] = mutation

    project["evolution"] = mutation["score"]

    return project



# ============================================================
# BIM ANALYSIS ENGINE
# ============================================================


def analyse_project(project):


    return {

        "Spatial Quality":

        random.randint(
            80,
            96
        ),


        "Structural Logic":

        random.randint(
            85,
            98
        ),


        "Sustainability":

        project["sustainability"]["energy"],


        "Compliance":

        project["compliance"]["score"],


        "Evolution":

        project["evolution"]

    }



# ============================================================
# FLOOR PLAN VISUALIZER
# ============================================================


def show_floor_plan(project):


    if go is None:

        st.warning(
            "Plotly unavailable"
        )

        return


    fig = go.Figure()


    x = 0


    for space in project["floors"][0]["spaces"]:


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

        title="AI Generated Ground Floor",

        template="plotly_dark",

        height=450,

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



# ============================================================
# 3D BIM VIEWER
# ============================================================


def show_3d_model(project):


    if go is None:

        st.warning(
            "Plotly unavailable"
        )

        return


    floors=len(
        project["floors"]
    )


    height=floors*3.5


    fig=go.Figure()



    fig.add_trace(

        go.Mesh3d(

            x=[
                0,40,40,0
            ],

            y=[
                0,0,40,40
            ],

            z=[
                0,
                0,
                height,
                height
            ],

            opacity=.45,

            name="Building Mass"

        )

    )


    grid=project["structure"]["grid"]


    for x in range(5):

        for y in range(5):

            fig.add_trace(

                go.Scatter3d(

                    x=[
                        x*grid,
                        x*grid
                    ],

                    y=[
                        y*grid,
                        y*grid
                    ],

                    z=[
                        0,
                        height
                    ],

                    mode="lines",

                    name="Column"

                )

            )


    fig.update_layout(

        title="BIM Structural Visualization",

        height=650,

        template="plotly_dark"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



# ============================================================
# PROJECT DISPLAY
# ============================================================


project=st.session_state.project


if project:


    st.divider()


    c1,c2,c3,c4=st.columns(4)


    c1.metric(

        "Floors",

        len(project["floors"])

    )


    c2.metric(

        "Structure",

        project["structure"]["system"]

    )


    c3.metric(

        "Energy",

        f"{project['sustainability']['energy']}%"

    )


    c4.metric(

        "Evolution",

        f"{project['evolution']}%"

    )



    tabs=st.tabs(

        [

        "🏢 BIM Explorer",

        "📐 Floor Plan",

        "🌆 3D Model",

        "🧠 AI Brain"

        ]

    )



    with tabs[0]:


        st.subheader(
            "BIM Object Tree"
        )


        for floor in project["floors"]:


            with st.expander(

                f"Floor {floor['level']}"

            ):


                for room in floor["spaces"]:


                    st.write(

                        f"📦 {room['name']} | {room['area']} m²"

                    )


                    for obj in room["objects"]:

                        st.caption(

                            f"{obj['type']} : {obj['material']}"

                        )



    with tabs[1]:

        show_floor_plan(project)



    with tabs[2]:

        show_3d_model(project)



    with tabs[3]:


        report=analyse_project(
            project
        )


        for k,v in report.items():


            st.progress(

                v/100,

                text=f"{k}: {v}%"

            )



        st.subheader(
            "AI Agents"
        )


        agents=[

            "🏛 Architect AI",

            "📐 Structural AI",

            "🌱 Sustainability AI",

            "⚖ Compliance AI",

            "🧬 Evolution AI"

        ]


        for agent in agents:

            st.markdown(

            f"""

            <div class="agent">

            {agent}

            <br>

            Status: ACTIVE

            </div>

            """,

            unsafe_allow_html=True

            )


else:


    st.info(

        "Generate a project to activate BIM Intelligence."

    )
