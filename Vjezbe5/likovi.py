class Kruznica:
    def __init__(self, r):
        self.r = r

    def __str__(self):
        return "Kružnica radijusa %.2f" % self.r


class Kvadrat:
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return "Kvadrat duljine %.2f" % self.a


if __name__ == '__main__':
    print('*** test likovi ***')
    kruznica = Kruznica(3)
    kvadrat = Kvadrat(4.5)
    print(kruznica)
    print(kvadrat)
