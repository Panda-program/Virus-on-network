import random
class Node (object):
    def __init__(self, canvas, x: 'int', y: 'int', state: 'State', virus_spread_chance, virus_check_frequency, recovery_chance, gain_resistance_chance):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.state = state
        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
        self.tickCount = 0
        
        self.connections = []
        self.neighbors = []
        self.nextState = None
        self.width = 12
        self.circle = self.canvas.create_oval(x, y, x + self.width, y + self.width, outline="", fill="red" if state == State.INFECTED else "blue")
        
        
    def createConnection(self, neighbor: 'Node'):
        if (neighbor in self.neighbors):
            return False
        self.neighbors.append(neighbor)
        connection = Connection(self, neighbor, self.canvas)
        self.connections.append(connection)
        neighbor.addConnection(connection, self)
        return True
    
    def addConnection(self, connection: 'Connection', neighbor: 'Node'):
        if (neighbor not in self.neighbors):
            self.neighbors.append(neighbor)
            self.connections.append(connection)
        else:
            return
        
    def isNeighbor(self, node: 'Node'):
        return node in self.neighbors
        
    def getDegree(self):
        return len(self.neighbors)
    
    def getState(self):
        return self.state
    
    def setState(self, state: 'State'):
        self.state = state
    
    def setNextState(self, state: 'State'):
        if (self.state == State.RESISTANT):
            return
        self.nextState = state
    
    def infect(self):
        self.canvas.itemconfig(self.circle, fill="red")
        for neighbor in self.neighbors:
            infectedChance = random.random() * 100
            if (infectedChance <= self.virus_spread_chance):
                neighbor.setNextState(State.INFECTED)
    
    def recover(self):
        self.nextState = State.SUSCEPTIBLE
        self.canvas.itemconfig(self.circle, fill="blue")
    
    def becomeResistant(self):
        self.state = State.RESISTANT
        self.canvas.itemconfig(self.circle, fill="grey")
    
    def check(self):
        if (self.state == State.RESISTANT):
            return
        elif (self.state == State.INFECTED):
            if (self.tickCount % self.virus_check_frequency != 0):
                self.nextState = self.state
                return
            recoveryChance = random.random() * 100
            if (recoveryChance <= self.recovery_chance):
                self.nextState = State.RECOVERED
            else:
                resistanceChance = random.random() * 100
                if (resistanceChance <= self.gain_resistance_chance):
                    self.nextState = State.RESISTANT
                else:
                    self.setNextState(State.INFECTED)

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
        
        
    
class Connection (object):
    def __init__(self, node1: 'Node', node2: 'Node', canvas: 'Canvas'):
        self.nodes = [node1, node2]
        self.canvas = canvas
        self.connectionLine = self.canvas.create_line(self.nodes[0].x + self.nodes[0].width / 2, #x1
                                                      self.nodes[0].y + self.nodes[0].width / 2, #y1
                                                      self.nodes[1].x + self.nodes[1].width / 2, #x2
                                                      self.nodes[1].y + self.nodes[1].width / 2, #y2
                                                      width=1, fill="white")
        canvas.tag_lower(self.connectionLine) #change z index of line to be behind nodes
        
    def hasNode(self, node: 'Node'):
        return node == self.node1 or node == self.node2
    
    def getFirstNode(self):
        return self.nodes[0]
    
    def getSecondNode(self):
        return self.nodes[1]
    
    def getConnectionLine(self):
        return self.connectionLine
    
    def check(self):
        if (self.nodes[0].state == State.RESISTANT or self.nodes[1].state == State.RESISTANT):
            self.canvas.itemconfig(self.connectionLine, fill="grey")
        elif (self.nodes[0].state == State.INFECTED or self.nodes[1].state == State.INFECTED):
            self.canvas.itemconfig(self.connectionLine, fill="red")
        else:
            self.canvas.itemconfig(self.connectionLine, fill="white")
    
    def recover(self):
        self.canvas.itemconfig(self.connectionLine, fill="grey")
        
    def compareConnection(self, connection: 'Connection'):
        conNode1 = connection.getFirstNode()
        conNode2 = connection.getSecondNode()
        return self.nodes[0] == conNode1 and self.nodes[1] != conNode2 or self.nodes[0] != conNode1 and self.nodes[1] == conNode2


class State (enumerate):
    INFECTED = 1
    SUSCEPTIBLE = 2
    RESISTANT = 3
    RECOVERED = 4