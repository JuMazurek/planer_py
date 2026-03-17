"""
jeden wpis to słownik; słownik zawiera pary

wszystkie wpisy to lista
"""
#(osobna funkcja na każdą akcję) - wybór za pomocą menu nawigacji.

from datetime import datetime
import json
import os

priorytet_waga = {
    "niski": 1,
    "średni": 2,
    "wysoki": 3
}

lista_wpisow = []


def pokaz_menu():
    print("PLAN DNIA")
    print("1. Wczytaj z pliku")
    print("2. Nowy wpis")
    print("3. Wyświetl wpisy")
    print("4. Edytuj wpis")
    print("5. Zapisz do pliku")
    print("0. Zakończ program")

def utworz_wpis():
    print("DODAWANIE NOWEGO WPISU")

    while True: #temat

        temat = input("Temat *: ").strip() #usuwanie pustych znaków, żeby spacja albo enter nie mogło być tytułem wpisu
        if temat: #sprawdzenie czy puste
            break
        else:
            print("To pole nie może być puste. Spróbuj ponownie.")

    while True: #czas

        czas = input("Godzina i data (DD.MM.RRRR HH:MM) *: ").strip()
        try:
            dt = datetime.strptime(czas, "%d.%m.%Y %H:%M")
            czas = dt.strftime("%d.%m.%Y %H:%M")
            break
        except ValueError:
            print("Nieprawidłowy format. Użyj DD.MM.RRR HH:MM.")
    
    miejsce = input("Miejsce: ").strip() #miejsce

    while True: #priorytet
        priorytet = input("Jaki priorytet ma ten wpis? Wybierz niski, średni lub wysoki: ").strip().lower()
        if priorytet == "":
            priorytet = "niski"
            break
        elif priorytet in ["niski", "średni", "wysoki"]:
            break
        else:
            print("Niepoprawny wybór. Wybierz niski, średni lub wysoki.")

    while True: #notatki
        notatki = input("Notatki (maks. 256 znaków): ").strip()
        if len(notatki) <= 256:
            break
        else:
            print("Limit znaków to 256. Wprowadź notatkę ponownie.")

    nowy_wpis = {
        "temat": temat,
        "czas": czas,
        "miejsce": miejsce,
        "priorytet": priorytet,
        "notatki": notatki
    }

    lista_wpisow.append(nowy_wpis)
    print("Dodano wpis.")


def wyswietl_wpisy(lista_wpisow):
    global priorytet_waga
    if not lista_wpisow: 
        print("Brak wpisów do wyświetlenia.")
        return
    print("\nSortować wpisy?\n1. W kolejności utworzenia (domyślnie)\n2. Po dacie i godzinie (od najstarszego) \n3. Po dacie i godzinie (od najnowszego)\n4. Wg priorytetu wpisu")
    wybor_sortowania = input("Wybór: ").strip()

    if wybor_sortowania == "2":
        lista_wpisow.sort(key=lambda wpis: datetime.strptime(wpis["czas"], "%d.%m.%Y %H:%M"))
    elif wybor_sortowania == "3":
        lista_wpisow.sort(reverse=True, key=lambda wpis: datetime.strptime(wpis["czas"], "%d.%m.%Y %H:%M"))
    elif wybor_sortowania == "4":
        lista_wpisow.sort(reverse=True, key=lambda wpis: priorytet_waga.get(wpis["priorytet"], 0))
    else:
        print("LISTA WPISÓW")
    for indeks_wpisu, wpis in enumerate(lista_wpisow, start=1):
        print(f"\nWpis #{indeks_wpisu}:")
        print(f"Temat: {wpis['temat']}")
        print(f"Czas: {wpis['czas']}")
        print(f"Miejsce: {wpis['miejsce']}")
        print(f"Priorytet: {wpis['priorytet']}")
        print(f"Notatki: {wpis['notatki']}")
    #zostaną wyświetlone wszystkie zadania z pamięci programu, dla chętnych - sortowanie wg daty i godziny

def edytuj_wpis(lista_wpisow):
    if not lista_wpisow:
        print("Brak wpisów do edycji.")
        return

    print("EDYCJA WPISU")
    for indeks_wpisu, wpis in enumerate(lista_wpisow, start=1):
        print(f"{indeks_wpisu}. {wpis['temat']} ({wpis['czas']})")

    while True:
        try:
            wybor = int(input("Wybierz numer wpisu do edycji: "))
            if 1 <= wybor <= len(lista_wpisow):
                wybrany_wpis = lista_wpisow[wybor-1]
                break
            else:
                print("Nieprawidłowy numer.")
        except ValueError:
            print("Podaj liczbę.")

    print("\nWybrany wpis:")
    for klucz, wartosc in wybrany_wpis.items():
        print(f"{klucz.capitalize()}: {wartosc}")

    decyzja = input("Chcesz zmodyfikować czy usunąć wpis? Wpisz edytuj lub usuń: ").strip().lower()
    if decyzja == "usuń":
        potwierdzenie = input("Na pewno chcesz usunąć wpis?: ").strip().lower()
        if potwierdzenie == "tak":
            lista_wpisow.pop(wybor-1)
            print("Wpis usunięty.")
        else:
            print("Operacja anulowana.")
    elif decyzja == "edytuj":
        # Formularz edycji
        print("Wciśnij Enter, aby pozostawić aktualną wartość.")
        temat = input(f"Temat [{wybrany_wpis['temat']}]: ").strip()
        if temat:
            wybrany_wpis['temat'] = temat

        while True:
            czas = input(f"Czas [{wybrany_wpis['czas']}] (DD.MM.RRRR HH:MM): ").strip()
            if not czas:
                break
            try:
                dt = datetime.strptime(czas, "%d.%m.%Y %H:%M")
                wybrany_wpis['czas'] = dt.strftime("%d.%m.%Y %H:%M")
                break
            except ValueError:
                print("Nieprawidłowy format.")

        miejsce = input(f"Miejsce [{wybrany_wpis['miejsce']}]: ").strip()
        if miejsce:
            wybrany_wpis['miejsce'] = miejsce

        while True:
            priorytet = input(f"Priorytet [{wybrany_wpis['priorytet']}] (niski/średni/wysoki): ").strip().lower()
            if not priorytet:
                break
            if priorytet in ["niski", "średni", "wysoki"]:
                wybrany_wpis['priorytet'] = priorytet
                break
            else:
                print("Niepoprawny wybór.")

        while True:
            notatki = input(f"Notatki [{wybrany_wpis['notatki']}]: ").strip()
            if not notatki:
                break
            if len(notatki) <= 256:
                wybrany_wpis['notatki'] = notatki
                break
            else:
                print("Limit znaków 256.")

        print("Wpis zaktualizowany.")
    else:
        print("Niepoprawna opcja. Powrót do menu.")

plik_wyjsciowy = "plan_dnia.json"

def zapisz_do_pliku(lista_wpisow):

    print("ZAPIS DO PLIKU")
    wybor_pliku = input(f"Zapisać do domyślnego pliku '{plik_wyjsciowy}'? ").strip().lower()
    if wybor_pliku == "nie":
        nazwa_pliku = input("Podaj nazwę pliku (użyj rozszerzenia .json): ").strip()
        if not nazwa_pliku.endswith(".json"):
            nazwa_pliku += ".json"
    else:
        nazwa_pliku = plik_wyjsciowy

    try:
        with open(nazwa_pliku,"w", encoding="utf-8") as zapisz:
            json.dump(lista_wpisow, zapisz, ensure_ascii=False, indent=4)
        print(f"Dane zapisano do pliku '{nazwa_pliku}'.")
    except Exception as blad:
        print(f"Wystąpił błąd podczas zapisu: {blad}")
   

def wczytaj_z_pliku():
    print("WCZYTYWANIE Z PLIKU")
    pliki = [plik for plik in os.listdir() if plik.endswith(".json")]
    if not pliki:
        print("Brak plików JSON w tej lokalizacji.")
        return None
    
    print("Dostępne pliki: ")
    for indeks_pliku, plik in enumerate(pliki, start=1):
        print(f"{indeks_pliku}.{plik}")

    while True:
            wybor_pliku = input("Wybierz numer pliku do wczytania lub wpisz " + "Anuluj" + " aby anulować: ").strip().lower()

            if wybor_pliku == "anuluj":
                print("Wczytywanie anulowane.")
                return None
            try:
                wybor_pliku = int(wybor_pliku)
                if 1 <= wybor_pliku <= len(pliki):
                    wybrany_plik = pliki[wybor_pliku-1]
                    break
                else:
                    print("Niepoprawny numer. Wybierz ponownie.")
            except ValueError:
                print("Nieprawidłowy wybór. Podaj liczbę.")

    try:
        with open(wybrany_plik, "r", encoding="utf-8") as plik:
            lista = json.load(plik)
        print(f"Wczytano dane z pliku '{wybrany_plik}'.")
        return lista
    except Exception as blad:
        print(f"Wystąpił błąd podczas wczytywania pliku: {blad}")
        return None


    

while True:
    pokaz_menu()

    try:
        wybor = int(input("Wybierz opcję: "))
    except ValueError:
        print("Spróbuj ponownie. Wybierz jedną z podanych opcji.")
        continue

    if wybor == 1:
        nowe_wpisy = wczytaj_z_pliku()
        if nowe_wpisy is not None:
            lista_wpisow = nowe_wpisy
        else:
            print("Pozostawiono poprzednie wpisy w pamięci.")
    elif wybor == 2:
        utworz_wpis()
    elif wybor == 3:
        wyswietl_wpisy(lista_wpisow)
    elif wybor == 4:
        edytuj_wpis(lista_wpisow)
    elif wybor == 5:
        zapisz_do_pliku(lista_wpisow)
    elif wybor == 0:
        czy_zapisac = input("Czy chcesz zapisać do pliku przed zakończeniem programu? ").strip().lower()
        if czy_zapisac == "tak":
            zapisz_do_pliku(lista_wpisow)
        else:
            print("Do zobaczenia!")
            break
    else:
        print("Nieprawidłowy wybór, spróbuj ponownie.")