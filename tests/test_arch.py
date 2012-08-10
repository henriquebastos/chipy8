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
