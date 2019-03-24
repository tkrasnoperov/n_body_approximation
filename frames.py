import numpy as np

class RotationalFrame():
    def __init__(self, center, omega):
        self.center = center
        self.omega = np.array([0, 0, omega])

    def field(self, x, v):
        return self.centrifugal(x) + self.coriolis(v)

    def centrifugal(self, x):
        return -np.cross(self.omega, np.cross(self.omega, x))

    def coriolis(self, v):
        return -2 * np.cross(self.omega, v)
