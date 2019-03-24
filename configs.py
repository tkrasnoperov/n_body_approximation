import numpy as np

from utils import *

class Configs():
    def __init__(self, name="unnamed"):
        self.n_procs = 8

        self.name = name
        self.movie = None

        self.theta = [0, .15, .3]

        # self.n_dimensions = 2
        self.n_dims = 3
        self.G = 1
        self.alpha = .1

        self.width = 800
        self.height = 800
        self.center = np.array([self.width / 2, self.height / 2])

        self.n_frames = 5
        self.n_steps = 1
        self.h = .001

        self.low_color = np.array([.2, .05, .1])
        self.high_color = np.array([.8, .8, 1])
        self.diff_color = self.high_color - self.low_color

        self.low_radius = 2
        self.high_radius = 5
        self.diff_radius = self.high_radius - self.low_radius

        self.c_color = .5
        self.k_color = 1.5
        self.c_radius = 0
        self.k_radius = 1.5

        self.color_scale = lambda x: sigmoid(x, c=self.c_color, k=self.k_color)
        self.radius_scale = lambda x: sigmoid(x, c=self.c_radius, k=self.k_radius)

def radius_from_depth(z, conf):
    radius_tanh = conf.radius_scale(np.linalg.norm(z))
    radius = conf.low_radius + radius_tanh * conf.high_radius

    return radius

def color_from_depth(z, conf):
    color_tanh = conf.color_scale(np.linalg.norm(z))
    color = hex_from_color(conf.low_color + color_tanh * conf.diff_color)

    return color

def color_from_mass(mass, conf):
    mass_tanh = conf.scale(np.linalg.norm(mass))
    color = hex_from_color(conf.low_color + mass_tanh * conf.diff_color)

    return color

def color_from_field(field, conf):
    field_tanh = conf.scale(np.linalg.norm(field))
    color = hex_from_color(conf.low_color + field_tanh * conf.diff_color)

    return color
