import tkinter as tk
from node import Node, State

WIDTH = 1040
HEIGHT = 720
canvas = tk.Canvas(width=WIDTH, height=HEIGHT)
canvas.pack()

testNode = Node(canvas, 10, 10, State.SUSCEPTIBLE)
secondNode = Node(canvas, 100, 100, State.SUSCEPTIBLE)   
testNode.createConnection(secondNode)

if __name__ == '__main__':
    canvas.mainloop()