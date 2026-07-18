def mutate_design(d):
    # Mutate structural elements (small integer changes)
    if random.random() < 0.3:
        d["columns"] += random.randint(-2, 2)
        d["columns"] = max(10, min(40, d["columns"]))
    if random.random() < 0.3:
        d["beams"] += random.randint(-4, 4)
        d["beams"] = max(20, min(80, d["beams"]))
    
    # Room‑level mutation (if rooms are stored as a list)
    if "rooms" in d:
        for room in d["rooms"]:
            if random.random() < 0.1:
                room["width"] += random.gauss(0, 0.5)
                room["height"] += random.gauss(0, 0.5)
                room["width"] = max(2.0, min(10.0, room["width"]))
                room["height"] = max(2.0, min(10.0, room["height"]))
    return d