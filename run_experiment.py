import numpy as np
import matplotlib.pyplot as plt
from pipeline import Mieszkanie, Pokoj, Grzejnik, Drzwi, Okno

if __name__ == "__main__":
    mieszkanie = Mieszkanie(7, 7)

    pokoj1 = Pokoj(3, 4, 1)
    pokoj2 = Pokoj(4, 4, 1)
    pokoj3 = Pokoj(3, 3, 1)
    pokoj4 = Pokoj(4, 3, 1)

    mieszkanie.dodaj_pokoj(pokoj1, 0, 0)
    mieszkanie.dodaj_pokoj(pokoj2, 3, 0)
    mieszkanie.dodaj_pokoj(pokoj3, 0, 4)
    mieszkanie.dodaj_pokoj(pokoj4, 3, 4)

    grzejnik1 = Grzejnik(1026, 0, 2, 3)
    grzejnik2 = Grzejnik(1026, 5, 0, 3)
    grzejnik3 = Grzejnik(1026, 7, 6, 3)
    mieszkanie.dodaj_grzejnik(grzejnik1)
    mieszkanie.dodaj_grzejnik(grzejnik2)
    mieszkanie.dodaj_grzejnik(grzejnik3)

    drzwi1 = Drzwi(2, 2, 2, 1)
    drzwi2 = Drzwi(4, 3, 1, 2)
    drzwi3 = Drzwi(1, 3.5, 1, 2)
    mieszkanie.dodaj_drzwi(drzwi1)
    mieszkanie.dodaj_drzwi(drzwi2)
    mieszkanie.dodaj_drzwi(drzwi3)

    okno1 = Okno(0, 1.5, 0.1, 1, temp=-2, beta=1)
    okno2 = Okno(4.5, 0, 1, 0.1, temp=-2, beta=1)
    okno3 = Okno(3.5, 6.9, 1, 0.1, temp=-2, beta=1)
    mieszkanie.dodaj_okno(okno1)
    mieszkanie.dodaj_okno(okno2)
    mieszkanie.dodaj_okno(okno3)

    for t in range(1, mieszkanie.k):
        mieszkanie.krok_czasowy(t)
        for grzejnik in mieszkanie.grzejniki:
            grzejnik.aplikuj_cieplo(pokoj1, t)
            grzejnik.aplikuj_cieplo(pokoj2, t)
            grzejnik.aplikuj_cieplo(pokoj4, t)
        for drzwi in mieszkanie.drzwi:
            drzwi.ustaw_srednia_temperature(mieszkanie, t)
        for okno in mieszkanie.okna:
            okno.ustaw_temperature(mieszkanie, t)

    mieszkanie.mapa_ciepla(mieszkanie.k - 1)