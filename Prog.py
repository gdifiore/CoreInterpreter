from tokenizer import Tokenizer
from StmtSeq import StmtSeq
from DeclSeq import DeclSeq

class Prog():
    def __init__(self):
        self._DS = DeclSeq()
        self.SS = StmtSeq()
        

    def parse(self):
        tok = self.tokenizer.getToken()

        if tok != 1:
            raise Exception(f"ERROR: Expected program but got: {tok}")

        self.tokenizer.skipToken()

        self._DS = DeclSeq()
        self._DS.parse()

        tok = self.tokenizer.getToken()
        if tok != 2:
            raise Exception(f"ERROR: Expected begin but got: {tok}")

        self.tokenizer.skipToken()

        self._SS = StmtSeq()
        self._SS.parse()

        tok = self.tokenizer.getToken()
        if tok != 3:
            raise Exception(f"ERROR: Expected end but got: {tok}")

        self.tokenizer.skipToken()

        tok = self.tokenizer.getToken()
        if tok != 33:
            raise Exception(f"ERROR: Expected EOF but got: {tok}")

        return

    def print(self):
        print("program", end="")
        self._DS.print()
        print(" begin")
        self._SS.print()
        print("\nend", end = "")

    def exec(self):
        self._SS.exec()
