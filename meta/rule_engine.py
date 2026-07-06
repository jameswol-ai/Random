RULES = {
    "spawn_rate": 1.0,
    "gravity": 1.0,
    "urban_pressure": 0.5
}

def evolve_rules(stats):
    global RULES

    if stats["density"] > 0.7:
        RULES["spawn_rate"] *= 0.95

    if stats["buildings"] > 200:
        RULES["urban_pressure"] += 0.02

    if stats["water"] < 50:
        RULES["gravity"] *= 1.01