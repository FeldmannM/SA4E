# Michael Feldmann
import subprocess

def start_clients(num_clients):
    processes = []
    for _ in range(num_clients):
        p = subprocess.Popen(['python', 'firefly_client.py'])
        processes.append(p)

    for p in processes:
        p.wait()

if __name__ == '__main__':
    num_clients = 12  # Anzahl der Clients, die gestartet werden sollen
    start_clients(num_clients)
