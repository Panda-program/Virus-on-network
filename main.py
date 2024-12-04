import tkinter as tk
from map import Map

WIDTH = 1040
HEIGHT = 720
canvas = tk.Canvas(width=WIDTH, height=HEIGHT)
canvas.pack()

map = Map(canvas)
map.createMap(10)
print("SUPER")

if __name__ == '__main__':
    canvas.mainloop()