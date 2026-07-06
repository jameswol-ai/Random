import random

def fitness(d):
    r = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    stability = max(0, 100 - abs(r - 2.2) * 25)
    density = min(100, (d["structure"]["columns"] + d["structure"]["beams"]) / 1.2)
    efficiency = max(0, 100 - abs(d["area"] / 150 - 1) * 30)

    return (stability + density + efficiency) / 3


def evolve(population, gens, pop_size, generator, mutate_fn):
    history = []

    for _ in range(gens):
        for d in population:
            d["score"] = fitness(d)

        population.sort(key=lambda x: x["score"], reverse=True)
        history.append(population[0]["score"])

        survivors = population[:max(2, pop_size // 2)]

        population = survivors + [
            mutate_fn(random.choice(survivors))
            for _ in survivors
        ]

        population = population[:pop_size]

    return population[0], history