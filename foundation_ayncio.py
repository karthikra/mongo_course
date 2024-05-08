import httpx
import asyncio
import datetime

urls = [
    'https://weather.talkpython.fm/api/weather?city=New York&state=NY&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Los Angeles&state=CA&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Chicago&state=IL&Country=US&units=imperial'
    'https://weather.talkpython.fm/api/weather?city=Houston&state=TX&country=US&units=imperial'
    'https://weather.talkpython.fm/api/weather?city=Phoenix&state=AZ&country=US&units=imperial'
    'https://weather.talkpython.fm/api/weather?city=Philadelphia&state=PA&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=San Antonio&state=TX&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=San Diego&state=CA&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Dallas&state=X&country=US&units=imperial'
    'https://weather.talkpython.fm/api/weather?city=San Jose&state=CA&country=US&units=imperial'
]


async def get_weather(url):
    print(f"Getting weather from {url}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

    return resp.json()

def show_report(report):
    print(report["forecast"],report["location"])

async def main():
    t0 = datetime.datetime.now()
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_weather(url)))
    for task in tasks:

        report = await task
        show_report(report)

    dt = datetime.datetime.now() - t0
    print(f"Done in {dt.total_seconds():.2f} sec")

if __name__ == '__main__':
    asyncio.run( main())
