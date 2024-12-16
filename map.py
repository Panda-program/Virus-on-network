import random
from node import Node, State

"""
    Represents a simulation map, responsible for handling the creation of nodes and connections, as well as the simulation loop.
"""

class Map:
    # Constructor for the Map class
    def __init__(self, canvas, speed, numberOfNodes, avgNodeDegree, initialOutbreakSize, virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):
        """
            Parameters:
            canvas: The canvas object to draw the nodes and connections on
            speed: The speed of the simulation in milliseconds
            numberOfNodes: The number of nodes to create
            avgNodeDegree: The average number of connections each node should have
            initialOutbreakSize: The number of nodes to infect at the start of the simulation
            virusSpreadChance: The chance of the virus spreading to a neighbor node
            virusCheckFreq: The number of ticks between each virus spread check
            recoveryChance: The chance of an infected node recovering
            gainResistChance: The chance of a recovered node gaining resistance to the virus
        """
        self.speed = speed
        self.canvas = canvas
        self.width = 700
        self.height = 700
        self.numberOfNodes = numberOfNodes
        self.avgNodeDegree = avgNodeDegree
        self.initialOutbreakSize = initialOutbreakSize
        self.virusSpreadChance = virusSpreadChance
        self.virusCheckFreq = virusCheckFreq
        self.recoveryChance = recoveryChance
        self.gainResistChance = gainResistChance
        
        self.nodes = []
        self.isLoaded = False
        self.isEnd = False
        
    # Setup method for initializing the map for simulation
    def setup(self):
        # Reset the map if already loaded
        if self.isLoaded:
            self.reset()
            
        self.createMap()
        self.createConnections()
        self.infectNodes()

        # Ensure tick and check for all nodes to start simulation
        for node in self.nodes:
            node.tick()
        for node in self.nodes:
            node.check()

        # Set flags to indicate that the map is loaded and simulation has started
        self.isLoaded = True
        self.isEnd = False
        
    # Create the nodes for the map with random positions
    def createMap(self):
        numOfNodes = 0
        for i in range(self.numberOfNodes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.nodes.append(Node(self.canvas, x, y, State.SUSCEPTIBLE, self.virusSpreadChance, self.virusCheckFreq, self.recoveryChance, self.gainResistChance))
            numOfNodes += 1
        print("Number of nodes created: ", numOfNodes)

    # method to reset the map and clear the canvas
    def reset(self):
        self.isEnd = True
        self.isLoaded = False
        self.canvas.delete("all")
        self.nodes = []

    # method to check if the map is loaded
    def isMapLoaded(self):
        return self.isLoaded
    
    # algorithm to create connections between nodes based on the average node degree and euclidean distance
    def createConnections(self):
        totalConnections = self.avgNodeDegree * self.numberOfNodes // 2
        currentConnections = 0
        
        while (currentConnections < totalConnections):
            node = random.choice(self.nodes)
            nearestNode = None
            nearestDistance = float("inf")
        
            # Find the nearest node that is not a neighbor and has less than the average node degree
            for n in self.nodes:
                if (n != node and not node.isNeighbor(n)):
                    distance = self.getDistance(node, n)
                    if (distance < nearestDistance and n.getDegree() < self.avgNodeDegree and node.isNeighbor(n) == False):
                        nearestNode = n
                        nearestDistance = distance
            
            # Create a connection between the nodes if a suitable node is found
            if (nearestNode != None):
                connection = node.createConnection(nearestNode)
                if (connection):
                    currentConnections += 1
                
                
        print("total connections: ", totalConnections)
        print("Number of connections created: ", currentConnections)
    
    # method to infect nodes at the start of the simulation
    def infectNodes(self):
        while (self.initialOutbreakSize > 0):
            node = random.choice(self.nodes)
            if (node.state == State.SUSCEPTIBLE):
                node.setState(State.INFECTED)
                self.initialOutbreakSize -= 1
    
    # recursive method which handles the simulation loop
    def tick(self):
        if (self.isEnd or self.isLoaded == False):
            return
        infectedCount = 0
        
        for node in self.nodes:
            node.tick()
        for node in self.nodes:
            node.check()
            if (node.state == State.INFECTED):
                infectedCount += 1

        # check if the simulation has ended
        if (self.isEnd):
            print("The simulation has ended")
            return
        if (infectedCount == 0):
            self.isEnd = True
        
        self.canvas.after(self.speed, self.tick)
        
    # method to calculate the euclidean distance between two nodes
    def getDistance(self, node1, node2):
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
                
                