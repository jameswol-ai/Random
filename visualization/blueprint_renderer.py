import streamlit as st


def render_blueprint(plan):
    st.markdown("### 🗺️ Generative Layout Arrangement")

    html = '<div style="display:flex;flex-wrap:wrap;gap:16px;">'

    for room in plan:
        html += f"""
        <div style="
            flex:1 1 30%;
            padding:16px;
            background:{room['color']};
            color:white;
            border-radius:8px;
        ">
            <h4>{room['name']}</h4>
            <p>{room['w']}m × {room['h']}m</p>
        </div>
        """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)