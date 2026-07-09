import pytest
from src.evolution import crossover, evaluate_design, pareto_front
from src.design_generator import generate_design

def test_crossover():
    p1 = generate_design("Luxury Villa", 4, num_floors=2)
    p2 = generate_design("Luxury Villa", 4, num_floors=2)
    child = crossover(p1, p2)
    assert len(child["floors"]) == 2
    # Verify at least one floor differs from p1
    assert any(child["floors"][i] != p1["floors"][i] for i in range(2))

def test_pareto_front():
    d1 = {"fitness": {"a":80,"b":70}, "score":75}
    d2 = {"fitness": {"a":90,"b":60}, "score":75}
    d3 = {"fitness": {"a":70,"b":80}, "score":75}
    front = pareto_front([d1, d2, d3])
    assert len(front) == 3  # all non-dominated
