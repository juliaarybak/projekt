import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Mieszkanie:
    def __init__(self, width, height):
        #Reprezentacja mieszkania.

        self.width = width
        self.height = height
        self.pokoje = []    # Lista pokoi w mieszkaniu
        self.okna = []      # Lista okien w mieszkaniu
        self.drzwi = []     # Lista drzwi w mieszkaniu
        self.grzejniki = [] # Lista grzejników w mieszkaniu

    def dodaj_pokoj(self, pokoj):
        #Dodaje pokój do mieszkania.

        self.pokoje.append(pokoj)

    def dodaj_okno(self, okno):
        #Dodaje okno do mieszkania.

        self.okna.append(okno)

    def dodaj_drzwi(self, drzwi):
        # Dodaje drzwi do mieszkania.

        self.drzwi.append(drzwi)

    def dodaj_grzejnik(self, grzejnik):
        #Dodaje grzejnik do mieszkania.

        self.grzejniki.append(grzejnik)

    def rysuj(self):
        #Rysuje mieszkanie z wszystkimi pokojami, oknami i grzejnikami.

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect("equal")
        ax.set_title("Plan mieszkania")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")

        # Rysowanie pokoi
        for pokoj in self.pokoje:
            pokoj.rysuj(ax)

        # Rysowanie okien
        for okno in self.okna:
            okno.rysuj(ax)

        # Rysowanie okien
        for drzwi in self.drzwi:
            drzwi.rysuj(ax)

        # Rysowanie grzejników
        for grzejnik in self.grzejniki:
            grzejnik.rysuj(ax)

        plt.grid(False)
        plt.show()


class Pokoj:
    def __init__(self, x_start, x_end, y_start, y_end):
        #Reprezentacja pokoju.

        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end

    def rysuj(self, ax, kolor="lightblue"):
        #Rysuje pokój na danym obiekcie wykresu (ax).

        szerokosc = self.x_end - self.x_start
        wysokosc = self.y_end - self.y_start
        prostokat = patches.Rectangle(
            (self.x_start, self.y_start), szerokosc, wysokosc, edgecolor="black", facecolor="white"
        )
        ax.add_patch(prostokat)

class Okno:
    def __init__(self, x_start, x_end, y_start, y_end):
        #Reprezentacja okna.

        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end

    def rysuj(self, ax, kolor="blue"):
        #Rysuje okno jako linię na danym obiekcie wykresu (ax).

        ax.plot([self.x_start, self.x_end], [self.y_start, self.y_end], color=kolor, linewidth=4)


class Drzwi:
    def __init__(self, x_start, x_end, y_start, y_end):
        #Reprezentacja drzwi.

        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end

    def rysuj(self, ax, kolor="white"):
        #Rysuje drzwi jako linię na danym obiekcie wykresu (ax).

        ax.plot([self.x_start, self.x_end], [self.y_start, self.y_end], color=kolor, linewidth = 4)


class Grzejnik:
    def __init__(self, x_start, x_end, y_start, y_end):
        #Reprezentacja grzejnika.

        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end

    def rysuj(self, ax, kolor="red"):
        #Rysuje grzejnik jako prostokąt na danym obiekcie wykresu (ax).

        ax.add_patch(plt.Rectangle(
            (self.x_start, self.y_start),  # Lewy dolny róg prostokąta
            self.x_end - self.x_start,     # Szerokość prostokąta
            self.y_end - self.y_start,     # Wysokość prostokąta
            color=kolor
        ))


# Przykład użycia
if __name__ == "__main__":
    mieszkanie = Mieszkanie(width=7, height=7)

    # Tworzenie pokoi
    pokoj1 = Pokoj(0, 3, 4, 7)  # Pokój 1
    pokoj2 = Pokoj(3, 7, 4, 7)  # Pokój 2
    pokoj3 = Pokoj(0, 3, 0, 4)  # Pokój 3
    pokoj4 = Pokoj(3, 7, 0, 4)  # Pokój 4

    # Dodanie pokoi do mieszkania
    mieszkanie.dodaj_pokoj(pokoj1)
    mieszkanie.dodaj_pokoj(pokoj2)
    mieszkanie.dodaj_pokoj(pokoj3)
    mieszkanie.dodaj_pokoj(pokoj4)

    okno1 = Okno(3.5, 4.5, 7, 7)  # okno pokoj 2
    okno2 = Okno(4.5, 5.5, 0, 0)  # okno pokoj 4
    okno3 = Okno(0, 0, 1, 2) #okno pokoj 3

    # Dodanie okien do mieszkania
    mieszkanie.dodaj_okno(okno1)
    mieszkanie.dodaj_okno(okno2)
    mieszkanie.dodaj_okno(okno3)

    drzwi1 = Drzwi(1, 2, 4, 4)  # drzwi pokoj 1
    drzwi2 = Drzwi(4, 5, 4, 4)  # drzwi pokoj 2
    drzwi3 = Drzwi(3, 3, 1.5, 2.5)  # drzwi pokoj 3

    # Dodanie okien do mieszkania
    mieszkanie.dodaj_drzwi(drzwi1)
    mieszkanie.dodaj_drzwi(drzwi2)
    mieszkanie.dodaj_drzwi(drzwi3)

    grzejnik1 = Grzejnik(6.5, 7, 5, 6)  # Grzejnik w pokoju 2
    grzejnik2 = Grzejnik(4.5, 5.5, 0, 0.5)  # Grzejnik w pokoju 4
    grzejnik3 = Grzejnik(0, 0.5, 1, 2)  # Grzejnik w pokoju 3

    # Dodanie grzejników do mieszkania
    mieszkanie.dodaj_grzejnik(grzejnik1)
    mieszkanie.dodaj_grzejnik(grzejnik2)
    mieszkanie.dodaj_grzejnik(grzejnik3)

    # Rysowanie mieszkania
    mieszkanie.rysuj()