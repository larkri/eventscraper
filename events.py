import requests
import json


def fetch_and_save_data():
    url = 'https://polisen.se/api/events'  # API-URL

    try:
        # Skicka GET-förfrågan till API:et
        response = requests.get(url)

        # Kontrollera om anslutningen var framgångsrik
        if response.status_code == 200:
            print("Anslutning lyckades! Hämtar data...")

            # Om data finns, spara som en JSON-fil
            data = response.json()  # Hämta JSON-data

            # Skriv JSON-data till en fil
            with open('events_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print("Data sparades i 'events_data.json'.")
        else:
            print(f"Fel: Fick statuskod {response.status_code} från API:et.")

    except requests.exceptions.RequestException as e:
        # Om det uppstår ett problem med att nå API:et
        print(f"Fel vid anslutning: {e}")


# Kör funktionen för att hämta och spara data
fetch_and_save_data()
