from hack_assembler.constants import MNEMONICS
from hack_assembler.tokens import Token, TokenType
from hack_assembler.errors import LexerError


class Lexer(object):
    def __init__(self, text: str):
        self._text = text

        self._pos: int = 0
        """Current character's index"""

        self._current_char: str | None = self._text[self._pos]
        """Current character"""

        self._current_line: int = 1
        self._current_column: int = 1

    def _is_valid_subsequent_symbol_char(self, char: str) -> bool:
        return char is not None and char.isalnum() or char in ['_', '.', '$', ':']

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

    def _peek(self, n: int = 1) -> str | None:
        """
        Peeking into the **_text** buffer without actually consuming the next **n** character.
        """
        peek_pos = self._pos + n
        if peek_pos > len(self._text) - 1:
            return None
        else:
            return self._text[peek_pos]

    def _skip_white_space(self) -> None:
        while self._current_char is not None and self._current_char.isspace():
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
                     value=char,
                     line=line,
                     column=column)

    def _symbol(self) -> Token:
        line = self._current_line
        column = self._current_column
        char = ''
        while self._current_char is not None and self._is_valid_subsequent_symbol_char(self._current_char):
            char += self._current_char
            self._advance()

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
                char = self._current_char
                self._advance()

                return Token(
                    type=TokenType.EOL,
                    value=char,
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

            if self._current_char == '@':
                line = self._current_line
                column = self._current_column
                self._advance()
                return Token(type=TokenType.AT_SIGN,
                             value='@',
                             line=line,
                             column=column)

            if self._current_char == '(':
                line = self._current_line
                column = self._current_column
                self._advance()
                return Token(type=TokenType.LPAREN,
                             value='(',
                             line=line,
                             column=column)

            if self._current_char == ')':
                line = self._current_line
                column = self._current_column
                self._advance()
                return Token(type=TokenType.RPAREN,
                             value=')',
                             line=line,
                             column=column)

            if self._current_char == '=':
                line = self._current_line
                column = self._current_column
                self._advance()
                return Token(type=TokenType.EQUAL_SIGN,
                             value='=',
                             line=line,
                             column=column)

            if self._current_char == ';':
                line = self._current_line
                column = self._current_column
                self._advance()
                return Token(type=TokenType.SEMICOLON,
                             value=';',
                             line=line,
                             column=column)

            # region Handle mnemonics
            if (
                self._peek() is not None and self._peek(2) is not None and
                (
                    (self._current_char in ['A', 'M', 'D']
                     and self._peek() in ['+', '-', '|', '&']
                     and self._peek(2) in ['1', 'A', 'M', 'D']
                     and (self._current_char + self._peek() + self._peek(2)) in MNEMONICS)
                    or (
                    (self._current_char + self._peek() + self._peek(2)) in MNEMONICS
                    and not self._is_valid_subsequent_symbol_char(self._peek(3))
                    )
                )
            ):
                line = self._current_line
                column = self._current_column
                char = self._current_char
                self._advance()
                char += self._current_char
                self._advance()
                char += self._current_char
                self._advance()
                return Token(type=TokenType.MNEMONIC,
                             value=char,
                             line=line,
                             column=column)

            if (
                self._peek() is not None and
                (
                    (self._current_char == '-' and self._peek()
                     in ['1', 'A', 'M', 'D'])
                    or (self._current_char == '!' and self._peek() in ['A', 'M', 'D'])
                    or (
                    ((self._current_char == 'A' and self._peek() in ['M', 'D'])
                     or (self._current_char == 'M' and self._peek() == 'D'))
                    and not self._is_valid_subsequent_symbol_char(self._peek(2))
                    )
                )
            ):
                line = self._current_line
                column = self._current_column
                char = self._current_char
                self._advance()
                char += self._current_char
                self._advance()
                return Token(type=TokenType.MNEMONIC,
                             value=char,
                             line=line,
                             column=column)

            if (
                (self._current_char in ['0', '1']
                 and (not self._peek().isdigit()))
                or (
                    self._current_char in [
                        'A', 'M', 'D'] and not self._is_valid_subsequent_symbol_char(self._peek())
                )
            ):
                line = self._current_line
                column = self._current_column
                char = self._current_char
                self._advance()
                return Token(type=TokenType.MNEMONIC,
                             value=char,
                             line=line,
                             column=column)
            # endregion

            if self._current_char.isdigit():
                return self._integer()

            if self._current_char.isalpha() or self._current_char in ['_', '.', '$', ':']:
                return self._symbol()

            raise LexerError(
                message=f'Lexer error on character \'{self._current_char}\' at line {self._current_line}, column {self._current_column}'
            )

        return Token(type=TokenType.EOF,
                     value='',
                     line=self._current_line,
                     column=self._current_column)
