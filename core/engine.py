from analytics.fitness import calculate_fitness, aggregate_score
from core.genetics import generate_base_design, mutate_design


def run_evolutionary_loop(btype, bedrooms, generations, pop_size, new_id):
    population = [
        generate_base_design(btype, bedrooms, new_id)
        for _ in range(pop_size)
    ]

    history = []

    for _ in range(generations):

        scored = []
        for d in population:
            fit = calculate_fitness(d)
            d["fitness"] = fit
            d["score"] = aggregate_score(fit)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        history.append(scored[0]["score"])

        survivors = scored[:max(2, pop_size // 2)]

        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate_design(s))

        population = new_pop[:pop_size]

    return scored[0], history