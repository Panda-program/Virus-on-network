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
            
            tileX = x // self.tileSize
            tileY = y // self.tileSize
            
            self.tiles[tileX][tileY].append(Node(self.canvas, x, y, State.SUSCEPTIBLE))
    
    def createConnections(self, maxDistance):
        distance = maxDistance
        for row in self.tiles:
            for column in row:
                for node in column:
                    startCol = max(0, (node.x - distance) // self.tileSize)
                    startRow = max(0, (node.y - distance) // self.tileSize)
                    endRow = min(9, (node.y + distance) // self.tileSize)
                    endCol = min(9, (node.x + distance) // self.tileSize)
                    
                    for i in range(startRow + 1, endRow -1):
                        for j in range(startCol + 1, endCol - 1):
                            for neighbor in self.tiles[i][j]:
                                if (node != neighbor):
                                    node.createConnection(neighbor)
                    
                    for neighbor in self.tiles[startRow][startCol]:
                        if (node != neighbor and self.isDistanceValid(node, neighbor, distance)):
                            node.createConnection(neighbor)
                    for neighbor in self.tiles[endRow][endCol]:
                        if (node != neighbor and self.isDistanceValid(node, neighbor, distance)):
                            node.createConnection(neighbor)
    
    def isDistanceValid(self, node1, node2, distance):
        if (node1 == None or node2 == None):
            return False
        # Compare squared distances to avoid unnecessary sqrt calculations
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5 <= distance
                
                