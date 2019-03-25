import numpy as np
# import matplotlib.pyplot as plt

class EnergyMonitor():
    def __init__(self, systems):
        self.systems = systems
        self.states = [[] for _ in range(len(systems))]

    def track(self):
        for i in range(len(self.systems)):
            # print(self.systems[i].momentum())
            self.states[i].append(self.systems[i].momentum()[0])

    def print_states(self, filename="logs/energy.txt"):
        with open(filename, 'w') as f:
            for state in self.states:
                print(",".join([str(x) for x in state]), file=f)
