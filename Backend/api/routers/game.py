from fastapi import APIRouter, Depends
from pydantic import BaseModel

from language.custom_exceptions import LexerException, SyntaxException, RuntimeException
from api.business.game_service import GameService
from api.infrastructure.game_repository import GameRepository

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games")

game_service = None


@router.on_event("startup")
async def startup_event():
    global game_service
    game_repository = GameRepository()
    game_service = GameService(game_repository)


def get_game_service():
    return game_service


class GameData(BaseModel):
    username: str
    game_name: str
    code: str


class GameEvent(BaseModel):
    event_name: str
    parameters: list[int | float | str] | None = None

class ArrayData(BaseModel):
    name: str
    values: list[int | float | str]

@router.post("/")
async def create_game(game_data: GameData, game_service: GameService = Depends(get_game_service)):
    # logger.info(game_data)
    try:
        return game_service.create_game(game_data.username, game_data.game_name, game_data.code).id
    except LexerException as le:
        return {"error": f"Lexer Error: {le}"}
    except SyntaxException as se:
        return {"error": f"Syntax Error: {se}"}


@router.patch("/{id}")
async def run_event(
    id: str,
    game_event: GameEvent,
    game_service: GameService = Depends(get_game_service),
):
    # logger.info(game_event)
    try:
        return game_service.run_event(id, game_event.event_name, game_event.parameters)
    except RuntimeException as re:
        print(re)
        return {"error": f"Runtime Error: {re}"}

@router.patch("/{id}/add-array")
async def add_var(
    id: str,
    array_data: ArrayData,
    game_service: GameService = Depends(get_game_service),
):
    try:
        return game_service.add_array(id, array_data.name, array_data.values)
    except RuntimeException as re:
        print(re)
        return {"error": f"Runtime Error: {re}"}
