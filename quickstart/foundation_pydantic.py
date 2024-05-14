from pydantic import BaseModel


class Weather(BaseModel):
    description: str
    category: str


class Wind(BaseModel):
    speed: float
    deg: float


class Forecast(BaseModel):
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    low: float
    high: float


class Location(BaseModel):
    city: str
    state: str
    country: str


class RateLimiting(BaseModel):
    unique_lookups_remaining: int
    lookup_reset_window: str


class WeatherModel(BaseModel):
    weather: Weather
    wind: Wind
    units: str
    forecast: Forecast
    location: Location
    rate_limiting: RateLimiting


def main():
    data = {
        "weather": {
            "description": "overcast clouds",
            "category": "Clouds"
        },
        "wind": {
            "speed": 2.06,
            "deg": 170
        },
        "units": "metric",
        "forecast": {
            "temp": 28.8,
            "feels_like": 31.46,
            "pressure": 1014,
            "humidity": 65,
            "low": 27.9,
            "high": 28.8
        },
        "location": {
            "city": "Bengaluru",
            "state": "KA",
            "country": "IN"
        },
        "rate_limiting": {
            "unique_lookups_remaining": 47,
            "lookup_reset_window": "1 hour"
        }
    }
    report = WeatherModel(**data)
    print(report.forecast)


if __name__ == '__main__':
    main()
