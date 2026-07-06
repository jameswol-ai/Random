# ============================================================
# RANDOM V55.1 AI BIM STUDIO
# Parametric Architecture + BIM Intelligence Engine
#
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import uuid
from datetime import datetime


# Optional visualization
try:
    import plotly.graph_objects as go
    PLOTLY = True
except Exception:
    PLOTLY = False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RANDOM AI BIM Studio V55.1",
    page_icon="🏛️",
    layout="wide"
)


# ============================================================
# RANDOM AI VISUAL SYSTEM
# ============================================================

st.markdown(
"""
<style>

.main {
background:#070b18;
}

.hero {

background:
linear-gradient(
135deg,
#111936,
#080d20
);

padding:35px;

border-radius:25px;

border:1px solid #263252;

}


.logo {

font-size:52px;

font-weight:900;

}


.subtitle {

color:#aab7d8;

font-size:20px;

}


.card {

background:#11182d;

padding:20px;

border-radius:18px;

border:1px solid #263252;

}


.metric {

font-size:34px;

font-weight:900;

color:#8ea2ff;

}


.stButton button {

background:#4255ff;

color:white;

height:45px;

border-radius:14px;

font-weight:800;

width:100%;

}

</style>

""",
unsafe_allow_html=True
)



# ============================================================
# UNIT CONVERSION ENGINE
# ============================================================

def mm_to_inches(mm):

    return mm / 25.4



def mm_to_feet_inches(mm):

    inches = mm_to_inches(mm)

    feet = int(inches // 12)

    remaining = round(
        inches % 12,
        1
    )

    return f"{feet}'-{remaining}\""



def m_to_feet_inches(m):

    total_inches = m * 39.3701

    feet = int(total_inches // 12)

    inches = round(
        total_inches % 12,
        1
    )

    return f"{feet}'-{inches}\""



def sqm_to_sqft(area):

    return round(
        area * 10.7639,
        2
    )



def show_length(
    mm,
    mode
):

    metric = f"{mm} mm"

    imperial = mm_to_feet_inches(mm)


    if mode == "Metric":

        return metric


    if mode == "Imperial":

        return imperial


    return f"{metric} ({imperial})"



def show_area(
    area,
    mode
):

    metric = f"{area} m²"

    imperial = (
        f"{sqm_to_sqft(area)} ft²"
    )


    if mode == "Metric":

        return metric


    if mode == "Imperial":

        return imperial


    return f"{metric} ({imperial})"



# ============================================================
# BIM DATABASE
# ============================================================

if "bim" not in st.session_state:

    st.session_state.bim = {

        "id":
        str(uuid.uuid4()),


        "created":
        str(datetime.now()),


        "project":
        "AI Residence",


        "units":
        "Dual",


        "levels":
        [],


        "spaces":
        [],


        "walls":
        [],


        "doors":
        [],


        "windows":
        [],


        "grid":
        [],


        "columns":
        [],


        "beams":
        [],


        "foundation":
        {},


        "roof":
        {},


        "cost":
        {}

    }



# ============================================================
# ARCHITECTURAL GENERATORS
# ============================================================

def generate_spaces(
    bedrooms,
    bathrooms
):

    spaces = [

        {
        "name":"Living Room",
        "area":35
        },

        {
        "name":"Kitchen",
        "area":18
        },

        {
        "name":"Dining",
        "area":16
        },

        {
        "name":"Corridor",
        "area":12
        },

        {
        "name":"Balcony",
        "area":10
        },

        {
        "name":"Laundry",
        "area":8
        }

    ]


    for i in range(bedrooms):

        spaces.append(

        {
        "name":
        f"Bedroom {i+1}",

        "area":
        16

        }

        )


    for i in range(bathrooms):

        spaces.append(

        {
        "name":
        f"Bathroom {i+1}",

        "area":
        6

        }

        )


    return spaces



def generate_walls():

    return [

        {
        "id":"W001",
        "length":6000,
        "height":3000,
        "thickness":200
        },


        {
        "id":"W002",
        "length":5000,
        "height":3000,
        "thickness":200
        }

    ]



def generate_doors():

    return [

        {
        "id":"D001",
        "type":"Entrance",
        "width":1200,
        "height":2400
        },


        {
        "id":"D002",
        "type":"Internal",
        "width":900,
        "height":2100
        }

    ]



def generate_windows():

    return [

        {
        "id":"WIN001",
        "width":1500,
        "height":1200
        }

    ]

# ============================================================
# STRUCTURAL GENERATORS
# ============================================================

def generate_grid(spacing):

    grid = []

    letters = [
        "A",
        "B",
        "C",
        "D",
        "E"
    ]


    for row in letters:

        for number in range(1,6):

            grid.append(

            {
            "name":
            f"{row}{number}",

            "spacing":
            spacing,

            "x":
            number * spacing,

            "y":
            letters.index(row) * spacing

            }

            )


    return grid



def generate_columns(grid):

    columns = []

    for point in grid:

        columns.append(

        {
        "id":
        f"C-{point['name']}",

        "grid":
        point["name"],

        "size":
        "300x300mm",

        "material":
        "Reinforced Concrete"

        }

        )


    return columns



def generate_beams():

    return [

        {
        "id":"B001",

        "span":"6000mm",

        "size":"250x450mm"

        },

        {
        "id":"B002",

        "span":"5000mm",

        "size":"250x450mm"

        }

    ]



def generate_foundation():

    return {

        "type":
        "Pad Foundation",

        "depth":
        1200,

        "material":
        "Concrete C25"

    }



def generate_roof():

    return {

        "type":
        "Pitched Roof",

        "pitch":
        "30 degrees",

        "covering":
        "Metal Sheet"

    }



# ============================================================
# COST ENGINE
# ============================================================

def generate_cost(area):

    return {

        "Floor Area":
        area,


        "Concrete Volume":
        round(
            area * 0.25,
            2
        ),


        "Steel Quantity":
        round(
            area * 0.04,
            2
        ),


        "Floor Finish":
        area,


        "Estimated Cost USD":
        round(
            area * 650,
            2
        )

    }



# ============================================================
# RANDOM AI HEADER
# ============================================================

st.markdown(

"""
<div class="hero">

<div class="logo">

🏛️ RANDOM AI BIM STUDIO V55.1

</div>


<div class="subtitle">

Artificial Intelligence • Architecture • BIM • Documentation

</div>


</div>

""",

unsafe_allow_html=True

)



# ============================================================
# SIDEBAR CONTROLS
# ============================================================

with st.sidebar:


    st.header(
        "🏗️ BIM PROJECT SETUP"
    )


    project_name = st.text_input(

        "Project Name",

        "AI Residence"

    )


    bedrooms = st.slider(

        "Bedrooms",

        1,

        12,

        4

    )


    bathrooms = st.slider(

        "Bathrooms",

        1,

        10,

        3

    )


    floors = st.slider(

        "Floors",

        1,

        5,

        2

    )


    units = st.radio(

        "📐 Drawing Units",

        [

        "Metric",

        "Imperial",

        "Dual"

        ],

        horizontal=True

    )


    grid_spacing = st.selectbox(

        "📏 Grid Spacing",

        [

        1,

        1.5,

        3

        ]

    )


    generate = st.button(

        "🚀 GENERATE BIM MODEL"

    )



# ============================================================
# AI BUILDING GENERATION
# ============================================================

if generate:


    spaces = generate_spaces(

        bedrooms,

        bathrooms

    )


    area = sum(

        item["area"]

        for item in spaces

    )


    grid = generate_grid(

        grid_spacing

    )


    st.session_state.bim.update(

    {


    "project":
    project_name,


    "units":
    units,


    "levels":

    [

        {
        "name":
        f"Level {i+1}",

        "height":
        3000

        }

        for i in range(floors)

    ],


    "spaces":
    spaces,


    "walls":
    generate_walls(),


    "doors":
    generate_doors(),


    "windows":
    generate_windows(),


    "grid":
    grid,


    "columns":
    generate_columns(grid),


    "beams":
    generate_beams(),


    "foundation":
    generate_foundation(),


    "roof":
    generate_roof(),


    "cost":
    generate_cost(area)


    }

    )


    st.success(

        "🏛️ RANDOM AI BIM model generated"

    )



# ============================================================
# DASHBOARD METRICS
# ============================================================

bim = st.session_state.bim


col1,col2,col3,col4 = st.columns(4)


metrics = [

(col1,"ROOMS",len(bim["spaces"])),

(col2,"WALLS",len(bim["walls"])),

(col3,"STRUCTURE",
len(bim["columns"])),

(col4,"GRID",
len(bim["grid"]))

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
# BIM DOCUMENTATION TABS
# ============================================================

tabs = st.tabs(

[
"📐 Floor Plan",
"🏠 Elevation",
"✂️ Section",
"🧱 BIM Objects",
"📊 Schedules",
"💰 Cost"

]

)



# ============================================================
# FLOOR PLAN
# ============================================================

with tabs[0]:


    st.subheader(
        "Architectural Floor Plan"
    )


    if PLOTLY:


        fig = go.Figure()



        # Draw walls

        for wall in bim["walls"]:


            if wall["id"] == "W001":

                fig.add_shape(

                type="line",

                x0=0,

                y0=0,

                x1=6,

                y1=0,

                line=dict(width=8)

                )


            else:

                fig.add_shape(

                type="line",

                x0=6,

                y0=0,

                x1=6,

                y1=5,

                line=dict(width=8)

                )



        # Draw grid

        for point in bim["grid"]:


            fig.add_annotation(

            x=point["x"],

            y=point["y"],

            text=point["name"],

            showarrow=False

            )



        fig.update_layout(

            height=600,

            title="RANDOM AI Generated Plan",

            xaxis_title="m",

            yaxis_title="m"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:

        st.info(
            "Plotly visualization unavailable"
        )



# ============================================================
# ELEVATION
# ============================================================

with tabs[1]:


    st.subheader(

        "Building Elevation"

    )


    st.json(

    {

    "Levels":

    bim["levels"],


    "Roof":

    bim["roof"],


    "Height":

    "3000mm per floor"

    }

    )



# ============================================================
# SECTION
# ============================================================

with tabs[2]:


    st.subheader(

        "Building Section"

    )


    st.json(

    {

    "Foundation":

    bim["foundation"],


    "Slab":

    "150mm Reinforced Concrete",


    "Ceiling":

    "3000mm",


    "Roof":

    bim["roof"]

    }

    )



# ============================================================
# BIM OBJECT TREE
# ============================================================

with tabs[3]:


    st.subheader(

        "BIM Database"

    )


    st.json(

    {

    "Spaces":

    bim["spaces"],


    "Walls":

    bim["walls"],


    "Doors":

    bim["doors"],


    "Windows":

    bim["windows"],


    "Columns":

    bim["columns"],


    "Beams":

    bim["beams"],


    "Grid":

    bim["grid"]

    }

    )



# ============================================================
# SCHEDULES
# ============================================================

with tabs[4]:


    st.subheader(

        "Room Schedule"

    )


    for room in bim["spaces"]:

        st.write(

        f"""

**{room['name']}**

Area:
{show_area(
room['area'],
bim['units']
)}

"""

        )



    st.divider()



    st.subheader(

        "Wall Schedule"

    )


    for wall in bim["walls"]:

        st.write(

        f"""

**{wall['id']}**

Length:
{show_length(
wall['length'],
bim['units']
)}

Height:
{show_length(
wall['height'],
bim['units']
)}

Thickness:
{show_length(
wall['thickness'],
bim['units']
)}

"""

        )



    st.divider()



    st.subheader(

        "Door Schedule"

    )


    for door in bim["doors"]:

        st.write(

        f"""

**{door['id']}**

Type:
{door['type']}

Width:
{show_length(
door['width'],
bim['units']
)}

Height:
{show_length(
door['height'],
bim['units']
)}

"""

        )



    st.divider()



    st.subheader(

        "Window Schedule"

    )


    for window in bim["windows"]:

        st.write(

        f"""

Window:
{window['id']}

Width:
{show_length(
window['width'],
bim['units']
)}

Height:
{show_length(
window['height'],
bim['units']
)}

"""

        )



# ============================================================
# COST REPORT
# ============================================================

with tabs[5]:


    st.subheader(

        "AI Cost Intelligence"

    )


    cost = bim["cost"]


    for item,value in cost.items():

        st.write(

        f"**{item}:** {value}"

        )



# ============================================================
# FOOTER
# ============================================================

st.caption(

"RANDOM V55.1 AI BIM STUDIO | Parametric Architecture Intelligence"

)
