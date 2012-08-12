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
            0x00EE: self.op_00EE,
            0x1   : self.op_1NNN,
            0x2   : self.op_2NNN,
            0x3   : self.op_3XNN,
            0x4   : self.op_4XNN,
            0x5   : self.op_5XY0,
            0x6   : self.op_6XNN,
            0x7   : self.op_7XNN,
            0x8000: self.op_8XY0,
            0x8001: self.op_8XY1,
            0x8002: self.op_8XY2,
            0x8003: self.op_8XY3,
            0xA   : self.op_ANNN,
            0xF055: self.op_F055,
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

    def increment_program_counter(self):
        self.program_counter += 0x2

    def skip_next_instruction(self):
        self.program_counter += 0x4

    # INSTRUCTIONS

    def op_00EE(self):
        'Return from a subroutine.'
        self.program_counter = self.stack.pop()

    def op_1NNN(self, address):
        'Jump to address NNN.'
        self.program_counter = address

    def op_2NNN(self, address):
        'Execute subroutine starting at address NNN.'
        self.stack.append(self.program_counter)
        self.program_counter = address

    def op_3XNN(self, X, NN):
        'Skip the following instruction if the value of VX == NN.'
        if self.registers[X] == NN:
            self.skip_next_instruction()
        else:
            self.increment_program_counter()

    def op_4XNN(self, X, NN):
        'Skip the following instruction if the value of VX != NN.'
        if self.registers[X] != NN:
            self.skip_next_instruction()
        else:
            self.increment_program_counter()

    def op_5XY0(self, X, Y):
        'Skip next instruction if the value of VX == the value of VY.'
        if self.registers[X] == self.registers[Y]:
            self.skip_next_instruction()
        else:
            self.increment_program_counter()

    def op_6XNN(self, X, NN):
        'Store number NN in register VX.'
        self.registers[X] = NN
        self.increment_program_counter()

    def op_7XNN(self, X, NN):
        'Add the value NN to register VX.'
        self.registers[X] = (self.registers[X] + NN) % 256
        self.increment_program_counter()

    def op_8XY0(self, X, Y):
        'Store the value of register VY in register VX.'
        self.registers[X] = self.registers[Y]
        self.increment_program_counter()

    def op_8XY1(self, X, Y):
        'Set VX to VX OR VY'
        self.registers[X] |= self.registers[Y]
        self.increment_program_counter()

    def op_8XY2(self, X, Y):
        'Set VX to VX AND VY'
        self.registers[X] &= self.registers[Y]
        self.increment_program_counter()

    def op_8XY3(self, X, Y):
        'Set VX to VX XOR VY.'
        self.registers[X] ^= self.registers[Y]
        self.increment_program_counter()

    def op_ANNN(self, address):
        'Store memory address NNN in register I.'
        self.index_register = address
        self.increment_program_counter()

    def op_F055(self, X):
        'Store values of V0 to VX inclusive in mem starting at addr I.'
        data = self.registers[0:X+1]
        self.memory.load(self.index_register, data)
        self.increment_program_counter()

