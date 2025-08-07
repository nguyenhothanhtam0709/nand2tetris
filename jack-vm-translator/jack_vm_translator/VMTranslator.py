import argparse
from pathlib import Path
from typing import cast
from _errors import Error
from _lexer import Lexer
from _parser import Parser
from _code_gen import CodeGenerator


def main() -> None:
    """
    Entrypoint
    """
    parser = argparse.ArgumentParser(
        description="Simple Jack vm translator.")
    parser.add_argument("input", help="Path to input file")
    args = parser.parse_args()

    input_file_path = args.input

    if not cast(str, input_file_path).endswith('.vm'):
        raise Error(f'Invalid Jack vm bytecode file: {input_file_path}')

    output_file_path = cast(str, input_file_path).replace(".vm", ".asm")

    with open(Path(input_file_path).resolve(), "r") as infile:
        vm_code = infile.read()

        lexer = Lexer(text=vm_code)
        # token = lexer.get_next_token()
        # while token.type != TokenType.EOF:
        #     print(token)
        #     token = lexer.get_next_token()
        parser = Parser(lexer=lexer)
        # print(parser.parse())
        code_generator = CodeGenerator(ast=parser.parse())

        with open(Path(output_file_path).resolve(), "w") as outfile:
            outfile.write(code_generator.generate_asm_code())


if __name__ == "__main__":
    main()
