from language.nodes import Node
from language.actions import Action
from language.variables import Variable, VariableScope, VariableTable


class Function:
    def __init__(self, root: Node, params: list[Variable]) -> None:
        self.syntax_root = root
        self.params = params
        self.name = root.children[1].value

    def eval(self, var_table: VariableTable, actions: list[Action]):
        self.syntax_root.eval(var_table, actions)


class SourceCode:
    def __init__(self, functions: list[Function]) -> None:
        self.functions = functions

    def get_function(self, name: str) -> Function:
        for function in self.functions:
            if function.name == name:
                return function


class CodeRunner:
    def __init__(self, code: SourceCode) -> None:
        self.code = code
        self.globalScope = VariableScope()
        self.var_table = VariableTable(self.globalScope)

    def runFunction(self, name: str, params: list[str] | None) -> None:
        actions: list[Action] = []
        function = self.code.get_function(name)
        self.var_table.add_var_scope(VariableScope())
        function.eval(self.var_table, actions)
