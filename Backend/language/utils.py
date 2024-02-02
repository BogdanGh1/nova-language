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
class AtomCode:
    code: int
    pos: tuple[int, int] | int | None = None
    value: str | None = None


class HashTable:
    MODULO = 107

    def __init__(self) -> None:
        self.table = [[] for _ in range(self.MODULO)]

    def __repr__(self) -> str:
        repr = {}
        for index, row in enumerate(self.table):
            if row != []:
                repr[index] = row
        return str(repr)

    def __get_hash(self, x: str) -> int:
        sum = 0
        for ch in x:
            sum += ord(ch)
        return sum % self.MODULO

    def find(self, x: str) -> bool:
        hash = self.__get_hash(x)
        for value in self.table[hash]:
            if x == value:
                return True
        return False

    def add(self, x: str) -> None:
        if not self.find(x):
            hash = self.__get_hash(x)
            self.table[hash].append(x)

    def get_pos(self, x: str) -> tuple[int, int]:
        hash = self.__get_hash(x)
        for index, value in enumerate(self.table[hash]):
            if x == value:
                return hash, index
        return False
