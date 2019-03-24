import numpy as np
from colorutils import Color

def random_sphere_point(radius):
    point = 2 * radius * (np.random.random(3) - .5)
    if np.linalg.norm(point) > radius:
        return random_sphere_point(radius)

    return point

def random_surface_point(radius):
    point = random_sphere_point(1)
    return .1 * point / np.linalg.norm(point)

# def arrow_from_field(field, scale):
#     field_tanh = scale(np.linalg.norm(field), k=2)
#     arrow = field / field_tanh
#     color = hex_from_color(LOW_COLOR + field_tanh * DIFF_COLOR)
#
#     return arrow, color
#
# arrow_function = lambda x, y: arrow_from_field(grav.field([x, y]))
# mesh = ArrowMesh(gui, canvas, width, height, RESOLUTION, arrow_function)
#
# min_point_size = 1
# max_point_size = 3
# def point_from_field(field):
#     field_tanh = scale(np.linalg.norm(field), k=25)
#     point = min_point_size + field_tanh * (max_point_size - min_point_size)
#     color = hex_from_color(LOW_COLOR + field_tanh * DIFF_COLOR)
#
#     return point, color
#
# point_function = lambda x, y: point_from_field(grav.field([x, y]))
# mesh = PointMesh(gui, canvas, width, height, RESOLUTION, point_function)

def clockwise(x):
    rot = np.array([
        [0,     1,      0],
        [-1,    0,      0],
        [0,     0,      1],
    ])

    return rot.dot(x)

def tanh(x, k=1):
    result = (np.exp(k * x) - np.exp(-k * x)) / (np.exp(k * x) + np.exp(-k * x))
    if np.isnan(result):
        return 1.
    return result

def sigmoid(x, c=0, k=1):
    result = 1 / (1 + np.exp(-k * (x - c)))
    result = 1 if np.isnan(result) else result
    result = 0 if result < 0 else result

    return result

def crosshair(canvas, center, width, height, color="#fff"):
    vertical = canvas.create_line(
        center[0] - width / 2,
        center[1],
        center[0] + width / 2,
        center[1],
        fill=color
    )
    horizontal = canvas.create_line(
        center[0],
        center[1] - height / 2,
        center[0],
        center[1] + height / 2,
        fill=color
    )

    return vertical, horizontal

def hex_from_color(color):
    color = 255 * np.minimum(color, np.ones(3))
    return Color((int(color[0]), int(color[1]), int(color[2]))).hex
