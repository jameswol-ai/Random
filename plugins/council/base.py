class BaseAgent:
    name = "BaseAgent"

    def analyze(self, design: dict) -> dict:
        return {
            "agent": self.name,
            "score": 0,
            "notes": "Not implemented"
        }