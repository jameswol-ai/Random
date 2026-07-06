import json
import random
from engine.fitness import calculate_fitness, score
from engine.generator import generate_base_design

from plugins.structural_critic import StructuralCritic

from plugins.council.council_orchestrator import ArchitectureCouncil
council = ArchitectureCouncil()

for d in pop:
    f = calculate_fitness(d)
    d["fitness"] = f

    base_score = score(f)

    # 🧠 COUNCIL EVALUATION
    review = council.evaluate(d)
    d["council"] = review

    # blended intelligence
    d["score"] = int((base_score + review["final_score"]) / 2)

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

        critic = StructuralCritic()

for d in pop:
    f = calculate_fitness(d)
    d["fitness"] = f
    d["score"] = score(f)

    # 🧠 NEW: AI critique layer
    critique = critic.analyze(d)
    d["critique"] = critique

    # blend AI judgment into evolution score
    d["score"] = int((d["score"] + critique["scores"]["overall"]) / 2)