from .base import BaseAgent

class CostAgent(BaseAgent):
    name = "Cost Engineer"

    def analyze(self, d):
        cost_per_sqm = d["cost"] / max(1, d["area_sqm"])

        if cost_per_sqm < 1400:
            score = 75
            note = "Budget-efficient but may undercut material quality."
        elif cost_per_sqm <= 2000:
            score = 92
            note = "Optimal cost balance for construction viability."
        else:
            score = 55
            note = "High-cost structure. Value efficiency questionable."

        return {"agent": self.name, "score": score, "notes": note}