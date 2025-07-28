from abc import ABC
from hack_assembler.ast import AstNode
from hack_assembler.errors import Error


class NodeVisitor(ABC):
    def _visit(self, node: AstNode):
        visitor = getattr(
            self, f'_visit_{type(node).__name__}', self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node: AstNode):
        raise Error(f'No visit method found for {type(node).__name__}')
