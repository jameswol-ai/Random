import streamlit as st 

def render_blueprint(plan): 
    st.markdown("### ️ Generative Layout Arrangement") 
    html = '
' 
    for room in plan: 
        html += f""" 

        #### {room['name']}

        {room['w']}m × {room['h']}m

        """ 
    html += "
" 
    st.markdown(html, unsafe_allow_html=True)