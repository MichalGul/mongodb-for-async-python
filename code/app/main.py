import fastapi
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from api import package_api
from api import stats_api
from infrastructure import mongo_setup
from dotenv import load_dotenv



api = fastapi.FastAPI()
templates = Jinja2Templates(directory='templates')
load_dotenv(dotenv_path=".env")


def main():
    configure_routing()
    # Will not work because we try to run different asyncio loop
    # asyncio.run(mongo_setup.init_connection('pypi', 'user', 'password', 'admin'))
    uvicorn.run(api)


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name="static")
    api.include_router(package_api.router)
    api.include_router(stats_api.router)
    print("Routing configured")


@api.on_event("startup")
async def configure_db():
    MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    AUTH_SOURCE = os.getenv("AUTH_SOURCE")
    ADDRESS = os.getenv("ADDRESS")
    PORT = os.getenv("PORT")

    await mongo_setup.init_connection(ADDRESS, PORT, DATABASE_NAME, MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, AUTH_SOURCE)
    print("Connected to the MongoDB database!")


@api.get('/hello', include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse('index.html', {"name": "The app!", "request": request})


if __name__ == '__main__':
    main()
else:
    configure_routing()
