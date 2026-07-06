from .base import BaseAgent

class StructuralAgent(BaseAgent):
    name = "Structural Engineer"

    def analyze(self, d):
        ratio = d["structure"]["beams"] / max(1, d["structure"]["columns"])

        if ratio < 1.6:
            score = 45
            note = "Undersupported beam network. Structural risk."
        elif ratio <= 2.6:
            score = 88
            note = "Balanced load distribution. Structurally sound."
        else:
            score = 65
            note = "Over-engineered framing. Material inefficiency."

        return {"agent": self.name, "score": score, "notes": note}