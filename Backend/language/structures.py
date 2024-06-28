from language.nodes import Node
from language.actions import Action, PrintAction
from language.variables import VariableTable
from language.lexer import get_functions_atoms
from language.parser import build_syntax_tree

import random
import time
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
        ret = self.syntax_root.eval(var_table, actions, code_runner, params)
        var_table.remove_function_var_scopes()
        return ret


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

class RandomFunction:
    def __init__(self) -> None:
        self.name = "random"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: "CodeRunner",
        params: list,
    ):
        current_time = time.time()
        random.seed(current_time)
        return random.randint(params[0], params[1])

class IntFunction:
    def __init__(self) -> None:
        self.name = "int"

    def eval(
        self,
        var_table: VariableTable,
        actions: list[Action],
        code_runner: "CodeRunner",
        params: list,
    ):
        return int(params[0])

def get_base_functions() -> list[Function]:
    return [PrintFunction(), RandomFunction(),IntFunction()]


class SourceCode:
    def __init__(self, text: str) -> None:
        self.functions = get_base_functions()
        functions_atoms = get_functions_atoms(text)
        for function_atoms in functions_atoms:
            root = build_syntax_tree(function_atoms)
            self.functions.append(Function(root))

    def add_function(self, function) -> None:
        self.functions.append(function)

    def get_function(self, name: str) -> Function:
        for function in self.functions:
            if function.name == name:
                return function


class CodeRunner:
    def __init__(self, code: SourceCode) -> None:
        self.code = code
        self.var_table = VariableTable()

    def run(self, name: str, params: list | None = None) -> list[Action]:
        self.actions: list[Action] = []
        self.run_function(name, params)
        return self.actions

    def add_function(self, function) -> None:
        self.code.add_function(function)

    def add_custom_global(self, var) -> None:
        self.var_table.add_global_any(var)

    def run_function(self, name: str, params: list | None = None) -> list[Action]:
        function = self.code.get_function(name)
        return function.eval(self.var_table, self.actions, self, params)
