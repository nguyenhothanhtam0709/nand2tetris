from uuid import uuid4
from _node_visitor import NodeVisitor
from _ast_ import ProgramNode, ArithLogicCmdNode, StackCmdNode
from _constants import VMCommand, VMMemorySegment, SP, THIS, THAT, ARG, LCL
from _errors import Error


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
