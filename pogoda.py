import datetime
import requests
import threading
from playsound import playsound
from PIL import Image

filename = "apikey"
def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

def play_audio():
    playsound("burza.mp3")


audio_thread = threading.Thread(target=play_audio)
audio_thread.start()

while True:
    # Pobieranie prognozy dla podanej lokalizacji i dnia
    def pobierz_prognoze_pogody(lokalizacja, dzien_prognozy):
        # Klucz API, adres i parametry potrzebne do połączenia z API
        
        klucz_api = "get_file_contents(filename)" #Wprowadź swój klucz API
        adres_podstawowy = "https://api.openweathermap.org/data/2.5/forecast"
        parametry = {
            "q": lokalizacja,
            "appid": klucz_api,
            "units": "metric",
            "lang": "pl",
        }

        # Pobranie odpowiedzi z API
        odpowiedz = requests.get(adres_podstawowy, params=parametry)
        dane = odpowiedz.json()

        # zmiana naturalnego jezyka na date
        if dzien_prognozy == "dzisiaj":
            data = datetime.datetime.now().strftime("%Y-%m-%d")
            dzien_prognozy = "dziś"
        elif dzien_prognozy == "jutro":
            data = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
            dzien_prognozy = "jutro"
        else:
            data = dzien_prognozy
        # Pobranie pogody dla podanego dnia
        prognoza = None
        for prognoza in dane["list"]:
            if prognoza["dt_txt"].startswith(data):
                break
        # Jeśli pogoda została pobrana, wyświetlenie jej szczegółów

        if prognoza:
            temperatura_min = prognoza["main"]["temp_min"]
            tempetatura_max = prognoza["main"]["temp_max"]
            temperatura_odcz = prognoza["main"]["feels_like"]
            wilgotnosc = prognoza["main"]["humidity"]
            predkosc_wiatru = prognoza["wind"]["speed"]
            ciezar_opadu = prognoza["rain"]["3h"] if "rain" in prognoza else 0
            snieg = prognoza["snow"]["3h"] if "snow" in prognoza else 0
            cisnienie = prognoza["main"]["pressure"]
            opis_pogody = prognoza["weather"][0]["description"]

            print(f"Prognoza pogody dla {lokalizacja} na dzień {dzien_prognozy}:")
            print(f"Temperatura minimalna: {temperatura_min}°C")
            print(f"Temperatura maksymalna: {tempetatura_max}°C")
            print(f"Temperatura odczuwalna: {temperatura_odcz}°C")
            print(f"Wilgotność: {wilgotnosc}%")
            print(f"Prędkość wiatru: {predkosc_wiatru} m/s")
            if "rain" in prognoza:
                print(f"Przewidywane opady: {ciezar_opadu} mm")
            if "snow" in prognoza:
                print(f"Przewidywane opady śniegu: {snieg} cm")
            print(f"Ciśnienie: {cisnienie} hPa")
            print(f"Opis pogody: {opis_pogody}")

        else:
            print(
                f"Nie udało się pobrać prognozy pogody dla {lokalizacja} na dzień {dzien_prognozy}."
            )

    # Pobieranie aktualnej pogody
    def pobierz_aktualna_pogode(lokalizacja):
        klucz_api = "get_file_contents(filename)"#Wprowadź swój klucz API
        adres_podstawowy = "https://api.openweathermap.org/data/2.5/weather"
        parametry = {
            "q": lokalizacja,
            "appid": klucz_api,
            "units": "metric",
            "lang": "pl",
        }
        odpowiedz = requests.get(adres_podstawowy, params=parametry)
        dane = odpowiedz.json()

        # Jeśli aktualna pogoda została pobrana, wyświetlenie jej szczegółów
        temperatura = dane["main"]["temp"]
        temperatura_odcz = dane["main"]["feels_like"]
        wilgotnosc = dane["main"]["humidity"]
        predkosc_wiatru = dane["wind"]["speed"]
        opady = dane["rain"]["1h"] if "rain" in dane else 0
        snieg = dane["snow"]["1h"] if "snow" in dane else 0
        cisnienie = dane["main"]["pressure"]
        opis_pogody = dane["weather"][0]["description"]

        print(f"Aktualna pogoda dla {lokalizacja}:")
        print(f"Temperatura: {temperatura}°C")
        print(f"Temperatura odczuwalna: {temperatura_odcz}°C")
        print(f"Wilgotność: {wilgotnosc}%")
        print(f"Prędkość wiatru: {predkosc_wiatru} m/s")
        if "rain" in dane:
            print(f"Przewidywane opady: {opady} mm")
        if "snow" in dane:
            print(f"Przewidywane opady śniegu: {snieg} cm")
        print(f"Ciśnienie: {cisnienie} hPa")
        print(f"Opis pogody: {opis_pogody}")

    # wprowadzanie lokalizacji i wybór aktualnej pogody albo prognozy
    lokalizacja = input("Podaj lokalizację: ")
    rodzaj_prognozy = input(
        "Czy chcesz otrzymać aktualną czy prognozowaną pogodę? (aktualna/prognoza): "
    )
    # wprowadzanie dnia
    if rodzaj_prognozy == "prognoza":
        dzien_prognozy = input(
            "Dla którego dnia chcesz otrzymać prognozę pogody (dzisiaj, jutro, nazwa dnia tygodnia): "
        )
        pobierz_prognoze_pogody(lokalizacja, dzien_prognozy)
    elif rodzaj_prognozy == "aktualna":
        pobierz_aktualna_pogode(lokalizacja)
    else:
        print("Niepoprawny rodzaj prognozy.")

    while True:
        koniec = input("Czy chcesz zakończyć działanie programu? (tak / nie): ")
        if koniec not in ["tak", "nie"]:
            print("Niepoprawna odpowiedź, spróbuj ponownie.")
            continue
        elif koniec == "tak":
            print("Dziękujemy za skorzystanie z naszego systemu.")
            obrazek = Image.open("kot.jpg")
            obrazek.show()
            exit()
        else:
            break


# dodac integracje a chatterbot
