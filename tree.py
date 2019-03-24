from pathos.multiprocessing import ProcessingPool as Pool
import numpy as np

class TreeNode():
    n_dims = 3
    n_children = 2 ** n_dims
    children_indices = np.arange(n_children).reshape([2] * n_dims)

    def __init__(self, origin, side):
        self.origin = np.array(origin)
        self.side = side

        self.bodies = []
        self.n_bodies = len(self.bodies)

        self.children = None
        self.set_center_of_mass()

    def add(self, body):
        if self.n_bodies == 1:
            self.make_children()
            self.locate_child(self.bodies[0].location).add(self.bodies[0])

        if self.n_bodies >= 1:
            self.locate_child(body.location).add(body)

        self.bodies.append(body)
        self.n_bodies = len(self.bodies)
        self.set_center_of_mass()

    def make_children(self):
        self.children = []
        child_side = self.side / 2
        for i in range(2 ** TreeNode.n_dims):
            # print(i, "bin:", binary(i, TreeNode.n_dims))
            origin = self.origin + child_side * (binary(i, TreeNode.n_dims) - .5)
            child = TreeNode(origin, child_side)

            self.children.append(child)

    def locate_child(self, location):
        location = (location - self.origin) > 0
        child = self.children[decimal(location)]
        # print(location, decimal(location), self.origin, child.origin)

        return child

    def set_center_of_mass(self):
        if self.n_bodies:
            self.center, self.mass = center_of_mass(self.bodies)
        else:
            self.center = np.zeros(TreeNode.n_dims)
            self.mass = 0

    def print_tree(self, indent=0):
        print("\t" * indent, self.n_bodies)
        if self.children:
            for child in self.children:
                child.print_tree(indent=indent + 1)

def center_of_mass(bodies):
    masses = np.array([body.mass for body in bodies])
    locations = np.array([body.location for body in bodies])

    total_mass = np.sum(masses)
    mass_shape = np.sum([masses[i] * locations[i] for i in range(len(masses))], axis=0)
    # print(total_mass)
    # print(mass_shape)
    center = mass_shape / total_mass
    # print("center", center)

    # print(center)
    # exit()
    return center, total_mass

def binary(x, bits):
    chunk = np.zeros(bits)
    b = np.array([int(b) for b in list(bin(x)[2:])])
    chunk[bits - len(b):] = b

    return chunk

def decimal(x):
    return int(np.sum([b * 2 ** i for i, b in enumerate(reversed(x))]))
