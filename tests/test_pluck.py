#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import unittest
from plucky import pluck


class TestPluck(unittest.TestCase):
    def test_empty_selector(self):
        self.assertEqual(pluck(1, ''), 1)

    def test_null_obj(self):
        self.assertEqual(pluck(None, "x"), None)

    def test_null_obj_with_default(self):
        self.assertEqual(pluck(None, "x", default=1), 1)

    def test_itemgetter_idx_from_str(self):
        self.assertEqual(pluck("str", "[0]"), "s")

    def test_itemgetter_idx_from_list(self):
        self.assertEqual(pluck(range(3), "[1]"), 1)

    def test_itemgetter_idx_from_dict(self):
        self.assertEqual(pluck({1: 1}, "[1]"), 1)

    def test_itemgetter_key_from_dict(self):
        self.assertEqual(pluck({1: 1, "1": "1"}, '["1"]'), "1")

    def test_itemgetter_key2_from_dict(self):
        self.assertEqual(pluck({1: 1, "1": "1"}, "['1']"), "1")

    def test_itemgetter_keys_from_dict(self):
        self.assertEqual(pluck({1: 1, "1": "1"}, '[1, "1"]'), [1, "1"])

    def test_itemgetter_keys1_from_dict(self):
        self.assertEqual(pluck({1: 1, "1": "1"}, '[1, "2"]'), [1])

    def test_itemgetter_slice_all_from_dict(self):
        self.assertEqual(pluck({1: 1, "1": "1"}, "[:]"), [1])

    def test_attrgetter_dict(self):
        self.assertEqual(pluck({1: 1, "a": "a"}, "a"), "a")

    def test_attrgetter_list_one(self):
        self.assertEqual(pluck([{"a": "a"}, {"b": "b"}], "a"), ["a"])

    def test_attrgetter_list_two(self):
        self.assertEqual(pluck([{"a": "a"}, {"a": "b"}], "a"), ["a", "b"])


if __name__ == '__main__':
    unittest.main()
