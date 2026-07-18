def generate_floor_plan(design):
    rooms = [
        {"name": "Living", "w": 6.5, "h": 5.0, "color": "#1e3a8a"},
        {"name": "Kitchen", "w": 4.5, "h": 4.0, "color": "#064e3b"},
        {"name": "Bath", "w": 3.0, "h": 2.5, "color": "#78350f"}
    ]
    for i in range(design["bedrooms"]):
        rooms.append({
            "name": f"Bedroom {i+1}",
            "w": 4.5,
            "h": 4.0,
            "color": "#4c1d95"
        })
    return rooms