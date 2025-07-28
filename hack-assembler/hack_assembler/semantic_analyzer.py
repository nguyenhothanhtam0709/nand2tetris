from hack_assembler.ast_visitor import NodeVisitor
from hack_assembler.ast import ProgramNode, AInstructionNode, CInstructionNode, SymbolDeclarationNode
from hack_assembler.symbol_table import SymbolTable


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, ast: ProgramNode):
        super().__init__()
        self._ast = ast
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
        pass

    def _visit_CInstructionNode(self, node: CInstructionNode) -> None:
        pass

    def _visit_SymbolDeclarationNode(self, node: SymbolDeclarationNode) -> None:
        pass
