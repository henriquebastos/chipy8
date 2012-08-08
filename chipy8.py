

class Memory(object):
    def __init__(self):
        self._stream = [0x00] * 4096

    def __len__(self):
        return len(self._stream)

    def read_byte(self, address):
        return self._stream[address]

    def write_byte(self, address, data):
        self._stream[address] = data

    def load(self, address, data):
        for offset, datum in enumerate(data):
            self._stream[address + offset] = datum

    def read_word(self, address):
        high = self.read_byte(address) << 8
        low = self.read_byte(address + 1)
        return high + low


instruction = lambda op: op >> 12
mask = lambda i: i << 12
address = lambda op: op ^ mask(instruction(op))
register1 = lambda op: (op ^ mask(instruction(op))) >> 8
constant8 = lambda op: (op >> 8 << 8) ^ op

class Chip8(object):
    def __init__(self):
        self.registers = [0x00] * 16
        self.index_register = 0
        self.program_counter = 0x200

        self.memory = Memory()
        # 0x000-0x1FF - Chip 8 interpreter (contains font set in emu)
        # 0x050-0x0A0 - Used for the built in 4x5 pixel font set (0-F)
        # 0x200-0xFFF - Program ROM and work RAM

        self.screen = [0x00] * 32 * 64
        self.keyboard = [0x00] * 16
        self.stack = []

        self.delay_timer = 0
        self.sound_timer = 0

    def decode(self, opcode):
        if opcode in [0x00E0, 0x00EE]:
            return (opcode,)

        if instruction(opcode) in [0x0, 0x1, 0x2, 0xA, 0xB]:
            return instruction(opcode), address(opcode)

        if instruction(opcode) in [0x3, 0x4, 0x6, 0x7]:
            return instruction(opcode), register1(opcode), constant8(opcode)

