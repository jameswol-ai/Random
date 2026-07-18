def generate_random_genome(params):
    genome = BuildingGenome()
    
    # Random number of rooms (e.g., 3–8)
    num_rooms = random.randint(params["min_rooms"], params["max_rooms"])
    
    # Generate rooms with random sizes and positions
    rooms = []
    for i in range(num_rooms):
        w = random.uniform(3.0, 8.0)   # width in meters
        h = random.uniform(3.0, 8.0)   # height in meters
        x = random.uniform(0, 20)      # x coordinate
        y = random.uniform(0, 20)      # y coordinate
        room = {
            "id": f"R{i+1}",
            "name": random.choice(["Living", "Bedroom", "Kitchen", "Bath", "Study"]),
            "x": x, "y": y,
            "width": w, "height": h
        }
        rooms.append(room)
    
    genome.rooms = rooms
    genome.columns = generate_random_columns(rooms)  # place columns in corners
    genome.beams = generate_random_beams(rooms)      # connect columns
    
    return genome