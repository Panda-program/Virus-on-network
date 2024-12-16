import tkinter as tk
from tkinter import ttk
from map import Map
from UI import UI

# Constants for window size
WIDTH = 1040
HEIGHT = 720


def setup_canvas(root): # Method for canvas
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True) # frame for canvas
    canvas = tk.Canvas(canvas_frame, width=WIDTH - 200, height=HEIGHT, bg="black") #canvas for canvas_frame
    canvas.pack()
    return canvas

# Method for UI
def setup_ui(root, map):
    ui_frame = tk.Frame(root, width=200)
    ui_frame.pack(side=tk.LEFT, fill=tk.Y, pady=0)

    ui = UI(root, map, ui_frame, tk, ttk)
    ui.setup()

number_of_nodes = 4
avg_node_degree = 3
initial_outbreak_size = 1
virus_spread_chance = 20.0
virus_check_frequency = 1
recovery_chance = 4.0
gain_resistance_chance = 3.0
speed = 100 # in milliseconds

root = tk.Tk()
root.title("Canvas and UI Example")
canvas = setup_canvas(root)

map = Map(canvas, speed, number_of_nodes, avg_node_degree, initial_outbreak_size, virus_spread_chance, virus_check_frequency, recovery_chance, gain_resistance_chance)
setup_ui(root, map)

root.mainloop()
