from __future__ import annotations

import datetime
from typing import Any, List, Optional

import beanie
import bson

import pydantic
import pymongo


class Release(pydantic.BaseModel):
    major_ver: int
    minor_ver: int
    build_ver: int
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.utcnow)
    comment: Optional[str]
    url: Optional[str]
    size: int


class Package(beanie.Document):
    id: str
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.utcnow)
    last_updated: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.utcnow)
    summary: str
    description: str
    home_page: Optional[str]
    docs_url: Optional[str]
    package_url: Optional[str]
    author_name: Optional[str]
    author_email: Optional[str]
    license: Optional[str]
    releases: list[Release]
    maintainer_ids: list[beanie.PydanticObjectId]

    class Settings:
        name = "packages"
        indexes = [
            pymongo.IndexModel([("last_updated", pymongo.DESCENDING)], name='last_updated_descending'),
            pymongo.IndexModel([("created_date", pymongo.ASCENDING)], name='created_date_ascending'),
            pymongo.IndexModel([("last_updates", pymongo.DESCENDING)], name='created_date_descending'),
            pymongo.IndexModel([("author_email", pymongo.DESCENDING)], name='author_email_descending'),
            pymongo.IndexModel([("releases.created_date", pymongo.ASCENDING)], name='releases_created_date_ascending'),

            pymongo.IndexModel([("releases.major_ver", pymongo.ASCENDING)], name='releases_major_ver'),
            pymongo.IndexModel([("releases.minor_ver", pymongo.ASCENDING)], name='releases_minor_ver'),
            pymongo.IndexModel([("releases.build_ver", pymongo.ASCENDING)], name='releases_build_ver'),

            pymongo.IndexModel([
                ("releases.major_ver", pymongo.ASCENDING),
                ("releases.minor_ver", pymongo.ASCENDING),
                ("releases.build_ver", pymongo.ASCENDING)
            ],
                name='releases_ver_ascending'),

        ]


class PackageTopLevel(pydantic.BaseModel):
    id: str
    last_updated: datetime.datetime
    summary: str

    class Settings:
        projection = {
            "id": "$_id",
            "last_updated": "$last_updated",
            "summary": "$summary"
        }
