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

def pack_rooms(rooms, max_width=20.0):
    """Pack rooms into a strip using shelf algorithm."""
    # Sort by width descending
    rooms_sorted = sorted(rooms, key=lambda r: r["w"], reverse=True)
    packed = []
    y = 0.0
    row_height = 0.0
    x = 0.0
    for r in rooms_sorted:
        if x + r["w"] > max_width:
            x = 0.0
            y += row_height + 0.5
            row_height = 0.0
        r["x"] = x
        r["y"] = y
        packed.append(r)
        row_height = max(row_height, r["h"])
        x += r["w"] + 0.3
    return packed

def generate_floor_plan(design):
    bedrooms = design.get("bedrooms", 3)
    rooms = []
    for name in ["Living", "Kitchen", "Bathroom"]:
        w, h = ROOM_SIZES[name]
        rooms.append({
            "name": name,
            "w": w,
            "h": h,
            "color": ROOM_COLORS[name]
        })
    for i in range(bedrooms):
        w, h = ROOM_SIZES["Bedroom"]
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": w,
            "h": h,
            "color": ROOM_COLORS["Bedroom"]
        })
    num_flex = random.randint(1, 3)
    for i in range(num_flex):
        w, h = ROOM_SIZES["Flex"]
        rooms.append({
            "name": f"Flex {i+1}",
            "w": w,
            "h": h,
            "color": ROOM_COLORS["Flex"]
        })
    return pack_rooms(rooms, max_width=20.0)