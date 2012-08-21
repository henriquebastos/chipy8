# -*- coding: utf-8 -*-

import unittest

import pynes
from chipy8.compiler import lexical #, syntax, semantic

class PongTest(unittest.TestCase):

    def test_asm_compiler(self):
        f = open ('fixtures/PONG.SRC')
        code = f.read()
        f.close()
        tokens = lexical(code)

    def test_fixbug_with_marker_dt_loop(self):
        code = 'DT_loop'
        tokens = lexical(code)
        self.assertEquals(1, len(tokens))
        