import json
import sqlite3

class Ispiti(dict):

    def dodaj(self, student, kolegij, ocjena):
        if student not in self:
            self[student] = {}
        self[student][kolegij] = ocjena

    def izbrisi(self, student, kolegij):
        if kolegij in self[student]:
            self[student].pop(kolegij)

    def promijeni(self, student, kolegij, ocjena):
        self[student][kolegij] = ocjena

    def spremi_datoteka(self, datoteka):
        with open(datoteka, "w") as f:
            for student in self:
                kolegiji = self[student]
                for kolegij in kolegiji:
                    f.write("%s\t%s\t%s\n" %
                            (student, kolegij, kolegiji[kolegij]))

    def spremi_json(self, datoteka):
        with open(datoteka, "w") as f:
            json.dump(self, f)

    @staticmethod
    def ucitaj_datoteka(datoteka):
        isp = Ispiti()
        with open(datoteka, 'r') as f:
            for line in f:
                ispit = line.split("\n")[0].split("\t")
                student = ispit[0]
                kolegij = ispit[1]
                ocjena = int(ispit[2])

                isp.dodaj(student, kolegij, ocjena)

        return isp

    @staticmethod
    def ucitaj_json(datoteka):
        isp = Ispiti()
        with open(datoteka, "r") as f:
            isp = json.load(f)

        return isp    


class IspitiDB():

    def __init__(self, baza):
        self.conn = sqlite3.Connection(baza)
        self.cur = self.conn.cursor()

        self.cur.executescript("""
            DROP TABLE IF EXISTS ispiti;
            DROP TABLE IF EXISTS kolegiji;
            DROP TABLE IF EXISTS studenti;

            CREATE TABLE studenti (
            student_id integer PRIMARY KEY,
            ime_prezime text NOT NULL UNIQUE);

            CREATE TABLE kolegiji (
            kolegij_id integer PRIMARY KEY,
            naziv text NOT NULL UNIQUE);

            CREATE TABLE ispiti (
            student_id integer,
            kolegij_id integer,
            ocjena integer NOT NULL,
            PRIMARY KEY (student_id, kolegij_id),
            FOREIGN KEY (student_id) REFERENCES studenti (student_id),
            FOREIGN KEY (kolegij_id) REFERENCES kolegij (kolegij_id));
            """)

    def vrati_kolegij_id(self, naziv):
        self.cur.execute("""SELECT kolegij_id FROM kolegiji WHERE naziv = ?""", (naziv,))
        row = self.cur.fetchone()
        if row:
            return row[0]
    
    def vrati_student_id(self, ime_prezime):
        self.cur.execute(
            """SELECT student_id FROM studenti WHERE ime_prezime = ?""", (ime_prezime,))
        row = self.cur.fetchone()
        if row:
            return row[0]

    def dodaj_kolegij(self, naziv):
        self.cur.execute("""INSERT INTO kolegiji (naziv) VALUES (?)""", (naziv, ))
        self.conn.commit()
        return self.cur.lastrowid

    def dodaj_student(self, ime_prezime):
        self.cur.execute(
            """INSERT INTO studenti (ime_prezime) VALUES (?)""", (ime_prezime, ))
        self.conn.commit()
        return self.cur.lastrowid

    def promijeni_student(self, ime_prezime, novo_ime):
        self.cur.execute(
            """UPDATE studenti SET ime_prezime = ? WHERE ime_prezime = ?""", (novo_ime, ime_prezime))
        self.conn.commit()
        return self.vrati_student_id(novo_ime)


    def izbrisi_student(self, ime_prezime):
        self.cur.execute(
            "DELETE FROM studenti WHERE ime_prezime = ?", (ime_prezime, ))
        self.conn.commit()
    

    def ispitaj(self, student, kolegij, ocjena=None):
        student_id = self.vrati_student_id(student)
        kolegij_id = self.vrati_kolegij_id(kolegij)

        self.cur.execute("SELECT 1 FROM ispiti WHERE student_id = (?) AND kolegij_id = (?)",
                         (student_id, kolegij_id))
        row = self.cur.fetchone()

        if ocjena == None:
            if row:
                self.cur.execute("DELETE FROM ispiti WHERE student_id = (?) AND kolegij_id = (?)",
                                 (student_id, kolegij_id))
                self.conn.commit()
        else:
            if row:
                self.cur.execute("UPDATE ispiti SET ocjena = (?) WHERE student_id = (?) AND kolegij_id = (?)",
                                 (ocjena, student_id, kolegij_id))
                self.conn.commit()
            else:
                if student_id == None:
                    student_id = self.dodaj_student(student)
                
                if kolegij_id == None:
                    kolegij_id = self.dodaj_kolegij(kolegij)

                self.cur.execute("INSERT INTO ispiti (student_id, kolegij_id, ocjena) VALUES (?, ?, ?)",
                                 (student_id, kolegij_id, ocjena))
                self.conn.commit()

    def svi_ispiti(self):
        self.cur.execute("""
            SELECT s.ime_prezime, k.naziv, i.ocjena
            FROM studenti AS s
            JOIN ispiti AS i ON s.student_id = i.student_id
            JOIN kolegiji AS k ON k.kolegij_id = i.kolegij_id
        """)

        isp = Ispiti()
        for counter in self.cur.fetchall():
            isp.dodaj(counter[0], counter[1], counter[2])

        return isp




def test_datoteka():
    print("*** TEST datoteka ***")
    ok = True
    ok &= "spremi_datoteka" in dir(Ispiti) and isinstance(Ispiti.__dict__["spremi_datoteka"], type(Ispiti.spremi_datoteka))
    ok &= "ucitaj_datoteka" in dir(Ispiti) and isinstance(Ispiti.__dict__["ucitaj_datoteka"], staticmethod)
    data = {"Ante Antić": {"Linearna algebra": 5,
                           "Programiranje 1": 4},
            "Marija Marijić": {"Linearna algebra": 4,
                               "Matematička analiza": 5}}
    isp = Ispiti(data)
    print("  testiranje spremanja")
    isp.spremi_datoteka("ispiti.txt")
    ok &= set(open("ispiti.txt").read().split("\n")) == {"",
                                                         "Ante Antić\tLinearna algebra\t5",
                                                         "Ante Antić\tProgramiranje 1\t4",
                                                         "Marija Marijić\tLinearna algebra\t4",
                                                         "Marija Marijić\tMatematička analiza\t5"}
    print("  testiranje učitavanja")
    isp = Ispiti.ucitaj_datoteka("ispiti.txt")
    ok &= dict(isp) == data
    print("OK" if ok else "ERROR")
    print()


def test_json():
    print("*** TEST JSON ***")
    ok = True
    ok &= "spremi_json" in dir(Ispiti) and isinstance(Ispiti.__dict__["spremi_json"], type(Ispiti.spremi_json))
    ok &= "ucitaj_json" in dir(Ispiti) and isinstance(Ispiti.__dict__["ucitaj_json"], staticmethod)
    data = {"Ante Antić": {"Linearna algebra": 5,
                           "Programiranje 1": 4},
            "Marija Marijić": {"Linearna algebra": 4,
                               "Matematička analiza": 5}}
    isp = Ispiti(data)
    print("  testiranje spremanja")
    isp.spremi_json("ispiti.json")
    ok &= json.load(open("ispiti.json")) == data

    print("  testiranje učitavanja")
    isp = Ispiti.ucitaj_json("ispiti.json")
    ok &= dict(isp) == data
    print("OK" if ok else "ERROR")
    print()


def test_sqlite_1():
    print("*** TEST SQLITE studenti ***")
    conn = sqlite3.connect("ispiti.sqlite")
    cur = conn.cursor()
    isdb = IspitiDB("ispiti.sqlite")

    ok = True
    print("  vrati_student_id()", end="\t")
    cur.executemany("INSERT INTO studenti (ime_prezime) VALUES (?)", [("Ante",), ("Boris",)])
    conn.commit()
    id1 = isdb.vrati_student_id("Ante")
    id2 = isdb.vrati_student_id("Boris")
    id3 = isdb.vrati_student_id("Eugen")
    ok &= (id1, id2, id3) == (1, 2, None)
    cur.executescript("DELETE FROM studenti;")
    print("OK" if ok else "ERROR")

    ok = True

    print("  dodaj_student()", end="\t" * 2)
    student_id1 = isdb.dodaj_student("Ante Antić")
    student_id2 = isdb.dodaj_student("Pero Perić")
    student_id3 = isdb.dodaj_student("Ivana Ivanić")
    all_student = cur.execute("SELECT * FROM studenti").fetchall()
    ok &= (student_id1, student_id2, student_id3) == (1, 2, 3)
    ok &= all_student == [(1, "Ante Antić"), (2, "Pero Perić"), (3, "Ivana Ivanić")]
    print("OK" if ok else "ERROR")

    ok = True
    print("  promijeni_student()", end="\t")
    student_id4 = isdb.promijeni_student("Pero Perić", "Marija Marijić")
    student_id5 = isdb.promijeni_student("Luka Lukić", "Lana Lanić")
    ok &= (student_id4, student_id5) == (2, None)
    all_student = cur.execute("SELECT * FROM studenti").fetchall()
    ok &= all_student == [(1, 'Ante Antić'), (2, 'Marija Marijić'), (3, 'Ivana Ivanić')]
    print("OK" if ok else "ERROR")

    ok = True
    print("  izbrisi_student()", end="\t" * 2)
    isdb.izbrisi_student("Lana Lanić")
    isdb.izbrisi_student("Ivana Ivanić")
    all_student = cur.execute("SELECT * FROM studenti").fetchall()
    ok &= all_student == [(1, 'Ante Antić'), (2, 'Marija Marijić')]
    print("OK" if ok else "ERROR")
    print()



def test_sqlite_2():
    print("*** TEST SQLITE ispiti ***")
    conn = sqlite3.connect("ispiti2.sqlite")
    cur = conn.cursor()
    isdb = IspitiDB("ispiti2.sqlite")

    isdb.dodaj_student("Ante Antić")
    isdb.dodaj_kolegij("Linearna algebra")

    ok = True
    print("1. ispitaj()", end="\t")
    isdb.ispitaj("Ante Antić", "Linearna algebra", 5)
    one_ispit = cur.execute("SELECT * FROM ispiti").fetchone()
    ok &= one_ispit == (1, 1, 5)
    print("OK" if ok else "ERROR")

    print("2. ispitaj()", end="\t")
    isdb.ispitaj("Marija Marijić", "Linearna algebra", 5)
    one_ispit = cur.execute("SELECT * FROM ispiti").fetchall()[-1]
    ok &= one_ispit == (2, 1, 5)
    print("OK" if ok else "ERROR")

    print("3. ispitaj()", end="\t")
    isdb.ispitaj("Marija Marijić", "Linearna algebra", 4)
    one_ispit = cur.execute("SELECT * FROM ispiti").fetchall()[-1]
    ok &= one_ispit == (2, 1, 4)
    print("OK" if ok else "ERROR")

    print("4. ispitaj()", end="\t")
    isdb.ispitaj("Ivana Ivanić", "Programiranje 1", 5)
    one_ispit = cur.execute("SELECT * FROM ispiti").fetchall()[-1]
    ok &= one_ispit == (3, 2, 5)
    print("OK" if ok else "ERROR")

    print("5. ispitaj()", end="\t")
    isdb.ispitaj("Ivana Ivanić", "Programiranje 1")
    one_ispit = cur.execute("SELECT * FROM ispiti").fetchall()[-1]
    ok &= one_ispit == (2, 1, 4)
    print("OK" if ok else "ERROR")

    data = {"Ante Antić": {"Linearna algebra": 5,
                           "Programiranje 1": 4},
            "Marija Marijić": {"Linearna algebra": 4,
                               "Matematička analiza": 5}}

    print("   svi_ispiti()", end="\t")
    isdb.izbrisi_student("Ivana Ivanić")
    isdb.ispitaj("Ante Antić", "Programiranje 1", 4)
    isdb.ispitaj("Marija Marijić", "Matematička analiza", 5)
    ok &= isdb.svi_ispiti() == data
    print("OK")
    print()


if __name__ == "__main__":
    test_datoteka()
    test_json()
    test_sqlite_1()
    test_sqlite_2()