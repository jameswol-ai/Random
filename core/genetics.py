import random
import json

from domain.typologies import get_domain


def generate_base_design(btype, bedrooms, new_id):
    core_rooms = ["Living Room", "Gourmet Kitchen", "Primary Bathroom"] + ["Flex Space"] * random.randint(1, 3)

    est_area = 65 + 44 + (bedrooms * 18)

    return {
        "id": new_id(),
        "type": btype,
        "domain": get_domain(btype),
        "bedrooms": bedrooms,
        "rooms": core_rooms,
        "area_sqm": est_area,
        "structure": {
            "columns": random.randint(14, 36),
            "beams": random.randint(28, 72)
        },
        "cost": 0
    }


def mutate_design(design):
    d = json.loads(json.dumps(design))

    d["structure"]["columns"] = max(
        10, d["structure"]["columns"] + random.randint(-2, 4)
    )

    d["structure"]["beams"] = max(
        16, d["structure"]["beams"] + random.randint(-4, 6)
    )

    if random.random() > 0.5:
        d["rooms"].append("Adaptive Modular Terracing")
        d["area_sqm"] += 20

    d["cost"] = int(d["area_sqm"] * random.randint(1300, 2500))
    return d