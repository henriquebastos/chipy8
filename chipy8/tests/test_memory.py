# coding: utf-8
from unittest import TestCase
from chipy8.memory import Memory, FONT_SPRITES, FONT_ADDRESS


ADDRESS = 0x200


class TestMemory(TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_write(self):
        'Write a byte to memory then read it.'
        self.memory.write_byte(ADDRESS, 0x01)
        self.assertEqual(0x01, self.memory.read_byte(ADDRESS))

    def test_write_must_receive_byte(self):
        self.assertRaises(ValueError,
                          self.memory.write_byte, ADDRESS, 0x100)

    def test_load_must_receive_list_of_bytes(self):
        self.assertRaises(ValueError,
                          self.memory.load, ADDRESS, [0x100])

    def test_load(self):
        'Load a stream of bytes to memory starting on an address.'
        self.memory.load(ADDRESS, [0x01, 0x02, 0x03])
        self.assertEqual(0x01, self.memory.read_byte(ADDRESS))
        self.assertEqual(0x02, self.memory.read_byte(ADDRESS + 1))
        self.assertEqual(0x03, self.memory.read_byte(ADDRESS + 2))

    def test_read_word(self):
        self.memory.load(ADDRESS, [0x01, 0x02])
        self.assertEqual(0x0102, self.memory.read_word(ADDRESS))

    def test_read(self):
        self.memory.load(ADDRESS, [0x01, 0x02])
        self.assertListEqual([0x01, 0x02], self.memory.read(ADDRESS, 2))

    def test_font_sprites(self):
        'Chip8 has 16 preset sprites corresponding from 0 to F.'
        in_memory = self.memory.read(FONT_ADDRESS, len(FONT_SPRITES))
        self.assertEqual(FONT_SPRITES, in_memory)

