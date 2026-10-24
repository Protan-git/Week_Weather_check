from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal
from models import WeatherRecord

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/cities")
def get_cities():
    with SessionLocal() as db:
        cities = (
            db.query(WeatherRecord.city)
            .distinct()
            .order_by(WeatherRecord.city)
            .all()
        )

        return [city[0] for city in cities]


@app.get("/api/weather")
def get_weather_history(city: str):
    with SessionLocal() as db:
        records = (
            db.query(WeatherRecord)
            .filter(WeatherRecord.city == city)
            .order_by(WeatherRecord.record_date.asc())
            .all()
        )

        if not records:
            raise HTTPException(
                status_code=404,
                detail="Для этого города нет записей"
            )

        return [
            {
                "date": str(record.record_date),
                "temperature": record.temperature,
                "feels_like": record.feels_like,
                "humidity": record.humidity,
                "pressure": record.pressure,
                "wind_speed": record.wind_speed,
                "description": record.description,
            }
            for record in records
        ]