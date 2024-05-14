import asyncio
import datetime

import motor.motor_asyncio
import pydantic

import beanie
from typing import Optional


class Location(pydantic.BaseModel):
    city: str
    state: Optional[str]
    country: str


class User(beanie.Document):
    name: str
    email: str
    password_hash: Optional[str] = None
    is_active: bool = True
    created_at: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    last_login: Optional[datetime.datetime] = pydantic.Field(default_factory=datetime.datetime.now)

    location: Location = pydantic.Field(default_factory=Location)

    class Settings:
        name = "users"
        indexes = [
            "location.country"
        ]


async def create_new_user():
    user_count = await User.count()
    if user_count > 0:
        print(f"User already have {user_count} users in the database. Exiting...")
        return
    print("Creating a New User...")
    loc = Location(city="Bengaluru", state="KA", country="IN")
    user = User(name="Karthik", email="karthik@veeville.com", location=loc)
    print(f'User before saving to db{user}')

    await user.save()

    print(f'User after saving to db{user}')


async def init_connection(db_name: str):
    conn_str = f'mongodb://localhost:27017/{db_name}'
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)

    await beanie.init_beanie(database=client[db_name], document_models=[User])

    print(f'Connected to {db_name}')


async def inser_multiple_users():
    """Inserts multiple users"""
    u1 = User(name="Rajesh", email="r@veeville.com", location=Location(city="Bengaluru", state="KA", country="IN"))
    u2 = User(name="Ramesh", email="ram@veeville.com", location=Location(city="Mumbai", state="MH", country="IN"))
    u3 = User(name="Hamsa", email="ham@veeville.com", location=Location(city="Lille", state="Nord", country="FR"))

    await User.insert_many([u1, u2, u3])
    print("Inserted multiple users")


async def find_all_users():
    # users:list[User] = await User.find(User.location.country == "IN").sort(-User.name).to_list()
    user_query = User.find(User.location.country == "IN").sort(-User.name)

    async for user in user_query:
        user.password_hash = "a"
        await user.save()


# noinspection PyTypeChecker
async def find_user_one():
    users: list[User] = await User \
        .find(User.location.country == "IN") \
        .find(User.name == "Karthik") \
        .sort(-User.name) \
        .to_list()

    for u in users:
        print(u)


async def main():
    await init_connection('beanie_quickstart')
    # await create_new_user()
    await inser_multiple_users()
    # await find_all_users()
    # await find_user_one()
    pass


if __name__ == '__main__':
    asyncio.run(main())
