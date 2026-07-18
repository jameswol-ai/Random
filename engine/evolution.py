import random

def fitness(d):
    r = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    stability = max(0, 100 - abs(r - 2.2) * 25)
    density = min(100, (d["structure"]["columns"] + d["structure"]["beams"]) / 1.2)
    efficiency = max(0, 100 - abs(d["area"] / 150 - 1) * 30)

    return (stability + density + efficiency) / 3


def evolve(population, gens=5, pop_size=20):
    for gen in range(gens):
        # 1. Evaluate fitness for every individual
        for d in population:
            d["score"] = calculate_fitness(d)
        
        # 2. Sort by score (highest first)
        population.sort(key=lambda x: x["score"], reverse=True)
        
        # 3. Keep top 50% as survivors (elitism)
        survivors = population[:pop_size // 2]
        
        # 4. Build next generation
        next_gen = survivors.copy()
        while len(next_gen) < pop_size:
            # Pick two random survivors and mutate one
            parent = random.choice(survivors)
            child = parent.copy()
            child = mutate_design(child)
            next_gen.append(child)
        
        population = next_gen
    
    return population
        population.sort(key=lambda x: x["score"], reverse=True)
        history.append(population[0]["score"])

        survivors = population[:max(2, pop_size // 2)]

        population = survivors + [
            mutate_fn(random.choice(survivors))
            for _ in survivors
        ]

        population = population[:pop_size]

    return population[0], history