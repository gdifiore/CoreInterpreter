from tokenizer import Tokenizer
from Fac import Fac

class Exp:
    def __init__(self):
        self._alternative = 0
        self._Fac = Fac()
        self._Exp = Exp()
        

    def parse(self):
        tok = self.tokenizer.getToken()

        self._Fac.parse()

        self.tokenizer.skipToken()
        tok = self.tokenizer.getToken()

        if tok in [22, 23]:
            self._alternative = tok - 20
            self.tokenizer.skipToken()

            self._Exp.parse()
        else:
            self._alternative = 1

    def print(self):
        self._Fac.print()
        if self._alternative == 2:
            print(" + ", end='')
            self._Exp.print()
        else:
            print(" - ", end='')
            self._Exp.print()

    def exec(self):
        if self._alternative == 1:
            self._Fac.exec()
        elif self._alternative == 2:
            self._Fac.exec() + self._Exp.exec()
        else:
            self._Fac.exec() - self._Exp.exec()
