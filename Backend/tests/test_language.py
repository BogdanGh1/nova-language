from pathlib import Path
from language.structures import SourceCode, CodeRunner
from language.lexer import get_functions_atoms
from language.parser import build_syntax_tree

def test_if():
    text = Path("../resources/sort.js").read_text()
    functions_atoms = get_functions_atoms(text)
    root = build_syntax_tree(functions_atoms[0][:])
    source_code = SourceCode(text)
    code_runner = CodeRunner(source_code)
    res = code_runner.run("start")
    assert len(res) == 1

def test_for():
    text = Path("../resources/for.js").read_text()
    functions_atoms = get_functions_atoms(text)
    root = build_syntax_tree(functions_atoms[0][:])
    source_code = SourceCode(text)
    code_runner = CodeRunner(source_code)
    res = code_runner.run("start")
    assert len(res) == 100

def test_while():
    text = Path("../resources/while.js").read_text()
    source_code = SourceCode(text)
    code_runner = CodeRunner(source_code)
    res = code_runner.run("start")
    assert len(res) == 20