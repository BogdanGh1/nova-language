from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from api.routers.game import router as game_router
from api.routers.code import router as code_router
from api.routers.user import router as user_router

import logging

logging.basicConfig(level=logging.INFO)

import sys

sys.setrecursionlimit(20000)

app = FastAPI()

app.include_router(game_router)
app.include_router(code_router)
app.include_router(user_router)

logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


