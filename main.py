import tkinter as tk
from map import Map

WIDTH = 1040
HEIGHT = 720
canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

map = Map(canvas, 100)
map.createConnections(100)

print("done")
canvas.mainloop()