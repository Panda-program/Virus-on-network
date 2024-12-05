import tkinter as tk
from map import Map

WIDTH = 1040
HEIGHT = 720
canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

map = Map(canvas)
map.createMap(10)
map.createConnections(200, 2)

print("done")
canvas.mainloop()