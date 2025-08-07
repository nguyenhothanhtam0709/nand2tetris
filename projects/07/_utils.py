from _constants import ARITH_LOGIC_COMMANDS, VMCommand, VMMemorySegment


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
