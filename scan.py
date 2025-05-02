import requests
import time
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Funktion för att hämta data från Polisen API
def fetch_data_from_api():
    api_url = 'https://polisen.se/api/events'
    session = requests.Session()

    # Skapa en retry-strategi
    retry_strategy = Retry(
        total=3,  # Maximalt antal försök
        backoff_factor=1,  # Väntetid mellan försök (1, 2, 4 sekunder)
        status_forcelist=[500, 502, 503, 504],  # Försök igen vid dessa statuskoder
        allowed_methods=["GET"]  # Applicera på GET-metoder
    )

    # Använd retry-strategin med en HTTPAdapter
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    try:
        response = session.get(api_url, timeout=10)  # Timeout 10 sekunder
        if response.status_code == 200:
            data = response.json()
            print("Exempel på hämtad data:", data[0] if data else "Ingen data")  # Skriv ut första händelsen
            return data
        else:
            print(f"Fel vid hämtning av data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Fel vid förfrågan: {e}")
        return None


# Funktion för att lägga till nya händelser till events_data.json
def append_new_data(existing_data, new_data):
    new_events = []

    # Sortera den existerande datan
    existing_data.sort(key=lambda event: event['datetime'])  # Använd 'datetime' istället för 'date'
  # Anpassa till rätt fält om det inte är 'date'

    # Hitta nya händelser som inte redan finns i den existerande datan
    existing_ids = {event['id'] for event in existing_data}
    for event in new_data:
        if event['id'] not in existing_ids:
            new_events.append(event)

    # Om nya händelser finns, lägg till dem
    if new_events:
        existing_data.extend(new_events)
        # Skriv tillbaka den uppdaterade listan till events_data.json
        with open('events_data.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
        print(f"{len(new_events)} ny händelse(r) lades till i events_data.json")
    else:
        print("Inga nya händelser att lägga till.")

    return new_events, existing_data


# Funktion för att läsa in befintlig data från events_data.json
def load_existing_data():
    try:
        with open('events_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("events_data.json finns inte. Skapar en ny fil.")
        return []


# Huvudfunktion som körs i en loop
def main():
    print("Kontrollerar om nya datapunkter finns...")

    # Hämta den senaste datan från API:et
    data = fetch_data_from_api()

    if data:
        # Ladda existerande data från events_data.json
        existing_data = load_existing_data()

        # Lägg till nya händelser om det finns några
        new_events, updated_data = append_new_data(existing_data, data)

        # Vänta 30 sekunder innan nästa förfrågan
        print("Väntar 30 sekunder innan nästa kontroll...")
        time.sleep(9000)  # Väntar i 30 sekunder


if __name__ == "__main__":
    while True:
        main()
