from unittest import TestCase
from chipy8 import Chip8


class TestChip8Architecture(TestCase):
    def setUp(self):
        self.cpu = Chip8()

    def test_memory_length(self):
        'Chip8 has 4096 bytes of memory.'
        self.assertEqual(4096, len(self.cpu.memory))

    def test_register_count(self):
        'Chip8 has 16 registers.'
        self.assertEqual(16, len(self.cpu.registers))

    def test_program_counter(self):
        'Chip8 has a program counter starting at 0x200.'
        self.assertEqual(0x200, self.cpu.program_counter)

    def test_index_register(self):
        'Chip8 has an index register.'
        self.assertEqual(0, self.cpu.index_register)

    def test_screen(self):
        'Chip8 has a 64 * 32 screen (2048 pixels).'
        self.assertEqual(2048, len(self.cpu.screen))

    def test_delay_timer(self):
        'Chip8 has a delay timer that counts to 0 at 60Hz.'
        self.assertEqual(0, self.cpu.delay_timer)

    def test_sound_timer(self):
        'Chip8 has a count down sound timer that beeps on non-zero value.'
        self.assertEqual(0, self.cpu.sound_timer)

    def test_stack(self):
        'Chip8 has a stack to return from jumps and calls.'
        self.assertIsInstance(self.cpu.stack, list)

    def test_keyboard(self):
        'Chip8 has a hex keyboard with 16 keys.'
        self.assertEqual(16, len(self.cpu.keyboard))


class TestOpcodeDecode(TestCase):
    def setUp(self):
        self.cpu = Chip8()

    # Opcodes with no arguments

    def test_CLS(self):
        '00E0 - Clears the screen.'
        expected = (0x00E0,)
        self.assertEqual(expected, self.cpu.decode(0x00E0))

    def test_RET(self):
        '00EE - Returns from a subroutine.'
        expected = (0x00EE,)
        self.assertEqual(expected, self.cpu.decode(0x00EE))

    # Opcodes with one argument: memory address

    def test_RCA(self):
        '0NNN - Calls RCA 1802 program at address NNN.'
        expected = (0x0, 0x200)
        self.assertEqual(expected, self.cpu.decode(0x0200))

    def test_JMP(self):
        '1NNN - Jumps to address NNN.'
        expected = (0x1, 0x200)
        self.assertEqual(expected, self.cpu.decode(0x1200))

    def test_CALL(self):
        '2NNN - Calls subroutine at NNN.'
        expected = (0x2, 0x200)
        self.assertEqual(expected, self.cpu.decode(0x2200))

    def test_SETI(self):
        'ANNN - Sets I to the address NNN.'
        expected = (0xA, 0x200)
        self.assertEqual(expected, self.cpu.decode(0xA200))

    def test_JMP0(self):
        'BNNN - Jumps to the address NNN plus V0.'
        expected = (0xB, 0x200)
        self.assertEqual(expected, self.cpu.decode(0xB200))

    # Opcodes with 2 arguments: one register and a constant word.

    def test_BEQ(self):
        '3XNN - Skips the next instruction if VX equals NN.'
        expected = (0x3, 0x1, 0x99)
        self.assertEqual(expected, self.cpu.decode(0x3199))

    def test_BNE(self):
        "4XNN - Skips the next instruction if VX doesn't equal NN."
        expected = (0x4, 0x1, 0x99)
        self.assertEqual(expected, self.cpu.decode(0x4199))

    def test_SETR(self):
        '6XNN - Sets VX to NN.'
        expected = (0x6, 0x1, 0x99)
        self.assertEqual(expected, self.cpu.decode(0x6199))

    def test_ADDR(self):
        '7XNN - Adds NN to VX.'
        expected = (0x7, 0x1, 0x99)
        self.assertEqual(expected, self.cpu.decode(0x7199))

