import random
class Node (object):
    def __init__(self, canvas, x: 'int', y: 'int', state: 'State'):
        self.width = 35
        self.canvas = canvas
        self.x = x
        self.y = y
        self.connections = []
        self.id = random.randint(0, 100000)
        self.circle = self.canvas.create_oval(x, y, x + self.width, y + self.width, fill="red" if state == State.INFECTED else "blue")
        self.state = state
        
    def createConnection(self, neighbor: 'Node'):
        connection = Connection(self, neighbor, self.canvas)
        for con in self.connections:
            if (con.compareConnection(connection)):
                return
        self.connections.append(Connection(self, neighbor, self.canvas))
        neighbor.addConnection(connection)
    
    def addConnection(self, connection: 'Connection'):
        for con in self.connections:
            if (con.compareConnection(connection)):
                return
        self.connections.append(connection)
            
    def infect(self):
        self.state = State.INFECTED
        for connection in self.connections:
            if (connection.hasNode(self)):
                connection.setInfected()
        self.canvas.itemconfig(self.circle, fill="red")
    
class Connection (object):
    def __init__(self, node1: 'Node', node2: 'Node', canvas: 'Canvas'):
        nodes = [node1, node2]
        self.canvas = canvas
        self.connectionLine = self.canvas.create_line(nodes[0].x + nodes[0].width / 2, nodes[0].y + nodes[0].width / 2, nodes[1].x + nodes[1].width / 2, nodes[1].y + nodes[1].width / 2)
        
    def hasNode(self, node: 'Node'):
        return node == self.node1 or node == self.node2
    
    def getConnectionLine(self):
        return self.connectionLine
    
    def setInfected(self):
        self.canvas.itemconfig(self.connectionLine, fill="red")
    
    def setSusceptible(self):
        self.canvas.itemconfig(self.connectionLine, fill="black")
        
    def setRecovered(self):
        self.canvas.itemconfig(self.connectionLine, fill="grey")
        
    def compareConnection(self, connection: 'Connection'):
        return self.node1 == connection.node1 and self.node2 != connection.node2 or self.node1 != connection.node1 and self.node2 == connection.node2


class State (enumerate):
    INFECTED = 1
    SUSCEPTIBLE = 2
    RECOVERED = 3