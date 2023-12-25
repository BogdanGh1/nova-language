# main.py

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import logging

logging.basicConfig(level=logging.INFO)


app = FastAPI()

logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class Code(BaseModel):
    code: str


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.post("/code")
async def run_code(code: Code):
    logger.info(code)
    return {"pula": "pizda"}
