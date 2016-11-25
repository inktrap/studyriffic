#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
import os

import tests.config
import logging
logger = logging.getLogger(__file__)

import pprint
pp = pprint.PrettyPrinter(indent=4)

class TestCsvResults(unittest.TestCase):

    def setUp(self):
        pass

    # helper functions

    def test__check_format(self):
        #def _check_format(self, outfile, data):
        self.assertTrue(True)

    def test__joinList(self):
        #def _joinList(self, this_list):
        self.assertTrue(True)

    def test__flattenList(self):
        #def _flattenList(self, *args):
        self.assertTrue(True)

    # main functions (these should be tested first)

    def test_makeSettings(self):
        #def makeSettings(self, items):
        self.assertTrue(True)

    def test_makeTasks(self):
        #def makeTasks(self, items, settings):
        self.assertTrue(True)

    def test_makeAnswers(self):
        #def makeAnswers(self, items):
        self.assertTrue(True)

    def test_makeDemographics(self):
        #def makeDemographics(self, items):
        self.assertTrue(True)

    def test_makeAll(self):
        #def makeAll(self, demographics, tasks, answers):
        self.assertTrue(True)

    # functions with a lot of side effects that can only
    # be tested to throw the right assertions
    def test_write(self):
        #def write(self, data, outfile):
        self.assertTrue(True)

    def test_loadJson(self):
        #def loadJson(self, name, results):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

