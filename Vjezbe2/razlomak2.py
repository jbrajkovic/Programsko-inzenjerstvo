class Razlomak(object):
    '''Klasa razlomak'''
    brojnik = None
    nazivnik = None

    def __init__(self, brojnik, nazivnik = 1):
        if nazivnik == 0: raise Exception('Nazivnik ne moze biti 0')
        self._brojnik = brojnik
        self._nazivnik = nazivnik
        Razlomak.brojnik = brojnik
        Razlomak.nazivnik = nazivnik

    def __str__(self):
        return '%d|%d' % (self._brojnik, self._nazivnik)

    @staticmethod
    def inverz(razlomak):
        return Razlomak(Razlomak.nazivnik, Razlomak.brojnik)

    @staticmethod
    def stvori(realanBroj):
        cijeliDio = str(realanBroj).split('.')[0]
        decimalniDio = str(realanBroj).split('.')[1]

        if int(cijeliDio) == 0:
            brojnik = int(decimalniDio.lstrip('0'))
        else:
            brojnik = int(cijeliDio + decimalniDio)

        nazivnik = pow(10, len(decimalniDio))
        return Razlomak(brojnik, nazivnik)


print('*** test1 ***')
r1 = Razlomak(314,100)
r2 = Razlomak.inverz(r1)

print(r1,r2,r1)

print('*** test2 ***')
r1 = Razlomak.stvori(3.14)
print(r1)
r2 = Razlomak.stvori(0.006021)
print(r2)
r3 = Razlomak.stvori(-75.204)
print(r3)