from language.nodes import Node
from language.actions import Action, PrintAction
from language.variables import VariableTable
from language.lexer import get_functions_atoms
from language.parser import build_syntax_tree


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
        var_table.create_new_var_scope(True)
        self.syntax_root.eval(var_table, actions, code_runner)
        var_table.remove_function_var_scopes()


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


def get_base_functions() -> list[Function]:
    return [PrintFunction()]


class SourceCode:
    def __init__(self, text: str) -> None:
        self.functions = get_base_functions()
        functions_atoms = get_functions_atoms(text)
        for function_atoms in functions_atoms:
            root = build_syntax_tree(function_atoms)
            self.functions.append(Function(root))

    def get_function(self, name: str) -> Function:
        for function in self.functions:
            if function.name == name:
                return function


class CodeRunner:
    def __init__(self, code: SourceCode) -> None:
        self.code = code
        self.var_table = VariableTable()

    def run(self, name: str) -> list[Action]:
        self.actions: list[Action] = []
        self.run_function(name)
        return self.actions

    def run_function(self, name: str, params: list | None = None) -> None:
        function = self.code.get_function(name)
        function.eval(self.var_table, self.actions, self, params)
