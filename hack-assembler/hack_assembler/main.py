from typing import cast
import json
from hack_assembler.lexer import Lexer
from hack_assembler.parser import Parser
from hack_assembler.semantic_analyzer import SemanticAnalyzer
from hack_assembler.translator import Translator

if __name__ == '__main__':
    code = """@R0
  D=M
  @R1
  D=D-M
  // If (D > 0) goto ITSR0
  @ITSR0
  D;JGT
  // Its R1
  @R1
  D=M
  @OUTPUT_D
  0;JMP
(ITSR0)
  @R0
  D=M
(OUTPUT_D)
  @R2
  M=D
(END)
  @END
  0;JMP"""
    lexer = Lexer(
        text=code
    )
    parser = Parser(lexer=lexer)

    ast = parser.parse()
    sematic_analyzer = SemanticAnalyzer(ast=ast)

    symbol_table = sematic_analyzer.analyze()

    translator = Translator(
        ast=ast,
        symbol_table=symbol_table
    )
    print(translator.translate())
