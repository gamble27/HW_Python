from math import log
from cmath import inf


def inf_sum(argument, accuracy=0.1):
    if accuracy <= 0:
        return log((1+argument)/(1-argument))
    elif accuracy > 1:
        return 0

    if abs(argument) > 1:
        return float(inf)

    x_i = argument
    result: float = 0
    i = 1
    while x_i > accuracy:
        result += x_i/i
        x_i *= argument*argument
        i += 2
    return 2*result


if __name__ == "__main__":
    x = float(input("x = "))
    eps = input("epsilon = ")
    eps = float(eps) if eps is not None else 0.1

    print(inf_sum(x, eps))
