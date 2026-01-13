#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for MyFilter class."""

import unittest
from pathlib import Path

import tests.tst_filterbase


class MyFilterTest(tests.tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of class MyFilter for the test
        from filter import MyFilter
        self.filter = MyFilter()
        base_dir = Path(__file__).resolve().parent
        self.filter.MODEL_PATH = base_dir / "model" / "test_nb_spam_vocab2500.pkl"

       
if __name__ == '__main__':
    unittest.main()
