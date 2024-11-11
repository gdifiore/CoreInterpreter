from tokenizer import Tokenizer
from IdList import IdList

class Out:
    def __init__(self):
        self._id_list = IdList()
        

    def parse(self):
        tok = self.tokenizer.getToken()

        if tok != 11:
            raise Exception(f"ERROR: Expected write but got: {tok}")

        self.tokenizer.skipToken()

        self._id_list.parse(True)

        tok = self.tokenizer.getToken()

        if tok != 12:
            raise Exception(f"ERROR: Expected ;, got {tok}")

        self.tokenizer.skipToken()

    def print(self):
        print("write", end='')
        self._id_list.print()
        print(";")

    def exec(self):
        self._id_list.writeIdList()
