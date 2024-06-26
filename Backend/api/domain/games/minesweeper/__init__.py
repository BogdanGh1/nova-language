from api.domain.games.game import Game
from api.domain.games.minesweeper.custom import (
    get_custom_functions,
    get_custom_variables,
)
from language.structures import CodeRunner


class MinesweeperGame(Game):
    def __init__(self, id, username: str, code_runner: CodeRunner) -> None:
        super().__init__(id, username, code_runner)
        for custom_function in get_custom_functions():
            code_runner.add_function(custom_function)
        for custom_variable in get_custom_variables():
            code_runner.add_custom_global(custom_variable)