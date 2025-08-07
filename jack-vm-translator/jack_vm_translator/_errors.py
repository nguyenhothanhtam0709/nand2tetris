from typing import List, Optional, Union
from _token import Token, TokenType


class Error(RuntimeError):
    def __init__(self, message: Optional[str] = None):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return self.message


class LexerError(Error):
    pass


class ParserError(Error):
    pass


class UnexpectedTokenError(ParserError):
    def __init__(self, token: Token, expected: Optional[Union[TokenType, List[TokenType]]] = None):
        message = ''
        if expected is None:
            message = f'Unexpected token {token}'
        else:
            expected_str = expected.value if isinstance(
                expected, TokenType) else ",".join(map(str, expected))
            message = f'Expect {expected_str} - provide {token}'
        super().__init__(message=message)
