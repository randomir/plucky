#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.pardir)

import unittest
from plucky import pluckable


class TestPluckable(unittest.TestCase):
    def setUp(self):
        self.src = {
            "a": 1,
            "b": range(10),
            "c": {
                "I": {
                    "a": 1,
                    "b": 2
                },
                "II": [{
                    "x": "x1",
                    "y": "y1"
                }, {
                    "x": "x2",
                    "y": "y2"
                }]
            },
            "users": [{
                "uid": 1,
                "name": {
                    "first": "john",
                    "last": "smith"
                },
            }, {
                "uid": 2,
                "name": {
                    "last": "bonobo"
                }
            }, {
                "uid": 3
            }],
            1: "one",
            2: "two"
        }
        self.obj = pluckable(self.src)
        self.obj2 = pluckable(self.src, skipmissing=False)
        
    def test_simple_getattr(self):
        self.assertEqual(self.obj.a.value, 1)

    def test_simple_getattr_default(self):
        self.assertEqual(self.obj.nonexisting.value, None)

    def test_nested_getattr(self):
        self.assertEqual(self.obj.c.I.b.value, 2)

    def test_getattr_on_list(self):
        self.assertEqual(self.obj.users.uid.value, [1, 2, 3])

    def test_getattr_on_list_dict(self):
        self.assertEqual(self.obj.users.name.first.value, ["john"])

    def test_getattr_on_pluckable_list(self):
        users_list = self.obj.value['users']
        self.assertEqual(pluckable(users_list).name.last.value, ["smith", "bonobo"])

    def test_getitem_index_from_list_simple(self):
        L = list(range(10))
        self.assertEqual(pluckable(L)[7].value, L[7])

    def test_getitem_index_missing_from_list_simple(self):
        L = list(range(10))
        self.assertEqual(pluckable(L)[70].value, None)

    def test_getitem_index2_from_list_simple(self):
        L = list(range(10))
        self.assertEqual(pluckable(L)[5, 7].value, [L[5], L[7]])

    def test_getitem_slice_from_list_simple(self):
        L = list(range(10))
        self.assertEqual(pluckable(L)[2:5].value, L[2:5])

    def test_getitem_slice_and_index_from_list_simple(self):
        L = list(range(10))
        self.assertEqual(pluckable(L)[2:5, 8].value, L[2:5] + [L[8]])

    def test_getitem_slice_rot_list_simple(self):
        L = list(range(10))
        self.assertEqual(pluckable(L)[:5, 5:].value, L[:5] + L[5:])

    def test_getitem_slice_reverse_list_simple(self):
        L = list(range(10))
        self.assertEqual(pluckable(L)[::-1].value, list(reversed(L)))

    def test_getitem_slice_reverse_dup_list_simple(self):
        L = list(range(10))
        self.assertEqual(pluckable(L)[:, ::-1].value, L + list(reversed(L)))

    def test_getitem_str_from_dict_simple(self):
        D = {"x": 1}
        self.assertEqual(pluckable(D)["x"].value, 1)

    def test_getitem_str2_from_dict_simple(self):
        D = {"x": 1, "y": 2, "z": 3}
        self.assertEqual(pluckable(D)["x", "z"].value, [1, 3])

    def test_getitem_str2_from_dict_deep(self):
        self.assertEqual(self.obj.c.I["a", "b"].value, [1, 2])

    def test_getitem_inter_key_invalid_from_dict_deep(self):
        self.assertEqual(self.obj.invalid.I["a", "b"].value, None)

    def test_getitem_str2_from_list_dict_deep(self):
        self.assertEqual(self.obj.c.II["x"].value, ["x1", "x2"])

    def test_getitem_str2_from_list_dict_deep_rev(self):
        self.assertEqual(self.obj.c.II["x"][::-1].value, ["x2", "x1"])

    def test_getitem_str2_from_list_dict_deep(self):
        self.assertEqual(self.obj.c.II["x", "y"].value, ["x1", "x2", "y1", "y2"])

    def test_getitem_str_int_from_dict_deep(self):
        self.assertEqual(self.obj["a", 1].value, [1, "one"])

    def test_skipmissing_list_indices(self):
        self.assertEqual(pluckable([1, 2], skipmissing=False)[0, 2].value, [1, None])

    def test_skipmissing_list_slice(self):
        self.assertEqual(pluckable([1, 2], skipmissing=False)[0:5].value, [1, 2])

    def test_skipmissing_dict_keys(self):
        D = {"x": 1}
        self.assertEqual(pluckable(D, skipmissing=False)["x", "y"].value, [1, None])

    def test_skipmissing_dict_keys2(self):
        D = {"x": 1}
        self.assertEqual(pluckable(D, skipmissing=False)["x", "y"].invalid.value, [None, None])

    def test_skipmissing_dict_deep(self):
        self.assertEqual(self.obj2.c.I["a", "x", "b"].value, [1, None, 2])

    def test_skipmissing_dict_deep2(self):
        self.assertEqual(self.obj2.users.name.last.value, ["smith", "bonobo", None])

    def test_skipmissing_dict_deep3(self):
        self.assertEqual(self.obj2.users.name.last.missing.value, [None, None, None])


if __name__ == '__main__':
    unittest.main()
