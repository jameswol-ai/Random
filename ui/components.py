import streamlit as st

def render_blueprint(plan):
    st.markdown("### Layout Canvas")
    html = '<div style="display: flex; flex-wrap: wrap; gap: 12px;">'
    for r in plan:
        html += f"""
        <div style="background: {r['color']}; padding: 16px; border-radius: 8px; 
                    min-width: 100px; color: white;">
            <strong>{r['name']}</strong><br>
            {r['w']} × {r['h']}
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)