from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from src.api import boarding_passes
# API imports
from src.api import users
from .config import (
    CORS_ALLOWED_HOSTS,
    CORS_ALLOWED_METHODS,
    CORS_ALLOWED_HEADERS,
    CORS_ALLOW_CREDENTIALS,
)
from .db import database

app = FastAPI()

app.mount("/static", StaticFiles(directory="/opt/data/static"), name="static")
templates = Jinja2Templates(directory="/application/src/app/templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_HOSTS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOWED_METHODS,
    allow_headers=CORS_ALLOWED_HEADERS,
)

app.include_router(users.users_router)
app.include_router(boarding_passes.bp_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/{spa_wildcard}')
async def main(request: Request, spa_wildcard: str):
    return templates.TemplateResponse('index.html', context={'request': request})
