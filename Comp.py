# <comp> ::= (<op> <comp op> <op>)
from Interpreter import gTokenizer
from Op import Op
from CompOp import CompOp

class Comp:
    def __init__(self):
        self._Op1 = Op()
        self._CompOp = CompOp()
        self._Op2 = Op()

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 20:
            raise Exception(f"ERROR: Expected ( but got: {tok}")

        gTokenizer.skipToken()

        self._Op1.parse()

        gTokenizer.skipToken()

        self._CompOp.parse()

        gTokenizer.skipToken()

        self._Op2.parse()

        if tok != 21:
            raise Exception(f"ERROR: Expected ) but got: {tok}")

    def print(self):
        print("( ", end='')
        self._Op1.print()
        self._CompOp.print()
        self._Op2.print()
        print(" )", end='')

    def exec(self) -> bool:
        operators = {
            1: '!=',
            2: '==',
            3: '<',
            4: '>',
            5: '<=',
            6: '>='
        }
        op = operators[self._CompOp._alternative]

        expression = f"{self._Op1.exec()} {op} {self._Op2.exec()}"
        return eval(expression)
