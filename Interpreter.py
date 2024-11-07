#from program import Program
from tokenizer import Tokenizer
import sys
import os

gTokenizer = None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} file.core program_data")
        exit(1)

    file = sys.argv[1]
    data = sys.argv[2]
    if not os.path.exists(file):
        print(f"ERROR: File '{file}' does not exist.")
        exit(1)

    if not os.path.exists(data):
        print(f"ERROR: File '{data}' does not exist.")
        exit(1)

    # change this to have the tokenizer handle the source and data files
    gTokenizer = Tokenizer(file)

# token_vals = []
# while True:
#     token = gTokenizer.getToken()
#     token_vals.append(token)
#     if token == 33:  # EOF token
#         break
#     gTokenizer.skipToken()

# print(*token_vals)

#p = Program()

#p.parse()
#p.print()
#p.exec()
