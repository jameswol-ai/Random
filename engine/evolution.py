import random
from engine.generator import generate_base_design, mutate_design
from engine.fitness import calculate_fitness, score

def run_evolution(btype="Residential", bedrooms=3, gens=2, pop_size=5):
    """
    Run evolutionary optimisation with flat dictionaries.
    """
    # Safety caps for Vercel
    gens = min(gens, 5)
    pop_size = min(pop_size, 15)
    
    # Generate initial population
    population = [generate_base_design(btype, bedrooms) for _ in range(pop_size)]
    
    # Evolution loop
    for gen in range(gens):
        # Evaluate fitness for all individuals
        for d in population:
            f = calculate_fitness(d)
            d["score"] = score(f)
        
        # Sort by score (descending)
        population.sort(key=lambda x: x["score"], reverse=True)
        
        # Elitism: keep top half
        survivors = population[:max(2, pop_size // 2)]
        
        # Create next generation
        next_gen = survivors.copy()
        while len(next_gen) < pop_size:
            parent = random.choice(survivors)
            child = mutate_design(parent)
            next_gen.append(child)
        
        population = next_gen[:pop_size]
    
    # Return best design
    best = max(population, key=lambda x: x["score"])
    history = [d["score"] for d in population]
    
    return best, history