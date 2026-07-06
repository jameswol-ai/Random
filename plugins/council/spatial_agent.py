from .base import BaseAgent

class SpatialAgent(BaseAgent):
    name = "Spatial Planner"

    def analyze(self, d):
        rooms = len(d["rooms"])

        if rooms < 4:
            score = 60
            note = "Low spatial diversity."
        elif rooms <= 7:
            score = 90
            note = "Strong functional zoning."
        else:
            score = 72
            note = "Over-segmentation risk in circulation paths."

        return {"agent": self.name, "score": score, "notes": note}