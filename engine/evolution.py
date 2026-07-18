# engine/evolution.py (modified)

import random
from engine.generator import generate_base_design
from engine.fitness import calculate_fitness, score
from engine.generator import generate_base_design, mutate_design


from engine.generator import generate_base_design, mutate_design

def run_evolution(btype="Residential", bedrooms=3, gens=2, pop_size=5):
    gens = min(gens, 5)
    pop_size = min(pop_size, 15)
    population = [generate_base_design(btype, bedrooms) for _ in range(pop_size)]
    for _ in range(gens):
        for d in population:
            f = calculate_fitness(d)
            d["score"] = score(f)
        population.sort(key=lambda x: x["score"], reverse=True)
        survivors = population[:max(2, pop_size // 2)]
        next_gen = survivors.copy()
        while len(next_gen) < pop_size:
            parent = random.choice(survivors)
            child = mutate_design(parent)
            next_gen.append(child)
        population = next_gen[:pop_size]
    best = max(population, key=lambda x: x["score"])
    return best, [d["score"] for d in population] generate_base_design(btype, bedrooms)
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