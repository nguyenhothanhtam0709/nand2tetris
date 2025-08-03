from abc import ABC
import argparse
from enum import Enum
from pathlib import Path
from typing import cast
from uuid import uuid4
from typing import Optional, Union, Set, List

# region errors


class Error(RuntimeError):
    def __init__(self, message: Optional[str] = None):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return self.message


class LexerError(Error):
    pass
# endregion


# region constant
SP: str = 'SP'
LCL: str = 'LCL'
ARG: str = 'ARG'
THIS: str = 'THIS'
THAT: str = 'THAT'

STACK_BASE_ADDRESS: int = 256
TEMP_BASE_ADDRESS: int = 15

TEMP_SEGMENT_MAX_SIZE: int = 8
POINTER_SEGMENT_MAX_SIZE: int = 2


class VMCommand(Enum):
    """
    VM commands
    """
    # region Arithmetic/Logical commands
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"
    # endregion

    # region Memory access commands
    PUSH = "push"
    POP = "pop"
    # endregion

    # region Program flow commands
    LABEL = "label"
    GOTO = "goto"
    IF_GOTO = "if-goto"
    # endregion

    # region Function calling commands
    FUNCTION = "function"
    CALL = "call"
    RETURN = "return"
    # endregion


class VMMemorySegment(Enum):
    """
    VM memory segments
    """
    ARGUMENT = "argument"
    LOCAL = "local"
    STATIC = "static"
    CONSTANT = "constant"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


ARITH_LOGIC_COMMANDS: Set[str] = {
    VMCommand.ADD.value,
    VMCommand.SUB.value,
    VMCommand.NEG.value,
    VMCommand.EQ.value,
    VMCommand.GT.value,
    VMCommand.LT.value,
    VMCommand.AND.value,
    VMCommand.OR.value,
    VMCommand.NOT.value
}
# endregion

# region utils


def is_vm_command_keyword(kw: str) -> bool:
    """
    Test if **kw** is a Jack VM command keyword or not
    """
    return kw in VMCommand._value2member_map_


def is_stack_cmd_keyword(kw: str) -> bool:
    return kw in [VMCommand.PUSH.value, VMCommand.POP.value]


def is_arith_logic_cmd_keyword(kw: str) -> bool:
    return kw in ARITH_LOGIC_COMMANDS


def is_vm_segment_keyword(kw: str) -> bool:
    """
    Test if **kw** is a Jack VM memory segment keyword or not
    """
    return kw in VMMemorySegment._value2member_map_
# endregion

# region token


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
# endregion

# region lexer


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
# endregion

# region ast


class AstNodeType(Enum):
    PROGRAM = "PROGRAM"
    STACK_COMMAND = 'STACK_COMMAND'
    ARITH_LOGIC_COMMAND = 'ARITH_LOGIC_COMMAND'

    MEM_SEGMENT = "MEM_SEGMENT"


class AstNode(ABC):
    def __init__(self, type: AstNodeType) -> None:
        super().__init__()
        self.type = type


class MemSegmentNode(AstNode):
    def __init__(self, segment: Token, idx: Token) -> None:
        super().__init__(type=AstNodeType.MEM_SEGMENT)
        self.segment = segment
        self.idx = idx

    def __str__(self) -> str:
        return f'{self.type.value} [{self.segment.value} {self.idx.value}]'


class CmdNode(AstNode):
    def __init__(self, type: AstNodeType, cmd: Token):
        super().__init__(type=type)
        self.cmd = cmd

    def __str__(self) -> str:
        return f'{self.type.value} [{self.cmd.value}]'


class StackCmdNode(CmdNode):
    def __init__(self, cmd: Token, segment: MemSegmentNode):
        super().__init__(type=AstNodeType.STACK_COMMAND, cmd=cmd)
        self.segment = segment

    def __str__(self) -> str:
        return f'{super().__str__()}\n\t\t{self.segment}'


class ArithLogicCmdNode(CmdNode):
    def __init__(self, cmd: Token):
        super().__init__(type=AstNodeType.ARITH_LOGIC_COMMAND, cmd=cmd)


class ProgramNode(AstNode):
    def __init__(self, commands: List[AstNode]) -> None:
        super().__init__(type=AstNodeType.PROGRAM)
        self.commands = commands

    def __str__(self) -> str:
        char = f'{self.type.value}'
        for cmd in self.commands:
            char += f'\n\t{cmd}'
        return char
# endregion

# region ast visitor


class NodeVisitor(ABC):
    def _visit(self, node: AstNode):
        visitor = getattr(
            self, f'_visit_{type(node).__name__}', self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node: AstNode):
        raise Error(f'No visit method found for {type(node).__name__}')
# endregion

# region parser


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

# endregion


# region code generator
class CodeGenerator(NodeVisitor):
    """
    Generate Hack assembly from AST of Jack vm bytecode
    """

    def __init__(self, ast: ProgramNode):
        super().__init__()
        self._ast = ast

    def generate_asm_code(self) -> str:
        return self._visit(self._ast)

    def _visit_ProgramNode(self, node: ProgramNode) -> str:
        machine_codes = ''
        for cmd in node.commands:
            c = self._visit(cmd)
            if c is not None:
                machine_codes += f'\n{c}'
        return machine_codes.strip()

    def _visit_ArithLogicCmdNode(self, node: ArithLogicCmdNode) -> str:
        cmd = node.cmd
        if cmd.value in [VMCommand.NEG.value, VMCommand.NOT.value]:
            # Unary arithmetic/logic command
            return f"""
// {cmd.value}
@{SP}
M=M-1
A=M
D={'-M' if cmd.value == VMCommand.NEG.value else "!M"}
@{SP}
A=M
M=D
@{SP}
M=M+1
""".strip()

        # Binary arithmetic/logic command
        asm_code = f"""
// {cmd.value}
@{SP}
M=M-1
A=M
D=M
@{SP}
M=M-1
A=M
""".strip()

        if cmd.value in [VMCommand.GT.value, VMCommand.LT.value, VMCommand.EQ.value]:
            label_id = uuid4()
            TRUE_BRANCH_SYMBOL = f'{cmd.value.upper()}_TRUE_{label_id}'
            # FALSE_BRANCH_SYMBOL = f'{cmd.value.upper()}_FALSE_{label_id}'
            END_BRANCH_SYMBOL = f'{cmd.value.upper()}_END_{label_id}'

            logic_code = ''
            if cmd.value == VMCommand.GT.value:
                logic_code = f"""
D=M-D
@{TRUE_BRANCH_SYMBOL}
D;JGT
""".strip()
            elif cmd.value == VMCommand.LT.value:
                logic_code = f"""
D=M-D
@{TRUE_BRANCH_SYMBOL}
D;JLT
""".strip()
            else:
                logic_code = f"""
D=M-D
@{TRUE_BRANCH_SYMBOL}
D;JEQ
""".strip()

            return f"""
{asm_code}
{logic_code}
@{SP}
A=M
M=0
@{END_BRANCH_SYMBOL}
0;JMP
({TRUE_BRANCH_SYMBOL})
@{SP}
A=M
M=-1
({END_BRANCH_SYMBOL})
@{SP}
M=M+1
""".strip()

        # region add, sub, and, or
        al_sym = ''
        if cmd.value == VMCommand.ADD.value:
            al_sym = 'M=D+M'
        elif cmd.value == VMCommand.SUB.value:
            al_sym = 'M=M-D'
        elif cmd.value == VMCommand.AND.value:
            al_sym = 'M=D&M'
        elif cmd.value == VMCommand.OR.value:
            al_sym = 'M=D|M'

        return f"""
{asm_code}
{al_sym}
@{SP}
M=M+1
""".strip()

    def _visit_StackCmdNode(self, node: StackCmdNode) -> str:
        cmd = node.cmd
        if cmd.value == VMCommand.PUSH.value:
            return self._gen_asm_for_push_cmd(node)
        elif cmd.value == VMCommand.POP.value:
            return self._gen_asm_for_pop_cmd(node)

    def _gen_asm_for_push_cmd(self, node: StackCmdNode) -> str:
        cmd = node.cmd
        segment_node = node.segment

        comment_code = f"// {cmd.value} {segment_node.segment.value} {segment_node.idx.value}".strip()
        base_push_asm_code = f"""
@{SP}
A=M
M=D
@{SP}
M=M+1
""".strip()

        if segment_node.segment.value == VMMemorySegment.STATIC.value:
            return f"""
{comment_code}
@{segment_node.idx.value}
D=M
{base_push_asm_code}
""".strip()
        if segment_node.segment.value == VMMemorySegment.CONSTANT.value:
            return f"""
{comment_code}
@{segment_node.idx.value}
D=A
{base_push_asm_code}
""".strip()
        if segment_node.segment.value in [VMMemorySegment.ARGUMENT.value, VMMemorySegment.LOCAL.value, VMMemorySegment.THIS.value, VMMemorySegment.THAT.value]:
            ptr = ''
            if segment_node.segment.value == VMMemorySegment.THIS.value:
                ptr = THIS
            elif segment_node.segment.value == VMMemorySegment.THAT.value:
                ptr = THAT
            elif segment_node.segment.value == VMMemorySegment.ARGUMENT.value:
                ptr = ARG
            elif segment_node.segment.value == VMMemorySegment.LOCAL.value:
                ptr = LCL

            return f"""
{comment_code}
@{ptr}
D=M
@{segment_node.idx.value}
D=D+A
A=D
D=M
{base_push_asm_code}
""".strip()
        if segment_node.segment.value == VMMemorySegment.POINTER.value:
            ptr = ''
            if segment_node.idx.value == 0:
                ptr = THIS
            elif segment_node.idx.value == 1:
                ptr = THAT
            else:
                raise Error(
                    f'Invalid memory location {segment_node.idx.value} for pointer segment')

            return f"""
{comment_code}
@{ptr}
D=M
{base_push_asm_code}
""".strip()
        if segment_node.segment.value == VMMemorySegment.TEMP.value:
            ptr = f'R{segment_node.idx.value+5}'
            return f"""
{comment_code}
@{ptr}
D=M
{base_push_asm_code}
""".strip()
        else:
            raise Error(
                f'Invalid memory segment {segment_node.segment.value} for stack command `push`')

    def _gen_asm_for_pop_cmd(self, node: StackCmdNode) -> str:
        cmd = node.cmd
        segment_node = node.segment

        comment_code = f"// {cmd.value} {segment_node.segment.value} {segment_node.idx.value}".strip()
        base_pop_asm_code = f"""
@{SP}
M=M-1
A=M
D=M
""".strip()

        if segment_node.segment.value == VMMemorySegment.STATIC.value:
            return f"""
{comment_code}
{base_pop_asm_code}
@{segment_node.idx.value}
M=D
""".strip()
        if segment_node.segment.value in [VMMemorySegment.ARGUMENT.value, VMMemorySegment.LOCAL.value, VMMemorySegment.THIS.value, VMMemorySegment.THAT.value]:
            ptr = ''
            if segment_node.segment.value == VMMemorySegment.THIS.value:
                ptr = THIS
            elif segment_node.segment.value == VMMemorySegment.THAT.value:
                ptr = THAT
            elif segment_node.segment.value == VMMemorySegment.ARGUMENT.value:
                ptr = ARG
            elif segment_node.segment.value == VMMemorySegment.LOCAL.value:
                ptr = LCL

            return f"""
{comment_code}
@{segment_node.idx.value}
D=A
@{ptr}
D=D+M
@R13
M=D
{base_pop_asm_code}
@R13
A=M
M=D
""".strip()
        if segment_node.segment.value == VMMemorySegment.POINTER.value:
            ptr = ''
            if segment_node.idx.value == 0:
                ptr = THIS
            elif segment_node.idx.value == 1:
                ptr = THAT
            else:
                raise Error(
                    f'Invalid memory location {segment_node.idx.value} for pointer segment')

            return f"""
{comment_code}
{base_pop_asm_code}
@{ptr}
M=D
""".strip()
        if segment_node.segment.value == VMMemorySegment.TEMP.value:
            ptr = f'R{segment_node.idx.value+5}'
            return f"""
{comment_code}
{base_pop_asm_code}
@{ptr}
M=D
""".strip()
        else:
            raise Error(
                f'Invalid memory segment {segment_node.segment.value} for stack command `pop`')
# endregion


def main() -> None:
    """
    Entrypoint
    """
    parser = argparse.ArgumentParser(
        description="Simple Jack vm translator.")
    parser.add_argument("input", help="Path to input file")
    args = parser.parse_args()

    input_file_path = args.input

    if not cast(str, input_file_path).endswith('.vm'):
        raise Error(f'Invalid Jack vm bytecode file: {input_file_path}')

    output_file_path = cast(str, input_file_path).replace(".vm", ".asm")

    with open(Path(input_file_path).resolve(), "r") as infile:
        vm_code = infile.read()

        lexer = Lexer(text=vm_code)
        # token = lexer.get_next_token()
        # while token.type != TokenType.EOF:
        #     print(token)
        #     token = lexer.get_next_token()
        parser = Parser(lexer=lexer)
        # print(parser.parse())
        code_generator = CodeGenerator(ast=parser.parse())

        with open(Path(output_file_path).resolve(), "w") as outfile:
            outfile.write(code_generator.generate_asm_code())


if __name__ == "__main__":
    main()
