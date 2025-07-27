# eBNF of Hack assembly language

```ebnf

program             : (symbol_decl | instruction) (EOL (symbol_decl | instruction))*

symbol_decl         : LPAREN SYMBOL RPAREN

instruction         : a_instruction | c_instruction

a_instruction       : AT_SIGN SYMBOL
                    | AT_SIGN INT

c_instruction       : (dest EQUAL_SIGN)? comp (SEMICOLON jump)?

dest                : "M"
                    | "D"
                    | "MD"
                    | "A"
                    | "AM"
                    | "AD"
                    | "AMD" ;

comp                : "0"
                    | "1"
                    | "-1"
                    | "D"
                    | "A" | "M"
                    | "!D"
                    | "!A" | "!M"
                    | "-D"
                    | "-A" | "-M"
                    | "D+1"
                    | "A+1" | "M+1"
                    | "D-1"
                    | "A-1" | "M-1"
                    | "D+A" | "D+M"
                    | "D-A" | "D-M"
                    | "A-D" | "M-D"
                    | "D&A" | "D&M"
                    | "D|A" | "D|M" ;

jump                : "JGT"
                    | "JEQ"
                    | "JGE"
                    | "JLT"
                    | "JNE"
                    | "JLE"
                    | "JMP" ;

SYMBOL              : ID

ID                  : ( [a-zA-Z] | '_' | '.' | '$' | ':' ) ( [a-zA-Z0-9] | '_' | '.' | '$' | ':' )*
INT                 : [0-9]+
LPAREN              : '('
RPAREN              : ')'
AT_SIGN             : '@'
EQUAL_SIGN          : '='
SEMICOLON           : ';'
EOL                 : '\n'
```
