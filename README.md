============================================================
Symulacja Rozkładu Temperatury w Mieszkaniu
============================================================

Opis projektu
-------------
Projekt symulacji rozkładu temperatury w mieszkaniu został stworzony w języku Python z wykorzystaniem bibliotek NumPy oraz Matplotlib.
Celem projektu jest symulacja przepływu ciepła w mieszkaniu z uwzględnieniem różnych elementów, takich jak:
  - Pokoje (klasa Pokoj)
  - Grzejniki (klasa Grzejnik)
  - Drzwi (klasa Drzwi)
  - Okna (klasa Okno)

Mechanizm symulacji opiera się na dyskretyzacji przestrzeni i czasie oraz zastosowaniu metody różnic skończonych do rozwiązania równania dyfuzji ciepła. Wykorzystany został operator Laplasjana, który jest konstruowany przy użyciu iloczynu Kroneckera.

Funkcjonalności
---------------
- **Definicja geometrii mieszkania**: Możliwość definiowania różnych pokojów oraz ich położenia.
- **Symulacja przepływu ciepła**: Dynamiczna symulacja zmian temperatury w czasie.
- **Wpływ elementów architektonicznych**:
  - Grzejniki dodają ciepło w określonych obszarach.
  - Drzwi i okna wpływają na wymianę ciepła (okna nadają określoną temperaturę, a drzwi umożliwiają wyrównanie temperatur pomiędzy pomieszczeniami).
- **Wizualizacja**: Mapa cieplna mieszkania prezentowana jest za pomocą biblioteki Matplotlib.

Wymagania
----------
Aby uruchomić projekt, należy mieć zainstalowane następujące biblioteki:
  - Python 3.x
  - NumPy
  - Matplotlib

Instalacja bibliotek (przykład z użyciem pip):
------------------------------------------------
  pip install numpy matplotlib

Uruchomienie
------------
Aby uruchomić symulację, wystarczy wywołać skrypt w terminalu:
  
  python nazwa_skryptu.py

W przykładowym uruchomieniu symulacja przebiega dla kilku wartości temperatury zewnętrznej (np. 3.7, 4.6, 6.8, 5°C). W każdej iteracji symulowane są zmiany temperatury w czasie, a na koniec prezentowana jest mapa cieplna mieszkania.

Struktura kodu
---------------
Główne elementy projektu:
  - Funkcja `macierz(n)` oraz `laplasjan(n, m)` - tworzą macierz Laplasjana używaną do symulacji dyfuzji ciepła.
  - Klasa `Mieszkanie` - zarządza symulacją całego mieszkania, integrując wszystkie pomieszczenia i elementy wpływające na temperaturę.
  - Klasa `Pokoj` - definiuje geometrię i początkowy rozkład temperatury w danym pomieszczeniu oraz wykonuje symulację przepływu ciepła.
  - Klasa `Grzejnik` - dodaje ciepło do określonych obszarów pokoju z uwzględnieniem wpływu promienia.
  - Klasa `Drzwi` - odpowiada za wyrównywanie temperatur między pomieszczeniami poprzez symulację wymiany ciepła.
  - Klasa `Okno` - ustala temperaturę w obszarze okna, symulując wpływ temperatury zewnętrznej.

Uwagi
-----
- Projekt może być dalej rozwijany poprzez dodanie bardziej zaawansowanych modeli wymiany ciepła oraz uwzględnienie dodatkowych czynników środowiskowych.
- Warto zwrócić uwagę na parametry symulacji, takie jak krok przestrzenny (`h_x`), krok czasowy (`h_t`) czy wartość współczynnika dyfuzji (`alpha`), które wpływają na dokładność i stabilność symulacji.

Autor
-----
Projekt został stworzony przez Julię Rybak. Wszelkie sugestie oraz zgłaszanie błędów mile widziane.

Licencja
---------
Projekt jest udostępniany na licencji MIT. Pełną treść licencji znajdziesz w pliku LICENSE.

============================================================

