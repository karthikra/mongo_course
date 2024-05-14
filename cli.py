import asyncio
from typing import Optional

from infrastructure import mongo_setup
from models.user import Location
from services import package_service, user_service


def print_header():
    print("----------------------------")
    print("      CLI APPLICATION v1.0")
    print("----------------------------")
    print()


async def summary():
    package_count = await package_service.get_package_count()
    release_count = await package_service.get_release_count()
    user_count = await user_service.get_user_count()

    print('Pypi Package Stats')
    print(f'Packages: {package_count:,}')
    print(f'Releases: {release_count:,}')
    print(f'Users: {user_count:,}')
    print()


async def recently_updated_package():
    packages = await package_service.recently_updated_package()
    for package in packages:
        print(
            f"Package Name :{package.id} ({package.last_updated.date().isoformat()}) with , Package Summary: {package.summary}")


async def search_for_package():
    print("Lets find some packages")
    name = input("Enter the package name: ").strip().lower()
    package = await package_service.search_package_by_name(name)

    if package:
        print(
            f"Package Name: {package.id} update on {package.last_updated.date().isoformat()} with {len(package.releases)} releases")
    else:
        print(f"Package {name} not found")

    print("No lets find some packages with a certain release")
    text = input("Enter the version text in the format 1.2.3: ")
    parts = text.split('.')
    major = int(parts[0])
    minor = int(parts[1])
    build = int(parts[2])

    package_count = await package_service.search_package_with_release(major, minor, build)
    print(f"We found  {package_count} packages with packages versions {major}.{minor}.{build}")

    print()


async def create_release():
    print("Lets create a new release")
    package_name = input("Enter the package name: ").strip().lower()
    package = await package_service.search_package_by_name(package_name)
    if not package:
        print(f"Package {package_name} not found")
        return
    version_text = input("Enter the version text in the format 1.2.3: ")
    v_parts = (version_text.strip().split('.'))
    major, minor, build = int(v_parts[0]), int(v_parts[1]), int(v_parts[2])

    size = int(input("Enter the size of the release: "))
    comment = input("Enter the comment for the release: ")
    url = input("Enter the URL for the release or enter - to skip : ") or None

    await package_service.create_release(package_name, major, minor, build, size, comment, url)
    print(f"Release created successfully for {package_name} with version {version_text}")
    print()


async def create_user():
    print("Lets create a new user")
    name = input("Enter the name of the user: ").strip()
    email = input("Enter the email of the user: ").strip()

    if await user_service.get_user_by_email(email):
        print(f"User with email {email} already exists so cancelling the creation")
        return

    password = input("Enter the password for the user: ").strip()
    state: Optional[str] = str(input("Enter the state for the user: ")).strip() or None
    country: Optional[str] = str(input("Enter the country for the user: ")).strip() or None
    profile_img_url: Optional[str] = str(input("Enter the profile image URL for the user: ")).strip() or None


    location = Location(state=state, country=country)

    user = await user_service.create_user(name, email, password, profile_img_url, location)
    print(f"User {user.name} created successfully with user id {user.id}")


async def main():
    print_header()
    await mongo_setup.init_connection('pypi')
    print()
    await summary()
    while True:
        print("[s] Show summary statistics")
        print("[f] Search the database for packages")
        print("[p] Most recently updated packages")
        print("[u] Create a new user")
        print("[r] Create a release")
        print("[x] Exit program")
        resp = input("Enter the character for your command: ").strip().lower()
        print('-' * 40)

        match resp:
            case 's':
                await summary()
            case 'f':
                await search_for_package()
            case 'p':
                await recently_updated_package()
            case 'u':
                await create_user()
            case 'r':
                await create_release()
            case 'x':
                break
            case _:
                print("Invalid command. Please try again.")


if __name__ == '__main__':
    asyncio.run(main())
