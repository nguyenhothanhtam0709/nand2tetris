DEST_MNEMONICS = [
    "M",
    "D",
    "MD",
    "A",
    "AM",
    "AD",
    "AMD"
]

COMP_MNEMONICS = [
    "0",
    "1",
    "-1",
    "D",
    "A", "M",
    "!D",
    "!A", "!M",
    "-D",
    "-A", "-M",
    "D+1",
    "A+1", "M+1",
    "D-1",
    "A-1", "M-1",
    "D+A", "D+M",
    "D-A", "D-M",
    "A-D", "M-D",
    "D&A", "D&M",
    "D|A", "D|M"
]

JUMP_MNEMONICS = [
    "JGT",
    "JEQ",
    "JGE",
    "JLT",
    "JNE",
    "JLE",
    "JMP"
]

MNEMONICS = list(set(DEST_MNEMONICS + COMP_MNEMONICS + JUMP_MNEMONICS))
