def calculate_fitness(genome, population):
    raw_scores = {
        "stability": compute_stability(genome),
        "cost_efficiency": 1.0 - (compute_cost(genome) / max_cost_in_population),
        "complexity": compute_complexity(genome) / max_complexity_in_population
    }
    
    # Weighted sum (weights can be user‑adjusted in the UI)
    weights = {"stability": 0.4, "cost_efficiency": 0.4, "complexity": 0.2}
    genome.fitness = sum(raw_scores[k] * weights[k] for k in weights)
    genome.objectives = raw_scores  # store for Pareto analysis
    return genome.fitness