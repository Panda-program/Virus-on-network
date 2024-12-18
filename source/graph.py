import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

fig, ax = plt.subplots(figsize=(3, 2)) #velkost okna

ax.set_xlim(0, 100) #hodnoty na x suradnici
ax.set_ylim(0, 100) #hodnoty na y suradnici
ax.set_xlabel("čas") #nadpis suradnic
ax.set_ylabel("% uzlov")
ax.set_title("Stav Siete")

plt.show()
