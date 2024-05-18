from mongo_beanie.models import User
from passlib.handlers.argon2 import argon2 as crypto

crypto.default_rounds = 25


async def get_user_count() -> int:
    return await User.count()


async def get_user_by_email(email: str):
    email = email.lower().strip()
    return await User.find_one(User.email == email)


async def create_user(name, email, password, profile_img_url, location) -> User:
    email = email.lower().strip()
    name = name.strip()
    password = password.strip()

    if await get_user_by_email(email):
        raise Exception(f"User with email {email} already exists")
    hash_password = crypto.encrypt(password)
    user = User(name=name, email=email, hash_password=hash_password, profile_image_url=profile_img_url,
                location=location)
    await user.save()

    return user
