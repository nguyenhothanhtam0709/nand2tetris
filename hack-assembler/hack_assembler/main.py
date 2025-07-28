from hack_assembler.lexer import Lexer
from hack_assembler.tokens import TokenType

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

    token = lexer.get_next_token()
    while token.type != TokenType.EOF:
        print(token)
        token = lexer.get_next_token()
    print(token)
