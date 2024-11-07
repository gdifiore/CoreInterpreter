from Interpreter import gTokenizer, gDataFile
from sys import argv

class Id:
    # Static variables
    _eIds = [None] * 20
    _idCount = 0
    _dataFile = open(argv[2]) # only have one file handle open

    def __init__(self, name: str):
        self._name = name
        self._val = 0
        self._declared = False
        self._initialized = False
        Id._idCount += 1

    @staticmethod
    # one of these sets declared to True
    def parseId1():
        tok = gTokenizer.getToken()

        if tok != 32:
            raise Exception(f"ERROR: Expected Id but got: {tok}")

        name = gTokenizer.idName()
        gTokenizer.skipToken()

        # search for existing Id
        for k in range(Id.idCount):
            if Id.eIds[k] is not None and Id.eIds[k].name == name:
                raise Exception(f"ERROR: Double declaration {name} has already been declared.")

        # create a new Id instance and add to eIds
        if Id.idCount < len(Id.eIds):
            new_id = Id(name)
            Id.eIds[Id.idCount - 1] = new_id
            new_id._declared = True
            return new_id
        else:
            raise Exception("ERROR: Max number of IDs in a Core program is 20.")

    @staticmethod
    def parseId2():
        tok = gTokenizer.getToken()

        if tok != 32:
            raise Exception(f"ERROR: Expected Id but got: {tok}")

        name = gTokenizer.idName()
        gTokenizer.skipToken()

        # Search for an existing Id instance with the same name
        # is this right??
        for k in range(Id.idCount):
            if Id.eIds[k] is not None and Id.eIds[k].name == name:
                return Id.eIds[k]

        raise Exception(f"ERROR: Undeclared variable {name} has not been declared.")

    def exec(self):
        self.getIdVal()

    def print(self):
        if not self._declared:
            raise Exception(f"ERROR: Id not declared.")
        print(self._name, end='')

    def getIdVal(self):
        if not self._initialized:
            raise Exception(f"ERROR: Attempted to use value of variable {self._name} before initializing.")
        return self._val;

    def setIdVal(self, new_val):
        if not self._declared:
            raise Exception(f"ERROR: Id not declared.")
        self._val = new_val
        self._initialized = True

    def getIdName(self):
        if not self._declared:
            raise Exception(f"ERROR: Id not declared.")
        return self._name

    def readId(self):
        if not self._declared:
            raise Exception(f"ERROR: Id not declared.")

        val = self._dataFile.readline()

        if len(val) <= 0:
            raise Exception(f"ERROR: Input file is empty.")

        try:
            self._val = int(val)
            self._initialized = True
        except ValueError:
            raise Exception(f"ERROR: Expected int got: {val}.")
