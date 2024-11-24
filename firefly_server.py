# Michael Feldmann
import tkinter as tk
import threading
import grpc
from concurrent import futures
import time
import math
import firefly_pb2
import firefly_pb2_grpc
import sys

class Firefly:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.phase = -1
        self.rect = canvas.create_rectangle(x, y, x + size, y + size, fill='black', outline='')

    def set_phase(self, phase):
        self.phase = phase

    # GUI Update
    def update(self):
        if self.phase < 0:
            self.canvas.itemconfig(self.rect, fill='black')
        elif self.phase > math.pi:
            self.canvas.itemconfig(self.rect, fill='yellow')
        else:
            self.canvas.itemconfig(self.rect, fill='darkblue')

def get_toroidal_neighbors(x, y, n, m, fireflies):
    neighbors = []
    # Linker Nachbar
    left = (x - 1) % n
    while fireflies.get((left, y)) is None or fireflies[(left, y)].phase < 0:
        left = (left - 1) % n
    neighbors.append((left, y))

    # Rechter Nachbar
    right = (x + 1) % n
    while fireflies.get((right, y)) is None or fireflies[(right, y)].phase < 0:
        right = (right + 1) % n
    neighbors.append((right, y))

    # Oberer Nachbar
    up = (y - 1) % m
    while fireflies.get((x, up)) is None or fireflies[(x, up)].phase < 0:
        up = (up - 1) % m
    neighbors.append((x, up))

    # Unterer Nachbar
    down = (y + 1) % m
    while fireflies.get((x, down)) is None or fireflies[(x, down)].phase < 0:
        down = (down + 1) % m
    neighbors.append((x, down))

    return neighbors


class FireflyServiceServicer(firefly_pb2_grpc.FireflyServiceServicer):
    def __init__(self, fireflies):
        self.fireflies = fireflies
        self.positions = self.generate_positions()

    # Positionszuweisung im Torus
    def generate_positions(self):
        positions = []
        n, m = max(pos[0] for pos in self.fireflies.keys()) + 1, max(pos[1] for pos in self.fireflies.keys()) + 1

        size = 1
        while size <= max(n, m):
            for i in range(size):
                for j in range(size):
                    if i < n and j < m and (i, j) not in positions:
                        positions.append((i, j))
            size += 1

        for k in range(n):
            for l in range(m):
                if (k, l) not in positions:
                    positions.append((k, l))

        return iter(positions)

    # Positionsrueckgabe
    def GetPosition(self, request, context):
        try:
            position = next(self.positions)
            return firefly_pb2.PositionResponse(x=position[0], y=position[1])
        except StopIteration:
            context.set_code(grpc.StatusCode.OUT_OF_RANGE)
            context.set.details('No more positions available')
            return firefly_pb2.PositionResponse()

    # aktuelle Phase senden
    def SendPhases(self, request, context):
        firefly = self.fireflies.get((request.x, request.y))
        if firefly:
            firefly.set_phase(request.phases[0].phase)
            n = len({k[0] for k in self.fireflies.keys()})  # Anzahl der Reihen
            m = len({k[1] for k in self.fireflies.keys()})  # Anzahl der Spalten
            neighbors = get_toroidal_neighbors(request.x, request.y, n, m, self.fireflies)
            ''' #Debug-Ausgabe der Nachbarn und ihrer Phasen
            print(f"Client ({request.x}, {request.y}) hat Nachbarn:")
            for nx, ny in neighbors:
                phase = self.fireflies[(nx, ny)].phase
                print(f"  - Nachbar ({nx}, {ny}) mit Phase {phase}")
            '''
            neighbor_phases = [firefly_pb2.Phase(x=nx, y=ny, phase=self.fireflies[(nx, ny)].phase) for nx, ny in
                               neighbors]
            return firefly_pb2.PhasesResponse(phases=neighbor_phases)
        return firefly_pb2.PhasesResponse()


# Server unter Port 50051 starten
def serve(fireflies):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    firefly_pb2_grpc.add_FireflyServiceServicer_to_server(FireflyServiceServicer(fireflies), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    return server

def main():
    # Feste Werte verwenden, ausser sie werden vom Startskript überschrieben
    n = 5
    m = 5
    if len(sys.argv) == 3:
        n = int(sys.argv[1])
        m = int(sys.argv[2])

    #GUI
    root = tk.Tk()
    root.title(f'Firefly Server')
    max_size = 600
    size = min(max_size // n, max_size // m)
    width = n * size
    height = m * size

    canvas = tk.Canvas(root, width=width, height=height, bg='black')
    canvas.pack()
    fireflies = {}

    for i in range(n):
        for j in range(m):
            x, y = i * size, j * size
            firefly = Firefly(canvas, x, y, size)
            fireflies[(i, j)] = firefly

    server = serve(fireflies)

    # Aktualisierung der Server GUI
    def update_gui():
        while True:
            phases = [(x, y, firefly.phase) for (x, y), firefly in fireflies.items()]
            root.after(100, lambda: apply_updates(phases))
            time.sleep(0.1)

    def apply_updates(phases):
        for x, y, phase in phases:
            fireflies[(x, y)].update()
        root.update_idletasks()

    gui_thread = threading.Thread(target=update_gui)
    gui_thread.start()

    def on_closing():
        server.stop(0)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
