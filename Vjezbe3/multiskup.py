import bisect

zadatak = 1

class MultiSkup(object):

    def __init__(self, kolekcija = None):
        self.__kolekcija = []
        self.__rijecnik = {}
        self.__kljucevi = []

        if kolekcija is not None:
            if not isinstance(kolekcija, MultiSkup):
                self.__kolekcija = kolekcija
            self.__kolekcija.sort()

            broj_ponavljanja = []
            br = 0
            indeks = 0
            trenutni = self.__kolekcija[0]
            self.__kljucevi.append(trenutni)
            for el in self.__kolekcija:
                if el == trenutni:
                    br += 1
                else:
                    broj_ponavljanja.append(br)
                    self.__kljucevi.append(el)
                    trenutni = self.__kolekcija[indeks]
                    br = 1
                if (el == self.__kolekcija[len(self.__kolekcija) - 1]):
                    broj_ponavljanja.append(br)
                indeks += 1

            for i in range(0, len(self.__kljucevi)):
                self.__rijecnik[self.__kljucevi[i]] = broj_ponavljanja[i]

    def __setitem__(self, key, value):
        self.__rijecnik[key] = value
        if key not in self.__kljucevi:
            bisect.insort(self.__kljucevi, key)

    def __repr__(self):
        if (zadatak == 1):
            return "{%s}" % self.__rijecnik
        if (zadatak == 2):
            return "MultiSkup(%s)" % self.__kolekcija
        if (zadatak == 3):
            dijelovi = []
            for key in self.__kljucevi:
                dijelovi.append("%r*%r" % (key, self.__rijecnik[key]))
            return "{{%s}}" % ", ".join(dijelovi)

    def __str__(self):
        return repr(self)

    def __iter__(self):
        return iter(self.__kolekcija)

    def add(self, element, ponavljanja = 1):
        if element not in self.__kljucevi:
            self.__rijecnik[element] = ponavljanja
            self.__kljucevi.append(element)
        else:
            self.__rijecnik[element] += ponavljanja

    def __delitem__(self, key):
        i = bisect.bisect_left(self.__kljucevi, key)
        del self.__kljucevi[i]
        del self.__rijecnik[key]

    def remove(self, element, ponavljanja = 1):
        if (self.__rijecnik[element] == ponavljanja):
            del self.__rijecnik[element]
            self.__kljucevi.remove(element)
        else:
            self.__rijecnik[element] -= ponavljanja


print('*** test 1 ***')
a = MultiSkup([1, 1, 2, 2, 2, 3, 3, 4])
print(a)

zadatak = 2

print('*** test 2 ***')
a = MultiSkup([1,1,2,2,2,3,3,4])
for el in a:
    print(el)
print(repr(a))

zadatak = 3

print('*** test 3 ***')
a = MultiSkup([1,1,2,2,2,3,3,4])
a.add(4)
print(a)
a.add(2,3)
print(a)
a.remove(4,2)
print(a)