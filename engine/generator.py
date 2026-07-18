import random 
from core.utils import uid 
from core.config import ARCH_DOMAINS 

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