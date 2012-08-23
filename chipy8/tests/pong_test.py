# -*- coding: utf-8 -*-

import unittest

from chipy8.compiler import lexical, syntax, semantic

class PongTest(unittest.TestCase):


    def test_asm_compiler(self):
        f = open ('fixtures/PONG.SRC')
        code = f.read().split('\n')[57]
        f.close()
        tokens = lexical(code)
        ast = syntax(tokens)
        opcodes = semantic(ast)
        bin = ''.join([chr(opcode) for opcode in opcodes])
        f = open('fixtures/PONG', 'rb')
        content = f.read()
        c = content[:len(bin)]
        self.assertEquals(c,bin)

    def test_fixbug_with_marker_dt_loop(self):
        code = 'DT_loop'
        tokens = lexical(code)
        self.assertEquals(1, len(tokens))
