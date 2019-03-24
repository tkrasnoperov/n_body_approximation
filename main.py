from sys import exit
from time import time, sleep
import numpy as np
from tkinter import *

from configs import *
from utils import *
from space_map import *
from handle import *
from mesh import *
from monitor import *
from system import *
from run import *

conf = Configs("approximate")
gui, canvas = setup(conf)

R = 1.5
space_map = spacemap_from_orbit(conf.width, conf.height, 2 * R)

bodies_0 = []
bodies_1 = []
bodies_2 = []
bodies_3 = []
for i in range(100):
    location = random_sphere_point(R)
    velocity = random_surface_point(.1)
    mass = 1

    bodies_0.append(Body(mass, location.copy(), velocity.copy()))
    bodies_1.append(Body(mass, location.copy(), velocity.copy()))
    bodies_2.append(Body(mass, location.copy(), velocity.copy()))
    bodies_3.append(Body(mass, location.copy(), velocity.copy()))

# bodies_1 = bodies.copy()
# bodies_2 = bodies.copy()
# bodies_3 = bodies.copy()

color_0 = "#fff"
color_1 = "#ff0"
color_2 = "#f0f"
color_3 = "#0ff"

# system_0 = System(conf, bodies_0, n_procs=conf.n_procs)
system_1 = TreeSystem(gui, conf, bodies_1, theta=0, n_procs=conf.n_procs)
system_2 = TreeSystem(gui, conf, bodies_2, theta=.15, n_procs=conf.n_procs)
system_3 = TreeSystem(gui, conf, bodies_3, theta=.3, n_procs=conf.n_procs)

# system_0_handler = SystemHandler(gui, canvas, system_0, space_map, conf, color_0)
system_1_handler = SystemHandler(gui, canvas, system_1, space_map, conf, color_1)
system_2_handler = SystemHandler(gui, canvas, system_2, space_map, conf, color_2)
system_3_handler = SystemHandler(gui, canvas, system_3, space_map, conf, color_3)

tree_1_handler = TreeHandler(gui, canvas, system_1, space_map, conf, color_1)
tree_2_handler = TreeHandler(gui, canvas, system_2, space_map, conf, color_2)
tree_3_handler = TreeHandler(gui, canvas, system_3, space_map, conf, color_3)

systems = [
    # system_0,
    system_1,
    system_2,
    system_3
]
handlers = [
    # system_0_handler,
    system_2_handler,
    system_3_handler,

    tree_2_handler,
    tree_3_handler,

    system_1_handler,
    tree_1_handler,
]
monitor = EnergyMonitor(systems)

run(systems, handlers, monitor, conf)
# gui.mainloop()
