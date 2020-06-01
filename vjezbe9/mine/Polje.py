from vjezba_9.Mine.Mine import Kvadrat
from random import *


class Polje():

    def __init__(self, velicina, broj_mina):
        self.__velicina = velicina
        self.__broj_mina = broj_mina
        self.__kvadrati = [[Kvadrat() for col in range(velicina)] for row in range(velicina)]

        for mine in range(broj_mina):
            random_num = randrange(velicina ** 2)
            col = random_num // velicina
            row = random_num % velicina

            self.__kvadrati[col][row] = Kvadrat(-1)

        for col in range(velicina):
            for row in range(velicina):
                if self.__kvadrati[col][row].jeMina:
                    continue

                num_of_mines = 0

                for counter in [-1, 0, 1]:
                    row1 = self.check_for_a_mine(col - 1, row + counter)
                    row2 = self.check_for_a_mine(col, row + counter)
                    row3 = self.check_for_a_mine(col + 1, row + counter)

                    if (row1 == -1):
                        num_of_mines += 1
                    if (row2 == -1):
                        num_of_mines += 1
                    if (row3 == -1):
                        num_of_mines += 1

                self.__kvadrati[col][row] = Kvadrat(num_of_mines)

    def check_for_a_mine(self, x, y):
        if x >= 0 and y >= 0 and x < self.__velicina and y < self.__velicina:
            if self.__kvadrati[x][y].jeMina:
                return -1
            else:
                return 0

    def __str__(self):
        output = "   1 2 3 4 5\n  -----------"
        for cols in range(self.__velicina):
            output += "\n" + str(cols + 1) + "| "
            for rows in range(self.__velicina):
                output += str(self.__kvadrati[cols][rows]) + " "
            output +="|"

        output += "\n  ----------"

        return output