from tokenizer import Tokenizer
from Id import Id
from Exp import Exp

class Op():
    def __init__(self):
        self._alternative = 0
        self._int = None
        self._Id = Id()
        self._Exp = Exp()
        

    def parse(self):
        tok = self.tokenizer.getToken()

        if tok not in [31, 32, 20]:
            raise Exception(f"ERROR: Expected int, exp, or ( but got: {tok}")

        if tok == 31:
            self._int = self.tokenizer.intVal()
            self.tokenizer.skipToken()
        elif tok == 32:
            self.Id = Id.parseId2() # stmt_seq
        else:
            self.tokenizer.skipToken()
            self._exp = Exp()
            self._exp.parseExp()
            tok = self.tokenizer.getToken()
            if tok != 21:
                raise Exception(f"ERROR: Expected ) but got: {tok}")
            self.tokenizer.skipToken()

    def print(self):
        if self._alternative == 1:
            print(self._int, end='')
        elif self._alternative == 2:
            self._Id.print()
        else:
            print("(", end='')
            self._Exp.print()
            print(")", end='')

    def exec(self):
        if self._alternative == 1:
            return self._int
        elif self._alternative == 2:
            return self._Id.getIdVal()
        else:
            return self._Exp.exec()
