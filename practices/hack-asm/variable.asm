// Computes: temp = RAM[1]
//           RAM[1] = RAM[0]
//           RAM[0] = RAM[1]

@R1
D=M
@temp
M=D

@R0
D=M
@R1
M=D

@temp
D=M
@R0
M=D

(END)
@END
0;JMP