import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

fig = plt.figure()
ax = plt.axes(xlim=(-1, 1), ylim=(0, 4))
#ax.grid()
line, = ax.plot([], [])
x = np.linspace(-0.99, 0.99, 200)

def mmbr(i,x):
    res = 1
    for k in range(1,i+1):
        res *= -x
        res /= 2*k
        res *= 2*k-1
    return res

def taylor(i, x):
    y1 = 1
    for j in range(2,i + 1):
        y1 += mmbr(j,x)
    return y1

def init():
    line.set_data([], [])
    return line,

def animate(i):
    y = taylor(i, x)
    line.set_data(x, y)
    return line,

anim = anim.FuncAnimation(fig, animate, init_func=init,
                          frames=100, interval=200, blit=False)
func1 = 1 / ((1 + x)**0.5)
plt.plot(x, func1)
plt.show()
