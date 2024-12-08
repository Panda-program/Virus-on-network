class Node (object):
    def __init__(self, canvas, x: 'int', y: 'int', state: 'State'):
        self.nextState = None
        self.width = 12
        self.canvas = canvas
        self.x = x
        self.y = y
        self.connections = []
        self.neighbors = []
        self.circle = self.canvas.create_oval(x, y, x + self.width, y + self.width, outline="", fill="red" if state == State.INFECTED else "blue")
        self.state = state
        
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
    
    def setNextState(self, state: 'State'):
        self.nextState = state
    
    def setState(self, state: 'State'):
        self.state = state
    
    def recover(self):
        self.state = State.RECOVERED
        self.canvas.itemconfig(self.circle, fill="grey")
        for connection in self.connections:
            connection.recover()

    def tick(self):
        if (self.state == State.RECOVERED):
            return
        elif (self.state == State.INFECTED):
            self.canvas.itemconfig(self.circle, fill="red")
            for connection in self.connections:
                connection.infect()
            for neighbor in self.neighbors:
                neighbor.setNextState(State.INFECTED)
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
    
    def infect(self):
        if (self.nodes[0].state == State.RECOVERED or self.nodes[1].state == State.RECOVERED):
            return
        self.canvas.itemconfig(self.connectionLine, fill="red")
    
    def recover(self):
        self.canvas.itemconfig(self.connectionLine, fill="grey")
        
    def compareConnection(self, connection: 'Connection'):
        conNode1 = connection.getFirstNode()
        conNode2 = connection.getSecondNode()
        return self.nodes[0] == conNode1 and self.nodes[1] != conNode2 or self.nodes[0] != conNode1 and self.nodes[1] == conNode2


class State (enumerate):
    INFECTED = 1
    SUSCEPTIBLE = 2
    RECOVERED = 3