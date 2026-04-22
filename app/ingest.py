import requests
import os
from dotenv import load_dotenv
from app.db import get_connection   # ✅ FIXED IMPORT

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv("WEATHER_API_KEY")

print("Loaded API KEY:", API_KEY)


def fetch_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    data = response.json()

    print("API Response:", data)

    if response.status_code != 200 or "main" not in data:
        print("❌ API Error:", data)
        return None

    return data


def store_weather(data):
    if data is None:
        print("⚠️ No data to store")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO weather_data (temperature, humidity, wind_speed, city)
        VALUES (%s, %s, %s, %s)
    """, (
        data['main']['temp'],
        data['main']['humidity'],
        data['wind']['speed'],
        data['name']
    ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Data stored in database")


if __name__ == "__main__":
    data = fetch_weather()
    store_weather(data)