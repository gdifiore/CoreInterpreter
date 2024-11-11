from tokenizer import Tokenizer
from Stmt import Stmt

class StmtSeq():
    def __init__(self):
        self._Stmt = Stmt()
        self._StmtSeq = StmtSeq()
        

    def parse(self):
        self._Stmt.parse()

        tok = self.tokenizer.getToken()

        if tok not in [5, 8, 10, 11, 32, 3, 7]:
            raise Exception(f"ERROR: Expected if, while, read, write, id, end, or else, got: {tok}")

        # check for another statement
        if tok in [5, 8, 32, 10, 11]:
            self._StmtSeq = StmtSeq()
            self._StmtSeq.parse()

    def print(self):
        self._Stmt.printStmt()
        if self._StmtSeq is not None:
            self._StmtSeq.print()

    def exec(self):
        self._Stmt.execStmt()
        if self._StmtSeq is not None:
            self._StmtSeq.exec()
