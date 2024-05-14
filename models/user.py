import datetime
import pydantic
import beanie
from typing import Any, Optional

import pymongo


class Location(pydantic.BaseModel):
    state: Optional[str] = "KA"
    country: Optional[str] = "India"


class User(beanie.Document):
    name: str
    email: pydantic.EmailStr
    hash_password: Optional[str]
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.utcnow)
    last_login: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.utcnow)
    profile_image_url: Optional[str]
    location: Location

    class Settings:
        name = "users"
        indexes = [
            pymongo.IndexModel(keys=[("created_date", pymongo.DESCENDING)], name="created_date_descending"),
            pymongo.IndexModel(keys=[("last_login", pymongo.DESCENDING)], name="last_login_descending"),
            pymongo.IndexModel(keys=[("email", pymongo.ASCENDING)], name="email",unique=True),
        ]
