import tkinter as tk

class Noda (object):
    def __init__(self, x, y, infected):
        self.x = x
        self.y = y
        self.infected = infected
        self.neighbors = []
        self.circle = tk.Canvas.create_oval(x, y, x+10, y+10, fill="red" if infected else "blue")

    
    