class Node (object):
    def __init__(self, canvas, x: 'int', y: 'int', infected: 'bool'):
        self.width = 35
        self.canvas = canvas
        self.x = x
        self.y = y
        self.infected = infected
        self.neighbors = []
        self.circle = self.canvas.create_oval(x, y, x + self.width, y + self.width, fill="red" if infected else "blue")

    def createConnection(self, neighbor: 'Node'):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.add_neighbor(self)
    
    def infect(self):
        self.infected = True
        self.canvas.itemconfig(self.circle, fill="red")
    