# coding: utf-8
from unittest import TestCase
from chipy8 import Chip8, ENTRY_POINT


class TestInstructios(TestCase):
    def setUp(self):
        self.cpu = Chip8()

    def test_00EE(self):
        self.cpu.stack.append(0x200)
        self.cpu.memory.load(0x400, [0x00, 0xEE])
        self.cpu.program_counter = 0x400
        self.cpu.cycle()
        self.assertListEqual([], self.cpu.stack)
        self.assertEqual(0x200, self.cpu.program_counter)

    def test_1NNN(self):
        self.cpu.memory.load(ENTRY_POINT, [0x14, 0x00])
        self.cpu.cycle()
        self.assertEqual(0x400, self.cpu.program_counter)

    def test_2NNN(self):
        self.cpu.memory.load(ENTRY_POINT, [0x24, 0x00])
        self.cpu.cycle()
        self.assertEqual(0x400, self.cpu.program_counter)
        self.assertListEqual([0x200], self.cpu.stack)

    def test_3XNN_equal(self):
        value = 0x42
        self.cpu.registers[0x5] = value
        self.cpu.memory.load(ENTRY_POINT, [0x35, value])
        self.cpu.cycle()
        self.assertEqual(ENTRY_POINT+0x4, self.cpu.program_counter)

    def test_3XNN_unequal(self):
        valueA, valueB = 0x42, 0x24
        self.cpu.registers[0x5] = valueA
        self.cpu.memory.load(ENTRY_POINT, [0x35, valueB])
        self.cpu.cycle()
        self.assertEqual(ENTRY_POINT+0x2, self.cpu.program_counter)

    def test_4XNN_equal(self):
        value = 0x69
        self.cpu.registers[0x2] = value
        self.cpu.memory.load(0x200, [0x42, value])
        self.cpu.cycle()
        self.assertEqual(0x202, self.cpu.program_counter)

    def test_4XNN_unequal(self):
        valueA, valueB = 0x69, 0x70
        self.cpu.registers[0x2] = valueA
        self.cpu.memory.load(0x200, [0x42, valueB])
        self.cpu.cycle()
        self.assertEqual(0x204, self.cpu.program_counter)

    def test_8XY0(self):
        X, Y = 0x2, 0x4
        self.cpu.registers[Y] = 0x42
        self.cpu.memory.load(ENTRY_POINT, [0x82, 0x40])
        self.cpu.cycle()
        self.assertEqual(self.cpu.registers[X],
                         self.cpu.registers[Y])

    def test_ANNN(self):
        self.cpu.memory.load(ENTRY_POINT, [0xA4, 0x00])
        self.cpu.cycle()
        self.assertEqual(0x400, self.cpu.index_register)

    def test_FX55(self):
        self.cpu.index_register = 0x400
        self.cpu.memory.load(ENTRY_POINT, [0xF5, 0x55])
        self.cpu.cycle()
        registers = self.cpu.registers[:5+1]
        in_memory = self.cpu.memory.read(0x400, len(registers))
        self.assertEqual(registers, in_memory)

