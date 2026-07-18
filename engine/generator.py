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

def generate_base_design(btype, bedrooms): 
    rooms = ["Living", "Kitchen", "Bathroom"] + ["Flex"] * random.randint(1, 3) 
    area = 65 + 44 + (bedrooms * 18) 
    return {
        "id": uid(), 
        "type": btype, 
        "domain": get_domain(btype), 
        "bedrooms": bedrooms, 
        "rooms": rooms, 
        "area_sqm": area, 
        "structure": {
            "columns": random.randint(14, 36), 
            "beams": random.randint(28, 72)
        }, 
        "cost": 0 
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