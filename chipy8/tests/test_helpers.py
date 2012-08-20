# coding: utf-8
from unittest import TestCase
from chipy8 import bcd


class TestBCD(TestCase):
    def test_bcd_255(self):
        self.assertEqual(bcd(255), [2, 5, 5])

    def test_bcd_1(self):
        self.assertEqual(bcd(1), [0, 0, 1])

    def test_bcd_limit_to_byte(self):
        self.assertRaises(ValueError, bcd, 256)
