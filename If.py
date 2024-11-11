from tokenizer import Tokenizer
from Cond import Cond
from StmtSeq import StmtSeq

class If:
    def __init__(self):
        self._alternative = 0
        self._Cond = Cond()
        self._StmtSeq1 = StmtSeq()
        self._StmtSeq2 = StmtSeq()
        

    def parse(self):
        tok = self.tokenizer.getToken()

        if tok != 5:
            raise Exception(f"ERROR: Expected if but got: {tok}")

        self.tokenizer.skipToken()
        self._Cond.parse()

        tok = self.tokenizer.getToken()

        if tok != 6:
            raise Exception(f"ERROR: Expected then but got: {tok}")

        self.tokenizer.skipToken()
        self._StmtSeq1.parse()

        tok = self.tokenizer.getToken()
        if tok == 7:
            self._alternative = 2
            self.tokenizer.skipToken()
            self._StmtSeq2.parse()
        else:
            self._alternative = 1

        self.tokenizer.skipToken()
        tok = self.tokenizer.getToken()
        if tok != 3:
            raise Exception(f"ERROR: Expected end but got: {tok}")

        self.tokenizer.skipToken()
        tok = self.tokenizer.getToken()
        if tok != 12:
            raise Exception(f"ERROR: Expected ; but got: {tok}")

        self.tokenizer.skipToken()

    def print(self):
        # if <cond> then <stmt seq> end; | if <cond> then <stmt seq> else <stmt seq> end;
        print("if ", end='')
        self._Cond.print()
        print(" then ", end='')
        self._StmtSeq1.print()
        if self._alternative == 2:
            print(" else ", end='')
            self._StmtSeq2.print()
        print(" end;")

    def exec(self):
        if self._Cond.exec():
            self._StmtSeq1.exec()
        elif self._alternative == 2:
            self._StmtSeq2.exec()

