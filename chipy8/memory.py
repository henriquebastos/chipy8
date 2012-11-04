# coding: utf-8


FONT_SPRITES = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
    0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
]
FONT_ADDRESS = 0x50
FONT_LENGTH = 0x5


class Memory(object):
    MEM_SIZE = 4096

    def __init__(self):
        # 0x000-0x1FF - Chip 8 interpreter (contains font set in emu)
        # 0x200-0xFFF - Program ROM and work RAM
        self._stream = bytearray(self.MEM_SIZE)

        # 0x050-0x0A0 - Used for the built in 4x5 pixel font set (0-F)
        self.load(FONT_ADDRESS, FONT_SPRITES)

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

    def font_address(self, value):
        return FONT_ADDRESS + (value * FONT_LENGTH)

    def font(self, value):
        return self.read(self.font_address(value), FONT_LENGTH)


class Screen(list):
    WIDTH = 64
    HEIGHT = 32

    def __init__(self):
        super(Screen, self).__init__([0x00] * self.WIDTH * self.HEIGHT)

    def _index(self, x, y):
        return (y * self.WIDTH) + x

    def unpack_pixels(self, byte):
        '''
        Unpack a byte representing a row of pixels to a list of
        individual integers representing each pixel.

        Example: 0b10101010 ->  [1, 0, 1, 0, 1, 0, 1, 0]
        '''
        pixels = []
        for col in range(8):
            mask = 0x80 >> col
            pixel = byte & mask != 0
            pixels.append(int(pixel))
        return pixels

    def unpack_sprite(self, sprite):
        '''
        Unpack a sprite (list of bytes) into a uni-dimensional array of
        integers representing each pixel.
        '''
        pixels = []
        for byte in sprite:
            pixels.extend(self.unpack_pixels(byte))
        return pixels

    def draw(self, sprite, x, y):
        collision = 0

        for sprite_y, sprite_pixels in enumerate(sprite):
            pixels = self.unpack_pixels(sprite_pixels)

            for sprite_x, pixel in enumerate(pixels):
                i = self._index(x + sprite_x, y + sprite_y)
                collision |= self[i] & pixel
                self[i] = pixel

        return collision

    def get(self, x, y):
        return self[self._index(x, y)]

    def get_region(self, x, y, width=8, height=1):
        pixels = []
        for j in range(height):
            for i in range(width):
                pixel = self.get(x+i, y+j)
                pixels.append(pixel)
        return pixels
