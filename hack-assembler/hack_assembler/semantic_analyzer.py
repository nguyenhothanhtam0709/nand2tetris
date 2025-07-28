from hack_assembler.ast_visitor import NodeVisitor
from hack_assembler.ast import ProgramNode, AInstructionNode, CInstructionNode, SymbolDeclarationNode
from hack_assembler.symbol_table import SymbolTable, DeclaredSymbol


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, ast: ProgramNode):
        super().__init__()
        self._ast = ast
        self._current_line: int = 0
        self._symbol_table = SymbolTable()

    def analyze(self) -> SymbolTable:
        """
        Analyzing the sematic of provided AST and build symbol table
        """
        self._visit(self._ast)
        return self._symbol_table

    def _visit_ProgramNode(self, node: ProgramNode) -> None:
        for instruction_node in node.instructions:
            self._visit(instruction_node)

    def _visit_AInstructionNode(self, node: AInstructionNode) -> None:
        self._current_line += 1

    def _visit_CInstructionNode(self, node: CInstructionNode) -> None:
        self._current_line += 1

    def _visit_SymbolDeclarationNode(self, node: SymbolDeclarationNode) -> None:
        if self._symbol_table.lookup(node.token.value) is None:
            self._symbol_table.define(DeclaredSymbol(
                name=node.token.value, value=self._current_line+1))
        else:
            # raise duplicated symbol error
            pass
