import tkinter as tk

WIDTH = 1040
HEIGHT = 720

root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}") 


canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.grid(row=0, column=0, sticky="nsew")  


button = tk.Button(
    root,
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)
button.grid(row=0, column=0)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()

