# coding: utf-8
import sys
import pygame
from pygame.locals import (K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, 
                           K_a, K_b, K_c, K_d, K_e, K_f, QUIT, KEYDOWN, KEYUP, Rect)
import argparse
from unipath import Path
from chip8 import Chip8

parser = argparse.ArgumentParser(description='Chipy8')
parser.add_argument('rom', type=Path, help='ROM file')
args = parser.parse_args()

screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background = background.convert()


def invert(rect):
    r = rect.copy()
    r.x *= -1
    r.y *= -1
    return r

KEYMAP = { K_0: 0x0, K_1: 0x1, K_2: 0x2, K_3: 0x3,
           K_4: 0x4, K_5: 0x5, K_6: 0x6, K_7: 0x7,
           K_8: 0x8, K_9: 0x9, K_a: 0xA, K_b: 0xB,
           K_c: 0xC, K_d: 0xD, K_e: 0xE, K_f: 0xF,
           }

emulator = Chip8()

with open(args.rom, 'rb') as f:
    buffer = bytearray(4092 - 0x200)
    f.readinto(buffer)
    emulator.memory.load(0x200, buffer)

def wait_for_keypress():
    pygame.event.set_allowed(KEYDOWN)

    key = None
    while not key:
        event = pygame.event.wait()
        key = KEYMAP.get(event.key)

    pygame.event.set_blocked(None)

    return key

emulator.wait_for_keypress = wait_for_keypress

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            key = KEYMAP.get(event.key)
            if key:
                emulator.keyboard[key] = 1
        elif event.type == KEYUP:
            key = KEYMAP.get(event.key)
            if key:
                emulator.keyboard[key] = 0

    # print emulator.keyboard
    # print emulator.delay_timer
    emulator.cycle()

    if True or emulator.screen.changed:
        background.fill((0, 0, 0))

        for x in range(64):
            for y in range(32):
                if emulator.screen.get(x, y):
                    pixel = Rect(x*10, y*10, 10, 10)
                    pygame.draw.rect(background, (255, 255, 255), pixel)

        screen.blit(background, background.get_rect())

        pygame.display.update()
    emulator.screen.changed = False
