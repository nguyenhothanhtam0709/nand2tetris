from hack_assembler.tokens import Token, TokenType
from hack_assembler.lexer import Lexer
from hack_assembler.ast import AstNode, ProgramNode, SymbolDeclarationNode, AInstructionNode, CInstructionNode
from hack_assembler.errors import UnexpectedTokenError
from hack_assembler.constants import DEST_MNEMONICS, COMP_MNEMONICS, JUMP_MNEMONICS


class Parser(object):

    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Token = self._lexer.get_next_token()

    def parse(self) -> ProgramNode:
        return self._program()

    def _program(self) -> ProgramNode:
        instructions: list[AstNode] = []

        while True:
            match self._current_token.type:
                case TokenType.EOF:
                    pass

                case TokenType.EOL:
                    pass

                case TokenType.LPAREN:
                    # Symbol declaration
                    self._eat(TokenType.LPAREN)
                    token = self._current_token
                    self._eat(TokenType.SYMBOL)
                    self._eat(TokenType.RPAREN)
                    instructions.append(SymbolDeclarationNode(token=token))

                case TokenType.AT_SIGN:
                    # A instruction
                    self._eat(TokenType.AT_SIGN)
                    token = self._current_token
                    self._eat(TokenType.SYMBOL)
                    instructions.append(AInstructionNode(token=token))

                case TokenType.MNEMONIC:
                    # C instruction
                    dest: Token | None = None
                    comp: Token | None = None
                    jump: Token | None = None

                    token = self._current_token
                    self._eat(TokenType.MNEMONIC)

                    if token.value in DEST_MNEMONICS and self._current_token.type == TokenType.EQUAL_SIGN:
                        dest = token
                        self._eat(TokenType.EQUAL_SIGN)

                        token = self._current_token
                        self._eat(TokenType.MNEMONIC)

                    if token.value in COMP_MNEMONICS:
                        comp = token

                    if self._current_token.type == TokenType.SEMICOLON:
                        self._eat(TokenType.SEMICOLON)

                        jump = self._current_token if self._current_token.value in JUMP_MNEMONICS else None
                        self._eat(TokenType.MNEMONIC)

                    if comp is None and (dest is None or jump is None):
                        raise UnexpectedTokenError(token=self._current_token)

                    instructions.append(CInstructionNode(
                        comp=comp,
                        dest=dest,
                        jump=jump
                    ))

                case _:
                    raise UnexpectedTokenError(
                        token=self._current_token,
                        expected=[TokenType.LPAREN,
                                  TokenType.AT_SIGN, TokenType.MNEMONIC]
                    )

            if self._current_token.type == TokenType.EOF:
                break
            else:
                self._eat(TokenType.EOL)  # End of single instruction

        self._eat(TokenType.EOF)  # End of program

        return ProgramNode(instructions=instructions)

    def _eat(self, token_type: TokenType) -> None:
        """
        Compare the current token type with the passed token
        type and if they match then "eat" the current token
        and assign the next token to the self._current_token,
        otherwise raise and exception.
        """
        if self._current_token.type == token_type:
            self._current_token = self._lexer.get_next_token()
        else:
            raise UnexpectedTokenError(
                token=self._current_token,
                expected=token_type
            )
