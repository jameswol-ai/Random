import random
import uuid
import json

def domain_lookup(ARCH, t):
    for k, v in ARCH.items():
        if t in v:
            return k
    return "Unknown"


def generate_base(ARCH, t, beds, dna):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": t,
        "domain": domain_lookup(ARCH, t),
        "bedrooms": beds,
        "area": 120 + beds * 18,
        "structure": {
            "columns": int(random.gauss(dna["avg_columns"], 3)),
            "beams": int(random.gauss(dna["avg_beams"], 6))
        }
    }


def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] += random.randint(-3, 4)
    d["structure"]["beams"] += random.randint(-5, 6)
    return d