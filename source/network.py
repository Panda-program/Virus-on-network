import random
# Represents the simulation map and manages the nodes and simulation loop.
class Map:
    # Constructor for the Map class
    def __init__(self, canvas):
        
        self.canvas = canvas
        
        self.numberOfNodes = 0
        self.avgNodeDegree = 0
        self.initialOutbreakSize = 0
        
        self.speed = 0
        self.width = 700
        self.height = 700
        
        self.nodes = []
        self.isLoaded = False
        self.isEnd = False
        
    # Sets up the map and attributes for the simulation.
    def setup(self, speed, numberOfNodes, avgNodeDegree, initialOutbreakSize, virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):
        self.numberOfNodes = numberOfNodes
        self.avgNodeDegree = avgNodeDegree
        self.initialOutbreakSize = initialOutbreakSize
        self.virusSpreadChance = virusSpreadChance
        self.virusCheckFreq = virusCheckFreq
        self.recoveryChance = recoveryChance
        self.gainResistChance = gainResistChance
        self.speed = speed

        if self.isLoaded:
            self.reset()

        self.createMap()
        self.createConnections()
        self.infectNodes()

        for node in self.nodes:
            node.tick()
        for node in self.nodes:
            node.check()

        self.isLoaded = True
        self.isEnd = False
    
    # Creates nodes with random positions on the canvas.
    def createMap(self):
        numOfNodes = 0
        for i in range(self.numberOfNodes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.nodes.append(Node(self.canvas, x, y, State.SUSCEPTIBLE, self.virusSpreadChance, self.virusCheckFreq, self.recoveryChance, self.gainResistChance))
            numOfNodes += 1
        print("Number of nodes created: ", numOfNodes)

    def reset(self):
        self.isEnd = True
        self.isLoaded = False
        self.canvas.delete("all")
        self.nodes = []

    def isMapLoaded(self):
        return self.isLoaded
    
    # Creates connections between nodes based on the average node degree.
    def createConnections(self):
        totalConnections = self.avgNodeDegree * self.numberOfNodes // 2
        currentConnections = 0
        
        while currentConnections < totalConnections:
            node = random.choice(self.nodes)
            nearestNode = None
            nearestDistance = float("inf")
        
            for n in self.nodes:
                if n != node and not node.isNeighbor(n):
                    distance = self.getDistance(node, n)
                    if distance < nearestDistance and n.getDegree() < self.avgNodeDegree:
                        nearestNode = n
                        nearestDistance = distance
            
            if nearestNode is not None:
                connection = node.createConnection(nearestNode)
                if connection:
                    currentConnections += 1

        print("Total connections: ", totalConnections)
        print("Number of connections created: ", currentConnections)
    
    # Calculates euclidean distance between two nodes
    def getDistance(self, node1, node2):
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5

    # Infects nodes based on the initial outbreak size.
    def infectNodes(self):
        while self.initialOutbreakSize > 0:
            node = random.choice(self.nodes)
            if node.state == State.SUSCEPTIBLE:
                node.setState(State.INFECTED)
                self.initialOutbreakSize -= 1
    
    # Updates the simulation by ticking each node and checking for infections.
    def tick(self):
        if self.isEnd or not self.isLoaded:
            return
        
        for node in self.nodes:
            node.tick()
        for node in self.nodes:
            node.check()
                
        if self.getNumInfectedNodes() == 0:
            self.isEnd = True
            for _ in range(2):
                for node in self.nodes:
                    node.tick()
                for node in self.nodes:
                    node.check()
            print("The simulation has ended")
            
        print("Number of infected nodes: ", self.getNumInfectedNodes())
        
        self.canvas.after(self.speed, self.tick)
        
    
    def getNumInfectedNodes(self):
        return len([node for node in self.nodes if node.state == State.INFECTED])


# Represents a device in the simulation map.
class Node:
    def __init__(self, canvas, x: 'int', y: 'int', state: 'State', virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.state = state
        self.virusSpreadChance = virusSpreadChance
        self.virusCheckFreq = virusCheckFreq
        self.recoveryChance = recoveryChance
        self.gainResistChance = gainResistChance
        self.tickCount = 0
        
        self.connections = []
        self.neighbors = []
        self.nextState = None
        self.width = 12
        self.circle = self.canvas.create_oval(x, y, x + self.width, y + self.width, outline="", fill="red" if state == State.INFECTED else "blue")
    
    # Creates a connection between this node and a neighbor node.
    def createConnection(self, neighbor: 'Node'):
        if neighbor in self.neighbors:
            return False
        self.neighbors.append(neighbor)
        connection = Connection(self, neighbor, self.canvas)
        self.connections.append(connection)
        neighbor.addConnection(connection, self)
        return True
    
    
    def addConnection(self, connection: 'Connection', neighbor: 'Node'):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            self.connections.append(connection)

    def isNeighbor(self, node: 'Node'):
        return node in self.neighbors
    
    def getDegree(self):
        return len(self.neighbors)
    
    def getState(self):
        return self.state
    
    def setState(self, state: 'State'):
        self.state = state
    
    def setNextState(self, state: 'State'):
        if self.state == State.RESISTANT:
            return
        self.nextState = state
    
    # Infects the node and spreads the virus to its neighbors.
    def infect(self):
        self.canvas.itemconfig(self.circle, fill="red")
        for neighbor in self.neighbors:
            infectedChance = random.random() * 100
            if infectedChance <= self.virusSpreadChance:
                neighbor.setNextState(State.INFECTED)
                
    def recover(self):
        self.nextState = State.SUSCEPTIBLE
        self.canvas.itemconfig(self.circle, fill="blue")
    
    def becomeResistant(self):
        self.state = State.RESISTANT
        self.canvas.itemconfig(self.circle, fill="grey")
    
    # Checks if the node should recover, gain resistance, or remain infected.
    def check(self):
        if self.state == State.RESISTANT:
            return
        elif self.state == State.INFECTED:
            if self.tickCount % self.virusCheckFreq != 0:
                self.nextState = self.state
                return
            recoveryChance = random.random() * 100
            if recoveryChance <= self.recoveryChance:
                self.nextState = State.RECOVERED
            else:
                resistanceChance = random.random() * 100
                if resistanceChance <= self.gainResistChance:
                    self.nextState = State.RESISTANT
                else:
                    self.setNextState(State.INFECTED)

    # Updates the node's state based on the current state and tick count.
    def tick(self):
        self.tickCount += 1
        if self.state == State.RESISTANT:
            self.becomeResistant()
        elif self.state == State.RECOVERED:
            self.recover()
        elif self.state == State.INFECTED:
            self.infect()
        elif self.state == State.SUSCEPTIBLE:
            self.canvas.itemconfig(self.circle, fill="blue")
        if self.state == None:
            self.nextState = State.SUSCEPTIBLE
        
        for connection in self.connections:
            connection.check()
        self.state = self.nextState


# Represents a connection between two nodes (devices) in the simulation map.
class Connection:
    def __init__(self, node1: 'Node', node2: 'Node', canvas: 'Canvas'):
        self.nodes = [node1, node2]
        self.canvas = canvas
        self.connectionLine = self.canvas.create_line(self.nodes[0].x + self.nodes[0].width / 2,
                                                      self.nodes[0].y + self.nodes[0].width / 2,
                                                      self.nodes[1].x + self.nodes[1].width / 2,
                                                      self.nodes[1].y + self.nodes[1].width / 2,
                                                      width=1, fill="white")
        canvas.tag_lower(self.connectionLine)
    
    def hasNode(self, node: 'Node'):
        return node in self.nodes
    
    def getFirstNode(self):
        return self.nodes[0]
    
    def getSecondNode(self):
        return self.nodes[1]
    
    # Checks if the connection should be colored based on the state of the nodes.
    def check(self):
        if self.nodes[0].state == State.RESISTANT or self.nodes[1].state == State.RESISTANT:
            self.canvas.itemconfig(self.connectionLine, fill="grey")
        elif self.nodes[0].state == State.INFECTED or self.nodes[1].state == State.INFECTED:
            self.canvas.itemconfig(self.connectionLine, fill="red")
        else:
            self.canvas.itemconfig(self.connectionLine, fill="white")


# Enum class representing the possible states of a node in the simulation.
class State:
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3
    RESISTANT = 4
