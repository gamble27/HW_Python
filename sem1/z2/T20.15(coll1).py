import numpy as np
import matplotlib.pyplot as plt
from math import pi,sin


def liniyKa(x, xs, k):
    res = 1
    for xi in xs:
        res *= x-xi
        res /= 1 if xi==xs[k] else xs[k]-xi
    return res

'''
#свернутая альтернатива
def polinom(x,function):

    n = 2 ** (int(input('gimme k - tochnost\' \n'))) + 1
    xs = np.linspace(0, 2 * pi, n)
    ys = np.array([function(xi) for xi in xs])

    res = 0
    for i, yi in enumerate(ys):
        res += yi*liniyKa(x, xs, i)
    return res
'''
'''
def polinom(x, xs, ys):
    res = 0
    for i, yi in enumerate(ys):
        res += yi*liniyKa(x, xs, i)
    return res


n = 2 ** (int(input('gimme k \n'))) + 1
x = np.linspace(0, 2*pi, n)
y = np.array([sin(xi) for xi in x])
x0 = float(input('gimme x \n'))
print(polinom(x0,x,y))

'''

def polinom(x,function):

    n = 2 ** (int(input('gimme k - tochnost\' \n'))) + 1
    xs = np.linspace(0, 2 * pi, n)
    ys = np.array([function(xi) for xi in xs])

    res = 0
    for i, yi in enumerate(ys):
        res += yi*liniyKa(x, xs, i)

    plt.plot(xs, ys, '-c')
    plt.plot(xs, np.array([res]*n), ':m')
    plt.show()

    return res

x0 = float(input('gimme x \n'))
print(polinom(x0,sin))