# Michael Feldmann
import grpc
import time
import firefly_pb2
import firefly_pb2_grpc
import math
import random
import threading
import tkinter as tk

class FireflyClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = firefly_pb2_grpc.FireflyServiceStub(self.channel)
        self.x, self.y = self.get_position()
        self.phase = random.uniform(0, 2 * math.pi)

        # GUI
        self.root = tk.Tk()
        self.root.title(f'{self.x}, {self.y}')
        self.size = 200
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, bg='black')
        self.canvas.pack()
        self.rect = self.canvas.create_rectangle(0, 0, self.size, self.size, fill='darkblue')

    # Positionsabfrage, falls noch freie Plaetze vorhanden sind
    def get_position(self):
        try:
            request = firefly_pb2.PositionRequest()
            response = self.stub.GetPosition(request)
            return response.x, response.y
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.OUT_OF_RANGE:
                print("No more positions available")
                return None, None
            else:
                raise

    # aktuelle Phase senden
    def send_phases(self):
        if self.x is not None and self.y is not None:
            request = firefly_pb2.PhasesRequest(x=self.x, y=self.y, phases=[firefly_pb2.Phase(x=self.x, y=self.y, phase=self.phase)])
            return self.stub.SendPhases(request)
        return None

    def run(self):
        self.running = True
        threading.Thread(target=self.update_phase_loop).start()
        self.root.after(100, self.update_color_loop)
        self.root.mainloop()

    # Phasen Update
    def update_phase_loop(self):
        while self.running:
            response = self.send_phases()
            if response:
                neighbor_phases = [p.phase for p in response.phases]
                self.update_phase(neighbor_phases)
            time.sleep(0.05)

    # GUI Update
    def update_color_loop(self):
        if self.phase > math.pi:
            self.canvas.itemconfig(self.rect, fill='yellow')
        else:
            self.canvas.itemconfig(self.rect, fill='darkblue')
        self.root.after(100, self.update_color_loop)

    # Anwendung des Kuramoto-Modells
    def update_phase(self, neighbor_phases):
        if neighbor_phases:
            # Kopplungsfaktor
            K = 0.05
            # Zeitintervall für Synchronisation
            delta_t = 0.05
            interaction = sum(math.sin(neighbor_phase - self.phase) for neighbor_phase in neighbor_phases)
            self.phase += delta_t + (K / len(neighbor_phases)) * interaction * delta_t
            # Phase im Bereich [0, 2π] halten
            self.phase %= 2 * math.pi

    def stop(self):
        self.running = False

if __name__ == '__main__':
    client = FireflyClient()
    if client.x is not None and client.y is not None:
        client.run()
    else:
        print("Client could not get a valid position.")
