from api.domain.games.game import Game
from api.infrastructure.game_repository import GameRepository
from api.domain.games.factory import create_game
import uuid


class GameService:
    def __init__(self, game_repository: GameRepository) -> None:
        self.game_repository = game_repository

    def create_game(self, username: str, game_name: str, code: str) -> Game:
        game = create_game(game_name, username, code)
        return self.game_repository.add(game)

    def run_event(self, game_id, event_name, parameters) -> list[dict]:
        game: Game = self.game_repository.find_by_id(uuid.UUID(game_id))
        actions = game.run_function(event_name, parameters)
        return [action.to_dict() for action in actions]
    
    def add_array(self, game_id, name, array_values):
        game: Game = self.game_repository.find_by_id(uuid.UUID(game_id))
        game.code_runner.var_table.add_global_array(name,[len(array_values)])
        array = game.code_runner.var_table.get_var(name)
        for i, val in enumerate(array_values):
            array.add_value([i], val)