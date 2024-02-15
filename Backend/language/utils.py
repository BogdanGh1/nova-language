from dataclasses import dataclass


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
    def __init__(self, name: str, rule) -> None:
        self.name = name
        self._rule = rule[:]

    def add_atom(self, atom: Atom) -> None:
        for i in range(len(self._rule)):
            if (
                isinstance(self._rule[i], str)
                and self._rule[i] in ("id", "function_id", "const")
                and atom.type != "keyword"
            ):
                self._rule[i] = atom

    @property
    def rule(self):
        return self._rule

    def __str__(self) -> str:
        return self.name + " -> " + str(self._rule)

    def __repr__(self) -> str:
        return str(self)
