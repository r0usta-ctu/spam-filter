#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for MyFilter class."""

import unittest
import tests.tst_filterbase


class MyFilterTest(tests.tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of class MyFilter for the test
        from filter import MyFilter
        self.filter = MyFilter()
        self.filter.MODEL_PATH = "./model/test_pretrained_model.pkl"

       
if __name__ == '__main__':
    unittest.main()
