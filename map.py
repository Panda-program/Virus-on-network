import random
from node import Node, State

class Map:
    def __init__(self):
        self.width = 700
        self.height = 700
        self.tileSize = 70
        self.tiles = [[[] for _ in range(10)] for _ in range(10)]
        
    def createMap(self, numberOfNodes):
        for i in range(numberOfNodes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            tileX = x // self.tileSize
            tileY = y // self.tileSize
            
            self.tiles[tileX][tileY].append(Node(x, y, State.SUSCEPTIBLE))