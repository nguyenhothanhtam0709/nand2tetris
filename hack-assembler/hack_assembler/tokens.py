from enum import Enum


class TokenType(Enum):
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    AT_SIGN = 'AT_SIGN'
    EQUAL_SIGN = 'EQUAL_SIGN'
    SEMICOLON = 'SEMICOLON'
    EOL = 'EOL'
    EOF = 'EOF'

    MNEMONIC = 'MNEMONIC'

    INTEGER = 'INTEGER'
    SYMBOL = 'SYMBOL'


class Token(object):
    def __init__(self,
                 type: TokenType,
                 value: int | str,
                 line: int | None = None,
                 column: int | None = None):

        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        token_str = self.type.value if self.type in [
            TokenType.EOL, TokenType.EOF] else f'{self.type.value}, \'{self.value}\''
        return f'Token({token_str}, line {self.line}, column {self.column})'
