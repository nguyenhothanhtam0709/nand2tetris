from typing import cast
import json
from hack_assembler.lexer import Lexer
from hack_assembler.parser import Parser
from hack_assembler.ast import ProgramNode

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

    node = parser.parse()
    print(node)
    
