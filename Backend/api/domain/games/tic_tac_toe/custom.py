from language.actions import Action
from language.structures import VariableTable, CodeRunner
from language.variables import Array, Variable


class SetScoreAction(Action):
    def __init__(self, action_type: str, value: str) -> None:
        super().__init__(action_type)
        self.value = value

    def __str__(self) -> str:
        return super().__str__() + " " + self.value

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict["value"] = self.value
        return dict


class SetCellAction(Action):
    def __init__(self, action_type: str, index: int, value: str) -> None:
        super().__init__(action_type)
        self.index = index
        self.value = value

    def __str__(self) -> str:
        return super().__str__() + " " + str(self.index) + " " + self.value

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict["index"] = self.index
        dict["value"] = self.value
        return dict


class SetScoreXFunction:
    def __init__(self) -> None:
        self.name = "setScoreX"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: CodeRunner,
        params: list,
    ):
        var = var_table.get_var("scoreX")
        var.value = params[0]
        actions.append(SetScoreAction("setScoreX", str(params[0])))


class SetScoreOFunction:
    def __init__(self) -> None:
        self.name = "setScoreO"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: CodeRunner,
        params: list,
    ):
        var = var_table.get_var("scoreO")
        var.value = params[0]
        actions.append(SetScoreAction("setScoreO", str(params[0])))


class SetCellFunction:
    def __init__(self) -> None:
        self.name = "setCell"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: CodeRunner,
        params: list,
    ):
        var = var_table.get_var("board")
        var.add_value([params[0]], str(params[1]))
        actions.append(SetCellAction("setCell", params[0], str(params[1])))


def get_custom_functions():
    return [SetScoreXFunction(), SetScoreOFunction(), SetCellFunction()]


def get_custom_variables():
    return [Array("board", [9]), Variable("scoreX", 0), Variable("scoreO", 0)]
