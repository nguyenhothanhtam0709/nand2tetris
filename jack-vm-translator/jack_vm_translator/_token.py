from enum import Enum
from typing import Optional, Union


class TokenType(Enum):
    SYMBOL = "SYMBOl"
    COMMAND = 'COMMAND'
    MEMORY_SEGMENT = "MEMORY_SEGMENT"

    INTEGER = "INTEGER"

    EOL = 'EOL'
    EOF = 'EOF'


class Token(object):
    def __init__(self,
                 type: TokenType,
                 value: Optional[Union[int, str]] = None,
                 line: Optional[int] = None,
                 column: Optional[int] = None):

        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        token_str = self.type.value if self.type in [
            TokenType.EOL, TokenType.EOF] else f'{self.type.value}, \'{self.value}\''
        return f'Token({token_str}, line {self.line}, column {self.column})'
