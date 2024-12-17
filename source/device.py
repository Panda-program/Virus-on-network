import random
"""
Class to represent a device (node) in the network
"""
class Node (object):
    # Constructor for the Node class
    def __init__(self, canvas, x: 'int', y: 'int', state: 'State', virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):
        
        """
            Parameters:
            canvas: The canvas object to draw the node on
            x: The x coordinate of the node
            y: The y coordinate of the node
            state: The state of the node (susceptible, infected, resistant, recovered)
            virusSpreadChance: The chance of the virus spreading to a neighbor node
            virusCheckFreq: The number of ticks between each virus spread check
            recoveryChance: The chance of an infected node recovering
            gainResistChance: The chance of a recovered node gaining resistance to the virus
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
        
        
    """
    Method to create a connection between two nodes returning a boolean value to indicate if the creation of connection was successful
    """
    def createConnection(self, neighbor: 'Node'):
        if (neighbor in self.neighbors):
            return False
        self.neighbors.append(neighbor)
        connection = Connection(self, neighbor, self.canvas)
        self.connections.append(connection)
        neighbor.addConnection(connection, self)
        return True
    
    # Method to add an existing connection to the node and append the neighbor to the list of neighbors
    def addConnection(self, connection: 'Connection', neighbor: 'Node'):
        if (neighbor not in self.neighbors):
            self.neighbors.append(neighbor)
            self.connections.append(connection)
        else:
            return
        
    # Method for checking if a node is a neighbor    
    def isNeighbor(self, node: 'Node'):
        return node in self.neighbors
    
    #getter for degree - number of neighbors    
    def getDegree(self):
        return len(self.neighbors)
    
    #getter for state
    def getState(self):
        return self.state
    
    #setter for state
    def setState(self, state: 'State'):
        self.state = state
    
    #setter for next state
    def setNextState(self, state: 'State'):
        if (self.state == State.RESISTANT):
            return
        self.nextState = state
    
    #method for infecting self and neighbors
    def infect(self):
        self.canvas.itemconfig(self.circle, fill="red")
        for neighbor in self.neighbors:
            infectedChance = random.random() * 100
            if (infectedChance <= self.virusSpreadChance):
                neighbor.setNextState(State.INFECTED)
                
    #method for setting state and visual representation as recovered node
    def recover(self):
        self.nextState = State.SUSCEPTIBLE
        self.canvas.itemconfig(self.circle, fill="blue")
    
    #method for setting state and visual representation as resistant node
    def becomeResistant(self):
        self.state = State.RESISTANT
        self.canvas.itemconfig(self.circle, fill="grey")
    
    #main method for checking the state of the node and updating the upcoming state
    def check(self):
        if (self.state == State.RESISTANT):
            return
        elif (self.state == State.INFECTED):
            if (self.tickCount % self.virusCheckFreq != 0):
                self.nextState = self.state
                return
            recoveryChance = random.random() * 100
            if (recoveryChance <= self.recoveryChance):
                self.nextState = State.RECOVERED
            else:
                resistanceChance = random.random() * 100
                if (resistanceChance <= self.gainResistChance):
                    self.nextState = State.RESISTANT
                else:
                    self.setNextState(State.INFECTED)

    #main loop for the node handling the state transitions
    def tick(self):
        self.tickCount += 1
        if (self.state == State.RESISTANT):
            self.becomeResistant()
        elif (self.state == State.RECOVERED):
            self.recover()
        elif (self.state == State.INFECTED):
            self.infect()
        elif(self.state == State.SUSCEPTIBLE):
            self.canvas.itemconfig(self.circle, fill="blue")
        if (self.state == None):
            self.nextState = State.SUSCEPTIBLE
            
        for connection in self.connections:
            connection.check()
        self.state = self.nextState
        
        
'''
    Class to represent a connection between two nodes containing connected nodes and the visual line object
'''
class Connection (object):
    # Constructor for the Connection class
    def __init__(self, node1: 'Node', node2: 'Node', canvas: 'Canvas'):
        """
            Parameters:
            node1: The first node in the connection
            node2: The second node in the connection
            canvas: The canvas object to draw the connection
        """
        self.nodes = [node1, node2]
        self.canvas = canvas
        #create line object between nodes
        self.connectionLine = self.canvas.create_line(self.nodes[0].x + self.nodes[0].width / 2, #x1
                                                      self.nodes[0].y + self.nodes[0].width / 2, #y1
                                                      self.nodes[1].x + self.nodes[1].width / 2, #x2
                                                      self.nodes[1].y + self.nodes[1].width / 2, #y2
                                                      width=1, fill="white")
        canvas.tag_lower(self.connectionLine) #change z index of line to be behind nodes
        
    #method returning boolean value if node is in connection
    def hasNode(self, node: 'Node'):
        return node == self.node1 or node == self.node2
    
    #getter for first node
    def getFirstNode(self):
        return self.nodes[0]
    
    #getter for second node    
    def getSecondNode(self):
        return self.nodes[1]
    
    #getter for connection line
    def getConnectionLine(self):
        return self.connectionLine
    
    #method for checking the state of the nodes and updating the visual representation of the connection
    def check(self):
        if (self.nodes[0].state == State.RESISTANT or self.nodes[1].state == State.RESISTANT):
            self.canvas.itemconfig(self.connectionLine, fill="grey")
        elif (self.nodes[0].state == State.INFECTED or self.nodes[1].state == State.INFECTED):
            self.canvas.itemconfig(self.connectionLine, fill="red")
        else:
            self.canvas.itemconfig(self.connectionLine, fill="white")
    
    #method for updating the visual representation of the connection
    def recover(self):
        self.canvas.itemconfig(self.connectionLine, fill="grey")
    
    #method for updating the visual representation of the connection
    def compareConnection(self, connection: 'Connection'):
        conNode1 = connection.getFirstNode()
        conNode2 = connection.getSecondNode()
        return self.nodes[0] == conNode1 and self.nodes[1] != conNode2 or self.nodes[0] != conNode1 and self.nodes[1] == conNode2

class Connection (object):
    # Constructor for the Connection class
    def __init__(self, node1: 'Node', node2: 'Node', canvas: 'Canvas'):
        """
            Parameters:
            node1: The first node in the connection
            node2: The second node in the connection
            canvas: The canvas object to draw the connection
        """
        self.nodes = [node1, node2]
        self.canvas = canvas
        #create line object between nodes
        self.connectionLine = self.canvas.create_line(self.nodes[0].x + self.nodes[0].width / 2, #x1
                                                      self.nodes[0].y + self.nodes[0].width / 2, #y1
                                                      self.nodes[1].x + self.nodes[1].width / 2, #x2
                                                      self.nodes[1].y + self.nodes[1].width / 2, #y2
                                                      width=1, fill="white")
        canvas.tag_lower(self.connectionLine) #change z index of line to be behind nodes
        
    #method returning boolean value if node is in connection
    def hasNode(self, node: 'Node'):
        return node == self.node1 or node == self.node2
    
    #getter for first node
    def getFirstNode(self):
        return self.nodes[0]
    
    #getter for second node    
    def getSecondNode(self):
        return self.nodes[1]
    
    #getter for connection line
    def getConnectionLine(self):
        return self.connectionLine
    
    #method for checking the state of the nodes and updating the visual representation of the connection
    def check(self):
        if (self.nodes[0].state == State.RESISTANT or self.nodes[1].state == State.RESISTANT):
            self.canvas.itemconfig(self.connectionLine, fill="grey")
        elif (self.nodes[0].state == State.INFECTED or self.nodes[1].state == State.INFECTED):
            self.canvas.itemconfig(self.connectionLine, fill="red")
        else:
            self.canvas.itemconfig(self.connectionLine, fill="white")
    
    #method for updating the visual representation of the connection
    def recover(self):
        self.canvas.itemconfig(self.connectionLine, fill="grey")
    
    #method for updating the visual representation of the connection
    def compareConnection(self, connection: 'Connection'):
        conNode1 = connection.getFirstNode()
        conNode2 = connection.getSecondNode()
        return self.nodes[0] == conNode1 and self.nodes[1] != conNode2 or self.nodes[0] != conNode1 and self.nodes[1] == conNode2


# Enum class for the states of the nodes
class State (enumerate):
    INFECTED = 1
    SUSCEPTIBLE = 2
    RESISTANT = 3
    RECOVERED = 4