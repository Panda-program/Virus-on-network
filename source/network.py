import random



class Map:
    """
    Represents a simulation map, responsible for handling the creation of nodes and connections, as well as the simulation loop.
    
    :ivar tkinter.Canvas canvas: The canvas object to draw the nodes and connections on.
    :ivar int numberOfNodes: The number of nodes in the simulation.
    :ivar int avgNodeDegree: The average number of connections each node should have.
    :ivar int initialOutbreakSize: The number of nodes to infect at the start of the simulation.
    :ivar int speed: Time for each tick in milliseconds.
    :ivar int WIDTH: width of the map
    :ivar int HEIGHT: height of the map
    :ivar list[Connection] connections: A list of connections between nodes.
    :ivar list[Node] nodes: A list of nodes in the simulation.
    :ivar bool isLoaded: True -> map is loaded, False -> not loaded.
    :ivar bool isEnd: True -> simulation has ended, False -> simulation si running
    
    """
    # Constructor for the Map class
    def __init__(self, canvas):
        
        ''' 
            :param canvas: The canvas object to draw the map on.
            :type canvas: tkinter.Canvas
            
            Creates a new Map object with the given canvas.
        '''
        
        self.canvas = canvas
        
        self.numberOfNodes = 0
        self.avgNodeDegree = 0
        self.initialOutbreakSize = 0
        
        self.speed = 0
        self.WIDTH = 700
        self.HEIGHT = 700
        
        self.nodes = []
        self.isLoaded = False
        self.isEnd = False
        
    def setup(self, speed, numberOfNodes, avgNodeDegree, initialOutbreakSize, virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):
        """
            - Sets up the map and attributes for the simulation with the given parameters.
            - Calls the createMap(), createConnections(), and infectNodes() methods to properly setup map.
            - At the end performs the initial tick() and check() for each node to visually display the initial state of the simulation.
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
            Creates nodes based with random positions on the canvas.
        """
        numOfNodes = 0
        for i in range(self.numberOfNodes):
            x = random.randint(0, self.WIDTH - 1)
            y = random.randint(0, self.HEIGHT - 1)
            self.nodes.append(Node(self.canvas, x, y, State.SUSCEPTIBLE, self.virusSpreadChance, self.virusCheckFreq, self.recoveryChance, self.gainResistChance))
            numOfNodes += 1
        print("Number of nodes created: ", numOfNodes)

    def reset(self):
        """
            Resets the map, clearing the canvas and nodes[] list.
        """
        self.isEnd = True
        self.isLoaded = False
        self.canvas.delete("all")
        self.nodes = []

    def isMapLoaded(self):
        """
            :return: isLoaded attribute of the Map object
            :rtype: bool
        """
        return self.isLoaded
    
    def createConnections(self):
        """
            Creates connections between nodes based on the average node degree.
                - calculates the total number of connections needed based on avgNodeDegree and numberOfNodes
                - randomly selects a node and finds the nearest node to connect to
                - checks if the nearest node is already int the neighbors[] list of the selected node
                    - if not, creates a connection between the two nodes
                - repeats until the total number of connections is reached
                
                
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

        :param node1: The first node.
        :type node1: Node
        :param node2: The second node.
        :type node2: Node

        :return: The Euclidean distance between the two nodes.
        :rtype: float
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
            Handles the simulation loop.
                - calls the tick() and check() method for each node in the nodes[] list
                - checks if the simulation has ended (no more infected nodes)
                - if the simulation has ended, runs two more ticks and checks to prevent the visual representation from freezing
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
        Represents a device in the simulation that can be in one of the following states:
        SUSCEPTIBLE, INFECTED, RECOVERED, or RESISTANT.
        
        :ivar tkinter.Canvas canvas: The canvas object to draw the node on.
        :ivar int x: The x coordinate of the node.
        :ivar int y: The y coordinate of the node.
        :ivar State state: The current state of the node.
        :ivar State nextState: The next state of the node.
        :ivar float virusSpreadChance: The chance of the virus spreading to a neighbor node.
        :ivar int virusCheckFreq: The number of ticks between each check if node is infected.
        :ivar float recoveryChance: The chance of an infected node recovering from the virus.
        :ivar float gainResistChance: The chance of a infected node gaining resistance to the virus.
        :ivar int tickCount: The number of ticks since the node was created.
        :ivar list[Connection] connections: A list of connections to neighboring nodes.
        :ivar list[Node] neighbors: A list of neighboring nodes.
        :ivar int WIDTH: The width of the circle representing the node.
        :ivar int circle: The id of the circle object on the canvas.
        
        
    """
    def __init__(self, canvas, x: 'int', y: 'int', state: 'State', virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):
        """
            Initializes the Node object.

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
        self.WIDTH = 12
        self.circle = self.canvas.create_oval(x, y, x + self.WIDTH, y + self.WIDTH, outline="", fill="red" if state == State.INFECTED else "blue")
    
    def createConnection(self, neighbor: 'Node'):
        """
            Creates a connection between this node and a neighbor node.
            
            :param neighbor: The neighboring node to connect to.
            :type neighbor: Node
            
            :return: True -> connection was created, False -> neighbor is already in neighbors[] list.
            :rtype: bool
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
            Adds connection to the connections[] list and neighbor to the neighbors[] list if neighbor is not already in the neighbors[] list.
            
            :param connection: The connection to add.
            :type connection: Connection
            :param neighbor: The neighbor node to add.
            :type neighbor: Node
        """
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            self.connections.append(connection)

    def isNeighbor(self, node: 'Node'):
        """
            Checks if the given node is a neighbor of this node.

            :param node: The node to check.
            :type node: Node

            :return: True -> node is a neighbor, False -> node is not a neighbor.
            :rtype: bool
        """
        return node in self.neighbors
    
    def getDegree(self):
        """
            :return: The number of neighbors.
            :rtype: int
        """
        return len(self.neighbors)
    
    def getState(self):
        """
            :return: The current state of the node.
            :rtype: State
        """
        return self.state
    
    def setState(self, state: 'State'):
        """
            Sets current state of the node.

            :param state: The state to set.
            :type state: State
        """
        self.state = state
    
    def setNextState(self, state: 'State'):
        """
            Sets the next state of the node if the current state is not RESISTANT.

            :param state: The state to set.
            :type state: State
        """
        if self.state == State.RESISTANT:
            return
        self.nextState = state
    
    def infect(self):
        """
            Sets the circle color to red and infects neighboring nodes based on the virus spread chance.
        """
        self.canvas.itemconfig(self.circle, fill="red")
        for neighbor in self.neighbors:
            infectedChance = random.random() * 100
            if infectedChance <= self.virusSpreadChance:
                neighbor.setNextState(State.INFECTED)
                
    def recover(self):
        """
            Sets the nodes nextState to SUSCEPTIBLE and the circle color to blue.
        """
        self.nextState = State.SUSCEPTIBLE
        self.canvas.itemconfig(self.circle, fill="blue")
    
    def becomeResistant(self):
        """
            Sets the nodes state to RESISTANT and the circle color to grey.
        """
        self.state = State.RESISTANT
        self.canvas.itemconfig(self.circle, fill="grey")
    
    def check(self):
        """
            Based on the current state of the node, updates the next state of the node.
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
            - Calls appropriate methods to update node based on the current state of the node.
            - If tickCount is a multiple of virusCheckFreq, the node checks if it is infected.
            - Sets the state of the node to the next state.
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
        
        :ivar list[Node] nodes: A list of the two nodes connected by the connection.
        :ivar tkinter.Canvas canvas: The canvas object to draw the connection on.
        :ivar int connectionLine: The id of the line object on the canvas.
        
    """
    def __init__(self, node1: 'Node', node2: 'Node', canvas: 'Canvas'):
        self.nodes = [node1, node2]
        self.canvas = canvas
        self.connectionLine = self.canvas.create_line(self.nodes[0].x + self.nodes[0].WIDTH / 2,
                                                      self.nodes[0].y + self.nodes[0].WIDTH / 2,
                                                      self.nodes[1].x + self.nodes[1].WIDTH / 2,
                                                      self.nodes[1].y + self.nodes[1].WIDTH / 2,
                                                      WIDTH=1, fill="white")
        canvas.tag_lower(self.connectionLine)
    
    def hasNode(self, node: 'Node'):
        """
            :param node: The node to check.
            :type node: Node
            
            :return: True -> node is in the nodes[] list, False -> node is not in the nodes[] list.
            :rtype: bool
        """
        return node in self.nodes
    
    def getFirstNode(self):
        """
            :return: The first node in the nodes[] list.
            :rtype: Node
        """
        return self.nodes[0]
    
    def getSecondNode(self):
        """
            :return: The second node in the nodes[] list.
            :rtype: Node
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

    :ivar SUSCEPTIBLE: Node can be infected by virus
    :vartype SUSCEPTIBLE: int
    :ivar INFECTED: Node is infected by virus
    :vartype INFECTED: int
    :ivar RECOVERED: Node has recovered from virus
    :vartype RECOVERED: int
    :ivar RESISTANT: Node is resistant to virus
    :vartype RESISTANT: int
    """

    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3
    RESISTANT = 4
