from dataclasses import dataclass


class Node:
    def __init__(self, name: str = None, value=None) -> None:
        self.name = name
        self.value = value
        self.children = []

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


@dataclass
class Atom:
    value: str
    index: int
    type: str | None = None

    @property
    def value_type(self):
        if self.type == "keyword" or self.type == None:
            return self.value
        return self.type


class Production:
    def __init__(self, name: str, rule: list[str]) -> None:
        self.name = name
        self._rule = rule

    @property
    def rule(self):
        return self._rule

    def __str__(self) -> str:
        return self.name + " -> " + str(self._rule)

    def __repr__(self) -> str:
        return str(self)
