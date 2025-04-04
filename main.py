from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "685b7c77eb87173a41254253f3eaeff8"  # 🔑 Replace with your real API key

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "weather": None})

@app.post("/forecast", response_class=HTMLResponse)
def get_weather(request: Request, city: str = Form(...)):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = {
            "city": city.title(),
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"],
        }
    else:
        weather = {"error": "City not found!"}

    return templates.TemplateResponse("index.html", {"request": request, "weather": weather})
