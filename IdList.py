from Interpreter import gTokenizer
from Id import Id

class IdList:
    _id: Id = None
    _idList = None

    def __init__():
        pass

    def parse(self, isDeclared):
        tok = gTokenizer.getToken()

        # error check for the id token
        if tok != 32:
            raise Exception(f"ERROR: Expected Id but got: {tok}")

        # DS or SS parsing
        if isDeclared:
            self._id = Id.parseId1()
        else:
            self._id = Id.parseId2()

        tok = gTokenizer.getToken()

        if tok != 12 or tok != 13:
            print("Error: Expected , or ;, got " + str(tok))
            exit(1)

        # comma or semicolon
        # comma keep reading, semicolon means list is over
        if tok == 13:
            gTokenizer.skipToken()
            self._idList = IdList()
            self._idList.parseIdList(isDeclared)
        elif tok == 12:
            return


    def print(self):
        self._id.print()
        if self._idList is not None:
            print(", ", end="")
            self._idList.print()

    def writeIdList(self):
        self._id.printId()
        print(" = ", end="")
        print(str(self._id.getIdVal())+ "\n", end="")
        if self._idList is not None:
            self._idList.writeIdList()

    def readIdList(self):
        self._id.readId()
        if self._idList is not None:
            self._idList.readIdList()