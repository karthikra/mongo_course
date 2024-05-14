import pydantic


class StatsModel(pydantic.BaseModel):
    package_count: int
    release_count: int
    user_count: int