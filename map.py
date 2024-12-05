import random
from node import Node, State

class Map:
    def __init__(self, canvas, numberOfNodes):
        self.canvas = canvas
        self.width = 700
        self.height = 700
        self.tileSize = 70
        self.numberOfNodes = numberOfNodes
        self.nodes = []
        self.createMap()
        
    def createMap(self):
        for i in range(self.numberOfNodes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.nodes.append(Node(self.canvas, x, y, State.SUSCEPTIBLE))
    
    def createConnections(self, avgNodeDegree):
        totalConnections = avgNodeDegree * self.numberOfNodes // 2
        currentConnections = 0
        
        while (currentConnections < totalConnections):
            node = random.choice(self.nodes)
            if (node.getDegree() >= avgNodeDegree):
                continue
            nearestNode = None
            nearestDistance = float("inf")
        
            for n in self.nodes:
                if (n != node):
                    distance = self.getDistance(node, n)
                    if (distance < nearestDistance and n.getDegree() < avgNodeDegree):
                        nearestNode = n
                        nearestDistance = distance
            if (nearestNode != None):
                node.createConnection(nearestNode)
                currentConnections += 1
        
        
                
    def getDistance(self, node1, node2):
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
                
                