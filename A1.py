# Michael Feldmann
import tkinter as tk
import threading
import time
import random
import math

class Firefly:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        # zufaelliger Anfangszustand
        self.phase = random.uniform(0, 2 * math.pi)
        # Natuerliche Frequenz
        self.omega = 1
        self.rect = canvas.create_rectangle(x, y, x + size, y + size, fill='darkblue', outline='')

    def update(self, neighbors):
        # Kuramoto-Modell
        # Kopplungsfaktor
        K = 0.1
        # Zeitintervall für Synchronisation
        delta_t = 0.1
        interaction = sum(math.sin(neighbor.phase - self.phase) for neighbor in neighbors)
        self.phase += self.omega * delta_t + (K / len(neighbors)) * interaction * delta_t

        # Aktualisierung der Farbe basierend auf der Phase
        if math.sin(self.phase) > 0:
            self.canvas.itemconfig(self.rect, fill='yellow')
        else:
            self.canvas.itemconfig(self.rect, fill='darkblue')

class Torus:
    def __init__(self, root, n, m):
        self.n = n
        self.m = m
        # Maximale Groeße des Fensters 600x600
        max_size = 600
        size = min(max_size // n, max_size // m)

        width = n * size
        height = m * size

        # GUI
        self.canvas = tk.Canvas(root, width=width, height=height, bg='black')
        self.canvas.pack()
        self.fireflies = []
        self.threads = []
        self.running = True
        for i in range(n):
            row = []
            for j in range(m):
                x = i * size
                y = j * size
                firefly = Firefly(self.canvas, x, y, size)
                row.append(firefly)
            self.fireflies.append(row)
        self.start_simulation()
        root.protocol("WM_DELETE_WINDOW", self.stop_simulation)

    def start_simulation(self):
        for i in range(self.n):
            for j in range(self.m):
                t = threading.Thread(target=self.run_firefly, args=(i, j))
                t.start()
                self.threads.append(t)

    def run_firefly(self, i, j):
        while self.running:
            neighbors = self.get_neighbors(i, j)
            self.fireflies[i][j].update(neighbors)
            time.sleep(0.1)

    # Berechnung der Nachbarn
    def get_neighbors(self, i, j):
        neighbors = [
            # oben
            self.fireflies[(i-1) % self.n][j],
            # links
            self.fireflies[i][(j-1) % self.m],
            # rechts
            self.fireflies[i][(j+1) % self.m],
            # unten
            self.fireflies[(i+1) % self.n][j]
        ]
        return neighbors

    def stop_simulation(self):
        self.running = False
        for t in self.threads:
            t.join()
        root.destroy()

if __name__ == '__main__':
    # Anzahl der Gluehwuermchen in Reihen und Spalten
    n, m = 4, 4
    root = tk.Tk()
    root.title(f'Aufgabe 1')
    Torus(root, n, m)
    root.mainloop()
