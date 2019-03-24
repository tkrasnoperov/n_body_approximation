import numpy as np
import tkinter as tk

from configs import *

class Mesh():
    def __init__(   self, gui, canvas, width, height, resolution, f):

        self.gui = gui
        self.canvas = canvas

        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.resolution = resolution

        self.x_ticks = np.linspace(space_left, space_right, resolution + 2)[1:-1]
        self.y_ticks = np.linspace(space_bottom, space_top, resolution + 2)[1:-1]

        self.space_grid = np.zeros((self.resolution, self.resolution, configs.n_dimensions))
        for i, x in zip(range(self.resolution), self.x_ticks):
            for j, y in zip(range(self.resolution), self.y_ticks):
                self.space_grid[i, j] = np.array([x, y])

        self.f = f

class ArrowMesh(Mesh):
    def __init__(   self, gui, canvas, pixel_width, pixel_height, resolution,
                    space_left, space_right, space_bottom, space_top, f):
        super().__init__(   gui, canvas, pixel_width, pixel_height, resolution,
                            space_left, space_right, space_bottom, space_top, f)

        for i in range(self.resolution):
            row = []
            for j in range(self.resolution):
                x = self.x_ticks[i]
                y = self.y_ticks[j]

                head, fill = self.f(x, y)
                arrow = self.canvas.create_line(
                    x - head[0],
                    y - head[1],
                    x + head[0],
                    y + head[1],
                    arrow=tk.LAST,
                    fill=fill
                )
                self.canvas.lower(arrow)

                row.append(arrow)
            self.grid.append(row)

    def update(self):
        for i in range(self.resolution):
            for j in range(self.resolution):
                x = self.x_ticks[i]
                y = self.y_ticks[j]

                radius, fill = self.f(x, y)
                self.canvas.coords(
                    self.grid[i][j],
                    x,
                    y,
                    x + radius[0],
                    y + radius[1],
                )
                self.canvas.itemconfig(
                    self.grid[i][j],
                    fill=fill
                )

        self.gui.update()

class PointMesh(Mesh):
    def __init__(   self, gui, canvas, pixel_width, pixel_height, resolution,
                    space_left, space_right, space_bottom, space_top, f):
        super().__init__(   gui, canvas, pixel_width, pixel_height, resolution,
                            space_left, space_right, space_bottom, space_top, f)

        for i in range(self.resolution):
            row = []
            for j in range(self.resolution):
                x = self.x_ticks[i]
                y = self.y_ticks[j]

                radius, fill = self.f(x, y)
                point = self.canvas.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill=fill
                )
                self.canvas.lower(point)

                row.append(point)
            self.grid.append(row)

    def update(self):
        for i in range(self.resolution):
            for j in range(self.resolution):
                x = self.x_ticks[i]
                y = self.y_ticks[j]

                radius, fill = self.f(x, y)
                self.canvas.coords(
                    self.grid[i][j],
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                )
                self.canvas.itemconfig(
                    self.grid[i][j],
                    fill=fill
                )

        self.gui.update()


class PixelMesh(Mesh):
    def __init__(   self, gui, canvas, pixel_width, pixel_height, resolution,
                    space_left, space_right, space_bottom, space_top, f):
        super().__init__(   gui, canvas, pixel_width, pixel_height, resolution,
                            space_left, space_right, space_bottom, space_top, f)

        for i in range(self.resolution):
            row = []
            for j in range(self.resolution):
                x = self.x_ticks[i]
                y = self.y_ticks[j]

                fill = self.f(x, y)
                pixel = canvas.create_rectangle(
                    x - (width / (resolution + 1)) / 2,
                    y - (height / (resolution + 1)) / 2,
                    x + (width / (resolution + 1)) / 2,
                    y + (height / (resolution + 1)) / 2,
                    fill=fill,
                    outline=fill
                )
                canvas.lower(pixel)

                row.append(pixel)
            self.grid.append(row)

    def update(self):
        for i in range(self.resolution):
            for j in range(self.resolution):
                x = self.x_ticks[i]
                y = self.y_ticks[j]

                fill = self.f(x, y)
                self.canvas.itemconfig(self.grid[i][j], fill=fill)
                self.canvas.itemconfig(self.grid[i][j], outline=fill)

        self.gui.update()
