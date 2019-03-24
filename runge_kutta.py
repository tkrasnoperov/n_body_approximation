import numpy as np

def RK4(state, f, h):
    k1 = h * f(state)
    k2 = h * f(state + k1 / 2.)
    k3 = h * f(state + k2 / 2.)
    k4 = h * f(state + k3)

    return state + (k1 + 2. * k2 + 2. * k3 + k4) / 6.
