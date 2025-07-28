from abc import ABC
from collections import OrderedDict


class Symbol(ABC):
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value


class BuiltinSymbol(Symbol):
    pass


class DeclaredSymbol(Symbol):
    pass


class SymbolTable(object):
    def __init__(self):
        self._symbols: dict[str, Symbol] = OrderedDict()
        self._init_builtin_symbols()

    def define(self, symbol: DeclaredSymbol) -> None:
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str) -> Symbol | None:
        return self._symbols.get(name)

    def _init_builtin_symbols(self) -> None:
        for i in range(0, 16):
            self.define(DeclaredSymbol(f'R{i}', i))

        self.define(DeclaredSymbol('SP', 0))
        self.define(DeclaredSymbol('LCL', 1))
        self.define(DeclaredSymbol('ARG', 2))
        self.define(DeclaredSymbol('THIS', 3))
        self.define(DeclaredSymbol('THAT', 4))

        self.define(DeclaredSymbol('SCREEN', 16384))
        self.define(DeclaredSymbol('KBD', 24576))
