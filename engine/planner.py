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
    """
    Generate a floor plan with room positions.
    Uses shelf packing algorithm.
    """
    rooms = design.get("rooms", [])
    bedrooms = design.get("bedrooms", 3)
    
    # Build room list with proper sizes
    room_list = []
    
    # Core rooms
    for name in ["Living", "Kitchen", "Bathroom"]:
        w, h = ROOM_SIZES[name]
        room_list.append({
            "name": name,
            "w": w,
            "h": h,
            "color": ROOM_COLORS[name]
        })
    
    # Bedrooms
    for i in range(bedrooms):
        w, h = ROOM_SIZES["Bedroom"]
        room_list.append({
            "name": f"Bedroom {i+1}",
            "w": w,
            "h": h,
            "color": ROOM_COLORS["Bedroom"]
        })
    
    # Flex rooms
    num_flex = max(1, len(rooms) - 3 - bedrooms)
    num_flex = min(num_flex, 3)
    for i in range(num_flex):
        w, h = ROOM_SIZES["Flex"]
        room_list.append({
            "name": f"Flex {i+1}",
            "w": w,
            "h": h,
            "color": ROOM_COLORS["Flex"]
        })
    
    # Pack them using shelf algorithm
    return pack_rooms(room_list, max_width=20.0)

def pack_rooms(rooms, max_width=20.0):
    """
    Pack rooms into a strip using shelf algorithm.
    Returns rooms with x, y coordinates.
    """
    # Sort by width descending
    rooms_sorted = sorted(rooms, key=lambda r: r["w"], reverse=True)
    packed = []
    y = 0.5
    row_height = 0.0
    x = 0.5
    
    for r in rooms_sorted:
        # Check if room fits on current row
        if x + r["w"] > max_width:
            x = 0.5
            y += row_height + 0.5
            row_height = 0.0
        
        # Place room
        r["x"] = x
        r["y"] = y
        packed.append(r)
        
        # Update row height
        row_height = max(row_height, r["h"])
        x += r["w"] + 0.3
    
    return packed