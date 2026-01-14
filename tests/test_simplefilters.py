#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for simple filters."""

import unittest
import tests.tst_filterbase

from filters.simplefilters import (
    NaiveFilter,
    ParanoidFilter,
    RandomFilter)


class NaiveFilterTest(tests.tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of the NaiveFilter class for the test
        self.filter = NaiveFilter()


class ParanoidFilterTest(tests.tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of the ParanoidFilter class for the test
        self.filter = ParanoidFilter()


class RandomFilterTest(tests.tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of the RandomFilter class for the test
        self.filter = RandomFilter()


if __name__ == '__main__':
    unittest.main(exit=False)