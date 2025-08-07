from typing import List
from _token import Token, TokenType
from _lexer import Lexer
from _ast_ import ProgramNode, CmdNode, StackCmdNode, MemSegmentNode, ArithLogicCmdNode
from _errors import UnexpectedTokenError
from _utils import is_stack_cmd_keyword, is_arith_logic_cmd_keyword


class Parser(object):
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Token = self._lexer.get_next_token()

    def parse(self) -> ProgramNode:
        return self._program()

    def _program(self) -> ProgramNode:
        cmds: List[CmdNode] = []

        while self._current_token.type != TokenType.EOF:
            self._eat(TokenType.EOL)
            if self._current_token.type == TokenType.EOL:
                continue
            if self._current_token.type == TokenType.EOF:
                continue
            if self._current_token.type == TokenType.COMMAND:
                cmds.append(self._cmd())
            else:
                raise UnexpectedTokenError(
                    token=self._current_token,
                    expected=[TokenType.LPAREN,
                              TokenType.AT_SIGN, TokenType.MNEMONIC]
                )

        self._eat(TokenType.EOF)
        return ProgramNode(commands=cmds)

    def _cmd(self) -> CmdNode:
        if is_stack_cmd_keyword(self._current_token.value):
            return self._stack_cmd()
        elif is_arith_logic_cmd_keyword(self._current_token.value):
            cmd = self._current_token
            self._eat(TokenType.COMMAND)
            return ArithLogicCmdNode(cmd=cmd)

    def _stack_cmd(self) -> StackCmdNode:
        cmd = self._current_token
        self._eat(TokenType.COMMAND)
        return StackCmdNode(cmd=cmd, segment=self._segment())

    def _segment(self) -> MemSegmentNode:
        segment_token = self._current_token
        self._eat(TokenType.MEMORY_SEGMENT)
        idx_token = self._current_token
        self._eat(TokenType.INTEGER)
        return MemSegmentNode(segment=segment_token, idx=idx_token)

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
