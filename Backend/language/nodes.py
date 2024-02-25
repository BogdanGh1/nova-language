from language.actions import Action
from language.variables import VariableTable
from language.utils import Atom


class Return:
    pass


class Node:
    def __init__(self, name: str = None, value=None) -> None:
        self.name = name
        self.value = value
        self.children: list[Node] = []

    def eval(self):
        pass

    def add_child(self, node: "Node") -> None:
        self.children.append(node)

    def get_size(self) -> int:
        if self.children == []:
            return 1
        s = 1
        for child in self.children:
            s += child.get_size()
        return s

    def find_next_nonterminal_leaf(self):
        if self.children == []:
            if self.name is not None:
                return self
            return None
        for child in self.children:
            r = child.find_next_nonterminal_leaf()
            if r is not None:
                return r
        return None

    def build_dict(self):
        if self.value is not None:
            if isinstance(self.value, Atom):
                return self.value.value
            return self.value
        d = {}
        d[self.name] = []
        for child in self.children:
            d[self.name].append(child.build_dict())
        return d


class Function_Node(Node):
    def eval(
        self, var_table: VariableTable, actions: list[Action], code_runner, params
    ):
        id_list = self.children[3].eval(var_table, actions, code_runner)
        for index, id in enumerate(id_list):
            var_table.add_var(id[0].value)
            var = var_table.get_var(id[0].value)
            var.value = params[index]
        return self.children[6].eval(var_table, actions, code_runner)


class Instruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        return self.children[0].eval(var_table, actions, code_runner)


class Instructions_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if len(self.children) == 2 and isinstance(self.children[1], Instructions_Node):
            ret = self.children[0].eval(var_table, actions, code_runner)
            if ret is not None:
                return ret
            ret = self.children[1].eval(var_table, actions, code_runner)
            return ret


class DefineInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        id_list = self.children[1].eval(var_table, actions, code_runner)
        for id, value in id_list:
            var_table.add_var(id.value)
            if id is not None:
                var = var_table.get_var(id.value)
                var.value = value


class DefineGlobalInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        id_list = self.children[2].eval(var_table, actions, code_runner)
        for id, value in id_list:
            var_table.add_global_var(id.value)
            if id is not None:
                var = var_table.get_var(id.value)
                var.value = value


class DefineArrayInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        id_list = self.children[2].eval(var_table, actions, code_runner)
        indexes = self.children[1].eval(var_table, actions, code_runner)
        for id, _ in id_list:
            var_table.add_array(id.value, indexes)


class DefineGlobalArrayInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        id_list = self.children[3].eval(var_table, actions, code_runner)
        indexes = self.children[2].eval(var_table, actions, code_runner)
        for id, _ in id_list:
            var_table.add_global_array(id.value, indexes)


class ArrayValue_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        indexes = self.children[1].eval(var_table, actions, code_runner)
        array = var_table.get_var(self.children[0].value.value)
        return array.get_value(indexes)


class ArrayRef_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        indexes = self.children[1].eval(var_table, actions, code_runner)
        return var_table.get_var(self.children[0].value.value), indexes


class ArrayIndexes_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value == "#":
            return []
        indexes = self.children[3].eval(var_table, actions, code_runner)
        index = self.children[1].eval(var_table, actions, code_runner)
        indexes.insert(0, index)
        return indexes


class AttributionInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if isinstance(self.children[0], ArrayRef_Node):
            array, indexes = self.children[0].eval(var_table, actions, code_runner)
            value = self.children[2].eval(var_table, actions, code_runner)
            array.add_value(indexes, value)
        else:
            var = var_table.get_var(self.children[0].value.value)
            if var is None:
                return
            var.value = self.children[2].eval(var_table, actions, code_runner)


class FunctionCallInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        return self.children[0].eval(var_table, actions, code_runner)


class ReturnInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        return self.children[1].eval(var_table, actions, code_runner)


class IfInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        cond = self.children[2].eval(var_table, actions, code_runner)
        if cond:
            var_table.create_new_var_scope()
            ret = self.children[5].eval(var_table, actions, code_runner)
            var_table.pop_var_scope()
            return ret
        else:
            var_table.create_new_var_scope()
            ret = self.children[7].eval(var_table, actions, code_runner)
            var_table.pop_var_scope()
            return ret


class Else_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value != "#":
            return self.children[2].eval(var_table, actions, code_runner)


class WhileInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        cond = self.children[2].eval(var_table, actions, code_runner)
        while cond:
            var_table.create_new_var_scope()
            ret = self.children[5].eval(var_table, actions, code_runner)
            var_table.pop_var_scope()
            if ret is not None:
                return ret
            cond = self.children[2].eval(var_table, actions, code_runner)


class For_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        var_table.create_new_var_scope()
        self.children[2].eval(var_table, actions, code_runner)
        cond = self.children[3].eval(var_table, actions, code_runner)
        while cond:
            var_table.create_new_var_scope()
            ret = self.children[8].eval(var_table, actions, code_runner)
            var_table.pop_var_scope()
            if ret is not None:
                var_table.pop_var_scope()
                return ret
            self.children[5].eval(var_table, actions, code_runner)
            cond = self.children[3].eval(var_table, actions, code_runner)
        var_table.pop_var_scope()


class Increment_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        var = var_table.get_var(self.children[0].value.value)
        if var is None:
            return
        if isinstance(self.children[0], ArrayRef_Node):
            array, indexes = self.children[0].eval(var_table, actions, code_runner)
            value = self.children[2].eval(var_table, actions, code_runner)
            array.add_value(indexes, value)
        else:
            var.value = self.children[2].eval(var_table, actions, code_runner)


class Condition_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        t1 = self.children[0].eval(var_table, actions, code_runner)
        t2 = self.children[1].eval(var_table, actions, code_runner)
        if t2 is None:
            return t1
        return t1 and t2


class C1_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value == "#":
            return None
        t1 = self.children[1].eval(var_table, actions, code_runner)
        t2 = self.children[2].eval(var_table, actions, code_runner)
        if t2 is None:
            return t1
        return t1 and t2


class AndTerm_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        t1 = self.children[0].eval(var_table, actions, code_runner)
        t2 = self.children[1].eval(var_table, actions, code_runner)
        if t2 is None:
            return t1
        return t1 or t2


class AndTerm1_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value == "#":
            return None
        t1 = self.children[1].eval(var_table, actions, code_runner)
        t2 = self.children[2].eval(var_table, actions, code_runner)
        if t2 is None:
            return t1
        return t1 or t2


class OrTerm_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        t1 = self.children[0].eval(var_table, actions, code_runner)
        rel, t2 = self.children[1].eval(var_table, actions, code_runner)
        match rel:
            case "==":
                return t1 == t2
            case "!=":
                return t1 != t2
            case "<=":
                return t1 <= t2
            case ">=":
                return t1 >= t2
            case "<":
                return t1 < t2
            case ">":
                return t1 > t2


class RelValue_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        return self.children[0].value, self.children[1].eval(
            var_table, actions, code_runner
        )


class ReturnValue_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value != "#":
            return self.children[0].eval(var_table, actions, code_runner)
        else:
            return Return()


class Id_List_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value != "#":
            id_list = self.children[2].eval(var_table, actions, code_runner)
            value = self.children[1].eval(var_table, actions, code_runner)
            id_list.insert(0, (self.children[0].value, value))
            return id_list
        else:
            return []


class Id_List1_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value != "#":
            id_list = self.children[3].eval(var_table, actions, code_runner)
            value = self.children[2].eval(var_table, actions, code_runner)
            id_list.insert(0, (self.children[1].value, value))
            return id_list
        else:
            return []


class InitialValue_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value != "#":
            return self.children[1].eval(var_table, actions, code_runner)


class Expression_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        t1 = self.children[0].eval(var_table, actions, code_runner)
        t2 = self.children[1].eval(var_table, actions, code_runner)
        if t2 is None:
            return t1
        return t1 + t2


class E1_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value == "#":
            return None
        t1 = self.children[1].eval(var_table, actions, code_runner)
        t2 = self.children[2].eval(var_table, actions, code_runner)
        if t2 is None:
            if self.children[0].value == "+":
                return t1
            elif self.children[0].value == "-":
                return -t1
        if self.children[0].value == "+":
            return t2 + t1
        elif self.children[0].value == "-":
            return t2 - t1
        else:
            return None


class T_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        t1 = self.children[0].eval(var_table, actions, code_runner)
        t2 = self.children[1].eval(var_table, actions, code_runner)
        if t2 is None:
            return t1
        return t1 * t2


class T1_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value == "#":
            return None
        t1 = self.children[1].eval(var_table, actions, code_runner)
        t2 = self.children[2].eval(var_table, actions, code_runner)
        if t2 is None:
            if self.children[0].value == "*":
                return t1
            elif self.children[0].value == "/":
                return 1 / t1
        if self.children[0].value == "*":
            return t2 * t1
        elif self.children[0].value == "/":
            return t2 / t1
        else:
            return None


class F_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value == "(":
            return self.children[1].eval(var_table, actions, code_runner)
        elif (
            isinstance(self.children[0].value, Atom)
            and self.children[0].value.type == "id"
        ):
            return var_table.get_var(self.children[0].value.value).value
        elif (
            isinstance(self.children[0].value, Atom)
            and self.children[0].value.type == "const"
        ):
            return self.children[0].value.value
        else:
            return self.children[0].eval(var_table, actions, code_runner)


class FunctionCall_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        parameters = self.children[2].eval(var_table, actions, code_runner)
        return code_runner.run_function(self.children[0].value.value, parameters)


class Parameters_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value == "#":
            return []
        parameters = self.children[1].eval(var_table, actions, code_runner)
        parameter = self.children[0].eval(var_table, actions, code_runner)
        parameters.insert(0, parameter)
        return parameters


class Parameters1_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action], code_runner):
        if self.children[0].value == "#":
            return []
        parameters = self.children[2].eval(var_table, actions, code_runner)
        parameter = self.children[1].eval(var_table, actions, code_runner)
        parameters.insert(0, parameter)
        return parameters


def create_node(name, value=None):
    match name:
        case "Function":
            return Function_Node(name=name, value=value)
        case "Id_List":
            return Id_List_Node(name=name, value=value)
        case "Id_List1":
            return Id_List1_Node(name=name, value=value)
        case "Instruction":
            return Instruction_Node(name=name, value=value)
        case "Instructions":
            return Instructions_Node(name=name, value=value)
        case "DefineInstruction":
            return DefineInstruction_Node(name=name, value=value)
        case "DefineGlobalInstruction":
            return DefineGlobalInstruction_Node(name=name, value=value)
        case "AttributionInstruction":
            return AttributionInstruction_Node(name=name, value=value)
        case "FunctionCallInstruction":
            return FunctionCallInstruction_Node(name=name, value=value)
        case "Expression":
            return Expression_Node(name=name, value=value)
        case "E1":
            return E1_Node(name=name, value=value)
        case "T":
            return T_Node(name=name, value=value)
        case "T1":
            return T1_Node(name=name, value=value)
        case "F":
            return F_Node(name=name, value=value)
        case "FunctionCall":
            return FunctionCall_Node(name=name, value=value)
        case "Parameters":
            return Parameters_Node(name=name, value=value)
        case "Parameters1":
            return Parameters1_Node(name=name, value=value)
        case "ReturnInstruction":
            return ReturnInstruction_Node(name=name, value=value)
        case "ReturnValue":
            return ReturnValue_Node(name=name, value=value)
        case "IfInstruction":
            return IfInstruction_Node(name=name, value=value)
        case "Else":
            return Else_Node(name=name, value=value)
        case "WhileInstruction":
            return WhileInstruction_Node(name=name, value=value)
        case "ForInstruction":
            return For_Node(name=name, value=value)
        case "Increment":
            return Increment_Node(name=name, value=value)
        case "Condition":
            return Condition_Node(name=name, value=value)
        case "C1":
            return C1_Node(name=name, value=value)
        case "AndTerm":
            return AndTerm_Node(name=name, value=value)
        case "AndTerm1":
            return AndTerm1_Node(name=name, value=value)
        case "OrTerm":
            return OrTerm_Node(name=name, value=value)
        case "RelValue":
            return RelValue_Node(name=name, value=value)
        case "InitialValue":
            return InitialValue_Node(name=name, value=value)
        case "DefineArrayInstruction":
            return DefineArrayInstruction_Node(name=name, value=value)
        case "DefineGlobalArrayInstruction":
            return DefineGlobalArrayInstruction_Node(name=name, value=value)
        case "ArrayValue":
            return ArrayValue_Node(name=name, value=value)
        case "ArrayRef":
            return ArrayRef_Node(name=name, value=value)
        case "ArrayIndexes":
            return ArrayIndexes_Node(name=name, value=value)
    return Node(value=value)
