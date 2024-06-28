from api.domain.games.game import Game
from api.domain.games.tic_tac_toe import TicTacToeGame
from api.domain.games.minesweeper import MinesweeperGame
from api.domain.games.sorting_visualizer import SortingVisualizaerGame
from language.structures import SourceCode, CodeRunner
import uuid


def create_game(name: str, username: str, text: str) -> Game:
    id = uuid.uuid4()
    source_code = SourceCode(text)
    code_runner = CodeRunner(source_code)
    match name:
        case "tictactoe":
            return TicTacToeGame(id, username, code_runner)
        case "minesweeper":
            return MinesweeperGame(id, username, code_runner)
        case "sorting-visualizer":
            return SortingVisualizaerGame(id, username, code_runner)
