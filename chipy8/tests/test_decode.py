# coding: UTF-8
from unittest import TestCase
from chipy8 import Chip8


class TestOpcodeDecode(TestCase):
    def setUp(self):
        self.cpu = Chip8()

    def test_0NNN(self):
        self.assertEqual(self.cpu.decode(0x0200), (0x0, (0x200,)))

    def test_00E0(self):
        self.assertEqual(self.cpu.decode(0x00E0), (0x00E0, tuple()))

    def test_00EE(self):
        self.assertEqual(self.cpu.decode(0x00EE), (0x00EE, tuple()))

    def test_1NNN(self):
        self.assertEqual(self.cpu.decode(0x1200), (0x1, (0x200,)))

    def test_2NNN(self):
        self.assertEqual(self.cpu.decode(0x2200), (0x2, (0x200,)))

    def test_3XNN(self):
        self.assertEqual(self.cpu.decode(0x3199), (0x3, (0x1, 0x99)))

    def test_4XNN(self):
        self.assertEqual(self.cpu.decode(0x4199), (0x4, (0x1, 0x99)))

    def test_5XY0(self):
        self.assertEqual(self.cpu.decode(0x5120), (0x5, (0x1, 0x2)))

    def test_6XNN(self):
        self.assertEqual(self.cpu.decode(0x6199), (0x6, (0x1, 0x99)))

    def test_7XNN(self):
        self.assertEqual(self.cpu.decode(0x7199), (0x7, (0x1, 0x99)))

    def test_8XY0(self):
        self.assertEqual(self.cpu.decode(0x8120), (0x8000, (0x1, 0x2)))

    def test_8XY1(self):
        self.assertEqual(self.cpu.decode(0x8121), (0x8001, (0x1, 0x2)))

    def test_8XY2(self):
        self.assertEqual(self.cpu.decode(0x8122), (0x8002, (0x1, 0x2)))

    def test_8XY3(self):
        self.assertEqual(self.cpu.decode(0x8123), (0x8003, (0x1, 0x2)))

    def test_8XY4(self):
        self.assertEqual(self.cpu.decode(0x8124), (0x8004, (0x1, 0x2)))

    def test_8XY5(self):
        self.assertEqual(self.cpu.decode(0x8125), (0x8005, (0x1, 0x2)))

    def test_8XY6(self):
        self.assertEqual(self.cpu.decode(0x8126), (0x8006, (0x1, 0x2)))

    def test_8XY7(self):
        self.assertEqual(self.cpu.decode(0x8127), (0x8007, (0x1, 0x2)))

    def test_8XYE(self):
        self.assertEqual(self.cpu.decode(0x812E), (0x800E, (0x1, 0x2)))

    def test_9XY0(self):
        self.assertEqual(self.cpu.decode(0x9120), (0x9000, (0x1, 0x2)))

    def test_ANNN(self):
        self.assertEqual(self.cpu.decode(0xA200), (0xA, (0x200,)))

    def test_BNNN(self):
        self.assertEqual(self.cpu.decode(0xB200), (0xB, (0x200,)))

    def test_CNNN(self):
        self.assertEqual(self.cpu.decode(0xCABB), (0xC, (0xA, 0xBB)))

    def test_DXYN(self):
        self.assertEqual(self.cpu.decode(0xD205),
                         (0xD, (0x2, 0x0, 0x5)))

    def test_EX9E(self):
        self.assertEqual(self.cpu.decode(0xE29E), (0xE09E, (0x2,)))

    def test_EXA1(self):
        self.assertEqual(self.cpu.decode(0xEAA1), (0xE0A1, (0xA,)))

    def test_FX07(self):
        self.assertEqual(self.cpu.decode(0xF0A1), (0xF0A1, (0x0,)))

    def test_FX0A(self):
        self.assertEqual(self.cpu.decode(0xF10A), (0xF00A, (0x1,)))

    def test_FX15(self):
        self.assertEqual(self.cpu.decode(0xF115), (0xF015, (0x1,)))

    def test_FX18(self):
        self.assertEqual(self.cpu.decode(0xF118), (0xF018, (0x1,)))

    def test_FX1E(self):
        self.assertEqual(self.cpu.decode(0xF11E), (0xF01E, (0x1,)))

    def test_FX29(self):
        self.assertEqual(self.cpu.decode(0xF129), (0xF029, (0x1,)))

    def test_FX33(self):
        self.assertEqual(self.cpu.decode(0xF133), (0xF033, (0x1,)))

    def test_FX55(self):
        self.assertEqual(self.cpu.decode(0xF155), (0xF055, (0x1,)))

    def test_FX65(self):
        self.assertEqual(self.cpu.decode(0xF165), (0xF065, (0x1,)))
