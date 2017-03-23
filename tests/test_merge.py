#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.pardir)

import unittest
from plucky import merge


class TestMerge(unittest.TestCase):
    def test_leaf_int(self):
        self.assertEqual(merge(1, 2), 3)

    def test_leaf_int_none(self):
        self.assertRaises(TypeError, merge, 1, None)

    def test_leaf_float(self):
        self.assertEqual(merge(1.2, 2.3), 3.5)

    def test_leaf_float_int(self):
        self.assertEqual(merge(1.2, 3), 4.2)

    def test_leaf_str(self):
        self.assertEqual(merge("abc", "def"), "abcdef")

    def test_leaf_str_num(self):
        self.assertRaises(TypeError, merge, "abc", 1)

    def test_dict_with_string_values(self):
        self.assertEqual(merge({"a": "x"}, {"a": "y"}), {"a": "xy"})

    def test_dict_with_different_keysets(self):
        self.assertEqual(merge({"a": "x"}, {"b": "y"}), {"a": "x", "b": "y"})

    def test_dict_with_numeric_values(self):
        self.assertEqual(merge({"a": 1.2}, {"a": 2.3}), {"a": 3.5})

    def test_lists_of_equal_len(self):
        self.assertEqual(merge([1, 2], [3, 4]), [4, 6])

    def test_lists_of_equal_len_no_recurse(self):
        self.assertEqual(merge([1, 2], [3, 4], recurse_list=False), [1, 2, 3, 4])

    def test_lists_no_recurse_in_dict(self):
        self.assertEqual(merge({'x': [1]}, {'x': [2]}, recurse_list=False), {'x': [1, 2]})

    def test_lists_of_inequal_len(self):
        self.assertEqual(merge([1, 2], [3]), [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
