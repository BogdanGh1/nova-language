from api.domain.games.game import Game
from api.domain.games.sorting_visualizer.custom import (
    get_custom_functions,
)
from language.structures import CodeRunner


class SortingVisualizaerGame(Game):
    def __init__(self, id, username: str, code_runner: CodeRunner) -> None:
        super().__init__(id, username, code_runner)
        for custom_function in get_custom_functions():
            code_runner.add_function(custom_function)
