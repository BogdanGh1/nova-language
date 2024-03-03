from fastapi import APIRouter, Depends
from pydantic import BaseModel

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


@router.post("/")
def create_game(
    game_data: GameData, game_service: GameService = Depends(get_game_service)
):
    # logger.info(game_data)
    return game_service.create_game(
        game_data.username, game_data.game_name, game_data.code
    ).id


@router.patch("/{id}")
def run_event(
    id: str,
    game_event: GameEvent,
    game_service: GameService = Depends(get_game_service),
):
    logger.info(game_event)
    return game_service.run_event(id, game_event.event_name, game_event.parameters)
