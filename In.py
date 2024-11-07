from Interpreter import gTokenizer, gDataFile
from IdList import IdList

class In:
    def __init__(self):
        self._id_list = IdList()
        self._file = gDataFile

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 10:
            raise Exception(f"ERROR: Expected read but got: {tok}")

        gTokenizer.skipToken()

        self._id_list.parse(False)

        tok = gTokenizer.getToken()

        if tok != 12:
            raise Exception(f"ERROR: Expected ;, got {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("read", end='')
        self._id_list.print()
        print(";")

    def exec(self):
        self._id_list.readIdList()
