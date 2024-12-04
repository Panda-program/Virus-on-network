import tkinter as tk

# Constants for window size
WIDTH = 1040
HEIGHT = 720


def setup_canvas(root): # Method for canvas
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # frame for canvas
    
    canvas = tk.Canvas(canvas_frame, width=WIDTH - 200, height=HEIGHT, bg="white") #canvas for canvas_frame
    canvas.pack()
    
    return canvas

def on_enter(e):
    button.config(bg="#005f73", fg="white")  # Darker background on hover

def on_leave(e):
    button.config(bg="#0a9396", fg="white")  # Original background when not hovering

def on_click():
    print("Button clicked!")

# Method for UI
def setup_ui(root):
    ui_frame = tk.Frame(root, width=200)
    ui_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Example buttons
    button = tk.Button(
        ui_frame,
        text="Click!",
        font=("Helvetica", 14, "bold"),  # Modern font
        bg="#0a9396",  # Initial button color
        fg="white",  # Text color
        relief="flat",  # Flat button, no borders
        width=15,
        height=2,
        bd=5,  # Border width (for a 3D effect)
        padx=10, pady=5,  # Padding inside the button
        activebackground="#005f73",  # Color when the button is clicked
        activeforeground="white",  # Text color when clicked
        highlightthickness=0,  # Remove focus highlight
        command=on_click,  # Set the command to run on click
    )   

    # Bind mouse hover effects to the button
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    # Pack the button into the window
    button.pack(pady=100)

    
    
def update(canvas): # Method for updating canvas
    
    canvas.after(1000, update, canvas)  # update every second

# Main application
def main():
    root = tk.Tk()
    root.title("Canvas and UI Example")

    # Set up canvas and UI
    canvas = setup_canvas(root)
    setup_ui(root)

    root.mainloop()
if __name__ == '__main__':
    main()
