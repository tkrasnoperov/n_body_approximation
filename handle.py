import numpy as np

from utils import *
from configs import *

class TreeHandler():
    def __init__(self, gui, canvas, system, space_map, conf, fill):
        self.gui = gui
        self.canvas = canvas
        self.system = system
        self.space_map = space_map
        self.conf = conf
        self.fill = fill

        self.handles = self.draw_tree(self.system.root)

    def draw_tree(self, tree):
        if not tree.children:
            return []

        side = tree.side / 2
        left = self.space_map.space_to_canvas(tree.origin - np.array([side, 0, 0]))
        right = self.space_map.space_to_canvas(tree.origin + np.array([side, 0, 0]))
        top = self.space_map.space_to_canvas(tree.origin - np.array([0, side, 0]))
        bottom = self.space_map.space_to_canvas(tree.origin + np.array([0, side, 0]))
        # print(tree.center)
        center = self.space_map.space_to_canvas(tree.center)
        # print(center)

        horiz_handle = self.canvas.create_line(
            left[0],
            left[1],
            right[0],
            right[1],
            fill=self.fill
        )
        vert_handle = self.canvas.create_line(
            top[0],
            top[1],
            bottom[0],
            bottom[1],
            fill=self.fill
        )
        circle_handle = self.canvas.create_oval(
            center[0] - 2,
            center[1] - 2,
            center[0] + 2,
            center[1] + 2,
            fill="#fff"
        )

        handles = [horiz_handle, vert_handle, circle_handle]
        if tree.children:
            child_handles = [self.draw_tree(child) for child in tree.children]
            for child in child_handles:
                handles += child

        return handles

    def update(self):
        for i in range(len(self.handles)):
            handle = self.handles[i]
            self.canvas.delete(handle)

        self.handles = self.draw_tree(self.system.root)
        self.gui.update()

    def export_frame(self, file):
        self.canvas.postscript(file="trash", colormode='color')

class SystemHandler():
    def __init__(self, gui, canvas, system, space_map, conf, fill):
        self.gui = gui
        self.canvas = canvas
        self.system = system
        self.space_map = space_map
        self.conf = conf
        self.fill = fill

        self.handles = []
        for body in system.bodies:
            canvas_x, canvas_y = self.space_map.space_to_canvas(body.location)
            radius = radius_from_depth(body.location[2], conf)
            # fill = color_from_depth(body.location[2], conf)

            handle = canvas.create_oval(
                canvas_x - radius,
                canvas_y - radius,
                canvas_x + radius,
                canvas_y + radius,
                fill=self.fill
            )
            self.handles.append(handle)

    def update(self):
        for i in range(len(self.handles)):
            handle, body = self.handles[i], self.system.bodies[i]

            radius = radius_from_depth(body.location[2], self.conf)
            # fill = color_from_depth(body.location[2], self.conf)
            canvas_x, canvas_y = self.space_map.space_to_canvas(body.location)

            self.canvas.coords(
                handle,
                canvas_x - radius,
                canvas_y - radius,
                canvas_x + radius,
                canvas_y + radius
            )
            self.canvas.itemconfig(handle, fill=self.fill)

        self.gui.update()

    def export_frame(self, file):
        self.canvas.postscript(file=file, colormode='color')
