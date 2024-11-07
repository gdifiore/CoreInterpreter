from Interpreter import gTokenizer
from IdList import IdList

class Decl:
    def __init__(self):
        self._idList = IdList()

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 4:
            raise Exception(f"ERROR: Expected int got {tok}")

        gTokenizer.skipToken()

        self._idList = IdList()
        self._idList.parseIdList(True)

        tok = gTokenizer.getToken()

        if tok != 12:
            raise Exception(f"ERROR: Expected ; got {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("int ", end='')
        self._idList.printIdList()
        print(";", end= '')
