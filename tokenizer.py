import sys
import os

class Tokenizer:
    """
    Tokenizer class for the Core language.
    This class is responsible for reading a Core source file and breaking it down into tokens.

    The constructor expects that the file path is valid.
    """

    TOKEN_MAP = {
        "reserved_words": {
            "program": 1,
            "begin": 2,
            "end": 3,
            "int": 4,
            "if": 5,
            "then": 6,
            "else": 7,
            "while": 8,
            "loop": 9,
            "read": 10,
            "write": 11,
        },
        "special_symbols": {
            ";": 12,
            ",": 13,
            "=": 14,
            "!": 15,
            "[": 16,
            "]": 17,
            "&&": 18,
            "||": 19,
            "(": 20,
            ")": 21,
            "+": 22,
            "-": 23,
            "*": 24,
            "!=": 25,
            "==": 26,
            "<": 27,
            ">": 28,
            "<=": 29,
            ">=": 30,
        },
        "integer": 31,
        "identifier": 32,
        "end_of_file": 33,
        "error_token": 34,
    }

    # Variables that will be modified and used by the Tokenizer class
    _file_handle = None
    _read_lines = None  # store lines read in from file
    _file_line_index = 0
    _current_line = []
    _current_line_index = 0
    _tokens = []  # storing all tokens, as tokenized
    _current_token_value = 0  # stores the value of the current token, e.g. integer = 31
    _all_tokens = []

    def __init__(self, core_file):
        self._core_file = core_file
        self._file_handle = open(core_file, encoding="utf-8")
        self._file_line_index = 0
        self._current_line = []
        self._current_line_index = 0
        self._tokens = []
        self._current_token_value = 0
        self._all_tokens = []

    def __del__(self):
        if self._file_handle:
            self._file_handle.close()

    def _get_next_line(self):
        """
        Reads the next line from the input file.

        If the end of the file is reached, returns "EOF".

        Returns:
            str: The next line from the file or "EOF" if the end of the file is reached.
        """
        try:
            while True:
                line = next(self._file_handle).rstrip('\n')
                if line.strip():  # skip lines that are entirely whitespace
                    return line
        except StopIteration:
            return "EOF"

    def _load_next_line(self):
        """
        Reads the next line from the input file, tokenizes it, and updates the
        internal state of the Tokenizer.

        If the end of the file is reached, it sets the current token to EOF.

        Returns:
            None
        """
        next_line = self._get_next_line()
        if next_line == "EOF":
            self._tokens = ["EOF"]
            self._current_token_value = self.TOKEN_MAP["end_of_file"]
            self._current_line = ["EOF"]
            self._current_line_index = 0
        else:
            self._current_line = self.tokenizeLine(next_line)
            self._tokens = self._current_line
            self._current_line_index = 0

        self._all_tokens += self._tokens

    def _handle_invalid_token(self, invalid_token):
        """
        Handles an invalid token by recording tokens up to this point and exiting.
        """
        tokens_prior_to_error = []
        print(self._all_tokens)
        for tok in self._all_tokens:
            if tok in self.TOKEN_MAP["reserved_words"]:
                tokens_prior_to_error.append(self.TOKEN_MAP["reserved_words"][tok])
            elif tok in self.TOKEN_MAP["special_symbols"]:
                tokens_prior_to_error.append(self.TOKEN_MAP["special_symbols"][tok])
            elif self.is_integer(tok):
                tokens_prior_to_error.append(self.TOKEN_MAP["integer"])
            elif self.is_identifier(tok):
                tokens_prior_to_error.append(self.TOKEN_MAP["identifier"])
            elif tok.isspace():
                continue # don't print any token
            else:
                tokens_prior_to_error.append(self.TOKEN_MAP["error_token"])

        print(f"ERROR: Invalid token encountered: '{invalid_token}'")
        print("Tokens prior to error:", tokens_prior_to_error)
        exit(1)


    def getToken(self):
        """
        Retrieves the next token from the token stream.

        This returns a token value between 1 and 32 if the current token is a valid Core
        token. Returns 33 if at the end of the file, and 34 for an illegal token.

        Returns:
            int: The current token value, which can be:
                 - 1 to 32 for valid Core tokens
                 - 33 for end-of-file token
                 - 34 for an error token
        """
        if not self._current_line:
            self._load_next_line()

        if self._current_token_value == self.TOKEN_MAP["end_of_file"]:
            return self._current_token_value

        if self._current_line_index >= len(self._current_line):
            self._current_token_value = self.TOKEN_MAP["end_of_file"]
            return self._current_token_value

        tok = self._current_line[self._current_line_index]

        if tok in self.TOKEN_MAP["reserved_words"]:
            self._current_token_value = self.TOKEN_MAP["reserved_words"][tok]
        elif tok in self.TOKEN_MAP["special_symbols"]:
            self._current_token_value = self.TOKEN_MAP["special_symbols"][tok]
        elif self.is_integer(tok):
            self._current_token_value = self.TOKEN_MAP["integer"]
        elif self.is_identifier(tok):
            self._current_token_value = self.TOKEN_MAP["identifier"]
        elif tok == "EOF":
            self._current_token_value = self.TOKEN_MAP["end_of_file"]
        elif tok.isspace():
            self._current_line_index += 1  # skip over whitespace token
            return self.getToken()  # recursively get the next token
        else:
            self._handle_invalid_token(tok)
            #self._current_token_value = self.TOKEN_MAP["error_token"]
            exit(1)

        return self._current_token_value

    def skipToken(self):
        """
        Moves the token cursor to the next token without returning anything.

        If there are no more tokens in the current line, it loads the next line
        from the input file and sets the cursor index to point to the first token.

        If the current token is end-of-file (33) or an error token (34), the cursor
        is not moved.

        Returns:
            None
        """
        # skip token if there are still some in the current line
        # otherwise reset and tokenize next line in file
        if (
            self._current_token_value == self.TOKEN_MAP["end_of_file"]
            or self._current_token_value == self.TOKEN_MAP["error_token"]
        ):
            return

        self._current_line_index += 1

        # If we have skipped past the last token, load the next line
        if self._current_line_index >= len(self._current_line):
            self._load_next_line()
            self._current_line_index = 0  # Reset index for new line

    def intVal(self):
        """
        Retrieves the value of the current token if it is an integer.

        If the current token is not an integer, it raises a ValueError.

        Returns:
            int: The value of the current integer token.

        Raises:
            ValueError: If the current token is not an integer.
        """
        if self._current_token_value != 31:
            raise ValueError("error in intVal(): token to process was not an integer.")

        # return current token, it should be an integer
        return int(self._current_line[self._current_line_index])

    def idName(self):
        """
        Retrieves the name of the current token if it is an identifier.

        If the current token is not an identifier, it raises a ValueError.

        Returns:
            str: The name of the current identifier token.

        Raises:
            ValueError: If the current token is not an identifier.
        """
        if self._current_token_value != 32:
            raise ValueError("error in idName(): token to process was not an identifier.")

        # return current token, it should be an identifier
        return self._current_line[self._current_line_index]

    # Private Functions
    def tokenizeLine(self, line):
        """
        Tokenizes the given line into a list of tokens, optimized for the specific
        symbols of the language.

        Args:
            line (str): The line of text to tokenize.

        Returns:
            List[str]: A list of tokens extracted from the line.
        """
        tokens = []
        current_token = ""
        i = 0

        # Lookup table for operators
        operators = {
            '&&': 2, '||': 2, '!=': 2, '==': 2, '<=': 2, '>=': 2,
            ';': 1, ',': 1, '=': 1, '!': 1, '[': 1, ']': 1, '(': 1, ')': 1,
            '+': 1, '-': 1, '*': 1, '<': 1, '>': 1
        }

        while i < len(line):
            char = line[i]

            if char in operators:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""

                # check for two-character operators
                if i + 1 < len(line) and line[i:i+2] in operators:
                    tokens.append(line[i:i+2])
                    i += 2
                else:
                    tokens.append(char)
                    i += 1
            elif char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""

                # capture consecutive whitespace as a single token
                whitespace = char
                i += 1
                while i < len(line) and line[i].isspace():
                    whitespace += line[i]
                    i += 1
                tokens.append(whitespace)
            else:
                current_token += char
                i += 1

        if current_token:
            tokens.append(current_token)

        return tokens

    def is_identifier(self, t):
        """
        Determines if the given token is a valid identifier.

        An identifier must start with a capital letter, and the rest can only be
        capital letters or numbers.

        Args:
            t (str): The token to check.

        Returns:
            bool: True if the token is a valid identifier, False otherwise.
        """
        if not t:
            return False

        if not t[0].isupper():
            return False

        for char in t[1:]:
            if not (char.isupper() or char.isdigit()):
                return False

        return True

    def is_integer(self, t):
        """
        Determines if the given token is a valid unsigned integer.

        Args:
            t (str): The token to check.

        Returns:
            bool: True if the token represents a valid unsigned integer, False otherwise.
        """
        if not t.isdigit():
            return False

        return int(t) >= 0

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print(f"Usage: {sys.argv[0]} file.core")
#         exit(1)

#     file = sys.argv[1]
#     if os.path.exists(file):
#         print(f"Tokenizing core source: {file}")
#         tokenizer = Tokenizer(file)
#     else:
#         print(f"ERROR Does file {file} exist?")
#         exit(1)

#     token_vals = []
#     while True:
#         token = tokenizer.getToken()
#         token_vals.append(token)
#         if token == 33:  # EOF token
#             break
#         tokenizer.skipToken()

#     print(*token_vals)
