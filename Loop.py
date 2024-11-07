# while <cond> loop <stmt seq> end;

from Interpreter import gTokenizer
from Cond import Cond
from StmtSeq import StmtSeq

class Loop:
    def __init__(self):
        self._alternative = 0
        self._Cond = Cond()
        self._StmtSeq = StmtSeq()

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 8:
            raise Exception(f"ERROR: Expected while but got: {tok}")

        gTokenizer.skipToken()
        self._Cond.parse()

        tok = gTokenizer.getToken()

        if tok != 9:
            raise Exception(f"ERROR: Expected loop but got: {tok}")

        gTokenizer.skipToken()
        self._StmtSeq.parse()

        tok = gTokenizer.getToken()
        if tok != 3:
            raise Exception(f"ERROR: Expected end but got: {tok}")

        gTokenizer.skipToken()
        tok = gTokenizer.getToken()
        if tok != 12:
            raise Exception(f"ERROR: Expected ; but got: {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("while ", end='')
        self._Cond.print()
        print(" loop ", end='')
        self._StmtSeq.print()
        print(" end;")

    def exec(self):
        while(self._Cond.exec()):
            self._StmtSeq.exec()
