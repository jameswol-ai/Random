import random

class BuildingGenome:
    def __init__(self):
        self.columns = random.randint(10, 40)
        self.beams = random.randint(20, 80)
        self.area = random.randint(100, 500)
        self.rooms = random.randint(3, 10)

    def mutate(self):
        self.columns += random.randint(-2, 3)
        self.beams += random.randint(-3, 4)
        self.area += random.randint(-20, 40)