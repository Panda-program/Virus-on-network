import tkinter as tk
from map import Map
import time

# Constants for window size
WIDTH = 1040
HEIGHT = 720


def setup_canvas(root): # Method for canvas
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # frame for canvas
    canvas = tk.Canvas(canvas_frame, width=WIDTH - 200, height=HEIGHT, bg="black") #canvas for canvas_frame
    canvas.pack()
    return canvas

# Method for UI
def setup_ui(root):
    ui_frame = tk.Frame(root, width=200)
    ui_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Main application
def main():
    number_of_nodes = 200
    avg_node_degree = 3
    initial_outbreak_size = 20
    virus_spread_chance = 20.0
    virus_check_frequency = 1
    recovery_chance = 4.0
    gain_resistance_chance = 3.0
    speed = 20 # in milliseconds
    
    root = tk.Tk()
    root.title("Canvas and UI Example")
    canvas = setup_canvas(root)
    setup_ui(root)
    
    map = Map(canvas, speed, number_of_nodes, avg_node_degree, initial_outbreak_size, virus_spread_chance, virus_check_frequency, recovery_chance, gain_resistance_chance)
    map.setup()
    map.tick()
    while(map.isMapLoaded == False):
        pass
    
    map.tick()

    root.mainloop()
if __name__ == '__main__':
    main()
