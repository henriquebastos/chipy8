

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
address = lambda op: (op | 0xF000) ^ 0xF000
register1 = lambda op: ((op | 0xF0FF) ^ 0xF0FF) >> 8
register2 = lambda op: ((op | 0xFF0F) ^ 0xFF0F) >> 4
constant8 = lambda op: (op | 0xFF00) ^ 0xFF00
instruction2 = lambda op: (op | 0x0FF0) ^ 0x0FF0
constant4 = lambda op: (op | 0xFFF0) ^ 0xFFF0

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

        if instruction(opcode) in [0x3, 0x4, 0x6, 0x7, 0xC]:
            return instruction(opcode), register1(opcode), constant8(opcode)

        if instruction(opcode) == 0x5:
            return instruction(opcode), register1(opcode), register2(opcode)

        if instruction(opcode) == 0xD:
            return instruction(opcode), register1(opcode), register2(opcode), constant4(opcode)
        if instruction2(opcode) in [0x8000, 0x8001, 0x8002, 0x8003, 0x8004, 0x8005, 0x8006, 0x8007, 0x800E, 0x9000]:
            return instruction2(opcode), register1(opcode), register2(opcode)

        if instruction(opcode) >= 0xE:
            return instruction(opcode), register1(opcode)
