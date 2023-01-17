import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
#
# dt = 0.005
# n=20
# L = 1
# particles=np.zeros(n,dtype=[("position", float , 2),
#                            ("velocity", float ,2),
#                            ("force", float ,2),
#                            ("size", float , 1)])
#
# particles["position"]=np.random.uniform(0,L,(n,2));
# particles["velocity"]=np.zeros((n,2));
# particles["size"]=0.5*np.ones(n);
#
# fig = plt.figure(figsize=(7,7))
# ax = plt.axes(xlim=(0,L),ylim=(0,L))
# scatter=ax.scatter(particles["position"][:,0], particles["position"][:,1])
#
# def update(frame_number):
#    particles["force"]=np.random.uniform(-2,2.,(n,2));
#    particles["velocity"] = particles["velocity"] + particles["force"]*dt
#    particles["position"] = particles["position"] + particles["velocity"]*dt
#
#    particles["position"] = particles["position"]%L
#    scatter.set_offsets(particles["position"])
#    return scatter,
#
# anim = FuncAnimation(fig, update, interval=10)
# plt.show()


# fig = plt.figure()
#
# x_positions = [1, 2]
# y_positions = [1, 2]
#
# ax = fig.add_subplot(111)
# ## store the scatter in abc object
# abc=ax.scatter(x_positions, y_positions)
# ### if you comment that line of set False to True, you'll see what happens.
# #ticks = arange(-0.06, 0.061, 0.02)
# #xticks(ticks)
# #yticks(ticks)
# plt.show()
# abc.remove()
# print(1)
# plt.show()
from IPython.display import display, clear_output
m = 100
n = 100
matrix = np.random.normal(0, 1, size=(m, n))

fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(m):
    ax.clear()
    ax.scatter(matrix[i, :], matrix[i, :])
    display(fig)
    clear_output(wait=True)
    plt.pause(0.2)



