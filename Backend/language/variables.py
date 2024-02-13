from dataclasses import dataclass


@dataclass
class Variable:
    name: str
    var_type: str
    value: int | str


class VariableScope:
    def __init__(self) -> None:
        self.variables = {}

    def add_var(self, v: Variable) -> None:
        self.variables[v.name] = v

    def get_var(self, var_name: str) -> Variable | None:
        if var_name in self.variables:
            return self.variables[var_name]
        return None


class VariableTable:
    def __init__(self, varScope: VariableScope) -> None:
        self.varScopes = [varScope]

    def add_var_scope(self, varScope: VariableScope) -> None:
        self.varScopes.append(varScope)

    def add_var(self, var_name: VariableScope) -> None:
        self.varScopes[-1].add_var(var_name)

    def add_global_var(self, var_name: VariableScope) -> None:
        self.varScopes[0].add_var(var_name)

    def pop_var_scope(self) -> None:
        self.varScopes.pop()

    def get_var(self, var_name: str) -> Variable | None:  # TODO
        for varScope in reversed(self.varScopes):
            var = varScope.get_var(var_name)
            if var is not None:
                return var
        return None
