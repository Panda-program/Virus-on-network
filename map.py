import random
from node import Node, State

class Map:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = 700
        self.height = 700
        self.tileSize = 70
        self.tiles = [[[] for _ in range(10)] for _ in range(10)] # spatial decomposition of map to tiles -> easier to find neighbors
        
    def createMap(self, numberOfNodes):
        for i in range(numberOfNodes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            tileX = min(9, x // self.tileSize)
            tileY = min(9, y // self.tileSize)
            
            self.tiles[tileY][tileX].append(Node(self.canvas, x, y, State.SUSCEPTIBLE))
    
    def createConnections(self, maxDistance, maxConnections):
        distance = maxDistance
        for row in self.tiles:
            for column in row:
                for node in column:
                    if (node == None or len(node.connections) >= maxConnections):
                        continue
                    startCol = max(0, (node.x - distance) // self.tileSize)
                    startRow = max(0, (node.y - distance) // self.tileSize)
                    endRow = min(9, (node.y + distance) // self.tileSize)
                    endCol = min(9, (node.x + distance) // self.tileSize)
                    
                    for i in range(startRow, endRow):
                        for j in range(startCol, endCol):
                            for neighbor in self.tiles[i][j]:
                                if (len(node.connections) >= maxConnections):
                                    continue
                                if (node != neighbor and neighbor != None and self.isDistanceValid(node, neighbor, distance)):
                                    node.createConnection(neighbor)
    
    def isDistanceValid(self, node1, node2, distance):
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5 <= distance
                
                