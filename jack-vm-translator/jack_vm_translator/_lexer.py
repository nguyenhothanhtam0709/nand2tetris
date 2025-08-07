from typing import Optional
from _token import Token, TokenType
from _errors import LexerError
from _utils import is_vm_command_keyword, is_vm_segment_keyword


class Lexer(object):
    def __init__(self, text: str):
        self._text = text

        self._pos: int = 0
        """Current character's index"""

        self._current_char: Optional[str] = self._text[self._pos]
        """Current character"""

        self._current_line: int = 1
        self._current_column: int = 1

    def _advance(self) -> None:
        """
        Advance the **pos** pointer and set the **current_char** variable.
        """
        if self._current_char == '\n':
            self._current_column = 0
            self._current_line += 1

        self._pos += 1
        if (self._pos > len(self._text) - 1):
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]
            self._current_column += 1

    def _peek(self, n: int = 1) -> Optional[str]:
        """
        Peeking into the **_text** buffer without actually consuming the next **n** character.
        """
        peek_pos = self._pos + n
        if peek_pos > len(self._text) - 1:
            return None
        else:
            return self._text[peek_pos]

    def _skip_white_space(self) -> None:
        while self._current_char is not None and self._current_char.isspace() and self._current_char != '\n':
            self._advance()

    def _skip_one_line_comment(self) -> None:
        while self._current_char is not None and self._current_char != '\n':
            self._advance()

    def _integer(self) -> Token:
        line = self._current_line
        column = self._current_column
        char = ''
        while self._current_char is not None and self._current_char.isdigit():
            char += self._current_char
            self._advance()
        return Token(type=TokenType.INTEGER,
                     value=int(char),
                     line=line,
                     column=column)

    def _symbol(self) -> Token:
        line = self._current_line
        column = self._current_column
        char = ''
        while self._current_char is not None and self._current_char.isalpha():
            char += self._current_char
            self._advance()

        if is_vm_command_keyword(char):
            return Token(
                type=TokenType.COMMAND,
                value=char,
                line=line,
                column=column
            )

        if is_vm_segment_keyword(char):
            return Token(
                type=TokenType.MEMORY_SEGMENT,
                value=char,
                line=line,
                column=column
            )

        return Token(
            type=TokenType.SYMBOL,
            value=char,
            line=line,
            column=column
        )

    def get_next_token(self) -> Token:
        """
        Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self._current_char is not None:
            if self._current_char == '\n':
                line = self._current_line
                column = self._current_column
                self._advance()
                return Token(
                    type=TokenType.EOL,
                    line=line,
                    column=column
                )

            if self._current_char.isspace():
                self._skip_white_space()
                continue

            if self._current_char == '/' and self._peek() == '/':
                self._advance()
                self._advance()

                self._skip_one_line_comment()
                continue

            if self._current_char.isdecimal():
                return self._integer()

            if self._current_char.isalpha():
                return self._symbol()

            raise LexerError(
                message=f'Lexer error on character \'{self._current_char}\' at line {self._current_line}, column {self._current_column}'
            )

        return Token(
            type=TokenType.EOF,
            line=self._current_line,
            column=self._current_column
        )
