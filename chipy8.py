# coding: utf-8


class Memory(object):
    def __init__(self):
        self._stream = [0x00] * 4096

    def __len__(self):
        return len(self._stream)

    def read_byte(self, address):
        return self._stream[address]

    def write_byte(self, address, data):
        if data > 0xFF:
            raise ValueError('%x > 0xFF' % data)

        self._stream[address] = data

    def load(self, address, data):
        for offset, datum in enumerate(data):
            self.write_byte(address + offset, datum)

    def read_word(self, address):
        high = self.read_byte(address) << 8
        low = self.read_byte(address + 1)
        return high + low

    def read(self, address, length):
        start = address
        stop = address + length
        return self._stream[start:stop]


ENTRY_POINT = 0x200

def I(op):
    if 0x8000 <= op <= 0x9FFF:
        return (op | 0x0FF0) ^ 0x0FF0
    elif op >= 0xE000:
        return (op | 0x0F00) ^ 0x0F00
    else:
        return op >> 12

X   = lambda op: ((op | 0xF0FF) ^ 0xF0FF) >> 8
Y   = lambda op: ((op | 0xFF0F) ^ 0xFF0F) >> 4
N   = lambda op: (op | 0xFFF0) ^ 0xFFF0
NN  = lambda op: (op | 0xFF00) ^ 0xFF00
NNN = lambda op: (op | 0xF000) ^ 0xF000


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

        self.INSTRUCTION_SET = {
            0x1   : op_1NNN,
            0x2   : op_2NNN,
            0x8000: op_8XY0,
            0xA   : op_ANNN,
            0xF055: op_F055,
        }

    def decode(self, op):
        if op in [0x00E0, 0x00EE]: # special case
            return (op, tuple())

        instruction = I(op)

        if instruction in [0x0, 0x1, 0x2, 0xA, 0xB]:
            args = (NNN(op),)

        elif instruction in [0x3, 0x4, 0x6, 0x7, 0xC]:
            args = X(op), NN(op)

        elif instruction == 0x5:
            args = X(op), Y(op)

        elif instruction == 0xD:
            args = X(op), Y(op), N(op)

        elif 0x8000 <= instruction <= 0x9000:
            args = X(op), Y(op)

        elif instruction >= 0xE:
            args = (X(op),)

        return instruction, args

    def execute(self, instruction, args):
        self.INSTRUCTION_SET[instruction](*args)

    def fetch(self):
        return self.memory.read_word(self.program_counter)

    def cycle(self):
        word = self.fetch()
        instruction, args = self.decode(word)
        self.execute(instruction, args)

    # INSTRUCTIONS

    def op_1NNN(self, address):
        self.program_counter = address

    def op_2NNN(self, address):
        self.stack.append(self.program_counter)
        self.program_counter = address

    def op_8XY0(self, X, Y):
        'Store the value of register VY in register VX'
        self.registers[X] = self.registers[Y]

    def op_ANNN(self, address):
        self.index_register = address

    def op_F055(self, X):
        X_inclusive = X + 1
        data = self.registers[0:X_inclusive]
        self.memory.load(self.index_register, data)

