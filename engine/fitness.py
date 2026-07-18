def calculate_fitness(d):
    """
    Calculate fitness scores using flat keys.
    """
    # Structural: favor beam:column ratio around 2.1
    ratio = d["beams"] / max(1, d["columns"])
    structural = max(0, 100 - abs(ratio - 2.1) * 22)
    
    # Cost: ideal cost per sqm ~ 1650
    cost_per_sqm = d["cost"] / max(1, d["area_sqm"])
    cost_score = max(0, 100 - abs(cost_per_sqm - 1650) * 0.04)
    
    # Complexity: more rooms is better (up to 10 rooms)
    complexity = min(100, len(d["rooms"]) * 9)
    
    return {
        "structural": structural,
        "cost": cost_score,
        "complexity": complexity
    }

def score(fitness_dict):
    """
    Average the fitness scores into a single number.
    """
    return int(sum(fitness_dict.values()) / len(fitness_dict))