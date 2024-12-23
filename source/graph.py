import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class GRAPH:
    def __init__(self):
        self.x_data = []
        self.y1_data = []
        self.y2_data = []
        self.y3_data = []


        self.fig = plt.figure(figsize=(3.7, 1.7))


        self.ani = animation.FuncAnimation(self.fig, self.update, interval=500)  # Update every 500ms

    def update(self, frame):
        new_x = len(self.x_data) + 1
        new_y1 = random.randint(0, 100)
        new_y2 = random.randint(0, 100)
        new_y3 = random.randint(0, 100)

        self.x_data.append(new_x)
        self.y1_data.append(new_y1)
        self.y2_data.append(new_y2)
        self.y3_data.append(new_y3)

        self.fig.clear()

        ax = self.fig.add_subplot(1, 1, 1)
        ax.plot(self.x_data, self.y1_data, color='red', label='infected')
        ax.plot(self.x_data, self.y2_data, color='blue', label='susceptible')
        ax.plot(self.x_data, self.y3_data, color='grey', label='resistant')

        ax.set_title("Network Status", fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.legend(fontsize=8)

    def show(self):
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.show()

if __name__ == "__main__": #na spustenie grafu samotneho 
    graph = GRAPH()
    graph.show()