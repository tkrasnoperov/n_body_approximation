import os
from multiprocessing import Pool
import cv2
from time import time

N_PROCS = 6

def load_frame(frame_name):
    os.system("convert {}.ps {}.jpg".format(frame_name, frame_name))
    return cv2.imread("{}.jpg".format(frame_name))

def create_avi(video_name, folder, n_frames, performance=True):
    start = time()
    with Pool(N_PROCS) as pool:
        frames = pool.map(load_frame, ["{}/frame_{}".format(folder, i) for i in range(n_frames)])

    print("frame load time:", time() - start)

    height, width, layers = frames[-1].shape
    video = cv2.VideoWriter(video_name, 0, 60, (width, height))

    start = time()
    for i, frame in zip(range(len(frames)), frames):
        print(i)
        video.write(frame)
    print("frame write time:", time() - start)

    cv2.destroyAllWindows()
    video.release()
