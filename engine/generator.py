import random
import uuid

def generate_base_design(btype="Residential", bedrooms=3):
    """
    Generate a flat design dictionary with top-level keys.
    No nested 'structure' or other sub-dictionaries.
    """
    area = 65 + 44 + (bedrooms * 18)
    columns = random.randint(14, 36)
    beams = random.randint(28, 72)
    
    # Generate room list with random sizes
    room_names = ["Living", "Kitchen", "Bathroom"] + ["Flex"] * random.randint(1, 3)
    rooms = []
    for name in room_names:
        rooms.append({
            "name": name,
            "w": round(random.uniform(3.0, 6.0), 1),
            "h": round(random.uniform(3.0, 5.0), 1)
        })
    
    return {
        "id": str(uuid.uuid4())[:8],
        "type": btype,
        "bedrooms": bedrooms,
        "area_sqm": area,
        "columns": columns,
        "beams": beams,
        "cost": area * 800,
        "rooms": rooms,
        "score": 0.0
    }

def mutate_design(d):
    """
    Mutate a flat design dictionary.
    """
    d = d.copy()
    d["columns"] += random.randint(-2, 2)
    d["beams"] += random.randint(-4, 4)
    d["area_sqm"] += random.randint(-20, 40)
    d["area_sqm"] = max(50, d["area_sqm"])
    d["columns"] = max(10, min(40, d["columns"]))
    d["beams"] = max(20, min(80, d["beams"]))
    
    if "rooms" in d:
        for room in d["rooms"]:
            if random.random() < 0.1:
                room["w"] += random.gauss(0, 0.5)
                room["h"] += random.gauss(0, 0.5)
                room["w"] = max(2.0, min(10.0, room["w"]))
                room["h"] = max(2.0, min(10.0, room["h"]))
    
    return d