from tokenizer import Tokenizer
from IdList import IdList
import sys

class In:
    def __init__(self):
        self._id_list = IdList()
        
        if sys.argv[2]:
            self._file = sys.argv[2]

    def parse(self):
        tok = self.tokenizer.getToken()

        if tok != 10:
            raise Exception(f"ERROR: Expected read but got: {tok}")

        self.tokenizer.skipToken()

        self._id_list.parse(False)

        tok = self.tokenizer.getToken()

        if tok != 12:
            raise Exception(f"ERROR: Expected ;, got {tok}")

        self.tokenizer.skipToken()

    def print(self):
        print("read", end='')
        self._id_list.print()
        print(";")

    def exec(self):
        self._id_list.readIdList()
