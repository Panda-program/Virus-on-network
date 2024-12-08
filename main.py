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

    # Example buttons
    # button1 = tk.Button(ui_frame, text="Button 1", command=lambda: print("Button 1 clicked"))
    # button1.pack(pady=10)

    # button2 = tk.Button(ui_frame, text="Button 2", command=lambda: print("Button 2 clicked"))
    # button2.pack(pady=10)
    # update every second

# Main application
def main():
    number_of_nodes = 300
    avg_node_degree = 4
    infected_nodes = 1
    recovered_nodes = 10
    root = tk.Tk()
    root.title("Canvas and UI Example")
    # Set up canvas and UI
    canvas = setup_canvas(root)
    setup_ui(root)
    map = Map(canvas, number_of_nodes, avg_node_degree, infected_nodes, recovered_nodes)
    while(map.isMapLoaded == False):
        pass
    map.tick()

    root.mainloop()
if __name__ == '__main__':
    main()
