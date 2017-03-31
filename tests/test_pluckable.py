#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.pardir)

import unittest
from plucky import pluckable


class TestPluckable(unittest.TestCase):
    def setUp(self):
        self.obj = pluckable({
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
            }],
            1: "one",
            2: "two"
        })
        
    def test_simple_getattr(self):
        self.assertEqual(self.obj.a.value, 1)

    def test_simple_getattr_default(self):
        self.assertEqual(self.obj.nonexisting.value, None)

    def test_nested_getattr(self):
        self.assertEqual(self.obj.c.I.b.value, 2)

    def test_getattr_on_list(self):
        self.assertEqual(self.obj.users.uid.value, [1, 2])

    def test_getattr_on_list_dict(self):
        self.assertEqual(self.obj.users.name.first.value, ["john"])

    def test_getattr_on_pluckable_list(self):
        users_list = self.obj.value['users']
        self.assertEqual(pluckable(users_list).name.last.value, ["smith", "bonobo"])


if __name__ == '__main__':
    unittest.main()
