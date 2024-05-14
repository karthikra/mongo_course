import datetime

import pydantic


class RecentPackage(pydantic.BaseModel):
    package_name: str
    last_updated: datetime.datetime


class RecentPackageModel(pydantic.BaseModel):
    count: int
    packages: list[RecentPackage]