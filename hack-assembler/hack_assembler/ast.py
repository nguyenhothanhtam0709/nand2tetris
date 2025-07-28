from abc import ABC
from enum import Enum
from hack_assembler.tokens import Token


class AstNodeType(Enum):
    PROGRAM = "PROGRAM"
    A_INSTRUCTION = 'A_INSTRUCTION'
    C_INSTRUCTION = 'C_INSTRUCTION'
    SYMBOL_DECLARATION = 'SYMBOL_DECLARATION'


class AstNode(ABC):
    def __init__(self, type: AstNodeType) -> None:
        super().__init__()
        self.type = type


class ProgramNode(AstNode):
    def __init__(self, instructions: list[AstNode]) -> None:
        super().__init__(type=AstNodeType.PROGRAM)
        self.instructions = instructions

    def __str__(self) -> str:
        char = f'{self.type.value}'
        for instruction in self.instructions:
            char += f'\n    {instruction}'
        return char


class AInstructionNode(AstNode):
    def __init__(self, token: Token) -> None:
        super().__init__(type=AstNodeType.A_INSTRUCTION)
        self.token = token

    def __str__(self) -> str:
        return f'{self.type.value} @{self.token.value}'


class CInstructionNode(AstNode):
    def __init__(self,
                 comp: Token,
                 dest: Token | None = None,
                 jump: Token | None = None) -> None:
        super().__init__(type=AstNodeType.C_INSTRUCTION)
        self.dest = dest
        self.comp = comp
        self.jump = jump

    def __str__(self) -> str:
        return f'{self.type.value} {f'{self.dest.value}=' if self.dest is not None else ''}{self.comp.value}{f';{self.jump.value}' if self.jump is not None else ''}'


class SymbolDeclaration(AstNode):
    def __init__(self, token: Token) -> None:
        super().__init__(type=AstNodeType.SYMBOL_DECLARATION)
        self.token = token

    def __str__(self) -> str:
        return f'{self.type.value} ({self.token.value})'
