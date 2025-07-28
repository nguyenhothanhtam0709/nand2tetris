from typing import cast
import argparse
from pathlib import Path
from hack_assembler.errors import Error
from hack_assembler.lexer import Lexer
from hack_assembler.tokens import TokenType
from hack_assembler.parser import Parser
from hack_assembler.semantic_analyzer import SemanticAnalyzer
from hack_assembler.translator import Translator


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simple Hack assembler.")
    parser.add_argument("input", help="Path to input file")
    parser.add_argument("output", help="Path to output file")
    args = parser.parse_args()

    input_file_path = args.input
    output_file_path = args.output

    if not cast(str, input_file_path).endswith('.asm'):
        raise Error(f'Invalid hack assembly file: {input_file_path}')

    if not cast(str, output_file_path).endswith('.hack'):
        raise Error(f'Invalid hack machine code file: {output_file_path}')

    with open(Path(input_file_path).resolve(), "r") as infile:
        asm_code = infile.read()

        lexer = Lexer(
            text=asm_code
        )
        parser = Parser(lexer=lexer)

        ast = parser.parse()
        sematic_analyzer = SemanticAnalyzer(ast=ast)

        symbol_table = sematic_analyzer.analyze()

        translator = Translator(
            ast=ast,
            symbol_table=symbol_table
        )
        machine_code = translator.translate()

        with open(Path(output_file_path).resolve(), "w") as outfile:
            outfile.write(machine_code)


if __name__ == '__main__':
    main()
#     code = """// This file is part of www.nand2tetris.org
# // and the book "The Elements of Computing Systems"
# // by Nisan and Schocken, MIT Press.
# // File name: projects/6/rect/RectL.asm

# // Symbol-less version of the Rect.asm program.
# // Designed for testing the basic version of the assembler.

# @0
# D=M
# @23
# D;JLE
# @16
# M=D
# @16384
# D=A
# @17
# M=D
# @17
# A=M
# M=-1
# @17
# D=M
# @32
# D=D+A
# @17
# M=D
# @16
# MD=M-1
# @10
# D;JGT
# @23
# 0;JMP
# """
#     lexer = Lexer(
#         text=code
#     )
#     # token = lexer.get_next_token()
#     # while token.type != TokenType.EOF:
#     #     print(token)
#     #     token = lexer.get_next_token()
#     parser = Parser(lexer=lexer)

#     ast = parser.parse()
#     sematic_analyzer = SemanticAnalyzer(ast=ast)

#     symbol_table = sematic_analyzer.analyze()

#     translator = Translator(
#         ast=ast,
#         symbol_table=symbol_table
#     )
#     print(translator.translate())
