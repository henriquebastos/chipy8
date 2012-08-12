# coding: utf-8
from unittest import TestCase
from chipy8 import Chip8, ENTRY_POINT


class TestInstructios(TestCase):
    def setUp(self):
        self.cpu = Chip8()

    def registers(self, **registers):
        for r, datum in registers.items():
            self.cpu.registers[int(r[-1])] = datum

    def execute(self, op, at=ENTRY_POINT):
        data = [op >> 8, ((op | 0xFF00) ^ 0xFF00)]
        self.cpu.memory.load(at, data)
        self.cpu.program_counter = at
        self.cpu.cycle()

    def test_00EE(self):
        self.cpu.stack.append(0x200)
        self.execute(0x00EE, at=0x400)
        self.assertListEqual([], self.cpu.stack)
        self.assertEqual(0x200, self.cpu.program_counter)

    def test_1NNN(self):
        self.execute(0x1400)
        self.assertEqual(0x400, self.cpu.program_counter)

    def test_2NNN(self):
        self.execute(0x2400)
        self.assertEqual(0x400, self.cpu.program_counter)
        self.assertListEqual([0x200], self.cpu.stack)

    def test_3XNN_equal(self):
        self.registers(V5=0x42)
        self.execute(0x3542)
        self.assertEqual(ENTRY_POINT+0x4, self.cpu.program_counter)

    def test_3XNN_unequal(self):
        self.registers(V5=0x42)
        self.execute(0x3524)
        self.assertEqual(ENTRY_POINT+0x2, self.cpu.program_counter)

    def test_4XNN_equal(self):
        self.registers(V2=0x69)
        self.execute(0x4269)
        self.assertEqual(ENTRY_POINT+0x2, self.cpu.program_counter)

    def test_4XNN_unequal(self):
        self.registers(V2=0x69)
        self.execute(0x4270)
        self.assertEqual(ENTRY_POINT+0x4, self.cpu.program_counter)

    def test_5XY0_equal(self):
        self.registers(V2=0x42, V3=0x42)
        self.execute(0x5230)
        self.assertEqual(ENTRY_POINT+0x4, self.cpu.program_counter)

    def test_5XY0_unequal(self):
        self.registers(V2=0x42, V3=0x24)
        self.execute(0x5230)
        self.assertEqual(ENTRY_POINT+0x2, self.cpu.program_counter)

    def test_6XNN(self):
        self.execute(0x6342)
        self.assertEqual(self.cpu.registers[3], 0x42)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_7XNN(self):
        self.registers(V1=0x1)
        self.execute(0x7142)
        self.assertEqual(self.cpu.registers[1], 0x43)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_7XNN_wraparound(self):
        self.registers(V1=0xFF)
        self.execute(0x7101)
        self.assertEqual(self.cpu.registers[1], 0x0)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY0(self):
        self.registers(V2=0x00, V4=0x42)
        self.execute(0x8240)
        self.assertEqual(self.cpu.registers[2],
                         self.cpu.registers[4])
        self.assertEqual(ENTRY_POINT+0x2, self.cpu.program_counter)

    def test_8XY1(self):
        self.registers(V1=0x0F, V2=0xF0)
        self.execute(0x8121)
        self.assertEqual(self.cpu.registers[1], 0xFF)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY2(self):
        self.registers(V1=0x0F, V2=0xF0)
        self.execute(0x8122)
        self.assertEqual(self.cpu.registers[1], 0x0)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY3(self):
        self.registers(V1=0xA, V2=0xC)
        self.execute(0x8123)
        self.assertEqual(self.cpu.registers[1], 0x6)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY4(self):
        self.registers(V1=0xF, V2=0xF0)
        self.execute(0x8124)
        self.assertEqual(self.cpu.registers[1], 0xFF)
        self.assertEqual(self.cpu.registers[0xF], 0x0)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY4_overflow(self):
        self.registers(V1=0x1, V2=0xFF)
        self.execute(0x8124)
        self.assertEqual(self.cpu.registers[1], 0x0)
        self.assertEqual(self.cpu.registers[0xF], 0x1)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY5(self):
        self.registers(V1=0xF, V2=0xE)
        self.execute(0x8125)
        self.assertEqual(self.cpu.registers[1], 0x1)
        self.assertEqual(self.cpu.registers[0xF], 0x1)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY5_borrow(self):
        self.registers(V1=0xE, V2=0xF)
        self.execute(0x8125)
        self.assertEqual(self.cpu.registers[1], 0xFF)
        self.assertEqual(self.cpu.registers[0xF], 0x0)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY6_one(self):
        self.registers(V2=0xF)
        self.execute(0x8126)
        self.assertEqual(self.cpu.registers[1], 0x7)
        self.assertEqual(self.cpu.registers[0xF], 0x1)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY6_zero(self):
        self.registers(V2=0xE)
        self.execute(0x8126)
        self.assertEqual(self.cpu.registers[1], 0x7)
        self.assertEqual(self.cpu.registers[0xF], 0x0)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY7(self):
        self.registers(V1=0x1, V2=0xF)
        self.execute(0x8127)
        self.assertEqual(self.cpu.registers[1], 0xE)
        self.assertEqual(self.cpu.registers[0xF], 0x1)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XY7_borrow(self):
        self.registers(V1=0x1, V2=0x0)
        self.execute(0x8127)
        self.assertEqual(self.cpu.registers[1], 0xFF)
        self.assertEqual(self.cpu.registers[0xF], 0x0)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XYE_one(self):
        self.registers(V2=0xFF)
        self.execute(0x812E)
        self.assertEqual(self.cpu.registers[1], 0xFE)
        self.assertEqual(self.cpu.registers[0xF], 0x1)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_8XYE_zero(self):
        self.registers(V2=0x7F)
        self.execute(0x812E)
        self.assertEqual(self.cpu.registers[1], 0xFE)
        self.assertEqual(self.cpu.registers[0xF], 0x0)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_9XY0_equal_dont_skip(self):
        self.registers(V6=0x42, V8=0x42)
        self.execute(0x9680)
        self.assertEqual(self.cpu.program_counter, 0x202)

    def test_9XY0_unequal_skip(self):
        self.registers(V6=0x42, V8=0x24)
        self.execute(0x9680)
        self.assertEqual(self.cpu.program_counter, 0x204)

    def test_ANNN(self):
        self.execute(0xA400)
        self.assertEqual(0x400, self.cpu.index_register)
        self.assertEqual(ENTRY_POINT+0x2, self.cpu.program_counter)

    def test_FX55(self):
        self.cpu.index_register = 0x400
        self.execute(0xF555)
        registers = self.cpu.registers[:5+1]
        in_memory = self.cpu.memory.read(0x400, len(registers))
        self.assertEqual(registers, in_memory)
        self.assertEqual(ENTRY_POINT+0x2, self.cpu.program_counter)

