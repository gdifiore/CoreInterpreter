from tokenizer import Tokenizer
from Op import Op

class Fac():
    def __init__(self):
        self._alternative = 0
        self._Op = Op()
        self._Fac = Fac()
        

    def parse(self):
        self._Op.parse()

        tok = self.tokenizer.getToken()

        if tok == 24:
            self.tokenizer.skipToken()
            self._Fac.parse()

    def print(self):
        self._Op.print()

        if self._Fac:
            print(" * ", end='')
            self._Fac.print()

    def exec(self):
        if self.fac:
            return self._Op.exec()
        else:
            return self._Op.exec() * self._Fac.exec()
