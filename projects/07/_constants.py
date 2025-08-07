
from enum import Enum
from typing import Set


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
