from vjezba_9.slagalica.Ploca import Ploca

print('*** test 1 ***')
broj_redova, broj_stupaca = 3, 3
pl = Ploca(broj_redova, broj_stupaca)
print(pl.vratiVelicinuPloce(), pl.vratiBrojPolja())
print()
pl.postaviPlocu([0,8,7,6,5,4,3,2,1])
for red in pl._Ploca__polja:
    for p in red:
        print(p, end = '|')
    print()


print('\n*** test 2 ***')
pl = Ploca(3, 4)
pl.postaviPlocu([1,2,3,4,5,6,7,8,9,10,11,0])
print(pl)
for p in pl:
    print(p, repr(p))

