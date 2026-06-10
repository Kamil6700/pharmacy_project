from tkinter import *
from tkinter import ttk
import tkintermapview


class Klient:
    def __init__(self, imie, nazwisko, lokalizacja):
        self.imie = imie
        self.nazwisko = nazwisko
        self.lokalizacja = lokalizacja
        self.leki = []  # lista obiektów Lek przypisanych do klienta
        self.coordinates = get_coordinates(lokalizacja)
        self.marker = None

    @property
    def pelne_imie(self):
        return f"{self.imie} {self.nazwisko}"


class Pracownik:
    def __init__(self, imie, nazwisko, lokalizacja, stanowisko):
        self.imie = imie
        self.nazwisko = nazwisko
        self.lokalizacja = lokalizacja
        self.stanowisko = stanowisko
        self.coordinates = get_coordinates(lokalizacja)
        self.marker = None

    @property
    def pelne_imie(self):
        return f"{self.imie} {self.nazwisko}"


class Lek:
    def __init__(self, nazwa, opis, klient=None):
        self.nazwa = nazwa
        self.opis = opis
        self.klient = klient  # referencja do Klient


# --- Listy główne ---
klienci = []       # lista Klient
pracownicy = []    # lista Pracownik
leki = []          # lista Lek


# --- Funkcja do pobierania współrzędnych ---
def get_coordinates(location):
    import requests
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location,
        'format': 'json',
        'limit': 1,
        'accept-language': 'pl'
    }
    headers = {'User-Agent': 'Mozilla/5.0 (projekt_apteka)'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        return [float(data[0]['lat']), float(data[0]['lon'])]
    else:
        return [52.23, 21.00]  # domyślne współrzędne (Warszawa), jeśli nie znaleziono


# --- GUI ---
root = Tk()
root.title('System zarządzania apteką')
root.geometry("1400x800")
root.minsize(900, 600)

# Zakładki
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)


# --- Zakładka Klienci ---
frame_klienci = Frame(notebook)
notebook.add(frame_klienci, text='Klienci')

frame_form_klient = Frame(frame_klienci)
frame_form_klient.pack(fill=X, padx=5, pady=5)

Label(frame_form_klient, text='Imię:').pack(side=LEFT)
entry_imie_klienta = Entry(frame_form_klient, width=12)
entry_imie_klienta.pack(side=LEFT, padx=2)

Label(frame_form_klient, text='Nazwisko:').pack(side=LEFT)
entry_nazwisko_klienta = Entry(frame_form_klient, width=12)
entry_nazwisko_klienta.pack(side=LEFT, padx=2)

Label(frame_form_klient, text='Lokalizacja:').pack(side=LEFT)
entry_lokalizacja_klienta = Entry(frame_form_klient, width=16)
entry_lokalizacja_klienta.pack(side=LEFT, padx=2)

button_dodaj_klienta = Button(frame_form_klient, text='Dodaj', command=lambda: dodaj_klienta())
button_dodaj_klienta.pack(side=LEFT, padx=2)

button_usun_klienta = Button(frame_form_klient, text='Usuń', command=lambda: usun_klienta())
button_usun_klienta.pack(side=LEFT, padx=2)

button_edytuj_klienta = Button(frame_form_klient, text='Edytuj', command=lambda: edytuj_klienta())
button_edytuj_klienta.pack(side=LEFT, padx=2)

button_szczegoly_klienta = Button(frame_form_klient, text='Pokaż szczegóły', command=lambda: pokaz_szczegoly_klienta())
button_szczegoly_klienta.pack(side=LEFT, padx=2)

button_leki_klienta = Button(frame_form_klient, text='Pokaż leki klienta', command=lambda: pokaz_leki_zaznaczonego_klienta())
button_leki_klienta.pack(side=LEFT, padx=2)

listbox_klienci = Listbox(frame_klienci)
listbox_klienci.pack(fill=BOTH, expand=True, padx=5, pady=5)

mapa_klienci = tkintermapview.TkinterMapView(frame_klienci, width=600, height=300, corner_radius=0)
mapa_klienci.pack(fill=BOTH, expand=True, padx=5, pady=5)
mapa_klienci.set_position(52.23, 21.00)
mapa_klienci.set_zoom(6)


# --- Zakładka Pracownicy ---
frame_pracownicy = Frame(notebook)
notebook.add(frame_pracownicy, text='Pracownicy')

frame_form_pracownik = Frame(frame_pracownicy)
frame_form_pracownik.pack(fill=X, padx=5, pady=5)

Label(frame_form_pracownik, text='Imię:').pack(side=LEFT)
entry_imie_pracownika = Entry(frame_form_pracownik, width=10)
entry_imie_pracownika.pack(side=LEFT, padx=2)

Label(frame_form_pracownik, text='Nazwisko:').pack(side=LEFT)
entry_nazwisko_pracownika = Entry(frame_form_pracownik, width=10)
entry_nazwisko_pracownika.pack(side=LEFT, padx=2)

Label(frame_form_pracownik, text='Lokalizacja:').pack(side=LEFT)
entry_lokalizacja_pracownika = Entry(frame_form_pracownik, width=12)
entry_lokalizacja_pracownika.pack(side=LEFT, padx=2)

Label(frame_form_pracownik, text='Stanowisko:').pack(side=LEFT)
entry_stanowisko_pracownika = Entry(frame_form_pracownik, width=14)
entry_stanowisko_pracownika.pack(side=LEFT, padx=2)

button_dodaj_pracownika = Button(frame_form_pracownik, text='Dodaj', command=lambda: dodaj_pracownika())
button_dodaj_pracownika.pack(side=LEFT, padx=2)

button_usun_pracownika = Button(frame_form_pracownik, text='Usuń', command=lambda: usun_pracownika())
button_usun_pracownika.pack(side=LEFT, padx=2)

button_edytuj_pracownika = Button(frame_form_pracownik, text='Edytuj', command=lambda: edytuj_pracownika())
button_edytuj_pracownika.pack(side=LEFT, padx=2)

button_szczegoly_pracownika = Button(frame_form_pracownik, text='Pokaż szczegóły', command=lambda: pokaz_szczegoly_pracownika())
button_szczegoly_pracownika.pack(side=LEFT, padx=2)

listbox_pracownicy = Listbox(frame_pracownicy)
listbox_pracownicy.pack(fill=BOTH, expand=True, padx=5, pady=5)

mapa_pracownicy = tkintermapview.TkinterMapView(frame_pracownicy, width=600, height=300, corner_radius=0)
mapa_pracownicy.pack(fill=BOTH, expand=True, padx=5, pady=5)
mapa_pracownicy.set_position(52.23, 21.00)
mapa_pracownicy.set_zoom(6)


# --- Zakładka Leki klienta ---
frame_leki = Frame(notebook)
notebook.add(frame_leki, text='Leki klienta')

frame_form_lek = Frame(frame_leki)
frame_form_lek.pack(fill=X, padx=5, pady=5)

Label(frame_form_lek, text='Nazwa leku:').pack(side=LEFT)
entry_nazwa_leku = Entry(frame_form_lek, width=15)
entry_nazwa_leku.pack(side=LEFT, padx=2)

Label(frame_form_lek, text='Opis / dawkowanie:').pack(side=LEFT)
entry_opis_leku = Entry(frame_form_lek, width=20)
entry_opis_leku.pack(side=LEFT, padx=2)

Label(frame_form_lek, text='Klient:').pack(side=LEFT)
combobox_klient_leku = ttk.Combobox(frame_form_lek, width=25, state='readonly')
combobox_klient_leku.pack(side=LEFT, padx=2)

button_dodaj_lek = Button(frame_form_lek, text='Dodaj', command=lambda: dodaj_lek())
button_dodaj_lek.pack(side=LEFT, padx=2)

button_usun_lek = Button(frame_form_lek, text='Usuń', command=lambda: usun_lek())
button_usun_lek.pack(side=LEFT, padx=2)

button_edytuj_lek = Button(frame_form_lek, text='Edytuj', command=lambda: edytuj_lek())
button_edytuj_lek.pack(side=LEFT, padx=2)

button_pokaz_leki_klienta = Button(frame_form_lek, text='Pokaż leki wybranego klienta', command=lambda: odswiez_liste_lekow(filtruj_po_kliencie=True))
button_pokaz_leki_klienta.pack(side=LEFT, padx=2)

button_pokaz_wszystkie_leki = Button(frame_form_lek, text='Pokaż wszystkie', command=lambda: odswiez_liste_lekow())
button_pokaz_wszystkie_leki.pack(side=LEFT, padx=2)

listbox_leki = Listbox(frame_leki)
listbox_leki.pack(fill=BOTH, expand=True, padx=5, pady=5)


# --- Funkcje pomocnicze ---
def opis_klienta(klient):
    return f"{klient.imie} {klient.nazwisko} ({klient.lokalizacja})"


def znajdz_klienta_po_opisie(opis):
    return next((k for k in klienci if opis_klienta(k) == opis), None)


def odswiez_combobox_klientow():
    wartosci = [opis_klienta(k) for k in klienci]
    combobox_klient_leku['values'] = wartosci


# --- Funkcje obsługi klientów ---
def odswiez_liste_klientow():
    listbox_klienci.delete(0, END)
    for idx, k in enumerate(klienci):
        listbox_klienci.insert(idx, f"{k.imie} {k.nazwisko} ({k.lokalizacja}) | Liczba leków: {len(k.leki)}")

    odswiez_combobox_klientow()

    # Odśwież markery na mapie klientów
    mapa_klienci.delete_all_marker()
    for k in klienci:
        k.marker = mapa_klienci.set_marker(k.coordinates[0], k.coordinates[1], text=k.pelne_imie)


def dodaj_klienta():
    imie = entry_imie_klienta.get()
    nazwisko = entry_nazwisko_klienta.get()
    lokalizacja = entry_lokalizacja_klienta.get()

    if not imie or not nazwisko or not lokalizacja:
        return

    klient = Klient(imie, nazwisko, lokalizacja)
    klient.marker = mapa_klienci.set_marker(klient.coordinates[0], klient.coordinates[1], text=klient.pelne_imie)
    klienci.append(klient)

    odswiez_liste_klientow()
    entry_imie_klienta.delete(0, END)
    entry_nazwisko_klienta.delete(0, END)
    entry_lokalizacja_klienta.delete(0, END)


def usun_klienta():
    idx = listbox_klienci.curselection()
    if not idx:
        return

    idx = idx[0]
    klient = klienci[idx]

    if klient.marker:
        klient.marker.delete()

    # Usuń z głównej listy wszystkie leki przypisane do klienta
    for lek in klient.leki[:]:
        if lek in leki:
            leki.remove(lek)

    klienci.pop(idx)
    odswiez_liste_klientow()
    odswiez_liste_lekow()
    button_dodaj_klienta.config(text='Dodaj', command=lambda: dodaj_klienta())

def edytuj_klienta():
    idx = listbox_klienci.curselection()
    if not idx:
        return

    idx = idx[0]
    klient = klienci[idx]

    entry_imie_klienta.delete(0, END)
    entry_nazwisko_klienta.delete(0, END)
    entry_lokalizacja_klienta.delete(0, END)

    entry_imie_klienta.insert(0, klient.imie)
    entry_nazwisko_klienta.insert(0, klient.nazwisko)
    entry_lokalizacja_klienta.insert(0, klient.lokalizacja)

    button_dodaj_klienta.config(text='Zapisz', command=lambda: zapisz_edycje_klienta(idx))


def zapisz_edycje_klienta(idx):
    imie = entry_imie_klienta.get()
    nazwisko = entry_nazwisko_klienta.get()
    lokalizacja = entry_lokalizacja_klienta.get()

    if not imie or not nazwisko or not lokalizacja:
        return

    klient = klienci[idx]
    klient.imie = imie
    klient.nazwisko = nazwisko
    klient.lokalizacja = lokalizacja
    klient.coordinates = get_coordinates(lokalizacja)

    if klient.marker:
        klient.marker.delete()

    klient.marker = mapa_klienci.set_marker(klient.coordinates[0], klient.coordinates[1], text=klient.pelne_imie)

    odswiez_liste_klientow()
    odswiez_liste_lekow()

    entry_imie_klienta.delete(0, END)
    entry_nazwisko_klienta.delete(0, END)
    entry_lokalizacja_klienta.delete(0, END)

    button_dodaj_klienta.config(text='Dodaj', command=lambda: dodaj_klienta())


# --- Funkcje obsługi pracowników ---
def odswiez_liste_pracownikow():
    listbox_pracownicy.delete(0, END)
    for idx, p in enumerate(pracownicy):
        listbox_pracownicy.insert(idx, f"{p.imie} {p.nazwisko} ({p.lokalizacja}) | {p.stanowisko}")

    # Odśwież markery na mapie pracowników
    mapa_pracownicy.delete_all_marker()
    for p in pracownicy:
        p.marker = mapa_pracownicy.set_marker(p.coordinates[0], p.coordinates[1], text=f"{p.imie} {p.nazwisko}")


def dodaj_pracownika():
    imie = entry_imie_pracownika.get()
    nazwisko = entry_nazwisko_pracownika.get()
    lokalizacja = entry_lokalizacja_pracownika.get()
    stanowisko = entry_stanowisko_pracownika.get()

    if not imie or not nazwisko or not lokalizacja or not stanowisko:
        return

    pracownik = Pracownik(imie, nazwisko, lokalizacja, stanowisko)
    pracownik.marker = mapa_pracownicy.set_marker(pracownik.coordinates[0], pracownik.coordinates[1], text=pracownik.pelne_imie)
    pracownicy.append(pracownik)

    odswiez_liste_pracownikow()

    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)
    entry_stanowisko_pracownika.delete(0, END)


def usun_pracownika():
    idx = listbox_pracownicy.curselection()
    if not idx:
        return

    idx = idx[0]
    pracownik = pracownicy[idx]

    if pracownik.marker:
        pracownik.marker.delete()

    pracownicy.pop(idx)
    odswiez_liste_pracownikow()
    button_dodaj_pracownika.config(text='Dodaj', command=lambda: dodaj_pracownika())


def edytuj_pracownika():
    idx = listbox_pracownicy.curselection()
    if not idx:
        return

    idx = idx[0]
    pracownik = pracownicy[idx]

    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)
    entry_stanowisko_pracownika.delete(0, END)

    entry_imie_pracownika.insert(0, pracownik.imie)
    entry_nazwisko_pracownika.insert(0, pracownik.nazwisko)
    entry_lokalizacja_pracownika.insert(0, pracownik.lokalizacja)
    entry_stanowisko_pracownika.insert(0, pracownik.stanowisko)

    button_dodaj_pracownika.config(text='Zapisz', command=lambda: zapisz_edycje_pracownika(idx))


def zapisz_edycje_pracownika(idx):
    imie = entry_imie_pracownika.get()
    nazwisko = entry_nazwisko_pracownika.get()
    lokalizacja = entry_lokalizacja_pracownika.get()
    stanowisko = entry_stanowisko_pracownika.get()

    if not imie or not nazwisko or not lokalizacja or not stanowisko:
        return

    pracownik = pracownicy[idx]
    pracownik.imie = imie
    pracownik.nazwisko = nazwisko
    pracownik.lokalizacja = lokalizacja
    pracownik.stanowisko = stanowisko
    pracownik.coordinates = get_coordinates(lokalizacja)

    if pracownik.marker:
        pracownik.marker.delete()

    pracownik.marker = mapa_pracownicy.set_marker(pracownik.coordinates[0], pracownik.coordinates[1], text=pracownik.pelne_imie)

    odswiez_liste_pracownikow()

    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)
    entry_stanowisko_pracownika.delete(0, END)

    button_dodaj_pracownika.config(text='Dodaj', command=lambda: dodaj_pracownika())


# --- Funkcje obsługi leków ---
def odswiez_liste_lekow(filtruj_po_kliencie=False):
    listbox_leki.delete(0, END)

    klient_filtr = None
    if filtruj_po_kliencie:
        klient_filtr = znajdz_klienta_po_opisie(combobox_klient_leku.get())

    pokazane_leki = leki
    if klient_filtr:
        pokazane_leki = klient_filtr.leki

    for idx, lek in enumerate(pokazane_leki):
        klient = lek.klient.pelne_imie if lek.klient else '-'
        listbox_leki.insert(idx, f"{lek.nazwa} - {lek.opis} [Klient: {klient}]")


def dodaj_lek():
    nazwa = entry_nazwa_leku.get()
    opis = entry_opis_leku.get()
    klient_opis = combobox_klient_leku.get()
    klient = znajdz_klienta_po_opisie(klient_opis)

    if not nazwa or not opis or not klient:
        return

    lek = Lek(nazwa, opis, klient)
    leki.append(lek)
    klient.leki.append(lek)

    odswiez_liste_lekow()
    odswiez_liste_klientow()

    entry_nazwa_leku.delete(0, END)
    entry_opis_leku.delete(0, END)
    combobox_klient_leku.set('')


def pobierz_zaznaczony_lek():
    idx = listbox_leki.curselection()
    if not idx:
        return None, None

    tekst_z_listy = listbox_leki.get(idx[0])
    for indeks, lek in enumerate(leki):
        klient = lek.klient.pelne_imie if lek.klient else '-'
        opis = f"{lek.nazwa} - {lek.opis} [Klient: {klient}]"
        if opis == tekst_z_listy:
            return indeks, lek

    return None, None


def usun_lek():
    idx, lek = pobierz_zaznaczony_lek()
    if lek is None:
        return

    if lek.klient and lek in lek.klient.leki:
        lek.klient.leki.remove(lek)

    leki.pop(idx)

    odswiez_liste_lekow()
    odswiez_liste_klientow()
    button_dodaj_lek.config(text='Dodaj', command=lambda: dodaj_lek())


def edytuj_lek():
    idx, lek = pobierz_zaznaczony_lek()
    if lek is None:
        return

    entry_nazwa_leku.delete(0, END)
    entry_opis_leku.delete(0, END)
    combobox_klient_leku.set('')

    entry_nazwa_leku.insert(0, lek.nazwa)
    entry_opis_leku.insert(0, lek.opis)

    if lek.klient:
        combobox_klient_leku.set(opis_klienta(lek.klient))

    button_dodaj_lek.config(text='Zapisz', command=lambda: zapisz_edycje_leku(idx))


def zapisz_edycje_leku(idx):
    nazwa = entry_nazwa_leku.get()
    opis = entry_opis_leku.get()
    klient_opis = combobox_klient_leku.get()
    nowy_klient = znajdz_klienta_po_opisie(klient_opis)

    if not nazwa or not opis or not nowy_klient:
        return

    lek = leki[idx]

    if lek.klient and lek in lek.klient.leki:
        lek.klient.leki.remove(lek)

    lek.nazwa = nazwa
    lek.opis = opis
    lek.klient = nowy_klient

    if lek not in nowy_klient.leki:
        nowy_klient.leki.append(lek)

    odswiez_liste_lekow()
    odswiez_liste_klientow()

    entry_nazwa_leku.delete(0, END)
    entry_opis_leku.delete(0, END)
    combobox_klient_leku.set('')

    button_dodaj_lek.config(text='Dodaj', command=lambda: dodaj_lek())


# --- Funkcje szczegółów ---
def pokaz_szczegoly_klienta():
    idx = listbox_klienci.curselection()
    if not idx:
        return

    idx = idx[0]
    klient = klienci[idx]

    if klient.marker:
        mapa_klienci.set_zoom(15)
        mapa_klienci.set_position(klient.coordinates[0], klient.coordinates[1])


def pokaz_szczegoly_pracownika():
    idx = listbox_pracownicy.curselection()
    if not idx:
        return

    idx = idx[0]
    pracownik = pracownicy[idx]

    if pracownik.marker:
        mapa_pracownicy.set_zoom(15)
        mapa_pracownicy.set_position(pracownik.coordinates[0], pracownik.coordinates[1])


def pokaz_leki_zaznaczonego_klienta():
    idx = listbox_klienci.curselection()
    if not idx:
        return

    idx = idx[0]
    klient = klienci[idx]

    okno = Toplevel(root)
    okno.title(f"Leki klienta: {klient.pelne_imie}")
    okno.geometry("500x300")

    Label(okno, text=f"Leki klienta: {klient.pelne_imie}", font=("Arial", 12, "bold")).pack(pady=5)

    lista = Listbox(okno)
    lista.pack(fill=BOTH, expand=True, padx=10, pady=10)

    if klient.leki:
        for lek in klient.leki:
            lista.insert(END, f"{lek.nazwa} - {lek.opis}")
    else:
        lista.insert(END, "Brak leków przypisanych do tego klienta.")


# --- Automatyczne odświeżenie listy przy starcie ---
odswiez_liste_klientow()
odswiez_liste_pracownikow()
odswiez_liste_lekow()
odswiez_combobox_klientow()

root.mainloop()
