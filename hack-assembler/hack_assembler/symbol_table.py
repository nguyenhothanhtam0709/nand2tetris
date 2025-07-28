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

    def define(self, symbol: DeclaredSymbol) -> None:
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str) -> Symbol | None:
        return self._symbols[name]
