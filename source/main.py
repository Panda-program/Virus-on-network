import tkinter as tk
from tkinter import ttk
from map import Map
from ui import UI

# Constants for window size
WIDTH = 1200
HEIGHT = 720


def setup_canvas(root): # Method for canvas
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True) # frame for canvas
    canvas = tk.Canvas(canvas_frame, width=WIDTH - 400, height=HEIGHT, bg="black") #canvas for canvas_frame
    canvas.pack()
    return canvas

# Method for UI
def setup_ui(root, canvas):
    ui_frame = tk.Frame(root, width=200)
    ui_frame.pack(side=tk.LEFT, fill=tk.Y)
    ui = UI(root, canvas, ui_frame, tk, ttk)
    ui.setup()

# Main application
def main():
    root = tk.Tk()
    root.title("Canvas and UI Example")
    canvas = setup_canvas(root)
    setup_ui(root, canvas)
    root.mainloop()
if __name__ == '__main__':
    main()
