import random



class Map:
    """
    Represents a simulation map, responsible for handling the creation of nodes and connections, as well as the simulation loop.
    """
    # Constructor for the Map class
    def __init__(self, canvas):
        """
            .. :param canvas: The canvas object to draw the nodes and connections on.
            .. :type canvas: tkinter.Canvas
            
        """
        self.numberOfNodes = 0
        self.avgNodeDegree = 0
        self.initialOutbreakSize = 0
        self.virusSpreadChance = 0
        self.virusCheckFreq = 0
        self.recoveryChance = 0
        self.gainResistChance = 0
        
        self.speed = 0
        self.canvas = canvas
        self.width = 700
        self.height = 700
        
        self.nodes = []
        self.isLoaded = False
        self.isEnd = False
        
    def setup(self, speed, numberOfNodes, avgNodeDegree, initialOutbreakSize, virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):
        """
            Initializes the map for the simulation with the given parameters.

            Parameters:
            :param: speed: The speed of the simulation in milliseconds.
            :type: speed: int
            numberOfNodes (int): The number of nodes to create.
            avgNodeDegree (int): The average number of connections each node should have.
            initialOutbreakSize (int): The number of nodes to infect at the start of the simulation.
            virusSpreadChance (float): The chance of the virus spreading to a neighbor node.
            virusCheckFreq (int): The number of ticks between each virus spread check.
            recoveryChance (float): The chance of an infected node recovering.
            gainResistChance (float): The chance of a recovered node gaining resistance to the virus.
        """
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
        
    def createMap(self):
        """
            Creates the nodes with random positions on the canvas.
        """
        numOfNodes = 0
        for i in range(self.numberOfNodes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.nodes.append(Node(self.canvas, x, y, State.SUSCEPTIBLE, self.virusSpreadChance, self.virusCheckFreq, self.recoveryChance, self.gainResistChance))
            numOfNodes += 1
        print("Number of nodes created: ", numOfNodes)

    def reset(self):
        """
            Resets the map, clearing the canvas and nodes.
        """
        self.isEnd = True
        self.isLoaded = False
        self.canvas.delete("all")
        self.nodes = []

    def isMapLoaded(self):
        """
            Returns whether the map has been loaded or not.

            Returns:
            bool: True if the map is loaded, False otherwise.
        """
        return self.isLoaded
    
    def createConnections(self):
        """
            Creates connections between nodes based on the average node degree.
        """
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
        
    def getDistance(self, node1, node2):
        """
            Calculates the Euclidean distance between two nodes.

            Parameters:
            node1 (Node): The first node.
            node2 (Node): The second node.

            Returns:
            float: The Euclidean distance between the two nodes.
        """
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
    
    def infectNodes(self):
        """
            Infects nodes at the start of the simulation based on the initial outbreak size.
        """
        while self.initialOutbreakSize > 0:
            node = random.choice(self.nodes)
            if node.state == State.SUSCEPTIBLE:
                node.setState(State.INFECTED)
                self.initialOutbreakSize -= 1
    
    def tick(self):
        """
            Handles the simulation loop. Updates the states of nodes and checks for new infections.
        """
        if self.isEnd or not self.isLoaded:
            return
        
        infectedCount = 0
        for node in self.nodes:
            node.tick()
        for node in self.nodes:
            node.check()
            if node.state == State.INFECTED:
                infectedCount += 1
                
        if infectedCount == 0:
            self.isEnd = True
            for _ in range(2):
                for node in self.nodes:
                    node.tick()
                for node in self.nodes:
                    node.check()
            print("The simulation has ended")
            
        print("Number of infected nodes: ", infectedCount)
        
        self.canvas.after(self.speed, self.tick)


class Node:
    """
        Represents a node in the simulation that can be in one of the following states:
        SUSCEPTIBLE, INFECTED, RECOVERED, or RESISTANT.
    """
    def __init__(self, canvas, x: 'int', y: 'int', state: 'State', virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):
        """
            Initializes the Node object.

            Parameters:
            canvas (Canvas): The canvas object to draw the node on.
            x (int): The x coordinate of the node.
            y (int): The y coordinate of the node.
            state (State): The initial state of the node.
            virusSpreadChance (float): The chance of the virus spreading to a neighbor node.
            virusCheckFreq (int): The number of ticks between each virus spread check.
            recoveryChance (float): The chance of an infected node recovering.
            gainResistChance (float): The chance of a recovered node gaining resistance to the virus.
        """
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
    
    def createConnection(self, neighbor: 'Node'):
        """
            Creates a connection between this node and a neighbor node.

            Parameters:
            neighbor (Node): The neighboring node to connect to.

            Returns:
            bool: True if the connection was created successfully, False otherwise.
        """
        if neighbor in self.neighbors:
            return False
        self.neighbors.append(neighbor)
        connection = Connection(self, neighbor, self.canvas)
        self.connections.append(connection)
        neighbor.addConnection(connection, self)
        return True
    
    def addConnection(self, connection: 'Connection', neighbor: 'Node'):
        """
            Adds an existing connection between this node and a neighbor.

            Parameters:
            connection (Connection): The connection to add.
            neighbor (Node): The neighboring node to add.
        """
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            self.connections.append(connection)

    def isNeighbor(self, node: 'Node'):
        """
            Checks if the given node is a neighbor of this node.

            Parameters:
            node (Node): The node to check.

            Returns:
            bool: True if the node is a neighbor, False otherwise.
        """
        return node in self.neighbors
    
    def getDegree(self):
        """
            Returns the number of neighbors this node has.

            Returns:
            int: The degree of the node.
        """
        return len(self.neighbors)
    
    def getState(self):
        """
            Returns the current state of the node.

            Returns:
            State: The current state of the node.
        """
        return self.state
    
    def setState(self, state: 'State'):
        """
            Sets the state of the node.

            Parameters:
            state (State): The state to set.
        """
        self.state = state
    
    def setNextState(self, state: 'State'):
        """
            Sets the next state of the node.

            Parameters:
            state (State): The state to set for the next tick.
        """
        if self.state == State.RESISTANT:
            return
        self.nextState = state
    
    def infect(self):
        """
            Infects the node and tries to infect its neighbors.
        """
        self.canvas.itemconfig(self.circle, fill="red")
        for neighbor in self.neighbors:
            infectedChance = random.random() * 100
            if infectedChance <= self.virusSpreadChance:
                neighbor.setNextState(State.INFECTED)
                
    def recover(self):
        """
            Makes the node recover and return to the susceptible state.
        """
        self.nextState = State.SUSCEPTIBLE
        self.canvas.itemconfig(self.circle, fill="blue")
    
    def becomeResistant(self):
        """
            Makes the node resistant to the virus.
        """
        self.state = State.RESISTANT
        self.canvas.itemconfig(self.circle, fill="grey")
    
    def check(self):
        """
            Checks the current state of the node and updates the next state.
        """
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

    def tick(self):
        """
            Updates the state of the node based on its current state.
        """
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


class Connection:
    """
        Represents a connection between two nodes, visualized as a line on the canvas.
    """
    def __init__(self, node1: 'Node', node2: 'Node', canvas: 'Canvas'):
        """
            Initializes a connection between two nodes.

            Parameters:
            node1 (Node): The first node in the connection.
            node2 (Node): The second node in the connection.
            canvas (Canvas): The canvas object to draw the connection.
        """
        self.nodes = [node1, node2]
        self.canvas = canvas
        self.connectionLine = self.canvas.create_line(self.nodes[0].x + self.nodes[0].width / 2,
                                                      self.nodes[0].y + self.nodes[0].width / 2,
                                                      self.nodes[1].x + self.nodes[1].width / 2,
                                                      self.nodes[1].y + self.nodes[1].width / 2,
                                                      width=1, fill="white")
        canvas.tag_lower(self.connectionLine)
    
    def hasNode(self, node: 'Node'):
        """
            Checks if the connection includes the given node.

            Parameters:
            node (Node): The node to check.

            Returns:
            bool: True if the node is in the connection, False otherwise.
        """
        return node == self.nodes[0] or node == self.nodes[1]
    
    def getFirstNode(self):
        """
            Returns the first node in the connection.

            Returns:
            Node: The first node in the connection.
        """
        return self.nodes[0]
    
    def getSecondNode(self):
        """
            Returns the second node in the connection.

            Returns:
            Node: The second node in the connection.
        """
        return self.nodes[1]
    
    def check(self):
        """
            Updates the visual representation of the connection based on the nodes' states.
        """
        if self.nodes[0].state == State.RESISTANT or self.nodes[1].state == State.RESISTANT:
            self.canvas.itemconfig(self.connectionLine, fill="grey")
        elif self.nodes[0].state == State.INFECTED or self.nodes[1].state == State.INFECTED:
            self.canvas.itemconfig(self.connectionLine, fill="red")
        else:
            self.canvas.itemconfig(self.connectionLine, fill="white")


class State:
    """
        Represents the different possible states a node can be in during the simulation.
    """
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3
    RESISTANT = 4