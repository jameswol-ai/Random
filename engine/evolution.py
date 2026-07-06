import json
import random
from engine.fitness import calculate_fitness, score
from engine.generator import generate_base_design

from plugins.structural_critic import StructuralCritic

def mutate(d):
    d = json.loads(json.dumps(d))

    d["structure"]["columns"] = max(10, d["structure"]["columns"] + random.randint(-2, 4))
    d["structure"]["beams"] = max(16, d["structure"]["beams"] + random.randint(-4, 6))

    if random.random() > 0.5:
        d["rooms"].append("Adaptive Module")
        d["area_sqm"] += 20

    d["cost"] = int(d["area_sqm"] * random.randint(1300, 2500))
    return d

def run_evolution(btype, bedrooms, generations, pop_size):
    pop = [generate_base_design(btype, bedrooms) for _ in range(pop_size)]
    history = []

    for _ in range(generations):
        scored = []

        for d in pop:
            f = calculate_fitness(d)
            d["fitness"] = f
            d["score"] = score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop_size // 2)]

        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate(s))

        pop = new_pop[:pop_size]

    return scored[0], history