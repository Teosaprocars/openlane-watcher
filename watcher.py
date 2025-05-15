import requests
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("OPENLANE_EMAIL")
PASSWORD = os.getenv("OPENLANE_PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LOGIN_URL = "https://www.openlane.eu/api/authentication/login"
SEARCH_URL = "https://www.openlane.eu/api/vehicle/search"

session = requests.Session()

def login():
    resp = session.post(LOGIN_URL, json={
        "email": EMAIL,
        "password": PASSWORD
    })
    if resp.status_code == 200:
        print("✅ Přihlášení úspěšné")
    else:
        print("❌ Chyba při přihlášení:", resp.status_code, resp.text)
        raise Exception("Login failed")

def get_matching_vehicles():
    params = {
        "page": 1,
        "pageSize": 100,
        "energy": "Electric",
        "yearMin": 2019,
        "priceMax": 15000,
        "buyNow": True
    }
    resp = session.get(SEARCH_URL, params=params)
    if resp.status_code != 200:
        print("❌ Chyba při získávání vozidel")
        return []

    data = resp.json()
    vehicles = data.get("items", [])
    results = []
    for v in vehicles:
        name = f"{v.get('make')} {v.get('model')} ({v.get('year')})"
        url = f"https://www.openlane.eu/cs/vehicle/{v.get('id')}"
        price = v.get("price")
        results.append((name, url, price))
    return results

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def main():
    login()
    vehicles = get_matching_vehicles()
    for name, url, price in vehicles:
        send_telegram(f"🔔 <b>{name}</b>\n💶 Cena: {price} €\n🔗 {url}")

if __name__ == "__main__":
    main()
