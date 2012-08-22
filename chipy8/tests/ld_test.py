# -*- coding: utf-8 -*-
'''
LD Load Instruction Test

With compared with the binary file at the end. It equals to the MOV.
'''
import unittest
from chipy8.compiler import lexical, syntax, semantic

class LdTest(unittest.TestCase):


    def test_ld_with_register_and_two(self):
        tokens = lexical('LD VA, 2')
        self.assertEquals(4, len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_REGISTER', tokens[1]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_XNN', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0x6a, 0x02])
