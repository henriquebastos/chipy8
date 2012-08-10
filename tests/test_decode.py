# coding: UTF-8
from unittest import TestCase
from chipy8 import Chip8


class TestOpcodeDecode(TestCase):
    def setUp(self):
        self.cpu = Chip8()

    # Opcodes with no arguments

    def test_00E0(self):
        '00E0 - Clears the screen.'
        expected = (0x00E0,)
        self.assertEqual(expected, self.cpu.decode(0x00E0))

    def test_00EE(self):
        '00EE - Returns from a subroutine.'
        expected = (0x00EE,)
        self.assertEqual(expected, self.cpu.decode(0x00EE))

    # Opcodes with one argument: memory address

    def test_0NNN(self):
        '0NNN - Calls RCA 1802 program at address NNN.'
        expected = (0x0, 0x200)
        self.assertEqual(expected, self.cpu.decode(0x0200))

    def test_1NNN(self):
        '1NNN - Jumps to address NNN.'
        expected = (0x1, 0x200)
        self.assertEqual(expected, self.cpu.decode(0x1200))

    def test_2NNN(self):
        '2NNN - Calls subroutine at NNN.'
        expected = (0x2, 0x200)
        self.assertEqual(expected, self.cpu.decode(0x2200))

    def test_ANNN(self):
        'ANNN - Sets I to the address NNN.'
        expected = (0xA, 0x200)
        self.assertEqual(expected, self.cpu.decode(0xA200))

    def test_BNNN(self):
        'BNNN - Jumps to the address NNN plus V0.'
        expected = (0xB, 0x200)
        self.assertEqual(expected, self.cpu.decode(0xB200))

    # Opcodes with 2 arguments: one register and a constant word.

    def test_3XNN(self):
        '3XNN - Skips the next instruction if VX equals NN.'
        expected = (0x3, 0x1, 0x99)
        self.assertEqual(expected, self.cpu.decode(0x3199))

    def test_4XNN(self):
        "4XNN - Skips the next instruction if VX doesn't equal NN."
        expected = (0x4, 0x1, 0x99)
        self.assertEqual(expected, self.cpu.decode(0x4199))

    def test_6XNN(self):
        '6XNN - Sets VX to NN.'
        expected = (0x6, 0x1, 0x99)
        self.assertEqual(expected, self.cpu.decode(0x6199))

    def test_7XNN(self):
        '7XNN - Adds NN to VX.'
        expected = (0x7, 0x1, 0x99)
        self.assertEqual(expected, self.cpu.decode(0x7199))

    # Opcodes with 2 register arguments

    def test_5XY0(self):
        '5XY0 - Skips the next instruction if VX equals VY.'
        expected = (0x5, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x5120))

    def test_8XY0(self):
        '8XY0 - Sets VX to the value of VY.'
        expected = (0x80, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x8120))

    def test_8XY1(self):
        '8XY1 - Sets VX to VX or VY.'
        expected = (0x81, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x8121))

    def test_8XY2(self):
        '8XY2 - Sets VX to VX and VY.'
        expected = (0x82, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x8122))

    def test_8XY3(self):
        '8XY3 - Sets VX to VX xor VY.'
        expected = (0x83, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x8123))

    def test_8XY4(self):
        "8XY4 - Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't."
        expected = (0x84, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x8124))

    def test_8XY5(self):
        "8XY5 - VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't."
        expected = (0x85, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x8125))

    def test_8XY6(self):
        '8XY6 - Shifts VX right by one. VF is set to the value of the least significant bit of VX before the shift.'
        expected = (0x86, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x8126))

    def test_8XY7(self):
        "8XY7 - Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't."
        expected = (0x87, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x8127))

    def test_8XYE(self):
        '8XYE - Shifts VX left by one. VF is set to the value of the most significant bit of VX before the shift.'
        expected = (0x8E, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x812E))

    def test_9XY0(self):
        "9XY0 - Skips the next instruction if VX doesn't equal VY."
        expected = (0x90, 0x1, 0x2)
        self.assertEqual(expected, self.cpu.decode(0x9120))
