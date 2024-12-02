
from simulator import Simulation

machines = ['M1', 'M2', 'M3']
simulation = Simulation(machines)

arrival_rates = {'A': 4, 'B': 8, 'C': 10}
processing_params = {'A': (5, 2), 'B': (7, 2), 'C': (8, 1.2)}
simulation.run(1000, arrival_rates, processing_params)
