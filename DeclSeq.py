from tokenizer import Tokenizer
from Decl import Decl

class DeclSeq():
    def __init__(self):
        self._Decl = Decl()
        self._DS = DeclSeq()
        

    def parse(self):
        self._Decl.parse()

        tok = self.tokenizer.getToken()


        # error check for int or begin token
        if tok not in [4, 2]:
            raise Exception(f"ERROR: Expected int or begin but got: {tok}")

        if tok == 4:
            self._DS = DeclSeq()
            self._DS.parse()


    def print(self):
        self._Decl.print()
        if self._DS is not None:
            self._DS.print()
