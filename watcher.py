import requests
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def get_matching_vehicles():
    response = requests.get("https://www.openlane.eu/api/vehicle/search", params={
        "page": 1,
        "pageSize": 100,
        "energy": "Electric",
        "yearMin": 2019,
        "priceMax": 15000,
        "buyNow": True
    })
    if response.status_code != 200:
        return []

    data = response.json()
    vehicles = data.get("items", [])
    matching = []
    for v in vehicles:
        name = v.get("make") + " " + v.get("model")
        url = f"https://www.openlane.eu/cs/vehicle/{v.get('id')}"
        matching.append((name, url))
    return matching

def main():
    current = get_matching_vehicles()
    if not current:
        return
    for name, url in current:
        send_telegram_message(f"🔔 Nové auto: <b>{name}</b>\n{url}")

if __name__ == "__main__":
    main()
