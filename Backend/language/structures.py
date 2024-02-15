from language.nodes import Node
from language.actions import Action, PrintAction
from language.variables import Variable, VariableScope, VariableTable


class Function:
    def __init__(self, root: Node) -> None:
        self.syntax_root = root
        self.name = root.children[1].value.value

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: "CodeRunner",
        params: list | None = None,
    ):
        self.syntax_root.eval(var_table, actions, code_runner)


class PrintFunction:
    def __init__(self) -> None:
        self.name = "print"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: "CodeRunner",
        params: list,
    ):
        actions.append(PrintAction("print", str(params[0])))


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

    def run(self, name: str) -> list[Action]:
        self.actions: list[Action] = []
        self.run_function(name)
        return self.actions

    def run_function(self, name: str, params: list | None = None) -> None:
        function = self.code.get_function(name)
        self.var_table.add_var_scope(VariableScope())
        function.eval(self.var_table, self.actions, self, params)
