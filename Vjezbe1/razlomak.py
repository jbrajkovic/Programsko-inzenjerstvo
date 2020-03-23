class Razlomak(object):

    def __init__(self, brojnik, nazivnik):
        self._brojnik = brojnik
        self._nazivnik = nazivnik

    def __eq__(self, other):
        return self.brojnik * other.nazivnik == self.nazivnik * other.brojnik

    def __lt__(self, other):
        return self.brojnik * other.nazivnik < self.nazivnik * other.brojnik

    def __le__(self, other):
        return self.brojnik * other.nazivnik <= self.nazivnik * other.brojnik

    def __add__(self, other):
        b = self.brojnik * other.nazivnik + self.nazivnik * other.brojnik
        n = self.nazivnik * other.nazivnik
        return Razlomak(b, n)

    def __sub__(self, other):
        b = self.brojnik * other.nazivnik - self.nazivnik * other.brojnik
        n = self.nazivnik * other.nazivnik
        return Razlomak(b, n)

    def __mul__(self, other):
        b = self.brojnik * other.brojnik
        n = self.nazivnik * other.nazivnik
        return Razlomak(b, n)

    def __truediv__(self, other):
        b = self.brojnik * other.nazivnik
        n = self.nazivnik * other.brojnik
        return Razlomak(b, n)

    def __str__(self):
        if self.nazivnik == 1:
            return '{}'.format(self.brojnik)
        else:
            return '{0}|{1}'.format(self.brojnik, self.nazivnik)

    def __repr__(self):
        return "Razlomak(" + repr(self.brojnik) + ", " + repr(self.nazivnik) + ")"

    def skrati(self):
        b = self.brojnik
        n = self.nazivnik

        while b % n != 0:
            b, n = n, b % n

        t = n
        self.brojnik //= t
        self.nazivnik //= t
        return

    @property
    def brojnik(self):
        return self._brojnik

    @brojnik.setter
    def brojnik(self, value):
        self._brojnik = value

    @property
    def nazivnik(self):
        return self._nazivnik

    @nazivnik.setter
    def nazivnik(self, value):
        self._nazivnik = value

print('*** test 1 ***')
r1 = Razlomak(12, 30)
print(r1.brojnik, r1.nazivnik)
r1.skrati()
print(r1.brojnik, r1.nazivnik)

print('*** test 2 ***')
r1 = Razlomak(12,30)
r2 = Razlomak(2,5)
r3 = Razlomak(3,6)
print(r1,r2,repr(r3))
print(r1 == r2)
print(r3 >= r1)
print(r3 < r2)

print('*** test 3 ***')
print(Razlomak(3,4)+Razlomak(5,2))
print(Razlomak(1,3)-Razlomak(2,6))
print(Razlomak(2,8)*Razlomak(4,2))
print(Razlomak(2,3)/Razlomak(4,5))