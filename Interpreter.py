from tokenizer import Tokenizer
import sys
import os

gTokenizer = None
gFile = None

class Prog():
    def __init__(self):
        self._DS = None
        self._SS = None

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 1:
            raise Exception(f"{type(self).__name__} ERROR: Expected program but got: {tok}")

        gTokenizer.skipToken()
        self._DS = DeclSeq()
        self._DS.parse()

        tok = gTokenizer.getToken()
        if tok != 2:
            raise Exception(f"{type(self).__name__} ERROR: Expected begin but got: {tok}")

        gTokenizer.skipToken()
        self._SS = StmtSeq()
        self._SS.parse()

        tok = gTokenizer.getToken()
        if tok != 3:
            raise Exception(f"{type(self).__name__} ERROR: Expected end but got: {tok}")

        gTokenizer.skipToken()

        tok = gTokenizer.getToken()
        if tok != 33:
            raise Exception(f"{type(self).__name__} ERROR: Expected EOF but got: {tok}")

    def print(self):
        print("program\n", end="")
        self._DS.print()
        print("\nbegin")
        self._SS.print()
        print("end\n", end = "")

    def exec(self):
        print("\n\nProgram Output:")
        self._SS.exec()

class DeclSeq():
    def __init__(self):
        self._Decl = None
        self._DS = None

    def parse(self):
        self._Decl = Decl()
        self._Decl.parse()

        tok = gTokenizer.getToken()

        # error check for int or begin token
        if tok not in [4, 2]:
            raise Exception(f"{type(self).__name__} ERROR: Expected int or begin but got: {tok}")

        if tok == 4:
            self._DS = DeclSeq()
            self._DS.parse()

    def print(self):
        self._Decl.print()
        if self._DS is not None:
            self._DS.print()

class StmtSeq():
    def __init__(self):
        self._Stmt = None
        self._StmtSeq = None

    def parse(self):
        self._Stmt = Stmt()
        self._Stmt.parse()

        tok = gTokenizer.getToken()

        if tok not in [5, 8, 10, 11, 32, 3, 7]:
            raise Exception(f"{type(self).__name__} ERROR: Expected if, while, read, write, id, end, or else, got: {tok}")

        # check for another statement
        if tok in [5, 8, 32, 10, 11]:
            self._StmtSeq = StmtSeq()
            self._StmtSeq.parse()

    def print(self):
        self._Stmt.print()
        if self._StmtSeq is not None:
            self._StmtSeq.print()

    def exec(self):
        self._Stmt.exec()
        if self._StmtSeq is not None:
            self._StmtSeq.exec()

class Decl():
    def __init__(self):
        self._idList = None

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 4:
            raise Exception(f"{type(self).__name__} ERROR: Expected int got {tok}")

        gTokenizer.skipToken()

        self._idList = IdList()
        self._idList.parse(True)

        tok = gTokenizer.getToken()

        if tok != 12:
            raise Exception(f"{type(self).__name__} ERROR: Expected ; got {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("int ", end='')
        self._idList.print()
        print(";", end= '')

class IdList():
    def __init__(self):
        self._id = None
        self._idList = None

    def parse(self, isDeclared):
        tok = gTokenizer.getToken()

        # error check for the id token
        if tok != 32:
            raise Exception(f"{type(self).__name__} ERROR: Expected Id but got: {tok}")

        # DS or SS parsing
        if isDeclared:
            self._id = Id.parseId1()
        else:
            self._id = Id.parseId2()

        tok = gTokenizer.getToken()

        if tok not in [12, 13]:
            print("Error: Expected , or ;, got " + str(tok))
            exit(1)

        # comma or semicolon
        # comma keep reading, semicolon means list is over
        if tok == 13:
            gTokenizer.skipToken()
            self._idList = IdList()
            self._idList.parse(isDeclared)
        elif tok == 12:
            return

    def print(self):
        self._id.print()
        if self._idList is not None:
            print(", ", end="")
            self._idList.print()

    def printIdList(self):
        self._id.print()
        print(" = ", end="")
        print(str(self._id.getIdVal())+ "\n", end="")
        if self._idList is not None:
            self._idList.printIdList()

    def readIdList(self):
        self._id.readId()
        if self._idList is not None:
            self._idList.readIdList()

class Stmt():
    def __init__(self):
        self._alternative = 0
        self.s1 = None # assign
        self.s2 = None # if
        self.s3 = None # loop
        self.s4 = None # in
        self.s5 = None # out

    def parse(self):
        tok = gTokenizer.getToken()

        if tok not in [5, 8, 32, 10, 11]:
            raise Exception(f"{type(self).__name__} ERROR: Expected identifier, if, while, read, or write but got: {tok}")

        if tok == 32: # assign
            self._alternative = 1
            self.s1 = Assign()
            self.s1.parse()
        elif tok == 5: # if
            self._alternative = 2
            self.s2 = If()
            self.s2.parse()
        elif tok == 8: # loop
            self._alternative = 3
            self.s3 = Loop()
            self.s3.parse()
        elif tok == 10: # in
            self._alternative = 4
            self.s4 = In()
            self.s4.parse()
        elif tok == 11: # out
            self._alternative = 5
            self.s5 = Out()
            self.s5.parse()

    def print(self):
        if self._alternative == 1:
            self.s1.print()
        elif self._alternative == 2:
            self.s2.print()
        elif self._alternative == 3:
            self.s3.print()
        elif self._alternative == 4:
            self.s4.print()
        elif self._alternative == 5:
            self.s5.print()

    def exec(self):
        if self._alternative == 1:
            self.s1.exec()
        elif self._alternative == 2:
            self.s2.exec()
        elif self._alternative == 3:
            self.s3.exec()
        elif self._alternative == 4:
            self.s4.exec()
        elif self._alternative == 5:
            self.s5.exec()

class Assign():
    def __init__(self):
        self._id = None
        self._exp = None

    def parse(self):
        self._id = Id.parseId2() # stmt_seq uses parseId2

        tok = gTokenizer.getToken()

        if tok != 14:
            raise Exception(f"{type(self).__name__} ERROR: Expected = but got: {tok}")

        gTokenizer.skipToken()

        self._exp = Exp()
        self._exp.parse()

        tok = gTokenizer.getToken()

        if tok != 12:
            raise Exception(f"{type(self).__name__} ERROR: Expected ;, got {tok}")

        gTokenizer.skipToken()

    def print(self):
        self._id.print()
        print(" = ", end='')
        self._exp.print()
        print(";")

    def exec(self):
        self._id.setIdVal(self._exp.exec())

class If():
    def __init__(self):
        self._alternative = 0
        self._Cond = None
        self._StmtSeq1 = None
        self._StmtSeq2 = None

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 5:
            raise Exception(f"{type(self).__name__} ERROR: Expected if but got: {tok}")

        gTokenizer.skipToken()
        self._Cond = Cond()
        self._Cond.parse()

        tok = gTokenizer.getToken()

        if tok != 6:
            raise Exception(f"{type(self).__name__} ERROR: Expected then but got: {tok}")

        gTokenizer.skipToken()
        self._StmtSeq1 = StmtSeq()
        self._StmtSeq1.parse()

        tok = gTokenizer.getToken()
        if tok == 7:
            self._alternative = 2
            gTokenizer.skipToken()
            self._StmtSeq2 = StmtSeq()
            self._StmtSeq2.parse()
        else:
            self._alternative = 1

        tok = gTokenizer.getToken()
        if tok != 3:
            raise Exception(f"{type(self).__name__} ERROR: Expected end but got: {tok}")

        gTokenizer.skipToken()
        tok = gTokenizer.getToken()
        if tok != 12:
            raise Exception(f"{type(self).__name__} ERROR: Expected ; but got: {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("if ", end='')
        self._Cond.print()
        print(" then ", end='')
        self._StmtSeq1.print()
        if self._alternative == 2:
            print("else ", end='')
            self._StmtSeq2.print()
        print("end;")

    def exec(self):
        if self._Cond.exec():
            self._StmtSeq1.exec()
        elif self._alternative == 2:
            self._StmtSeq2.exec()

class Loop():
    def __init__(self):
        self._alternative = 0
        self._Cond = None
        self._StmtSeq = None

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 8:
            raise Exception(f"{type(self).__name__} ERROR: Expected while but got: {tok}")

        gTokenizer.skipToken()
        self._Cond = Cond()
        self._Cond.parse()

        tok = gTokenizer.getToken()

        if tok != 9:
            raise Exception(f"{type(self).__name__} ERROR: Expected loop but got: {tok}")

        gTokenizer.skipToken()
        self._StmtSeq = StmtSeq()
        self._StmtSeq.parse()

        tok = gTokenizer.getToken()
        if tok != 3:
            raise Exception(f"{type(self).__name__} ERROR: Expected end but got: {tok}")

        gTokenizer.skipToken()
        tok = gTokenizer.getToken()
        if tok != 12:
            raise Exception(f"{type(self).__name__} ERROR: Expected ; but got: {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("while ", end='')
        self._Cond.print()
        print(" loop\n", end='')
        self._StmtSeq.print()
        print("end;")

    def exec(self):
        while(self._Cond.exec()):
            self._StmtSeq.exec()

class In():
    def __init__(self):
        self._id_list = IdList()

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 10:
            raise Exception(f"{type(self).__name__} ERROR: Expected read but got: {tok}")

        gTokenizer.skipToken()

        self._id_list.parse(False)

        tok = gTokenizer.getToken()

        if tok != 12:
            raise Exception(f"{type(self).__name__} ERROR: Expected ;, got {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("read ", end='')
        self._id_list.print()
        print(";")

    def exec(self):
        self._id_list.readIdList()

class Out():
    def __init__(self):
        self._id_list = None

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 11:
            raise Exception(f"{type(self).__name__} ERROR: Expected write but got: {tok}")

        gTokenizer.skipToken()

        self._id_list = IdList()
        self._id_list.parse(False)

        tok = gTokenizer.getToken()

        if tok != 12:
            raise Exception(f"{type(self).__name__} ERROR: Expected ;, got {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("write ", end='')
        self._id_list.print()
        print(";")

    def exec(self):
        self._id_list.printIdList()

class Cond():
    def __init__(self):
        self._alternative = 0
        self._Comp = None
        self._Cond1 = None
        self._Cond2 = None

    def parse(self):
        tok = gTokenizer.getToken()

        if tok not in [15, 16]:
            self._alternative = 1
            self._Comp = Comp()
            self._Comp.parse()
        elif tok == 15:
            self._alternative = 2
            gTokenizer.skipToken()
            self._Cond1 = Cond()
            self._Cond1.parse()
        elif tok == 16:
            gTokenizer.skipToken()

            self._Cond1 = Cond()
            self._Cond1.parse()

            gTokenizer.skipToken()
            tok = gTokenizer.getToken()

            if tok == 18:
                self._alternative = 3
            elif tok == 19:
                self._alternative = 4
            else:
                raise Exception(f"{type(self).__name__} ERROR: Expected && or || but got: {tok}")

            gTokenizer.skipToken()

            self._Cond2 = Cond()
            self._Cond2.parse()

            gTokenizer.getToken()

            if tok != 17:
                raise Exception(f"{type(self).__name__} ERROR: Expected ] but got: {tok}")

        gTokenizer.skipToken()

    def print(self):
        if self._alternative == 1:
            self._Comp.print()
            return
        elif self._alternative == 2:
            print("!", end='')
            self._Cond1.print()
            return
        elif self._alternative == 3:
            print("[", end='')
            self._Cond1.print()
            print(" && ", end='')
        else:
            print("[", end='')
            self._Cond1.print()
            print(" || ", end='')

        self._Cond2.print()
        print("]", end='')

    def exec(self) -> bool:
        if self._alternative == 1:
            return self._Comp.exec()
        elif self._alternative == 2:
            return not self._Comp.exec()
        elif self._alternative == 3:
            return self._Cond1.exec() and self._Cond2.exec()
        else:
            return self._Cond1.exec() or self._Cond2.exec()

class Comp():
    def __init__(self):
        self._Op1 = None
        self._CompOp = None
        self._Op2 = None

    def parse(self):
        tok = gTokenizer.getToken()

        if tok != 20:
            raise Exception(f"{type(self).__name__} ERROR: Expected ( but got: {tok}")

        gTokenizer.skipToken()

        self._Op1 = Op()
        self._Op1.parse()

        self._CompOp = CompOp()
        self._CompOp.parse()

        self._Op2 = Op()
        self._Op2.parse()

        tok = gTokenizer.getToken()
        if tok != 21:
            raise Exception(f"{type(self).__name__} ERROR: Expected ) but got: {tok}")

        gTokenizer.skipToken()

    def print(self):
        print("( ", end='')
        self._Op1.print()
        self._CompOp.print()
        self._Op2.print()
        print(" )", end='')

    def exec(self) -> bool:
        left_val = self._Op1.exec()
        right_val = self._Op2.exec()

        if self._CompOp._alternative == 1:
            return left_val != right_val
        elif self._CompOp._alternative == 2:
            return left_val == right_val
        elif self._CompOp._alternative == 3:
            return left_val < right_val
        elif self._CompOp._alternative == 4:
            return left_val > right_val
        elif self._CompOp._alternative == 5:
            return left_val <= right_val
        elif self._CompOp._alternative == 6:
            return left_val >= right_val
        else:
            raise Exception(f"{type(self).__name__} Invalid comparison operator: {self._CompOp._alternative}")

class Exp():
    def __init__(self):
        self._alternative = 0
        self._Fac = None
        self._Exp = None

    def parse(self):
        self._Fac = Fac()
        self._Fac.parse()

        tok = gTokenizer.getToken()

        if tok not in [22, 23]:
            self._alternative = 1
            return

        self._alternative = tok - 20

        gTokenizer.skipToken()

        self._Exp = Exp()
        self._Exp.parse()

    def print(self):
        self._Fac.print()
        if self._alternative == 2:
            print(" + ", end='')
            self._Exp.print()
        elif self._alternative == 3:
            print(" - ", end='')
            self._Exp.print()

    def exec(self):
        if self._alternative == 1:
            return self._Fac.exec()
        elif self._alternative == 2:
            return self._Fac.exec() + self._Exp.exec()
        elif self._alternative == 3:
            return self._Fac.exec() - self._Exp.exec()

class Fac():
    def __init__(self):
        self._Op = None
        self._Fac = None

    def parse(self):
        self._Op = Op()
        self._Op.parse()

        tok = gTokenizer.getToken()

        if tok == 24:
            gTokenizer.skipToken()
            self._Fac = Fac()
            self._Fac.parse()

    def print(self):
        self._Op.print()

        if self._Fac:
            print(" * ", end='')
            self._Fac.print()

    def exec(self):
        if self._Fac is None:
            return self._Op.exec()
        else:
            return self._Op.exec() * self._Fac.exec()

class Op():
    def __init__(self):
        self._alternative = 0
        self._int = None
        self._Id = None
        self._Exp = None

    def parse(self):
        tok = gTokenizer.getToken()

        if tok not in [31, 32, 20]:
            raise Exception(f"{type(self).__name__} ERROR: Expected int, exp, or ( but got: {tok}")

        if tok == 31:
            self._int = gTokenizer.intVal()
            gTokenizer.skipToken()
        elif tok == 32:
            self._Id = Id.parseId2() # stmt_seq
        else:
            gTokenizer.skipToken()
            self._Exp = Exp()
            self._Exp.parse()
            tok = gTokenizer.getToken()
            if tok != 21:
                raise Exception(f"{type(self).__name__} ERROR: Expected ) but got: {tok}")
            gTokenizer.skipToken()

    def print(self):
        if self._int is not None:
            print(self._int, end='')
        elif self._Id is not None:
            self._Id.print()
        elif self._Exp is not None:
            print("(", end='')
            self._Exp.print()
            print(")", end='')

    def exec(self):
        if self._int is not None:
            return self._int
        elif self._Id is not None:
            return self._Id.getIdVal()
        elif self._Exp is not None:
            return self._Exp.exec()

class CompOp():
    def __init__(self):
        self._alternative = 0

    def parse(self):
        tok = gTokenizer.getToken()

        if tok not in [25, 26, 27, 28, 29, 30]:
            raise Exception(f"{type(self).__name__} ERROR: Expected !=, ==, <, >, <=, or >= but got: {tok}")

        gTokenizer.skipToken()
        self._alternative = tok - 24

    def print(self):
        operators = {
            1: '!=',
            2: '==',
            3: '<',
            4: '>',
            5: '<=',
            6: '>='
        }
        print(operators.get(self._alternative, ''), end='')

class Id():
    _name = None
    _val = None
    _declared = None
    _initialized = None

    # Static variables
    _eIds = [None] * 20
    _idCount = 0

    def __init__(self, name: str):
        self._name = name
        self._declared = True
        self._initialized = False

    @classmethod
    def parseId1(cls):
        tok = gTokenizer.getToken()

        if tok != 32:
            raise Exception(f"{type(cls).__name__} ERROR: Expected Id but got: {tok}")

        name = gTokenizer.idName()
        gTokenizer.skipToken()

        # search for existing Id
        for k in range(cls._idCount):
            if cls._eIds[k] is not None and cls._eIds[k]._name == name:
                raise Exception(f"{type(cls).__name__} ERROR: Double declaration {name} has already been declared.")

        # create a new Id instance and add to eIds
        if cls._idCount < len(cls._eIds):
            new_id = Id(name)
            cls._eIds[cls._idCount] = new_id
            cls._idCount += 1
            return new_id
        else:
            raise Exception("ERROR: Max number of IDs in a Core program is 20.")

    @classmethod
    def parseId2(cls):
        tok = gTokenizer.getToken()

        if tok != 32:
            raise Exception(f"{type(cls).__name__} ERROR: Expected Id but got: {tok}")

        name = gTokenizer.idName()
        gTokenizer.skipToken()

        # search for an existing Id instance with the same name
        for k in range(cls._idCount):
            if cls._eIds[k] is not None and cls._eIds[k]._name == name:
                return cls._eIds[k]

        raise Exception(f"{type(cls).__name__} ERROR: Undeclared variable {name} has not been declared.")

    def exec(self):
        self.getIdVal()

    def print(self):
        if not self._declared:
            raise Exception(f"{type(self).__name__} ERROR: Id not declared.")
        print(self._name, end='')

    def getIdVal(self):
        if not self._initialized:
            raise Exception(f"{type(self).__name__} ERROR: Attempted to use value of variable {self._name} before initializing.")
        return self._val;

    def setIdVal(self, new_val):
        if not self._declared:
            raise Exception(f"{type(self).__name__} ERROR: Id not declared.")
        self._val = new_val
        self._initialized = True

    def readId(self):
        if not self._declared:
            raise Exception(f"{type(self).__name__} ERROR: Id not declared.")

        # passing data file is optional, so handle case where it's needed but user didn't pass in
        try:
            val = gFile.readline()
        except Exception as e:
            print(f"{type(self).__name__} ERROR: Did you mean to pass an input file?: {e}")
            exit(1)

        if len(val) <= 0:
            raise Exception(f"{type(self).__name__} ERROR: Input file is empty.")

        try:
            self._val = int(val)
            self._initialized = True
        except ValueError:
            raise ValueError(f"{type(self).__name__} ERROR: Expected int got: {val}.")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} file.core [program_data]")
        exit(1)

    file = sys.argv[1]
    data = sys.argv[2] if len(sys.argv) == 3 else None  # only set `data` if it exists

    if not os.path.exists(file):
        print(f"ERROR: File '{file}' does not exist.")
        exit(1)

    if data and not os.path.exists(data):
        print(f"ERROR: File '{data}' does not exist.")
        exit(1)

    gTokenizer = Tokenizer(file)
    if data:
        gFile = open(data)

    p = Prog()

    p.parse()
    p.print()
    p.exec()
