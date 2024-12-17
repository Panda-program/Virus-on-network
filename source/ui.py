from map import Map

class UI:
    def __init__(self, root, canvas, frame, tk, ttk):
        self.root = root
        self.canvas = canvas
        self.frame = frame
        self.tk = tk
        self.ttk = ttk
        self.map = Map(self.canvas)
        self.sliders = [
            ("number-of-nodes", 0, 350, False),
            ("average-node-degree", 0, 50, False),
            ("initial-outbreak-size", 0, 350, False),
            ("virus-spread-chance", 0, 100, True),
            ("virus-check-frequency", 1, 100, True),
            ("recovery-chance", 0, 100, True),
            ("gain-resistance-chance", 0, 100, True),
            ("Model speed", 0, 1000, False)
        ]
        self.slider_widgets = []
        self.labels = []

    def update_label(self, value_label, slider, formatDecimal):
        if formatDecimal:
            value_label.config(text=f'{slider.get():.2f}%')
        else:
            value_label.config(text=f'{slider.get():.0f}')

    def setup(self):
        for i, (text, min, max, formatDecimal) in enumerate(self.sliders):
            slider_frame = self.tk.Frame(self.frame, bg="#d9f7d9", width=200)
            slider_frame.pack(fill=self.tk.X, pady=10, padx=0, ipady=5, ipadx=20)
            label_frame = self.tk.Frame(slider_frame, bg="#d9f7d9")
            label_frame.grid(row=i * 2, column=0, pady=0, sticky="w")
            label = self.tk.Label(label_frame, text=text, bg="#d9f7d9", font=("Helvetica", 10), anchor="w")
            label.pack(side="left", padx=5)
            if formatDecimal:
                value_label = self.tk.Label(label_frame, text=f'{max/2:.2f}%', padx=4, pady=2, bg="#ffffff", bd=1, relief="solid", font=("Helvetica", 10))
            else:
                value_label = self.tk.Label(label_frame, text=f'{max/2:.0f}', padx=4, pady=2, bg="#ffffff", bd=1, relief="solid", font=("Helvetica", 10))
            value_label.pack(side="right", padx=5)
            slider = self.ttk.Scale(slider_frame, from_=min, to=max, value=max/2, orient="horizontal")
            slider.grid(row=(i * 2) + 1, column=0, sticky="ew", padx=5, pady=0)
            slider_frame.grid_columnconfigure(0, weight=1)
            slider.bind("<Motion>", lambda event, value_label=value_label, slider=slider, formatDecimal=formatDecimal: self.update_label(value_label, slider, formatDecimal))
            self.slider_widgets.append(slider)
            self.labels.append(value_label)

        button_frame = self.tk.Frame(self.frame)
        button_frame.pack(pady=10, padx=20)
        setup_button = self.tk.Button(button_frame, text="Setup", bg="#99cc99", font=("Helvetica", 12))
        setup_button.grid(row=0, column=0, padx=10)
        go_button = self.tk.Button(button_frame, text="Go", bg="#a3c4fc", font=("Helvetica", 12))
        go_button.grid(row=0, column=1, padx=10)
        reset_button = self.tk.Button(button_frame, text="Reset", bg="#f9d5d3", font=("Helvetica", 12))
        reset_button.grid(row=0, column=2, padx=10)
        setup_button.bind("<Button-1>", self.setup_map)
        go_button.bind("<Button-1>", self.start_simulation)
        reset_button.bind("<Button-1>", self.reset_simulation)

    def setup_map(self, event):
        number_of_nodes = int(self.slider_widgets[0].get())
        avg_node_degree = int(self.slider_widgets[1].get())
        initial_outbreak_size = int(self.slider_widgets[2].get())
        virus_spread_chance = float(self.slider_widgets[3].get())
        virus_check_frequency = float(self.slider_widgets[4].get())
        recovery_chance = float(self.slider_widgets[5].get())
        gain_resistance_chance = float(self.slider_widgets[6].get())
        speed = int(self.slider_widgets[7].get())
        self.map.setup(speed, number_of_nodes, avg_node_degree, initial_outbreak_size, virus_spread_chance, virus_check_frequency, recovery_chance, gain_resistance_chance)

    def start_simulation(self, event):
        self.map.tick()

    def reset_simulation(self, event):
        self.map.reset()