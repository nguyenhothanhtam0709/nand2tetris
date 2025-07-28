from hack_assembler.tokens import Token, TokenType


class Error(RuntimeError):
    def __init__(self, message: str | None = None):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return self.message


class LexerError(Error):
    pass


class ParserError(Error):
    pass


class UnexpectedTokenError(ParserError):
    def __init__(self, token: Token, expected: TokenType | list[TokenType] | None = None):
        super().__init__(
            f'Unexpected token {token}' if expected is None
            else f'Expect {expected.value if isinstance(expected, TokenType) else ','.join(map(str, expected))} - provide {token}')
