#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.pardir)

import unittest
from plucky import pluck


class TestPluck(unittest.TestCase):
    def setUp(self):
        self.simple = {
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
            }
        }
        
        self.users = {
            "user": [{
                "name": "a",
                "role": "b"
            }, {
                "name": "c",
            }, {
                "role": "d"
            }]
        }
    
    def test_1(self):
        self.assertEqual(pluck(self.simple, "a"), 1)
    
    def test_2(self):
        self.assertEqual(pluck(self.simple, "b.3"), 3)
    
    def test_3(self):
        self.assertEqual(pluck(self.simple, "c.I"), {"a": 1, "b": 2})
    
    def test_4(self):
        self.assertEqual(pluck(self.simple, "c.II.1.x"), "x2")
    
    def test_5(self):
        self.assertEqual(pluck(self.simple, "c.II.*.x"), ["x1", "x2"])
    
    def test_6(self):
        self.assertEqual(pluck(self.simple, "c.II.*.z"), [])
    
    def test_person_1(self):
        self.assertEqual(pluck(self.users, "user.*.role"), ["b", "d"])
    
    def test_person_2(self):
        self.assertEqual(pluck(self.users, "user.*.name"), ["a", "c"])
    
    def test_person_3(self):
        self.assertEqual(pluck(self.users, "user.*.username"), [])
    
    def test_person_4(self):
        self.assertEqual(pluck(self.users, "user.5"), None)
    
    def test_person_5(self):
        self.assertEqual(pluck(self.users, "user.5.x"), None)
    
    def test_person_6(self):
        self.assertEqual(pluck(self.users, "user.*.role.id"), [])


if __name__ == '__main__':
    unittest.main()
