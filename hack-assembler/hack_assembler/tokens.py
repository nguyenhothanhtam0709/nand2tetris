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
    def __init__(self, type: TokenType, value: int | str):
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type.value})' if self.type in [TokenType.EOL, TokenType.EOF] else f'Token({self.type.value}, \'{self.value}\')'
