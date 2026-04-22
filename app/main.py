from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()

# 🚀 Create FastAPI app
app = FastAPI()

# 🔑 Get API key from .env or Render
API_KEY = os.getenv("WEATHER_API_KEY")


@app.get("/")
def home():
    return {"message": "Weather API is running 🚀"}


@app.get("/weather/{city}")
def get_weather(city: str):

    # 🧠 Clean input
    city = city.strip().title()

    # 🌍 API request
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # ❌ Handle invalid city
    if response.status_code != 200 or "main" not in data:
        return {"error": "City not found"}

    # ✅ Return clean data
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "timezone": data["timezone"],
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"]
    }