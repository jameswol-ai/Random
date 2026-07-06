import streamlit as st

def render_blueprint(plan):
    st.markdown("### 🗺️ Layout Canvas")

    html = '<div style="display:flex;gap:16px;flex-wrap:wrap;background:#090d16;padding:20px;border-radius:10px;">'

    for r in plan:
        html += f"""
        <div style="
            background:{r['color']};
            padding:15px;
            border-radius:10px;
            color:white;
            min-width:180px;
        ">
            <div style="font-weight:600">{r['name']}</div>
            <div style="opacity:0.7">{r['w']} × {r['h']}</div>
        </div>
        """

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)