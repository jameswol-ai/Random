import random 
from core.utils import uid 
# from core.config import ARCH_DOMAINS
ARCH_DOMAINS = {
    "Residential": ["Villa", "Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}
def get_domain(btype): 
    for d, items in ARCH_DOMAINS.items(): 
        if btype in items: 
            return d 
    return "Unknown" 

def generate_base_design(btype="Residential", bedrooms=3):
    import random
    area = 65 + 44 + (bedrooms * 18)
    columns = random.randint(14, 36)
    beams = random.randint(28, 72)
    # Build room list (flat for now – we'll generate plan later)
    room_names = ["Living", "Kitchen", "Bathroom"] + ["Flex"] * random.randint(1, 3)
    rooms = [{"name": n, "w": random.uniform(3, 6), "h": random.uniform(3, 5)} for n in room_names]
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
    import random
    d = d.copy()
    d["columns"] += random.randint(-2, 2)
    d["beams"] += random.randint(-4, 4)
    d["area_sqm"] += random.randint(-20, 40)
    d["area_sqm"] = max(50, d["area_sqm"])
    if "rooms" in d:
        for room in d["rooms"]:
            if random.random() < 0.1:
                room["w"] += random.gauss(0, 0.5)
                room["h"] += random.gauss(0, 0.5)
                room["w"] = max(2.0, min(10.0, room["w"]))
                room["h"] = max(2.0, min(10.0, room["h"]))
    return d
