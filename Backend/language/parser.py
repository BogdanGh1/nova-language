from language.utils import Node, Atom, Production
from language.lexer import get_fip
from pathlib import Path
import string


def get_rules():
    rules_path = Path("language/resources/final_rules.txt")
    lines = rules_path.read_text().split("\n")
    rules = {}
    for line in lines:
        parts = line.split("->")
        neterminal = parts[0].strip()
        if neterminal not in rules:
            rules[neterminal] = []
        parts = parts[1].split("|")
        for part in parts:
            rules[neterminal].append(part.strip().split())
    return rules


def get_firsts(rules: dict):
    queue = list(rules.keys())
    firsts = {}
    i = 0
    while i < len(queue):
        if queue[i] in firsts:
            pass
        else:
            terminals = set()
            ok = True
            for rule in rules[queue[i]]:
                if not rule[0][0] in string.ascii_uppercase:
                    terminals.add(rule[0])
                else:
                    for atom in rule:
                        if not atom[0] in string.ascii_uppercase:
                            terminals.add(atom)
                            break
                        else:
                            if atom in firsts:
                                if "#" in firsts[atom]:
                                    for x in firsts[atom]:
                                        if x != "#":
                                            terminals.add(x)
                                else:
                                    for x in firsts[atom]:
                                        terminals.add(x)
                                    break
                            else:
                                queue.append(queue[i])
                                ok = False
                                break
                    if not ok:
                        break
            if ok:
                firsts[queue[i]] = terminals
        i += 1
    i = 0
    return firsts


def get_first_for_sequence(sequence: list, firsts: dict[set]):
    result = set()
    for element in sequence:
        if element not in firsts:
            result.add(element)
            return result
        if "#" not in firsts[element]:
            result = result.union(firsts[element])
            return result
        result = result.union(firsts[element])
        result.remove("#")
    return result


def epsilon_exists_in_sequence(sequence: list, firsts: dict[set]):
    for element in sequence:
        if element not in firsts:
            return False
        if "#" not in firsts[element]:
            return False
        return True


def get_follows(start_symbol: str, rules: dict, firsts: dict[set]):
    queue = list(rules.keys())
    follows = {}
    i = 0
    while i < len(queue):
        terminals = set()
        symbol = queue[i]
        ok = True
        for non_terminal in rules:
            for rule in rules[non_terminal]:
                for j in range(len(rule)):
                    if rule[j] == symbol:
                        if j == len(rule) - 1:
                            if non_terminal in follows:
                                for x in follows[non_terminal]:
                                    terminals.add(x)
                            elif non_terminal != symbol:
                                queue.append(symbol)
                                ok = False
                        else:
                            terminals = terminals.union(
                                get_first_for_sequence(rule[j + 1 :], firsts)
                            )
                            if epsilon_exists_in_sequence(rule[j + 1 :], firsts):
                                if non_terminal in follows:
                                    for x in follows[non_terminal]:
                                        terminals.add(x)
                                elif non_terminal != symbol:
                                    queue.append(symbol)
                                    ok = False
                if not ok:
                    break
            if not ok:
                break
        if ok:
            follows[symbol] = terminals
            if symbol == start_symbol:
                follows[symbol].add("$")

        i += 1
    return follows


def get_parse_table(rules, firsts, follows):
    table = {}
    for symbol in rules:
        for rule in rules[symbol]:
            current_firsts = get_first_for_sequence(rule, firsts)

            for first in current_firsts:
                if first != "#":
                    if symbol in table:
                        table[symbol][first] = rule
                    else:
                        table[symbol] = {}
                        table[symbol][first] = rule
            if "#" in current_firsts:
                for follow in follows[symbol]:
                    if symbol in table:
                        table[symbol][follow] = ["#"]
                    else:
                        table[symbol] = {}
                        table[symbol][follow] = ["#"]
                if "$" in follows[symbol]:
                    if symbol in table:
                        table[symbol]["$"] = rule
                    else:
                        table[symbol] = {}
                        table[symbol]["$"] = rule
    return table


def _parse(
    sequence: list[Atom], table: dict[dict[list]], start_symbol: str
) -> list[str]:
    stack = ["$", start_symbol]
    sequence.append(Atom(value="$", index=-1))
    sequence.reverse()
    productions = []
    while True:
        while stack[-1] == "#":
            stack.pop()
        if sequence[-1].value_type == "$" and stack[-1] == "$":
            break
        if not stack[-1][0] in string.ascii_uppercase:
            if stack[-1] == sequence[-1].value_type:
                productions[-1].add_atom(sequence[-1])
                stack.pop()
                sequence.pop()
            else:
                raise KeyError
        else:
            rule = table[stack[-1]][sequence[-1].value_type]
            productions.append(Production(stack[-1], rule))
            stack.pop()
            stack.extend(reversed(rule))

    return productions


def parse(text: str) -> list[str]:
    rules = get_rules()
    firsts = get_firsts(rules)
    follows = get_follows("Function", rules, firsts)
    parse_table = get_parse_table(rules, firsts, follows)

    atoms = get_fip(text)
    return _parse(atoms, parse_table, "Function")


def build_syntax_tree(text: str) -> Node:
    root = Node(name="Function")
    productions = parse(text)
    for production in productions:
        next = root.find_next_nonterminal_leaf()
        atoms = production.rule
        for atom in atoms:
            if isinstance(atom, Atom):
                node = Node(value=atom.value)
            elif not atom[0] in string.ascii_uppercase:
                node = Node(value=atom)
            else:
                node = Node(name=atom)
            next.add_child(node)
    return root
