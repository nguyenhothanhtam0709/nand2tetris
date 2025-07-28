from hack_assembler.ast_visitor import NodeVisitor
from hack_assembler.ast import ProgramNode, AInstructionNode, CInstructionNode, SymbolDeclarationNode
from hack_assembler.symbol_table import SymbolTable, DeclaredSymbol, Symbol
from hack_assembler.constants import DEST_MNEMONICS_TABLE, COMP_MNEMONICS_TABLE, JUMP_MNEMONICS_TABLE
from hack_assembler.tokens import TokenType


class CodeGenerator(NodeVisitor):
    """
    Generate Hack machine code from AST of Hack assembly language
    """

    def __init__(self, ast: ProgramNode, symbol_table: SymbolTable):
        super().__init__()

        self._ast = ast
        self._symbol_table = symbol_table
        self._allocatable_mem_ptr = 16

    def generate_binary_code(self) -> str:
        return self._visit(self._ast)

    def _visit_ProgramNode(self, node: ProgramNode) -> str:
        machine_codes = ''
        for instruction in node.instructions:
            c = self._visit(instruction)
            if c is not None:
                machine_codes += f'\n{c}'
        return machine_codes.strip()

    def _visit_AInstructionNode(self, node: AInstructionNode) -> str:
        return f'0{(self._resolve_symbol_to_value(node.token.value) if node.token.type == TokenType.SYMBOL else node.token.value):015b}'

    def _visit_CInstructionNode(self, node: CInstructionNode) -> str:
        return f'111{COMP_MNEMONICS_TABLE[node.comp.value]}{DEST_MNEMONICS_TABLE[node.dest.value if node.dest is not None else None]}{JUMP_MNEMONICS_TABLE[node.jump.value if node.jump is not None else None]}'

    def _visit_SymbolDeclarationNode(self, node: SymbolDeclarationNode) -> None:
        return None

    def _resolve_symbol_to_value(self, symbol_name: str) -> int:
        return self._resolve_symbol(symbol_name).value

    def _resolve_symbol(self, symbol_name: str) -> Symbol:
        symbol = self._symbol_table.lookup(symbol_name)
        if symbol is None:
            symbol = DeclaredSymbol(name=symbol_name, value=self._alloc())
            self._symbol_table.define(symbol=symbol)

        return symbol

    def _alloc(self) -> int:
        ptr = self._allocatable_mem_ptr
        self._allocatable_mem_ptr += 1
        return ptr
