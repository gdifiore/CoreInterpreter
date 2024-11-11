# while <cond> loop <stmt seq> end;

from tokenizer import Tokenizer
from Cond import Cond
from StmtSeq import StmtSeq

class Loop:
    def __init__(self):
        self._alternative = 0
        self._Cond = Cond()
        self._StmtSeq = StmtSeq()
        

    def parse(self):
        tok = self.tokenizer.getToken()

        if tok != 8:
            raise Exception(f"ERROR: Expected while but got: {tok}")

        self.tokenizer.skipToken()
        self._Cond.parse()

        tok = self.tokenizer.getToken()

        if tok != 9:
            raise Exception(f"ERROR: Expected loop but got: {tok}")

        self.tokenizer.skipToken()
        self._StmtSeq.parse()

        tok = self.tokenizer.getToken()
        if tok != 3:
            raise Exception(f"ERROR: Expected end but got: {tok}")

        self.tokenizer.skipToken()
        tok = self.tokenizer.getToken()
        if tok != 12:
            raise Exception(f"ERROR: Expected ; but got: {tok}")

        self.tokenizer.skipToken()

    def print(self):
        print("while ", end='')
        self._Cond.print()
        print(" loop ", end='')
        self._StmtSeq.print()
        print(" end;")

    def exec(self):
        while(self._Cond.exec()):
            self._StmtSeq.exec()
