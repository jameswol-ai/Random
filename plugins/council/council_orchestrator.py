from plugins.council.structural_agent import StructuralAgent
from plugins.council.cost_agent import CostAgent
from plugins.council.spatial_agent import SpatialAgent
from plugins.council.aesthetic_agent import AestheticAgent

class ArchitectureCouncil:

    def __init__(self):
        self.agents = [
            StructuralAgent(),
            CostAgent(),
            SpatialAgent(),
            AestheticAgent()
        ]

    def evaluate(self, design: dict) -> dict:
        results = []
        scores = []

        for agent in self.agents:
            r = agent.analyze(design)
            results.append(r)
            scores.append(r["score"])

        avg_score = int(sum(scores) / len(scores))

        return {
            "agent_reports": results,
            "final_score": avg_score,
            "verdict": self._verdict(avg_score)
        }

    def _verdict(self, score):
        if score >= 85:
            return "🟢 COUNCIL APPROVES DESIGN"
        elif score >= 70:
            return "🟡 APPROVED WITH MODIFICATIONS"
        return "🔴 REJECTED BY COUNCIL"