import numpy as np
import random

def voxelize(d, size):
    world = np.zeros(size)

    cx, cz = size[0]//2, size[2]//2

    for _ in range(d["structure"]["columns"]):
        x = cx + random.randint(-8, 8)
        z = cz + random.randint(-8, 8)
        h = random.randint(2, 8)

        for y in range(h):
            if 0 <= x < size[0] and 0 <= z < size[2]:
                world[x, y, z] = 1

    for _ in range(d["structure"]["beams"]):
        x = random.randint(0, size[0]-1)
        z = random.randint(0, size[2]-1)
        y = random.randint(2, 6)
        world[x, y, z] = 2

    return world


def analyze(world):
    return {
        "solid": int((world == 1).sum()),
        "beams": int((world == 2).sum()),
        "density": float((world > 0).sum() / world.size)
    }