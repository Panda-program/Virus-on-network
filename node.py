import tkinter as tk

class Node (object):
    def __init__(self, x: 'int', y: 'int', infected: 'bool'):
        self.x = x
        self.y = y
        self.infected = infected
        self.neighbors = []
        self.circle = tk.Canvas.create_oval(x, y, x+10, y+10, fill="red" if infected else "blue")

    def add_neighbor(self, neighbor: 'Node'):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.add_neighbor(self)
    
    def infect(self):
        self.infected = True
        tk.Canvas.itemconfig(self.circle, fill="red")
    