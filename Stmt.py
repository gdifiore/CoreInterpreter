from tokenizer import Tokenizer
from Assign import Assign
from If import If
from Loop import Loop
from In import In
from Out import Out

class Stmt:
    def __init__(self):
        self._alternative = 0
        self.s1 = Assign()
        self.s2 = If()
        self.s3 = Loop()
        self.s4 = In()
        self.s5 = Out()
        

    def parseStmt(self):
        tok = self.tokenizer.getToken()

        if tok not in [5, 8, 32, 10, 11]:
            raise Exception(f"ERROR: Expected identifier, if, while, read, or write but got: {tok}")

        if tok == 32: # assign
            self._alternative = 1
            self.s1 = Assign()
            self.s1.parse()
        elif tok == 5: # if
            self._alternative = 2
            self.s2 = If()
            self.s2.parse()
        elif tok == 8: # loop
            self._alternative = 3
            self.s3 = Loop()
            self.s3.parse()
        elif tok == 10: # in
            self._alternative = 4
            self.s4 = Out()
            self.s4.parse()
        elif tok == 11: # out
            self._alternative = 5
            self.s5 = In()
            self.s5.parse()

    def print(self):
        if self._alternative == 1:
            self.s1.print()
        elif self._alternative == 2:
            self.s2.print()
        elif self._alternative == 3:
            self.s3.print()
        elif self._alternative == 4:
            self.s4.print()
        elif self._alternative == 5:
            self.s5.print()

    def exec(self):
        if self._alternative == 1:
            self.s1.exec()
        elif self._alternative == 2:
            self.s2.exec()
        elif self._alternative == 3:
            self.s3.exec()
        elif self._alternative == 4:
            self.s4.exec()
        elif self._alternative == 5:
            self.s5.exec()
