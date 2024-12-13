import random
from node import Node, State

class Map:
    def __init__(self, canvas, speed, numberOfNodes, avgNodeDegree, initial_outbreak_size, virus_spread_chance, virus_check_frequency, recovery_chance, gain_resistance_chance):
        self.speed = speed
        self.canvas = canvas
        self.width = 700
        self.height = 700
        self.tileSize = 70
        self.numberOfNodes = numberOfNodes
        self.avgNodeDegree = avgNodeDegree
        self.initial_outbreak_size = initial_outbreak_size
        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
        
        self.nodes = []
        self.isLoaded = False
        self.createMap()
        self.createConnections()
        self.infectNodes()
        self.isLoaded = True
        
    def createMap(self):
        numOfNodes = 0
        for i in range(self.numberOfNodes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.nodes.append(Node(self.canvas, x, y, State.SUSCEPTIBLE, self.virus_spread_chance, self.virus_check_frequency, self.recovery_chance, self.gain_resistance_chance))
            numOfNodes += 1
        print("Number of nodes created: ", numOfNodes)
    
    def isMapLoaded(self):
        return self.isLoaded
    
    def createConnections(self):
        totalConnections = self.avgNodeDegree * self.numberOfNodes // 2
        currentConnections = 0
        
        while (currentConnections < totalConnections):
            node = random.choice(self.nodes)
            nearestNode = None
            nearestDistance = float("inf")
        
            for n in self.nodes:
                if (n != node and not node.isNeighbor(n)):
                    distance = self.getDistance(node, n)
                    if (distance < nearestDistance and n.getDegree() < self.avgNodeDegree and node.isNeighbor(n) == False):
                        nearestNode = n
                        nearestDistance = distance
            if (nearestNode != None):
                connection = node.createConnection(nearestNode)
                if (connection):
                    currentConnections += 1
                
                
        print("total connections: ", totalConnections)
        print("Number of connections created: ", currentConnections)
    
    def infectNodes(self):
        while (self.initial_outbreak_size > 0):
            node = random.choice(self.nodes)
            if (node.state == State.SUSCEPTIBLE):
                node.setState(State.INFECTED)
                self.initial_outbreak_size -= 1
    
    def tick(self):
        for node in self.nodes:
            node.tick()
        for node in self.nodes:
            node.check()
        infected_nodes = 0
        for node in self.nodes:
            if (node.state == State.INFECTED):
                infected_nodes += 1
        if infected_nodes > 0:
            self.canvas.after(self.speed, self.tick)
        else:
            # Perform a final cleanup: make sure all nodes are correctly colored
            for node in self.nodes:
                node.tick()  # Final update of states
            for node in self.nodes:
                node.check()  # Check connections
            print("Simulation finished, all nodes have transitioned to non-infected states.")
        
                
    def getDistance(self, node1, node2):
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
                
                