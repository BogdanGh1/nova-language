from api.domain.entity import Entity
from language.structures import CodeRunner


class Game(Entity):
    def __init__(self, id, username: str, code_runner: CodeRunner) -> None:
        super().__init__(id)
        self.username = username
        self.code_runner = code_runner

    def run_function(self, function_name: str) -> None:
        self.code_runner.run_function(function_name)
