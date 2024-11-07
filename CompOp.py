from Interpreter import gTokenizer

class CompOp():
    def __init__(self):
        self._alternative = 0

    def parse(self):
        tok = gTokenizer.getToken()

        if tok not in [25, 26, 27, 28, 29, 30]:
            raise Exception(f"ERROR: Expected !=, ==, <, >, <=, or >= but got: {tok}")

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
