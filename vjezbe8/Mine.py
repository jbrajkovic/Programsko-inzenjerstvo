class Kvadrat(object):

     def __init__(self, broj = 0):
          self.__broj = broj
          self.__otkriven = False
          self.__oznaka = False

     def otkrij(self):
          if self.__otkriven == False and self.__oznaka == False:
               self.__otkriven = True

     def oznaci(self):
          if self.__oznaka == False :
               self.__oznaka = True
          else:
               self.__oznaka = False

     @property
     def jeMina(self):
          if self.__broj == -1:
               return True
          else:
               return False

     @property
     def jeBroj(self):
          if self.__broj != 0 and self.__broj !=-1:
               return True
          else:
               return False

     @property
     def jePrazan(self):
          if self.__broj ==0:
               return True
          else:
               return False

     def __str__(self):
          if self.__oznaka == True:
               return "?"
          if self.__otkriven == False:
               return "."
          else:
               if self.jeMina == True:
                    return "x"
               if self.jeBroj == True:
                    return "%d" % self.__broj
               if self.jePrazan == True:
                    return " "

print('*** test 1 ***')
brojevi = [-1,0,1,2]
for broj in brojevi:
     k = Kvadrat(broj)
     print(k.jeMina, k.jeBroj, k.jePrazan)

print('*** test 2 ***')
kvadrati = [Kvadrat(broj) for broj in [-1,0,1,2]]
print(' oz ot oz ot')
for k in kvadrati:
     rez = []
     rez.append(str(k))
     for _ in range(2):
          k.oznaci()
          rez.append(str(k))
          k.otkrij()
          rez.append(str(k))
     print('%s %s %s %s %s ' % tuple(rez))