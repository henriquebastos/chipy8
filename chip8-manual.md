CHIP-8 Manual
=============


Instruction Table
-----------------

    OP      Description
    ----    -----------
    0NNN    Execute machine language subroutine at address NNN
    00E0    Clear the screen
    00EE    Return from a subroutine
    1NNN    Jump to address NNN
    2NNN    Execute subroutine starting at address NNN
    3XNN    Skip the following instruction if the value of register VX
            equals NN
    4XNN    Skip the following instruction if the value of register VX
            is not equal to NN
    5XY0    Skip the following instruction if the value of register VX
            is equal to the value of register VY
    6XNN    Store number NN in register VX
    7XNN    Add the value NN to register VX
    8XY0    Store the value of register VY in register VX
    8XY1    Set VX to VX OR VY
    8XY2    Set VX to VX AND VY
    8XY3    Set VX to VX XOR VY
    8XY4    Add the value of register VY to register VX
            Set VF to 01 if a carry occurs
            Set VF to 00 if a carry does not occur
    8XY5    Subtract the value of register VY from register VX
            Set VF to 00 if a borrow occurs
            Set VF to 01 if a borrow does not occur
    8XY6    Store the value of register VY shifted right one bit in  VX
            Set VF to the least significant bit prior to the shift
    8XY7    Set register VX to the value of VY minus VX
            Set VF to 00 if a borrow occurs
            Set VF to 01 if a borrow does not occur
    8XYE    Store the value of register VY shifted left one bit in VX
            Set VF to the most significant bit prior to the shift
    9XY0    Skip the following instruction if the value of register VX
            is not equal to the value of register VY
    ANNN    Store memory address NNN in register I
    BNNN    Jump to address NNN + V0
    CXNN    Set VX to a random number with a mask of NN
    DXYN    Draw a sprite at position VX, VY with N bytes of sprite data
            starting at the address stored in I
            Set VF to 01 if any set pixels are changed to unset, and 00
            otherwise
    EX9E    Skip the following instruction if the key corresponding to
            the hex value currently stored in register VX is pressed
    EXA1    Skip the following instruction if the key corresponding to
            the hex value currently stored in register VX is not pressed
    FX07    Store the current value of the delay timer in register VX
    FX0A    Wait for a keypress and store the result in register VX
    FX15    Set the delay timer to the value of register VX
    FX18    Set the sound timer to the value of register VX
    FX1E    Add the value stored in register VX to register I
    FX29    Set I to the memory address of the sprite data corresponding
             to the hexadecimal digit stored in register VX
    FX33    Store the binary-coded decimal equivalent of the value
            stored in register VX at addresses I, I+1, and I+2
    FX55    Store the values of registers V0 to VX inclusive in memory
            starting at address I
            I is set to I + X + 1 after operation
    FX65    Fill registers V0 to VX inclusive with the values stored in
            memory starting at address I
            I is set to I + X + 1 after operation


Assembly Syntax
---------------

    OP      Ex       NEMONIC
    ----    ----     ------------------------
    0NNN    0030     RCA
    00E0    00E0     CLS
    00EE    00EE     RTS
    1NNN    1200     JUMP         $200
    2NNN    2200     CALL         $200
    3XNN    3A00     SKIP.EQ      VA, #$00
    4XNN    4800     SKIP.NE      V8, #$00
    5XY0    5A70     SKIP.EQ      VA, V7
    6XNN    6A70     MOV          VA, $70
    7XNN    7B69     ADD          VB, $69
    8XY0    83A0     MOV          V3, VA
    8XY1    83A1     OR           V3, VA
    8XY2    83A2     AND          V3, VA
    8XY3    83A3     XOR          V3, VA
    8XY4    83B4     ADD.         V3, VB
    8XY5    83B5     SUB.         V3, VB
    8XY6    83x6     SHR.         V3
    8XY7    83B7     SUBB.        V3, VB
    8XYE    83xE     SHL.         V3
    9XY0    93B0     SKIP.NE      V3, VB
    ANNN    A200     MOV          I, $200
    BNNN    B404     JUMP         $404+V0
    CXNN    CAFF     RAND         VA, $FF
    DXYN    DXYN     SPRITE       VX, VY, #$N
    EX9E    EX9E     SKIP.KEY     VX
    EXA1    EXA1     SKIP.NOKEY   VX
    FX07    FX07     MOV          VX, DELAY
    FX0A    FX0A     WAITKEY      VX
    FX15    FX15     MOV          DELAY, VX
    FX18    FX18     MOV          SOUND, VX
    FX1E    FX1E     ADD          I, VX
    FX29    FX29     SPRITECHAR   VX
    FX33    FX33     MOVBCD       VX
    FX55    FX55     MOVM         (I), V0-VX
    FX65    FX65     MOVM         V0-VX, (I)
