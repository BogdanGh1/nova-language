from language.actions import Action
from language.structures import VariableTable, CodeRunner
from language.variables import Array, Variable

class GetSizeFunction:
    def __init__(self) -> None:
        self.name = "getSize"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: CodeRunner,
        params: list,
    ):
        array = var_table.get_var("array")
        return array.sizes[0]

class GetValueFunction:
    def __init__(self) -> None:
        self.name = "getValue"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: CodeRunner,
        params: list,
    ):
        array = var_table.get_var("array")
        return array.array_dict[(params[0],)]
    
class SwapAction(Action):
    def __init__(self, action_type: str, i1: int, i2: int, time: int) -> None:
        super().__init__(action_type)
        self.i1 = i1
        self.i2 = i2
        self.time = time

    def __str__(self) -> str:
        return super().__str__() + " " + str(self.i1) + " " + str(self.i2) + " " + str(self.time)

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict["i1"] = self.i1
        dict["i2"] = self.i2
        dict["time"] = self.time
        return dict

class SwapFunction:
    def __init__(self) -> None:
        self.name = "swap"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: CodeRunner,
        params: list,
    ):
        array = var_table.get_var("array")
        ad = array.array_dict
        ad[(params[0],)], ad[(params[1],)] = ad[(params[1],)], ad[(params[0],)]
        actions.append(SwapAction("swap", params[0], params[1], params[2]))
    
class SetValueAction(Action):
    def __init__(self, action_type: str, index: int, value: int, time: int) -> None:
        super().__init__(action_type)
        self.index = index
        self.value = value
        self.time = time

    def __str__(self) -> str:
        return super().__str__() + " " + str(self.index) + " " + str(self.value) + " " + str(self.time)

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict["index"] = self.index
        dict["value"] = self.value
        dict["time"] = self.time
        return dict
    
class SetValueFunction:
    def __init__(self) -> None:
        self.name = "setValue"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: CodeRunner,
        params: list,
    ):
        array = var_table.get_var("array")
        array.array_dict[(params[0],)] = params[1]
        actions.append(SetValueAction("setValue", params[0], params[1],params[2]))


def get_custom_functions():
    return [GetSizeFunction(), GetValueFunction(), SwapFunction(), SetValueFunction()]