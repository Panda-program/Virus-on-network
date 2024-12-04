import random
class Map:
    def __init__(self):
        self.width = 700
        self.height = 700
        self.tileSize = 70
        self.tiles = [[[] for _ in range(10)] for _ in range(10)]