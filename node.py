class Node (object):
    def __init__(self, canvas, x: 'int', y: 'int', state: 'State'):
        self.width = 35
        self.canvas = canvas
        self.x = x
        self.y = y
        self.connections = []
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
        self.nodes = [node1, node2]
        self.canvas = canvas
        self.connectionLine = self.canvas.create_line(self.nodes[0].x + self.nodes[0].width / 2, #x1
                                                      self.nodes[0].y + self.nodes[0].width / 2, #y1
                                                      self.nodes[1].x + self.nodes[1].width / 2, #x2
                                                      self.nodes[1].y + self.nodes[1].width / 2, #y2
                                                      width=2)
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
        if (self.nodes[0].state == State.RECOVERED or self.nodes[1].state == State.RECOVERED):
            self.connectionLine.config(fill="grey")
        else:
            self.connectionLine.config(fill="black")
        
    def compareConnection(self, connection: 'Connection'):
        conNode1 = connection.getFirstNode()
        conNode2 = connection.getSecondNode()
        return self.nodes[0] == conNode1 and self.nodes[1] != conNode2 or self.node[0] != conNode1 and self.nodes[1] == conNode2


class State (enumerate):
    INFECTED = 1
    SUSCEPTIBLE = 2
    RECOVERED = 3