from random import *
from vjezba_9.slagalica.slagalica import Polje


class Ploca():

    def __init__(self, broj_redova, broj_stupaca):
        self.__broj_redova = broj_redova
        self.__broj_stupaca = broj_stupaca

    def vratiVelicinuPloce(self):
        return (self.__broj_redova, self.__broj_stupaca)

    def vratiBrojPolja(self):
        return self.__broj_redova * self.__broj_stupaca

    def postaviPlocu(self, brojevi: list) -> list:
        self.__polja = []
        list_len = 0

        for cols in range(self.__broj_stupaca):
            new_row = []
            for rows in range(self.__broj_redova):
                new_row.append(Polje(brojevi[list_len]))
                list_len += 1

            self.__polja.append(new_row)


    def __iter__(self):
        polja_lista = []

        for counter1 in self.__polja:
            for counter2 in counter1:
                polja_lista.append(counter2)

        return iter(polja_lista)

    def __str__(self):
        output = ""
        list = self.__iter__()
        list_len = 0

        for el in list:
            output += str(el) + "\t"
            list_len += 1

            if(list_len == self.__broj_redova):
                list_len = 0
                output += "\n"

        return output




