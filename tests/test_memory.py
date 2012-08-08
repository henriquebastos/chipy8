# coding: utf-8
from unittest import TestCase
from chipy8 import Memory


class TestMemory(TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_write(self):
        'Write a byte to memory then read it.'
        address = 0x200
        self.memory.write_byte(0x200, 0x01)
        self.assertEqual(0x01, self.memory.read_byte(0x200))

    def test_load(self):
        'Load a stream of bytes to memory starting on an address.'
        address = 0x200
        self.memory.load(0x200, [0x01, 0x02, 0x03])
        self.assertEqual(0x01, self.memory.read_byte(address))
        self.assertEqual(0x02, self.memory.read_byte(address + 1))
        self.assertEqual(0x03, self.memory.read_byte(address + 2))