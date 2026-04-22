from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI()

# CORS (allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve index.html
@app.get("/")
def home():
    return FileResponse("index.html")


# ✅ Weather API
@app.get("/weather/{city}")
def get_weather(city: str):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "main" not in data:
        return {"error": "City not found"}

    return {
    "temperature": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "wind_speed": data["wind"]["speed"],
    "city": data["name"],
    "timestamp": data["dt"],
    "condition": data["weather"][0]["main"],
    "description": data["weather"][0]["description"],
    "feels_like": data["main"]["feels_like"],
    "pressure": data["main"]["pressure"],
    "timezone": data["timezone"]   # 🔥 ADD THIS LINE
}