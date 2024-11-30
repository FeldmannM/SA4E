# Michael Feldmann
import subprocess
import math

# Berechnung eines Torus durch die Anzahl der erwarteten Clients
def find_factors(number):
    sqrt_val = int(math.sqrt(number))
    for i in range(sqrt_val, 0, -1):
        if number % i == 0:
            return (i, number // i)
    return (1, number)

def start_server(num_clients, use_calculated):
    if use_calculated:
        n, m = find_factors(num_clients)
        subprocess.run(['python', 'firefly_server.py', str(n), str(m)])
    else:
        subprocess.run(['python', 'firefly_server.py'])

if __name__ == '__main__':
    # Argumente hier eingeben

    # Anzahl der erwarteten Clients
    num_clients = 12
    # Berechnete Werte fuer n und m verwenden (True/False)
    use_calculated = True

    start_server(num_clients, use_calculated)
