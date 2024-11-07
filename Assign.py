# <id> = <exp>;
from Interpreter import gTokenizer
from Id import Id
from Exp import Exp

class Assign:
    def __init__(self):
        self._id = Id()
        self._exp = Exp()

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 32:
            raise Exception(f"ERROR: Expected identifier but got: {tok}")

        self._id.parseId2() # stmt_seq uses parseId2

        tok = gTokenizer.getToken()

        if tok != 14:
            raise Exception(f"ERROR: Expected = but got: {tok}")

        gTokenizer.skipToken()

        self._exp.parse()

        gTokenizer.skipToken()

        tok = gTokenizer.getToken()

        if tok != 12:
            raise Exception(f"ERROR: Expected ;, got {tok}")

        gTokenizer.skipToken()

    def print(self):
        self._id.print()
        print(" = ", end='')
        self._exp.print()
        print(";")

    def exec(self):
        self._id.setIdVal(self._exp.exec())
