# engine/evolution.py (modified)

import random
from engine.generator import generate_base_design
from engine.fitness import calculate_fitness, score
from engine.generator import generate_base_design, mutate_design


def run_evolution(btype="Residential", bedrooms=3, gens=5, pop_size=20):
    gens = min(gens, 5)          # never more than 5
    pop_size = min(pop_size, 15) # never more than 15
    # ... rest of code
    # Generate initial population
    population = []
    for _ in range(pop_size):
        d = generate_base_design(btype, bedrooms)
        population.append(d)
    
    history = []
    for _ in range(gens):
        for d in population:
            # Compute fitness and store in d
            f = calculate_fitness(d)
            d["score"] = score(f)
        population.sort(key=lambda x: x["score"], reverse=True)
        history.append(population[0]["score"])
        survivors = population[:max(2, pop_size // 2)]
        # Mutate survivors to fill the population
        next_gen = survivors.copy()
        while len(next_gen) < pop_size:
            parent = random.choice(survivors)
            child = parent.copy()
            # Mutate (need a mutate function; we can use the one from genome or a simple random tweak)
            # For simplicity, we'll call a mutate_design function
            from engine.generator import mutate_design  # you'll need to implement this
            child = mutate_design(child)
            next_gen.append(child)
        population = next_gen[:pop_size]
    
    best = population[0]
    # Ensure it has an id
    if "id" not in best:
        import uuid
        best["id"] = str(uuid.uuid4())[:8]
    return best, history