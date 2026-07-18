import random

ROOM_SIZES = {
    "Living": (6.0, 5.0),
    "Kitchen": (4.0, 3.5),
    "Bathroom": (3.0, 2.5),
    "Bedroom": (4.5, 4.0),
    "Flex": (4.0, 3.5)
}

ROOM_COLORS = {
    "Living": "#e3f2fd",
    "Kitchen": "#fff3e0",
    "Bathroom": "#e8f5e9",
    "Bedroom": "#f3e5f5",
    "Flex": "#fce4ec"
}

def generate_floor_plan(design):
    """Generate rooms with positions, including a central corridor."""
    bedrooms = design.get("bedrooms", 3)
    rooms = []
    
    # Core rooms
    for name in ["Living", "Kitchen", "Bathroom"]:
        w, h = ROOM_SIZES[name]
        rooms.append({"name": name, "w": w, "h": h, "color": ROOM_COLORS[name]})
    
    # Bedrooms
    for i in range(bedrooms):
        w, h = ROOM_SIZES["Bedroom"]
        rooms.append({"name": f"Bedroom {i+1}", "w": w, "h": h, "color": ROOM_COLORS["Bedroom"]})
    
    # Flex rooms
    num_flex = random.randint(1, 3)
    for i in range(num_flex):
        w, h = ROOM_SIZES["Flex"]
        rooms.append({"name": f"Flex {i+1}", "w": w, "h": h, "color": ROOM_COLORS["Flex"]})
    
    # Pack with corridor
    return pack_with_corridor(rooms, max_width=20.0)

def pack_with_corridor(rooms, max_width=20.0, corridor_width=1.2):
    """
    Pack rooms on both sides of a central corridor.
    Returns rooms with x, y assigned.
    """
    # Sort rooms by height for balanced packing
    rooms_sorted = sorted(rooms, key=lambda r: r["h"], reverse=True)
    
    # Split into left and right sides
    left_side = []
    right_side = []
    total_width = 0
    
    for r in rooms_sorted:
        if total_width + r["w"] <= max_width / 2:
            left_side.append(r)
        else:
            right_side.append(r)
        total_width += r["w"] + 0.3
    
    # Pack left side (starts at x=0)
    left_packed = pack_shelf(left_side, start_x=0.5)
    # Pack right side (starts after corridor)
    right_packed = pack_shelf(right_side, start_x=corridor_width + 1.0)
    
    # Combine
    return left_packed + right_packed

def pack_shelf(rooms, start_x=0.0):
    """Shelf packing starting from a given x offset."""
    packed = []
    y = 0.5
    row_height = 0.0
    x = start_x
    
    for r in rooms:
        if x + r["w"] > 10.0:  # max width per side
            x = start_x
            y += row_height + 0.5
            row_height = 0.0
        
        r["x"] = x
        r["y"] = y
        packed.append(r)
        row_height = max(row_height, r["h"])
        x += r["w"] + 0.3
    
    return packed