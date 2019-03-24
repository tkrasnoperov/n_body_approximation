import sys, os
from time import time
import numpy as np
from tkinter import *

from video import *

def setup(conf):
    gui = Tk()
    gui.geometry("{}x{}".format(conf.width, conf.height))
    gui.resizable(0, 0)
    gui.title(conf.name)
    canvas = Canvas(
        gui,
        width=conf.width,
        height=conf.height,
        bg='#000000',
        highlightthickness=0,
        borderwidth=0
    )
    canvas.pack(fill="both")
    canvas.create_rectangle(0, 0, conf.width, conf.height, fill="#000")

    return gui, canvas

def run(systems, handlers, monitor, conf, performance=True):
    os.system("mkdir -p frames")

    frame_update_time = 0
    system_update_time = 0
    for i in range(conf.n_frames):
        print(i)
        start = time()
        for _ in range(conf.n_steps):
            for system in systems:
                system.update(conf.h)
            monitor.track()
        system_update_time += time() - start

        for handler in handlers:
            handler.update()
        frame_update_time += time() - start

        if conf.movie:
            handlers[0].export_frame("frames/frame_{}.ps".format(i))

    if performance:
        print("system update time:", system_update_time / conf.n_frames)
        print("frame update time:", frame_update_time / conf.n_frames)
        print("FPS:", conf.n_frames / frame_update_time)
        # print("SPS:", (n_frames * n_steps) / system_update_time)

    if conf.movie:
        create_avi("videos/{}.avi".format(conf.movie), "frames", conf.n_frames)
        os.system("rm -r frames")

    system.pool.close()
    monitor.print_states()
