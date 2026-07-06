import streamlit as st

def render(plan):
    html = "<div style='display:flex;flex-wrap:wrap;gap:10px;'>"

    for r in plan:
        html += f"""
        <div style='padding:10px;background:{r['c']};color:white;border-radius:8px;'>
            {r['name']}<br>{r['w']}×{r['h']}
        </div>
        """

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)