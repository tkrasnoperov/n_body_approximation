import sys
import numpy as np
import matplotlib.pyplot as plt

from configs import *

conf = Configs()

f = open("logs/energy.txt", 'r')
states = f.read().split('\n')[:-1]
for i, state in enumerate(states):
    plt.plot([float(x) for x in state.split(",")], label="theta={}".format(str(conf.theta[i])))

plt.legend(loc='upper right')
plt.xlabel("iterations")
plt.ylabel("x-momentum")
plt.show()
# plt.savefig("{}.pdf".format(sys.argv[1]), bbox_inches="tight")
f.close()
