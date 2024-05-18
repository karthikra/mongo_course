import fastapi
import uvicorn

from fastapi.templating import Jinja2Templates

from contextlib import asynccontextmanager


from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from mongo_beanie.api import package_api, stats_api
from mongo_beanie.infrastructure import mongo_setup


# this is a context manager that will setup the database connection
@asynccontextmanager
async def setup(api: fastapi.FastAPI):
    await mongo_setup.init_db('pypi')
    yield


api = fastapi.FastAPI(lifespan=setup)
templates = Jinja2Templates(directory="templates")


@api.get("/", include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"name": "THE BIG APP", "request": request})


def configure_routing():
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(package_api.router)
    api.include_router(stats_api.router)


# @api.on_event("startup")
# async def configure_db():
#     await mongo_setup.init_connection('pypi')


def main():
    configure_routing()
    uvicorn.run(api, host='localhost', port=8000)
    pass


if __name__ == '__main__':
    main()
else:
    configure_routing()
