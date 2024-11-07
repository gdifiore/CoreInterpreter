# <comp> | !<cond> | [<cond> && <cond>] | [<cond> || <cond>]
from Interpreter import gTokenizer
from Comp import Comp

class Cond:
    def __init__(self):
        self._alternative = 0
        self._Comp = Comp()
        self._Cond1 = Cond()
        self._Cond2 = Cond()

    def parse(self):
        tok = gTokenizer.getToken()

        if tok not in [15, 16]:
            self._alternative = 1
            self._Comp.parse()
        elif tok == 15:
            self._alternative = 2
            gTokenizer.skipToken()
            self._Cond1.parse()
        elif tok == 16:
            gTokenizer.skipToken()
            self._Cond1.parse()
            gTokenizer.skipToken()
            tok = gTokenizer.getToken()
            if tok == 18:
                self._alternative = 3
            elif tok == 19:
                self._alternative = 4
            else:
                raise Exception(f"ERROR: Expected && or || but got: {tok}")
            gTokenizer.skipToken()
            self._Cond2.parse()

            gTokenizer.getToken()

            if tok != 17:
                raise Exception(f"ERROR: Expected ] but got: {tok}")

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
