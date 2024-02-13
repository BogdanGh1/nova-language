from language.actions import Action
from language.variables import VariableTable


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
            return self.value
        d = {}
        d[self.name] = []
        for child in self.children:
            d[self.name].append(child.build_dict())
        return d


class Function_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action]):
        self.children[6].eval(var_table, actions)


class Instruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action]):
        self.children[0].eval(var_table, actions)


class Instructions_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action]):
        if len(self.children) == 2 and isinstance(self.children[1], Instructions_Node):
            self.children[0].eval(var_table, actions)
            self.children[1].eval(var_table, actions)
        elif len(self.children) == 1 and isinstance(self.children[0], Instruction_Node):
            self.children[0].eval(var_table, actions)


class DefineInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action]):
        print("Define instruction")


class DefineGlobalInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action]):
        print("Define global instruction")


class AttributionInstruction_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action]):
        print("Attribution instruction")


class Id_List_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action]):
        if self.value != "#":
            print(self.children[0].value)
            self.children[1].eval(var_table, actions)


class Id_List1_Node(Node):
    def eval(self, var_table: VariableTable, actions: list[Action]):
        if self.value != "#":
            print(self.children[0].value)
            self.children[2].eval(var_table, actions)


def create_node(name, value=None):
    match name:
        case "Function":
            return Function_Node(name=name, value=value)
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
        case "Id_List":
            return Id_List_Node(name=name, value=value)
        case "Id_List1":
            return Id_List1_Node(name=name, value=value)
    return Node(value=value)
