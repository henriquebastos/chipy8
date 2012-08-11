# coding: utf-8
from unittest import TestCase
from chipy8 import Chip8, ENTRY_POINT


class TestInstructios(TestCase):
    def setUp(self):
        self.cpu = Chip8()

    def test_1NNN(self):
        self.cpu.memory.load(ENTRY_POINT, [0x14, 0x00])
        self.cpu.cycle()
        self.assertEqual(0x400, self.cpu.program_counter)

    def test_2NNN(self):
        self.cpu.memory.load(ENTRY_POINT, [0x24, 0x00])
        self.cpu.cycle()
        self.assertEqual(0x400, self.cpu.program_counter)
        self.assertListEqual([0x200], self.cpu.stack)

