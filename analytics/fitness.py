
def calculate_fitness(d):
    structural_ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    struct_score = max(0, 100 - int(abs(structural_ratio - 2.1) * 22))

    cost_per_sqm = d["cost"] / max(1, d["area_sqm"])
    cost_score = max(0, 100 - int(abs(cost_per_sqm - 1650) * 0.04))

    complexity_score = min(100, len(d["rooms"]) * 9)

    return {
        "structural_integrity": struct_score,
        "cost_efficiency": cost_score,
        "spatial_complexity": complexity_score
    }


def aggregate_score(fit):
    return int(sum(fit.values()) / len(fit))