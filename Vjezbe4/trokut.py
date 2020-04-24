from math import *

class Trokut(object):

    def __init__(self, a, b, c):
        if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
            raise Exception("nije trokut")
        else:
            self.__a = a
            self.__b = b
            self.__c = c

    def __str__(self):
        return "trokut %s %s %s" % (self.__a, self.__b, self.__c)
    def __repr__(self):
        return "Trokut(%r, %r, %r)" % (self.__a, self.__b, self.__c)

    def opseg(self):
        return self.__a + self.__b + self.__c

    def povrsina(self):
        s = (self.__a + self.__b + self.__c) / 2
        return sqrt((s - self.__a) * (s - self.__b) * (s - self.__c))

class JednakokracniTrokut(Trokut):

    def __init__(self, baza, duljina_kraka):
        super(JednakokracniTrokut, self).__init__(baza, duljina_kraka, duljina_kraka)

class JednakostranicniTrokut(Trokut):

    def __init__(self, stranica):
        super(JednakostranicniTrokut, self).__init__(stranica, stranica, stranica)



print('*** test 1 ***')
lista_stranica = [(1,2,3),(3,4,5),(3,4,4),(3,3,3)]
for stranice in lista_stranica:
    try:
        t = Trokut(*stranice)
        print(repr(t))
    except Exception as e:
        print(e, stranice)

print('*** test 2 ***')
lista_stranica = [(3,4,5),(3,4,4),(3,3,3)]
for stranice in lista_stranica:
    t = Trokut(*stranice)
    print('%r ima opseg %.3f i povrsinu %.3f' % (t, t.opseg(), t.povrsina()))

print('*** test 3 ***')
trokuti = [Trokut(3,4,5),JednakokracniTrokut(3,4),JednakostranicniTrokut(5)]
for t in trokuti:
    print(t)