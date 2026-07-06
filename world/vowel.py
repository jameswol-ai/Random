import numpy as np

class VoxelWorld:
    def __init__(self, size=30):
        self.size = size
        self.grid = np.zeros((size, size, size), dtype=int)

    def set(self, x, y, z, value):
        self.grid[x, y, z] = value

    def get(self, x, y, z):
        return self.grid[x, y, z]

    def update(self):
        # placeholder for physics hooks
        pass