#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import unittest
from collections import namedtuple
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
                    "y": "y2",
                    "z": "z2"
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

    def test_getitem_str_str_from_list_dict_deep(self):
        self.assertEqual(self.obj.c.II["x", "y"].value, ["x1", "x2", "y1", "y2"])

    def test_getitem_str_from_list_dict_single(self):
        self.assertEqual(self.obj.c.II["z"].value, ["z2"])

    def test_getitem_str_int_from_dict_deep(self):
        self.assertEqual(self.obj["a", 1].value, [1, "one"])

    def test_skipmissing_list_indices(self):
        self.assertEqual(pluckable([1, 2], skipmissing=False)[0, 2].value, [1, None])

    def test_skipmissing_list_slice(self):
        self.assertEqual(pluckable([1, 2], skipmissing=False)[0:4].value, [1, 2, None, None])

    def test_skipmissing_dict_keys(self):
        D = {"x": 1}
        self.assertEqual(pluckable(D, skipmissing=False)["x", "y"].value, [1, None])

    def test_skipmissing_dict_keys2(self):
        D = {"x": 1}
        self.assertEqual(pluckable(D, skipmissing=False)["x", "y"].invalid.value, [None, None])

    def test_skipmissing_dict_slice(self):
        D = {"x": 1}
        self.assertEqual(pluckable(D, skipmissing=False)[0:5].invalid.value, [None] * 5)

    def test_skipmissing_dict_deep(self):
        self.assertEqual(self.obj2.c.I["a", "x", "b"].value, [1, None, 2])

    def test_skipmissing_dict_deep2(self):
        self.assertEqual(self.obj2.users.name.last.value, ["smith", "bonobo", None])

    def test_skipmissing_dict_deep3(self):
        self.assertEqual(self.obj2.users.name.last.missing.value, [None, None, None])

    def test_dict_numeric_key(self):
        self.assertEqual(pluckable({0: 0})[0].value, 0)

    def test_dict_slice_singular(self):
        self.assertEqual(pluckable({0: 0, 1: 1, 2: 2})[1:2].value, [1])

    def test_dict_slice_range(self):
        self.assertEqual(pluckable({0: 0, 1: 1, 2: 2})[1:3].value, [1, 2])

    def test_dict_slice_unbound_top(self):
        self.assertEqual(pluckable({0: 0, 1: 1, 2: 2})[1:].value, [1, 2])

    def test_dict_slice_unbound_bottom(self):
        self.assertEqual(pluckable({0: 0, 1: 1, 2: 2})[:2].value, [0, 1])

    def test_dict_slice_unbound(self):
        self.assertEqual(pluckable({0: 0, 1: 1, 2: 2})[:].value, [0, 1, 2])

    def test_dict_slice_step_from_zero(self):
        self.assertEqual(pluckable({0: 0, 1: 1, 3: 3, 4: 4})[::2].value, [0, 4])

    def test_dict_slice_step_from_one(self):
        self.assertEqual(pluckable({0: 0, 1: 1, 3: 3, 4: 4})[1::2].value, [1, 3])

    def test_dict_slice_reduced_to_single_result(self):
        self.assertEqual(pluckable({0: 0, 1: 1, 4: 4})[1::2].value, [1])

    def test_dict_extract_only_numerical_keys(self):
        self.assertEqual(sorted(pluckable({0: 0, 'a': 'a', 1: 1, 'b': 'b', 3: 3, 4: 4})[:].value), [0, 1, 3, 4])

    def test_inplace(self):
        p = pluckable(self.src, inplace=True)
        p2 = p.c.I.b
        self.assertEqual(id(p), id(p2))
        self.assertEqual(p2.obj, 2)

    def test_attrgetter_custom_attr_old_style_class(self):
        class Obj:
            x = 1
        self.assertEqual(pluckable(Obj).x.value, 1)

    def test_attrgetter_custom_attr_old_style_class_object(self):
        class Obj:
            x = 1
        self.assertEqual(pluckable(Obj()).x.value, 1)

    def test_attrgetter_custom_attr_class(self):
        class Obj(object):
            x = 1
        self.assertEqual(pluckable(Obj).x.value, 1)

    def test_attrgetter_custom_attr_class_object(self):
        class Obj(object):
            x = 1
        self.assertEqual(pluckable(Obj()).x.value, 1)

    def test_attrgetter_custom_attr_shadowed(self):
        class Dct(dict):
            x = 1
        d = Dct(x=2)
        self.assertEqual(pluckable(d).x.value, 1)
        self.assertEqual(pluckable(d)['x'].value, 2)

    def test_attrgetter_custom_attr_shadowed_combination(self):
        class Dct(dict):
            x = 1
            y = 2
        d = Dct(x=2)
        self.assertEqual(pluckable(d)['x', 'y'].value, [2, 2])

    def test_attrgetter_custom_attr_shadowed_combination_inv_deep(self):
        class Dct(dict):
            x = dict(y=1)
        d = Dct()
        self.assertEqual(pluckable(d)['x'].y.value, 1)

    def test_attrgetter_namedtuple(self):
        Point = namedtuple("Point", "x y z")
        self.assertEqual(pluckable(Point(3, 2, 1)).x.value, 3)


if __name__ == '__main__':
    unittest.main()
