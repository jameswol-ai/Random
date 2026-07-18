def calculate_fitness(d):
    ratio = d["beams"] / max(1, d["columns"])
    structural = max(0, 100 - abs(ratio - 2.1) * 22)
    cost_per_sqm = d["cost"] / max(1, d["area_sqm"])
    cost = max(0, 100 - abs(cost_per_sqm - 1650) * 0.04)
    complexity = min(100, len(d["rooms"]) * 9)
    return {"structural": structural, "cost": cost, "complexity": complexity}

def score(f):
    return int(sum(f.values()) / len(f))