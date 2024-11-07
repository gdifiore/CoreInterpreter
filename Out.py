from Interpreter import gTokenizer
from IdList import IdList

class Out:
    def __init__(self):
        self._id_list = IdList()

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 11:
            raise Exception(f"ERROR: Expected write but got: {tok}")

        gTokenizer.skipToken()

        self._id_list.parse(True)

        tok = gTokenizer.getToken()

        if tok != 12:
            raise Exception(f"ERROR: Expected ;, got {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("write", end='')
        self._id_list.print()
        print(";")

    def exec(self):
        self._id_list.writeIdList()
