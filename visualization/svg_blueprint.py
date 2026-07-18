import math

def generate_svg_blueprint(rooms):
    """Generate SVG with walls, doors, and dimensions."""
    if not rooms:
        return ""
    
    # Find bounds
    max_x = max(r["x"] + r["w"] for r in rooms) + 1
    max_y = max(r["y"] + r["h"] for r in rooms) + 1
    
    # Scale to fit
    scale = min(700 / max_x, 500 / max_y) * 0.9
    padding = 20
    
    svg = f'''
    <svg width="{(max_x * scale) + padding*2:.0f}" height="{(max_y * scale) + padding*2:.0f}" 
         xmlns="http://www.w3.org/2000/svg" style="background:#f5f0eb; border-radius:8px;">
        <defs>
            <marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
                <path d="M0,0 L8,3 L0,6" fill="#666"/>
            </marker>
        </defs>
    '''
    
    # 1. Draw room backgrounds
    for r in rooms:
        x = r["x"] * scale + padding
        y = r["y"] * scale + padding
        w = r["w"] * scale
        h = r["h"] * scale
        svg += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{r["color"]}" stroke="#444" stroke-width="2" rx="2"/>'
        svg += f'<text x="{x+w/2}" y="{y+h/2}" text-anchor="middle" dominant-baseline="central" font-family="Arial" font-size="14" font-weight="bold" fill="#222">{r["name"]}</text>'
        svg += f'<text x="{x+w/2}" y="{y+h-14}" text-anchor="middle" font-family="Arial" font-size="11" fill="#555">{r["w"]:.1f}×{r["h"]:.1f}m</text>'
    
    # 2. Draw walls between adjacent rooms
    for i, r1 in enumerate(rooms):
        for r2 in rooms[i+1:]:
            # Check if rooms share a wall
            if abs(r1["x"] + r1["w"] - r2["x"]) < 0.1:  # r1 right touches r2 left
                # Shared vertical wall
                x = (r1["x"] + r1["w"]) * scale + padding
                y1 = max(r1["y"], r2["y"]) * scale + padding
                y2 = min(r1["y"] + r1["h"], r2["y"] + r2["h"]) * scale + padding
                # Draw wall with door gap
                if y2 - y1 > 20:
                    svg += f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y1 + (y2-y1)*0.3}" stroke="#666" stroke-width="3"/>'
                    svg += f'<line x1="{x}" y1="{y1 + (y2-y1)*0.7}" x2="{x}" y2="{y2}" stroke="#666" stroke-width="3"/>'
                    # Door arc
                    svg += f'<path d="M{x},{y1 + (y2-y1)*0.3} Q{x+15},{y1 + (y2-y1)*0.5} {x},{y1 + (y2-y1)*0.7}" stroke="#444" stroke-width="1.5" fill="none" stroke-dasharray="3,3"/>'
    
    # 3. Exterior walls (top, bottom, left, right)
    min_x = min(r["x"] for r in rooms) * scale + padding
    max_x_wall = max(r["x"] + r["w"] for r in rooms) * scale + padding
    min_y = min(r["y"] for r in rooms) * scale + padding
    max_y_wall = max(r["y"] + r["h"] for r in rooms) * scale + padding
    
    # Exterior walls (thicker)
    svg += f'<rect x="{min_x-3}" y="{min_y-3}" width="{(max_x_wall - min_x) + 6}" height="{(max_y_wall - min_y) + 6}" fill="none" stroke="#333" stroke-width="4" rx="3"/>'
    
    # 4. Dimensions (along bottom edge)
    svg += f'''
    <line x1="{min_x}" y1="{max_y_wall + 20}" x2="{max_x_wall}" y2="{max_y_wall + 20}" stroke="#666" stroke-width="1" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <text x="{min_x + (max_x_wall - min_x)/2}" y="{max_y_wall + 35}" text-anchor="middle" font-family="Arial" font-size="12" fill="#666">
        Overall: {((max_x_wall - min_x) / scale):.1f}m
    </text>
    '''
    
    # 5. Scale bar
    scale_bar_len = 50  # pixels
    meters = scale_bar_len / scale
    svg += f'''
    <rect x="{padding}" y="{padding + 5}" width="{scale_bar_len}" height="4" fill="#333"/>
    <text x="{padding}" y="{padding + 20}" font-family="Arial" font-size="10" fill="#666">{meters:.1f}m</text>
    <text x="{padding + scale_bar_len}" y="{padding + 20}" font-family="Arial" font-size="10" fill="#666" text-anchor="end">Scale</text>
    '''
    
    # 6. North arrow
    svg += f'''
    <g transform="translate({padding + 60}, {padding + 30})">
        <polygon points="0,-12 4,4 -4,4" fill="#333"/>
        <polygon points="0,-12 2,2 -2,2" fill="#666"/>
        <text x="0" y="-16" text-anchor="middle" font-family="Arial" font-size="10" fill="#333" font-weight="bold">N</text>
    </g>
    '''
    
    svg += '</svg>'
    return svg