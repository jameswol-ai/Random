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

    def mutate(self, rate=0.1): 
        for room in self.rooms: 
            if random.random() < rate: 
                room["width"] += random.gauss(0, 0.5) 
                room["height"] += random.gauss(0, 0.5) 
                room["x"] += random.gauss(0, 0.3) 
                room["y"] += random.gauss(0, 0.3) 
                room["width"] = max(2.0, min(10.0, room["width"])) 
                room["height"] = max(2.0, min(10.0, room["height"])) 
        if random.random() < rate * 0.5: 
            # shift a random column
            pass