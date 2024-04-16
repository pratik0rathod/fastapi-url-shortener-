# setup .env if it exist
import os

from fastapi import FastAPI
from .core.routes import shortner_route,auth_route,short_route
from .core import database
app = FastAPI(title="Url Shortner")

app.include_router(auth_route)
app.include_router(shortner_route)
app.include_router(short_route)
