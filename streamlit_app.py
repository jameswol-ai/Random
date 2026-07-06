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
