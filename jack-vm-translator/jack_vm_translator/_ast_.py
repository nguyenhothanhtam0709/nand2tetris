from abc import ABC
from enum import Enum
from typing import List
from _token import Token


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
