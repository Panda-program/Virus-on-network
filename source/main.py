import tkinter as tk
import tkinter.ttk as ttk
from ui import UI

# Constants for window size
WIDTH = 1200
HEIGHT = 720

class MainApp:
    """
    Main application class that sets up the tkinter window, canvas, and UI elements.
    """

    def __init__(self, root):
        """
        Initializes the application with the given tkinter root window.

        :param root: The root tkinter window.
        """
        self.root = root
        self.root.title("Canvas and UI Example")
        self.canvas = self.setup_canvas()
        self.setup_ui()

    def setup_canvas(self):
        """
        Sets up the canvas for drawing.

        :returns: A tkinter Canvas object.
        """
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # frame for canvas
        canvas = tk.Canvas(canvas_frame, width=WIDTH - 400, height=HEIGHT, bg="black")  # canvas for canvas_frame
        canvas.pack()
        return canvas

    def setup_ui(self):
        """
        Sets up the UI elements on the left side of the window.

        Creates a UI object and calls its setup method.
        """
        ui_frame = tk.Frame(self.root, width=200)
        ui_frame.pack(side=tk.LEFT, fill=tk.Y)
        ui = UI(self.root, self.canvas, ui_frame, tk, ttk)
        ui.setup()

    def run(self):
        """
        Starts the main event loop of the tkinter application.
        """
        self.root.mainloop()

def main():
    """
    Creates the root tkinter window, initializes the MainApp, and runs the application.
    """
    root = tk.Tk()
    app = MainApp(root)
    app.run()

if __name__ == '__main__':
    main()
