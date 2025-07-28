
class Error(RuntimeError):
    def __init__(self, message: str | None = None):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return self.message


class LexerError(Error):
    pass
