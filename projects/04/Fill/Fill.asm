// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
//// Pseudo code
// LOOP:
//    if RAM[KBD] > 0 goto MAKE_BLACK_SCREEN
//    goto MAKE_WHITE_SCREEN
// 
// MAKE_BLACK_SCREEN:
//    if RAM[SCREEN] = -1 goto LOOP // screen is already black
//    i=SCREEN
// 
// BLACK_SCREEN_LOOP:
//    if i >= KBD goto LOOP
// 
//    RAM[i]=-1
//    i=i+1
// 
//    goto BLACK_SCREEN_LOOP
// 
// MAKE_WHITE_SCREEN:
//    if RAM[SCREEN] = 0 goto LOOP // screen is already white
//    i=SCREEN
// 
// WHITE_SCREEN_LOOP:
//    if i >= KBD goto LOOP
// 
//    RAM[i]=0
//    i=i+1
// 
//    goto WHITE_SCREEN_LOOP
//// 


(LOOP)
    @KBD
    D=M
    @MAKE_BLACK_SCREEN
    D;JGT

    @MAKE_WHITE_SCREEN
    0;JMP


(MAKE_BLACK_SCREEN)
@SCREEN
D=M
@LOOP
D;JLT

@SCREEN
D=A
@i
M=D // i=16384 (base address of screen memory map in RAM)

(BLACK_SCREEN_LOOP)
    @i
    D=M
    @KBD
    D=D-A
    @LOOP
    D;JGE

    @i
    A=M
    M=-1

    @i
    M=M+1

    @BLACK_SCREEN_LOOP
    0;JMP

(MAKE_WHITE_SCREEN)
@SCREEN
D=M
@LOOP
D;JEQ

@SCREEN
D=A
@i
M=D // i=16384 (base address of screen memory map in RAM)

(WHITE_SCREEN_LOOP)
    @i
    D=M
    @KBD
    D=D-A
    @LOOP
    D;JGE

    @i
    A=M
    M=0

    @i
    M=M+1

    @WHITE_SCREEN_LOOP
    0;JMP

(END)
    @END
    0;JMP