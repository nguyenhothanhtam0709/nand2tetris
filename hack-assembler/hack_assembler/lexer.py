from hack_assembler.constants import MNEMONICS
from hack_assembler.tokens import Token, TokenType


class LexerError(Exception):
    pass


class Lexer(object):
    def __init__(self, text: str):
        self._text = text

        self._pos: int = 0
        """Current character's index"""

        self._current_char: str | None = self._text[self._pos]
        """Current character"""

    def _is_valid_subsequent_symbol_char(self, char: str) -> bool:
        return char is not None and char.isalnum() or char in ['_', '.', '$', ':']

    def _advance(self) -> None:
        """
        Advance the **pos** pointer and set the **current_char** variable.
        """
        self._pos += 1
        if (self._pos > len(self._text) - 1):
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

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
        char = ''
        while self._current_char is not None and self._current_char.isdigit():
            char += self._current_char
            self._advance()
        return Token(type=TokenType.INTEGER, value=char)

    def _symbol(self) -> Token:
        char = ''
        while self._current_char is not None and self._is_valid_subsequent_symbol_char(self._current_char):
            char += self._current_char
            self._advance()

        return Token(
            type=TokenType.SYMBOL,
            value=char
        )

    def get_next_token(self) -> Token:
        """
        Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self._current_char is not None:
            if self._current_char == '\n':
                char = self._current_char
                self._advance()

                return Token(
                    type=TokenType.EOL,
                    value=char
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
                self._advance()
                return Token(type=TokenType.AT_SIGN, value='@')

            if self._current_char == '(':
                self._advance()
                return Token(type=TokenType.LPAREN, value='(')

            if self._current_char == ')':
                self._advance()
                return Token(type=TokenType.RPAREN, value=')')

            if self._current_char == '=':
                self._advance()
                return Token(type=TokenType.EQUAL_SIGN, value='=')

            if self._current_char == ';':
                self._advance()
                return Token(type=TokenType.SEMICOLON, value=';')

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
                char = self._current_char
                self._advance()
                char += self._current_char
                self._advance()
                char += self._current_char
                self._advance()
                return Token(type=TokenType.MNEMONIC, value=char)

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
                char = self._current_char
                self._advance()
                char += self._current_char
                self._advance()
                return Token(type=TokenType.MNEMONIC, value=char)

            if (
                (self._current_char in ['0', '1']
                 and (not self._peek().isdigit()))
                or (
                    self._current_char in [
                        'A', 'M', 'D'] and not self._is_valid_subsequent_symbol_char(self._peek())
                )
            ):
                char = self._current_char
                self._advance()
                return Token(type=TokenType.MNEMONIC, value=char)
            # endregion

            if self._current_char.isdigit():
                return self._integer()

            if self._current_char.isalpha() or self._current_char in ['_', '.', '$', ':']:
                return self._symbol()

            raise LexerError(
                message=f'Lexer error on character \'{self._current_char}\''
            )

        return Token(type=TokenType.EOF, value='')
