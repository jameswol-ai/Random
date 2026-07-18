# agents/agent.py — only 162 bytes

class Agent:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]

    def update(self, world):
        # simple wander behavior
        self.pos[0] += 1