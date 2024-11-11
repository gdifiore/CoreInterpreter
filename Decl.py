from tokenizer import Tokenizer
from IdList import IdList

class Decl:
    def __init__(self):
        self._idList = IdList()
        

    def parse(self):
        tok = self.tokenizer.getToken()

        if tok != 4:
            raise Exception(f"ERROR: Expected int got {tok}")

        self.tokenizer.skipToken()

        self._idList = IdList()
        self._idList.parseIdList(True)

        tok = self.tokenizer.getToken()

        if tok != 12:
            raise Exception(f"ERROR: Expected ; got {tok}")

        self.tokenizer.skipToken()

    def print(self):
        print("int ", end='')
        self._idList.printIdList()
        print(";", end= '')
