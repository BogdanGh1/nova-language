from pathlib import Path
from language.utils import Atom
import re

FIRST_SEPARATORS = [" ", "{", "}", "(", ")", ";", ",", "[", "]"]
SECOND_SEPARATORS = ["+", "-", "/", "*", "=", "<", ">"]


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


def get_final_separation(atoms: list[Atom]) -> list[Atom]:
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


def add_type(
    atoms_table: dict,
    atoms: list,
) -> None:
    for atom in atoms:
        if atom.value in atoms_table:
            atom.type = "keyword"
        elif is_constant(atom.value) or is_string(atom.value):
            atom.type = "const"
        elif is_variable(atom.value):
            atom.type = "id"
        else:
            raise ValueError(
                "Atom" + atom.value + "necunoscut la linia " + str(atom.index)
            )


def get_fip(text: str) -> list[Atom]:
    atoms = identify_atoms(text.split("\n"))

    atoms_table_file = Path("language/resources/atoms_table.txt")
    atoms_table = get_atoms_table(atoms_table_file)

    add_type(atoms_table, atoms)
    return atoms
