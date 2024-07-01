from language.actions import Action
from language.structures import VariableTable, CodeRunner
from language.variables import Array, Variable


class SetCellAction(Action):
    def __init__(self, action_type: str, row: int, col: int, value: str) -> None:
        super().__init__(action_type)
        self.row = row
        self.col = col
        self.value = value

    def __str__(self) -> str:
        return super().__str__() + " " + str(self.row) + " " + str(self.col) + " " + self.value

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict["row"] = self.row
        dict["col"] = self.col
        dict["value"] = self.value
        return dict


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
        var = var_table.get_var("__board")
        var.add_value([params[0],params[1]], str(params[2]))
        actions.append(SetCellAction("setCell", params[0], params[1], str(params[2])))

# class GetCellFunction:
#     def __init__(self) -> None:
#         self.name = "getCell"

#     def eval(
#         self,
#         var_table: VariableTable,
#         actions: list[Action],
#         code_runner: CodeRunner,
#         params: list,
#     ):
#         board = var_table.get_var("__board")
#         return board.array_dict[(params[0], params[1])]

def get_custom_functions():
    return [SetCellFunction()]


def get_custom_variables():
    return [Array("__board", [20,20])]
