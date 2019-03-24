from sys import exit
from pathos.multiprocessing import ProcessingPool as Pool
import numpy as np

from utils import *
from runge_kutta import *
from tree import *

import pdb

class Body():
    def __init__(self, mass, location, velocity=[0, 0, 0]):
        self.mass = mass
        self.location = np.array(location)
        self.velocity = np.array(velocity)

class System():
    def __init__(self, conf, bodies, frame=None, n_procs=1):
        self.conf = conf
        self.bodies = bodies
        self.n = len(bodies)
        self.frame = frame

        self.n_procs = n_procs
        self.pool = Pool(self.n_procs)

    def update(self, h):
        new_states = self.pool.map(self.compute_new_state, [(body, h) for body in self.bodies])

        for new_state, body in zip(new_states, self.bodies):
            body.location, body.velocity = new_state

    def compute_new_state(self, args):
        body, h = args
        state = np.array([body.location, body.velocity])

        k1 = h * self.state_dt(state, body)
        k2 = h * self.state_dt(state + k1 / 2., body)
        k3 = h * self.state_dt(state + k2 / 2., body)
        k4 = h * self.state_dt(state + k3, body)

        return state + (k1 + 2. * k2 + 2. * k3 + k4) / 6.

    def state_dt(self, state, body):
        x = state[0]
        v = state[1]
        field = self.grav_field(x, exclude_bodies=[body])
        if self.frame:
            field += self.frame.field(x, v)

        return np.array([v, field])

    def grav_field(self, location, exclude_bodies=[]):
        location = np.array(location)
        bodies = [body for body in self.bodies if body not in exclude_bodies]

        return np.sum([self.body_grav_field(body, location) for body in bodies], axis=0)

    def body_grav_field(self, body, location):
        diff = body.location - location
        dist = np.linalg.norm(diff)

        mag = self.conf.G * body.mass / (np.power(dist, 2) + np.power(self.conf.alpha, 2))
        mag = mag if mag != np.inf else 0

        return mag * diff / dist

    def energy(self):
        kinetic = np.sum([.5 * body.mass * np.linalg.norm(body.velocity) ** 2 for body in self.bodies])
        return kinetic

    def momentum(self):
        return np.sum([body.mass * body.velocity for body in self.bodies], axis=0)

class TreeSystem(System):
    n_dims = 3

    def __init__(self, gui, conf, bodies, frame=None, theta=.1, n_procs=8):
        super().__init__(conf, bodies, frame=frame, n_procs=n_procs)

        self.theta = theta
        self.root = self.make_tree()

    def update(self, h):
        new_states = self.pool.map(self.compute_new_state, [(body, h) for body in self.bodies])

        for new_state, body in zip(new_states, self.bodies):
            body.location, body.velocity = new_state

        self.root = self.make_tree()

    def make_tree(self):
        # side = 2 * max([np.max(np.abs(body.location)) for body in self.bodies])
        side = 6
        origin = [0] * self.conf.n_dims

        root = TreeNode(origin, side)
        for body in self.bodies:
            root.add(body)

        return root

    def grav_field(self, location, exclude_bodies=[]):
        f = self.tree_grav_field(location, self.root, exclude_bodies=exclude_bodies)
        # print('f', f)
        return f

    def tree_grav_field(self, location, tree, exclude_bodies=[]):
        if tree.n_bodies == 0:
            return np.zeros(TreeSystem.n_dims)
        if tree.n_bodies == 1 and exclude_bodies[0] == tree.bodies[0]:
            return np.zeros(TreeSystem.n_dims)
        if tree.n_bodies == 1:
            body = tree.bodies[0]
            # assert(np.array_equal(tree.center, tree.bodies[0].location))
            return self.body_grav_field(body, location)

        dist = np.linalg.norm(tree.center - location)
        # print(tree.side, dist * self.theta)

        if tree.side < dist * self.theta:
            # print("approx")
            body = Body(tree.mass, tree.center)
            # print("body", tree.mass, tree.n_bodies)
            return self.body_grav_field(body, location)

        # print("recurse")
        # print(len(tree.children))
        field = np.sum([self.tree_grav_field(location, child, exclude_bodies=exclude_bodies) for child in tree.children], axis=0)
        # print("f", field)
        return field
