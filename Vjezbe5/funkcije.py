from likovi import *
from math import pi


def opseg(lik):
    if isinstance(lik, Kruznica):
        return 2 * lik.r * pi

    else:
        return 4 * lik.a


def povrsina(lik):
    if isinstance(lik, Kruznica):
        return lik.r * lik.r * pi

    else:
        return lik.a * lik.a


if __name__ == '__main__':
    print('*** test funkcije ***')
    print(opseg.__name__)
    print(povrsina.__name__)
