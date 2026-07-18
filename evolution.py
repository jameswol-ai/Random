def evolve_population(initial_population, generations, population_size):
    if not initial_population:
        population = [generate_random_genome() for _ in range(population_size)]
    else:
        population = initial_population
    
    for gen in range(generations):
        # 1. Evaluate fitness for ALL individuals
        for genome in population:
            calculate_fitness(genome, population)
        
        # 2. Sort by fitness (or by Pareto rank)
        population.sort(key=lambda g: g.fitness, reverse=True)
        
        # 3. Selection: Keep top 20% as elites (elitism)
        elite_count = int(len(population) * 0.2)
        elites = population[:elite_count]
        
        # 4. Create next generation
        next_gen = elites.copy()
        
        # 5. Fill remaining slots with offspring
        while len(next_gen) < population_size:
            # Tournament selection: pick two parents from the top 50%
            parent1 = tournament_select(population, k=3)
            parent2 = tournament_select(population, k=3)
            
            # Crossover (if implemented) or just clone + mutate
            child = crossover(parent1, parent2) if random.random() < 0.7 else parent1.clone()
            
            # Mutation
            child.mutate(rate=0.1)
            
            next_gen.append(child)
        
        population = next_gen
    
    return population