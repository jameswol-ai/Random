import random, numpy as np
from .design_generator import generate_design, mutate, evaluate_design, total_score

def crossover(parent1, parent2):
    """Swap a random floor between two parents."""
    child = json.loads(json.dumps(parent1))
    if len(child["floors"]) > 1 and len(parent2["floors"]) > 1:
        swap_idx = random.randint(0, len(child["floors"])-1)
        # ensure both have enough floors
        if swap_idx < len(parent2["floors"]):
            child["floors"][swap_idx] = json.loads(json.dumps(parent2["floors"][swap_idx]))
    return child

def evolve_design_multi(building, modules, generations, population_size, num_floors=None, use_crossover=True):
    population = [generate_design(building, modules, num_floors) for _ in range(population_size)]
    history = []
    for gen in range(generations):
        for d in population:
            d["fitness"] = evaluate_design(d)
            d["score"] = total_score(d["fitness"])
        population.sort(key=lambda x: x["score"], reverse=True)
        history.append(population[0]["score"])
        # tournament selection
        survivors = tournament_select(population, tournament_size=3, num_survivors=population_size//2)
        next_pop = []
        for parent in survivors:
            next_pop.append(parent)
            if use_crossover and random.random() < 0.5:
                partner = random.choice(survivors)
                child = crossover(parent, partner)
            else:
                child = mutate(parent)
            next_pop.append(child)
        population = next_pop[:population_size]
    # final evaluation
    for d in population:
        d["fitness"] = evaluate_design(d)
        d["score"] = total_score(d["fitness"])
    return population[0], history, population

def tournament_select(population, tournament_size=3, num_survivors=5):
    selected = []
    for _ in range(num_survivors):
        contestants = random.sample(population, min(tournament_size, len(population)))
        winner = max(contestants, key=lambda x: x["score"])
        selected.append(winner)
    return selected

def pareto_front(designs):
    nondominated = []
    for i, d1 in enumerate(designs):
        dominated = False
        for j, d2 in enumerate(designs):
            if i == j: continue
            f1 = d1["fitness"]
            f2 = d2["fitness"]
            if all(f2[k] >= f1[k] for k in f1) and any(f2[k] > f1[k] for k in f1):
                dominated = True
                break
        if not dominated:
            nondominated.append(d1)
    return nondominated
