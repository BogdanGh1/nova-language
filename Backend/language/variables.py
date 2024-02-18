class Variable:
    def __init__(self, name: str, value) -> None:
        self.name = name
        self.value = value


class VariableScope:
    def __init__(self, function_flag: bool = False) -> None:
        self.variables = {}
        self.function_flag = function_flag

    def add_var(self, var_name: str) -> None:
        var = Variable(var_name, None)
        self.variables[var_name] = var

    def get_var(self, var_name: str) -> Variable | None:
        if var_name in self.variables:
            return self.variables[var_name]
        return None


class VariableTable:
    def __init__(self) -> None:
        globalScope = VariableScope()
        self.varScopes = [globalScope]

    def create_new_var_scope(self, function_flag: bool = False) -> None:
        varScope = VariableScope(function_flag)
        self.varScopes.append(varScope)

    def remove_function_var_scopes(self) -> None:
        while self.varScopes[-1].function_flag:
            self.varScopes.pop()

    def add_var(self, var_name: str) -> None:
        self.varScopes[-1].add_var(var_name)

    def add_global_var(self, var_name: str) -> None:
        self.varScopes[0].add_var(var_name)

    def add_global_var(self, var_name: VariableScope) -> None:
        self.varScopes[0].add_var(var_name)

    def pop_var_scope(self) -> None:
        self.varScopes.pop()

    def get_var(self, var_name: str) -> Variable | None:  # TODO
        for varScope in reversed(self.varScopes):
            var = varScope.get_var(var_name)
            if var is not None or varScope.function_flag:
                return var
        return None
