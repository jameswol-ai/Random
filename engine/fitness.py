def calculate_fitness(d):
    # Structural score: favour a beam:column ratio near 2.1
    if d["columns"] == 0:
        structural = 0
    else:
        ratio = d["beams"] / d["columns"]
        structural = 1.0 - min(abs(ratio - 2.1) / 2.1, 1.0)
    
    # Cost score: ideal cost per sqm ≈ 1650
    cost_per_sqm = d.get("cost", 0) / d.get("area", 1)
    cost = 1.0 - min(abs(cost_per_sqm - 1650) / 1650, 1.0)
    
    # Complexity score: more rooms is better (up to 6)
    complexity = min(d["rooms"] / 6.0, 1.0)
    
    # Average the three scores
    return (structural + cost + complexity) / 3.0