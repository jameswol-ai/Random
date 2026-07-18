import streamlit as st

def render_blueprint(plan):
    if not plan:
        st.info("No plan to display.")
        return
    # Find max extent
    max_x = max(r["x"] + r["w"] for r in plan)
    max_y = max(r["y"] + r["h"] for r in plan)
    # Add padding
    width = max_x + 2
    height = max_y + 2
    # Scale to fit in a 700px wide container
    scale = min(700 / width, 500 / height) * 0.95
    # Build SVG
    svg = f'<svg width="{width*scale:.0f}" height="{height*scale:.0f}" xmlns="http://www.w3.org/2000/svg" style="background:#f8f9fa;">'
    for r in plan:
        x = r["x"] * scale
        y = r["y"] * scale
        w = r["w"] * scale
        h = r["h"] * scale
        color = r["color"]
        svg += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="#333" stroke-width="2" rx="2" />'
        svg += f'<text x="{x+w/2}" y="{y+h/2}" text-anchor="middle" dominant-baseline="central" font-family="Arial" font-size="12" fill="#222">{r["name"]}</text>'
        svg += f'<text x="{x+w/2}" y="{y+h-10}" text-anchor="middle" font-family="Arial" font-size="10" fill="#555">{r["w"]:.1f}×{r["h"]:.1f}m</text>'
    svg += '</svg>'
    st.markdown(svg, unsafe_allow_html=True)