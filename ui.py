class UI:
    def __init__(self, root, map, frame, tk, ttk):
        self.root = root
        self.map = map
        self.frame = frame
        self.tk = tk
        self.ttk = ttk
        self.sliders = [
            ("number-of-nodes", 0, 350, False),
            ("average-node-degree", 0, 350, False),
            ("initial-outbreak-size", 0, 350, False),
            ("virus-spread-chance", 0, 100, True),
            ("virus-check-frequency", 1, 100, True),
            ("recovery-chance", 0, 100, True),
            ("gain-resistance-chance", 0, 100, True),
            ("Model speed", 0, 1000, False)
        ]
        self.slider_widgets = []
        self.labels = []  # Store references to the value labels for each slider

    def update_label(self, value_label, slider, formatDecimal):
        if formatDecimal:
            # Format to 2 decimal places
            value_label.config(text=f'{slider.get():.2f}%')
        else:
            # Format to 0 decimal places
            value_label.config(text=f'{slider.get():.0f}')

    def setup(self):
        # Create sliders and corresponding labels to display values


        # Create sliders and arrange them in the required format
        for i, (text, min, max, formatDecimal) in enumerate(self.sliders):
            slider_frame = self.tk.Frame(self.frame, bg="#d9f7d9", width=200)
            slider_frame.pack(fill=self.tk.X, pady=10, padx=0, ipady=5, ipadx=20)
            # Frame for the label and value in one row
            label_frame = self.tk.Frame(slider_frame, bg="#d9f7d9")
            label_frame.grid(row=i * 2, column=0, pady=0, sticky="w")

            # Label for the name of the slider
            label = self.tk.Label(label_frame, text=text, bg="#d9f7d9", font=("Helvetica", 10), anchor="w")
            label.pack(side="left", padx=5)  # Slider label on the left

            # Value label on the right side of the same row
            if formatDecimal:
                value_label = self.tk.Label(label_frame, text=f'{max/2:.2f}%', padx=4, pady=2, bg="#ffffff", bd=1, relief="solid", font=("Helvetica", 10))
            else:
                value_label = self.tk.Label(label_frame, text=f'{max/2:.0f}', padx=4, pady=2, bg="#ffffff", bd=1, relief="solid", font=("Helvetica", 10))
            value_label.pack(side="right", padx=5)  # Value label on the right

            # Slider placed in the next row below the label and value
            slider = self.ttk.Scale(slider_frame, from_=min, to=max, value=max/2, orient="horizontal")
            slider.grid(row=(i * 2) + 1, column=0, sticky="ew", padx=5, pady=0)  # Slider in the next row

            # Ensure the slider stretches fully by configuring the column weight
            slider_frame.grid_columnconfigure(0, weight=1)

            # Bind the slider to update the value label when the slider is moved
            slider.bind("<Motion>", lambda event, value_label=value_label, slider=slider, formatDecimal=formatDecimal: self.update_label(value_label, slider, formatDecimal))

            # Store the slider and its corresponding value label
            self.slider_widgets.append(slider)
            self.labels.append(value_label)

        # Create buttons in a separate row
        button_frame = self.tk.Frame(self.frame)
        button_frame.pack(pady=10, padx=20)

        setup_button = self.tk.Button(button_frame, text="Setup", bg="#99cc99", font=("Helvetica", 12))
        setup_button.grid(row=0, column=0, padx=10)

        go_button = self.tk.Button(button_frame, text="Go", bg="#a3c4fc", font=("Helvetica", 12))
        go_button.grid(row=0, column=1, padx=10)

        reset_button = self.tk.Button(button_frame, text="Reset", bg="#f9d5d3", font=("Helvetica", 12))
        reset_button.grid(row=0, column=2, padx=10)

        # Button bindings
        setup_button.bind("<Button-1>", self.setup_map)
        go_button.bind("<Button-1>", self.start_simulation)
        reset_button.bind("<Button-1>", self.reset_simulation)


    def setup_map(self, event):
        # Get values from sliders and pass them to the map setup
        number_of_nodes = int(self.slider_widgets[0].get())
        avg_node_degree = int(self.slider_widgets[1].get())
        initial_outbreak_size = int(self.slider_widgets[2].get())
        virus_spread_chance = float(self.slider_widgets[3].get())
        virus_check_frequency = float(self.slider_widgets[4].get())
        recovery_chance = float(self.slider_widgets[5].get())
        gain_resistance_chance = float(self.slider_widgets[6].get())
        speed = int (self.slider_widgets[7].get())

        # Update map parameters and run setup
        self.map.numberOfNodes = number_of_nodes
        self.map.avgNodeDegree = avg_node_degree
        self.map.initial_outbreak_size = initial_outbreak_size
        self.map.virus_spread_chance = virus_spread_chance
        self.map.virus_check_frequency = virus_check_frequency
        self.map.recovery_chance = recovery_chance
        self.map.gain_resistance_chance = gain_resistance_chance
        self.map.speed = speed

        self.map.setup()

    def start_simulation(self, event):
        # Start the simulation by calling tick on the map
        self.map.tick()

    def reset_simulation(self, event):
        # Reset the simulation
        self.map.reset()