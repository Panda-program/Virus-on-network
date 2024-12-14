import tkinter as tk
from tkinter import ttk

# Method for UI
root = tk.Tk()
root.geometry("500x600")

# Pozadie 
control_frame = tk.Frame(root, bg="lightblue", width=250, height=600)
control_frame.pack(side="left", fill="y")

# Sliders
sliders = [
    ("number-of-nodes", 150),
    ("average-node-degree", 6),
    ("initial-outbreak-size", 3),
    ("virus-spread-chance", 2.5),
    ("virus-check-frequency", 1),
    ("recovery-chance", 5),
    ("gain-resistance-chance", 5),
]

slider_widgets = []
for text, value in sliders:
    label = tk.Label(control_frame, text=text, bg="lightblue")
    label.pack(pady=5)
    slider = ttk.Scale(control_frame, from_=0, to=100, value=value, orient="horizontal")
    slider.pack(pady=5, fill="x")
    slider_widgets.append(slider)

# Buttons
setup_button = tk.Button(control_frame, text="Setup", bg="white")
setup_button.pack(pady=10, fill="x")

go_button = tk.Button(control_frame, text="Go", bg="white")
go_button.pack(pady=10, fill="x")

reset_button = tk.Button(control_frame, text="Reset", bg="white")
reset_button.pack(pady=10, fill="x")

# Cierny screen 
# canvas = tk.Canvas(root, bg="black", width=400, height=400)
# canvas.pack(side="right", fill="both", expand=True)

# Main application
def main():
    root = tk.Tk()
    root.title("Canvas and UI Example")
    root.mainloop()
if __name__ == '__main__':
    main()
