from .base import BaseAgent

class AestheticAgent(BaseAgent):
    name = "Architectural Aesthetic"

    def analyze(self, d):
        complexity = len(d["rooms"])

        if complexity < 4:
            score = 65
            note = "Minimalist composition, but lacks depth."
        elif complexity <= 7:
            score = 88
            note = "Balanced spatial rhythm and hierarchy."
        else:
            score = 70
            note = "Visually dense layout. Risk of design clutter."

        return {"agent": self.name, "score": score, "notes": note}