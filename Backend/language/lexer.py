from pathlib import Path
from dataclasses import dataclass
from language.utils import HashTable
from language.utils import AtomCode
import re

FIRST_SEPARATORS = [" ", "{", "}", "(", ")", ";", ",", "[", "]"]
SECOND_SEPARATORS = ["+", "-", "/", "*", "=", "<", ">"]


@dataclass
class Atom:
    value: str
    index: int

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return "'" + self.value + "'"


def get_atoms_table(file_path: Path) -> dict:
    atoms_table = {}
    with open(file_path, "r") as file:
        for line_index, line in enumerate(file):
            atoms_table[line.replace("\n", "")] = line_index + 3
    return atoms_table


def first_separation(line: str, line_index: int, separators: list) -> list:
    atoms = []
    currentAtom = ""
    for ch in line.replace("\n", ""):
        if ch in separators:
            if currentAtom != "":
                atoms.append(Atom(value=currentAtom, index=line_index))
            if ch != " ":
                atoms.append(Atom(value=ch, index=line_index))
            currentAtom = ""
        else:
            currentAtom += ch
    if currentAtom != "":
        atoms.append(Atom(value=currentAtom, index=line_index))
    return atoms


def second_separation(line: str, line_index: int, separators: list) -> list:
    atoms = []
    normalAtom = ""
    separatorAtom = ""
    for ch in line.replace("\n", ""):
        if ch in separators:
            separatorAtom += ch
            if normalAtom != "":
                atoms.append(Atom(value=normalAtom, index=line_index))
            normalAtom = ""
        else:
            normalAtom += ch
            if separatorAtom != "":
                atoms.append(Atom(value=separatorAtom, index=line_index))
            separatorAtom = ""
    if normalAtom != "":
        atoms.append(Atom(value=normalAtom, index=line_index))
    if separatorAtom != "":
        atoms.append(Atom(value=separatorAtom, index=line_index))
    return atoms


def get_final_separation(atoms: list[Atom]) -> list:
    final_atoms = []
    for atom in atoms:
        final_atoms.extend(second_separation(atom.value, atom.index, SECOND_SEPARATORS))
    return final_atoms


def identify_atoms(lines: list[str]) -> list[Atom]:
    atoms = []
    for line_index, line in enumerate(lines):
        line_atoms = first_separation(line, line_index + 1, FIRST_SEPARATORS)
        line_atoms = get_final_separation(line_atoms)
        atoms.extend(line_atoms)
    return atoms


def is_constant(value: str) -> bool:
    return re.fullmatch(r"^\d+$", value)


def is_string(value: str) -> bool:
    return re.fullmatch(r'^".*"$', value)


def is_variable(value: str) -> bool:
    return re.fullmatch(r"^[a-zA-Z][a-zA-Z0-9]*$", value)


def _get_fip(
    atoms_table: dict,
    variables_table: HashTable,
    constants_table: HashTable,
    atoms: list,
) -> list:
    fip = []
    for atom in atoms:
        if atom.value in atoms_table:
            fip.append(AtomCode(code=atoms_table[atom.value], value=atom.value))
        elif is_constant(atom.value):
            constants_table.add(atom.value)
            fip.append(
                AtomCode(
                    code=1, pos=constants_table.get_pos(atom.value), value=atom.value
                )
            )
        elif is_variable(atom.value):
            variables_table.add(atom.value)
            fip.append(
                AtomCode(
                    code=0,
                    pos=variables_table.get_pos(atom.value),
                    value=atom.value,
                )
            )
        elif is_string(atom.value):
            constants_table.add(atom.value)
            fip.append(
                AtomCode(
                    code=2, pos=constants_table.get_pos(atom.value), value=atom.value
                )
            )
        else:
            raise ValueError(
                "Atom" + atom.value + "necunoscut la linia " + str(atom.index)
            )
            # fip.append(AtomCode(code=-1, pos=atom.index, value=atom.value))
    return fip


def get_fip(atoms: list):
    variables_table = HashTable()
    constants_table = HashTable()

    atoms_table_file = Path("language/resources/atoms_table.txt")
    atoms_table = get_atoms_table(atoms_table_file)

    return _get_fip(atoms_table, variables_table, constants_table, atoms)


def get_values_from_fip(fip: list) -> list[str]:
    fip_values = []
    for x in fip:
        if x.code == 0:
            fip_values.append("id")
        elif x.code == 1:
            fip_values.append("const")
        else:
            fip_values.append(x.value)
    return fip_values
