import numpy as np
import matplotlib.pyplot as plt

def macierz(n):
    matrix = np.zeros((n, n))
    matrix[0, 0] = -2
    matrix[0, 1] = 1
    matrix[n - 1, n - 1] = -2
    matrix[n - 1, n - 2] = 1
    for i in range(1, n - 1):
        matrix[i, i - 1] = 1
        matrix[i, i] = -2
        matrix[i, i + 1] = 1
    return matrix

def laplasjan(n, m):
    D1 = macierz(n)
    D2 = macierz(m)
    Id1 = np.eye(n)
    Id2 = np.eye(m)
    L = np.kron(Id2, D1) + np.kron(D2, Id1)
    return L


class Mieszkanie:
    def __init__(self, szerokosc, wysokosc, h_x=0.1, h_t=0.0001, czas=0.5):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.h_x = h_x
        self.h_t = h_t
        self.czas = czas
        self.n = int(szerokosc / h_x)
        self.m = int(wysokosc / h_x)
        self.t = np.arange(0, czas, h_t)
        self.k = len(self.t)
        self.u = np.zeros((self.k, self.m, self.n))
        self.pokoje = []
        self.grzejniki = []
        self.drzwi = []
        self.okna = []

    def dodaj_pokoj(self, pokoj, x_pos, y_pos):
        pokoj.x_pos = x_pos
        pokoj.y_pos = y_pos
        self.pokoje.append(pokoj)

    def dodaj_grzejnik(self, grzejnik):
        self.grzejniki.append(grzejnik)

    def dodaj_drzwi(self, drzwi):
        self.drzwi.append(drzwi)

    def dodaj_okno(self, okno):
        self.okna.append(okno)

    def krok_czasowy(self, t):
        for pokoj in self.pokoje:
            pokoj.krok_czasowy(t)
        for drzwi in self.drzwi:
            drzwi.ustaw_srednia_temperature(self, t)
        for okno in self.okna:
            okno.ustaw_temperature(self, t)

    def mapa_ciepla(self, t):
        for pokoj in self.pokoje:
            x_start = int(pokoj.x_pos / self.h_x)
            y_start = int(pokoj.y_pos / self.h_x)
            x_end = x_start + pokoj.n
            y_end = y_start + pokoj.m
            self.u[t, y_start:y_end, x_start:x_end] = pokoj.u[t, :].reshape(pokoj.m, pokoj.n)

        plt.imshow(self.u[t, :, :], cmap='hot', origin='lower', extent=[0, self.szerokosc, 0, self.wysokosc])
        plt.colorbar(label="Temperatura")
        plt.xlabel('Pozycja X (m)')
        plt.ylabel('Pozycja Y (m)')
        plt.title('Mapa Ciepła (°C)')
        plt.legend()
        plt.show()


class Pokoj:
    def __init__(self, width, height, temperatura, h_x=0.1, h_t=0.0001, czas=0.5):
        self.h_x = h_x
        self.h_t = h_t
        self.x = np.arange(0, width, h_x)
        self.y = np.arange(0, height, h_x)
        self.n = len(self.x)
        self.m = len(self.y)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.t = np.arange(0, czas, h_t)
        u0 = np.full(self.n * self.m, temperatura)
        self.k = len(self.t)
        self.u = np.zeros((self.k, self.n * self.m))
        self.u[0, :] = u0.flatten()
        self.l = laplasjan(self.n, self.m)
        self.IB1 = [i for i in range(self.n * self.m) if i % self.n == 0]
        self.IB2 = [i for i in range(self.n * self.m) if (i + 1) % self.n == 0]
        self.IB3 = [i for i in range(self.n * self.m) if i < self.n]
        self.IB4 = [i for i in range(self.n * self.m) if self.n * self.m - self.n <= i]
        self.IB1_sasiad = [i for i in range(self.n * self.m) if (i - 1) % self.n == 0]
        self.IB2_sasiad = [i for i in range(self.n * self.m) if (i + 2) % self.n == 0]
        self.IB3_sasiad = [i for i in range(self.n * self.m) if self.n <= i < 2 * self.n]
        self.IB4_sasiad = [i for i in range(self.n * self.m) if
                           (self.m * self.n - 2 * self.n) <= i < (self.m * self.n - self.n)]
        self.sciany = list(set(self.IB1 + self.IB2 + self.IB3 + self.IB4))
        self.wnetrze = [i for i in range(self.n * self.m) if i not in self.sciany]

    def krok_czasowy(self, t, alpha=0.025):
        self.u[t, :] = self.u[t - 1, :] + ((alpha * self.h_t) / self.h_x ** 2) * np.matmul(self.l, self.u[t - 1, :])
        self.u[t, self.IB1] = self.u[t, self.IB1_sasiad]
        self.u[t, self.IB2] = self.u[t, self.IB2_sasiad]
        self.u[t, self.IB3] = self.u[t, self.IB3_sasiad]
        self.u[t, self.IB4] = self.u[t, self.IB4_sasiad]

    def srednia_temperatura(self, t):
        return np.sum(self.u[t, self.wnetrze]) / len(self.wnetrze)

    def mapa(self, t):
        u_plot = self.u[t, :].reshape(self.m, self.n)
        plt.pcolormesh(self.x, self.y, u_plot, shading='auto')
        plt.colorbar(label="Temperatura")
        plt.xlabel("Szerokość")
        plt.ylabel("Wysokość")
        plt.title("Mapa ciepła")
        plt.show()


class Grzejnik:
    def __init__(self, moc, x_pos, y_pos, promien_wplywu=1, ro=1.2, c=1005):
        self.moc = moc                      # Moc grzejnika (W)
        self.x_pos = x_pos                  # Pozycja grzejnika (x)
        self.y_pos = y_pos                  # Pozycja grzejnika (y)
        self.promien_wplywu = promien_wplywu  # Promień wpływu grzejnika (m)
        self.ro = ro                        # Gęstość powietrza (kg/m³)
        self.c = c                          # Ciepło właściwe powietrza (J/kg·K)

    def aplikuj_cieplo(self, pokoj, t):
        A = pokoj.n * pokoj.m * (pokoj.h_x ** 2)
        delta_T_global = self.moc / (self.ro * A * self.c * 10)

        x_start = int(max(0, round((self.x_pos - self.promien_wplywu - pokoj.x_pos) / pokoj.h_x)))
        y_start = int(max(0, round((self.y_pos - self.promien_wplywu - pokoj.y_pos) / pokoj.h_x)))
        x_end = int(min(pokoj.n, round((self.x_pos + self.promien_wplywu - pokoj.x_pos) / pokoj.h_x)))
        y_end = int(min(pokoj.m, round((self.y_pos + self.promien_wplywu - pokoj.y_pos) / pokoj.h_x)))

        room_temp = pokoj.u[t, :].reshape(pokoj.m, pokoj.n)

        for i in range(y_start, y_end):
            for j in range(x_start, x_end):
                odleglosc = np.sqrt(
                    (pokoj.x[j] + pokoj.x_pos - self.x_pos) ** 2 +
                    (pokoj.y[i] + pokoj.y_pos - self.y_pos) ** 2
                )
                if odleglosc <= self.promien_wplywu:
                    waga = np.exp(-odleglosc ** 2 / (2 * (self.promien_wplywu / 3) ** 2))
                    delta_T = delta_T_global * waga
                    room_temp[i, j] += delta_T  # ΔT w °C

        pokoj.u[t, :] = room_temp.flatten()


class Drzwi:
    def __init__(self, x, y, szerokosc, wysokosc):
        self.x = x
        self.y = y
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

    def ustaw_srednia_temperature(self, mieszkanie, t):
        door_rooms = []
        for pokoj in mieszkanie.pokoje:
            room_width = pokoj.n * pokoj.h_x
            room_height = pokoj.m * pokoj.h_x
            if (self.x < pokoj.x_pos + room_width and self.x + self.szerokosc > pokoj.x_pos and
                    self.y < pokoj.y_pos + room_height and self.y + self.wysokosc > pokoj.y_pos):
                door_i = int(np.floor((self.y - pokoj.y_pos) / pokoj.h_x))
                door_j = int(np.floor((self.x - pokoj.x_pos) / pokoj.h_x))
                door_i = max(0, door_i)
                door_j = max(0, door_j)
                door_i_end = int(np.ceil((self.y + self.wysokosc - pokoj.y_pos) / pokoj.h_x))
                door_j_end = int(np.ceil((self.x + self.szerokosc - pokoj.x_pos) / pokoj.h_x))
                door_i_end = min(pokoj.m, door_i_end)
                door_j_end = min(pokoj.n, door_j_end)
                door_height = door_i_end - door_i
                door_width = door_j_end - door_j
                if door_height > 0 and door_width > 0:
                    door_rooms.append((pokoj, door_i, door_j, door_height, door_width))
        if not door_rooms:
            return
        if len(door_rooms) == 1:
            (pokoj, door_i, door_j, door_height, door_width) = door_rooms[0]
            room_temp = pokoj.u[t, :].reshape(pokoj.m, pokoj.n)
            room_temp_copy = room_temp.copy()
            for i in range(door_i, door_i + door_height):
                for j in range(door_j, door_j + door_width):
                    row_min = max(0, i - 1)
                    row_max = min(pokoj.m, i + 2)
                    col_min = max(0, j - 1)
                    col_max = min(pokoj.n, j + 2)
                    neighbors = room_temp_copy[row_min:row_max, col_min:col_max]
                    mask = np.ones(neighbors.shape, dtype=bool)
                    mask[i - row_min, j - col_min] = False
                    neighbor_values = neighbors[mask]
                    if neighbor_values.size > 0:
                        new_temp = np.mean(neighbor_values)
                        room_temp[i, j] = new_temp
            pokoj.u[t, :] = room_temp.flatten()
        elif len(door_rooms) == 2:
            (pokoj1, door_i1, door_j1, door_height1, door_width1) = door_rooms[0]
            (pokoj2, door_i2, door_j2, door_height2, door_width2) = door_rooms[1]
            door_height = min(door_height1, door_height2)
            door_width = min(door_width1, door_width2)
            room_temp1 = pokoj1.u[t, :].reshape(pokoj1.m, pokoj1.n)
            room_temp2 = pokoj2.u[t, :].reshape(pokoj2.m, pokoj2.n)
            room_temp1_copy = room_temp1.copy()
            room_temp2_copy = room_temp2.copy()
            for di in range(door_height):
                for dj in range(door_width):
                    i1 = door_i1 + di
                    j1 = door_j1 + dj
                    i2 = door_i2 + di
                    j2 = door_j2 + dj
                    row_min1 = max(0, i1 - 1)
                    row_max1 = min(pokoj1.m, i1 + 2)
                    col_min1 = max(0, j1 - 1)
                    col_max1 = min(pokoj1.n, j1 + 2)
                    neighbors1 = room_temp1_copy[row_min1:row_max1, col_min1:col_max1]
                    mask1 = np.ones(neighbors1.shape, dtype=bool)
                    mask1[i1 - row_min1, j1 - col_min1] = False
                    neighbor_values1 = neighbors1[mask1]

                    row_min2 = max(0, i2 - 1)
                    row_max2 = min(pokoj2.m, i2 + 2)
                    col_min2 = max(0, j2 - 1)
                    col_max2 = min(pokoj2.n, j2 + 2)
                    neighbors2 = room_temp2_copy[row_min2:row_max2, col_min2:col_max2]
                    mask2 = np.ones(neighbors2.shape, dtype=bool)
                    mask2[i2 - row_min2, j2 - col_min2] = False
                    neighbor_values2 = neighbors2[mask2]

                    if neighbor_values1.size > 0 and neighbor_values2.size > 0:
                        new_temp = (np.mean(neighbor_values1) + np.mean(neighbor_values2)) / 2
                    elif neighbor_values1.size > 0:
                        new_temp = np.mean(neighbor_values1)
                    elif neighbor_values2.size > 0:
                        new_temp = np.mean(neighbor_values2)
                    else:
                        new_temp = (room_temp1_copy[i1, j1] + room_temp2_copy[i2, j2]) / 2

                    room_temp1[i1, j1] = new_temp
                    room_temp2[i2, j2] = new_temp
            pokoj1.u[t, :] = room_temp1.flatten()
            pokoj2.u[t, :] = room_temp2.flatten()


class Okno:
    def __init__(self, x, y, szerokosc, wysokosc, temp):
        self.x = x
        self.y = y
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.temp = temp

    def ustaw_temperature(self, mieszkanie, t):
        for pokoj in mieszkanie.pokoje:
            room_width = pokoj.n * pokoj.h_x
            room_height = pokoj.m * pokoj.h_x

            if (self.x < pokoj.x_pos + room_width and self.x + self.szerokosc > pokoj.x_pos and
                    self.y < pokoj.y_pos + room_height and self.y + self.wysokosc > pokoj.y_pos):

                win_i = int(np.floor((self.y - pokoj.y_pos) / pokoj.h_x))
                win_j = int(np.floor((self.x - pokoj.x_pos) / pokoj.h_x))
                win_i = max(0, win_i)
                win_j = max(0, win_j)
                win_i_end = int(np.ceil((self.y + self.wysokosc - pokoj.y_pos) / pokoj.h_x))
                win_j_end = int(np.ceil((self.x + self.szerokosc - pokoj.x_pos) / pokoj.h_x))
                win_i_end = min(pokoj.m, win_i_end)
                win_j_end = min(pokoj.n, win_j_end)


                room_temp = pokoj.u[t, :].reshape(pokoj.m, pokoj.n)
                room_temp[win_i:win_i_end, win_j:win_j_end] = self.temp

                pokoj.u[t, :] = room_temp.flatten()