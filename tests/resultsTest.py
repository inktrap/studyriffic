#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
import os

import tests.config
import logging
logger = logging.getLogger(__file__)

import pprint
pp = pprint.PrettyPrinter(indent=4)

class csvResultsTest():

    def setUp(self):
        pass

    # helper functions

    def _check_formatTest(self):
        #def _check_format(self, outfile, data):
        pass

    def _joinListTest(self):
        #def _joinList(self, this_list):
        pass

    def _flattenListTest(self):
        #def _flattenList(self, *args):
        pass

    # main functions (these should be tested first)

    def makeSettingsTest(self):
        #def makeSettings(self, items):
        pass

    def makeTasksTest(self):
        #def makeTasks(self, items, settings):
        pass

    def makeAnswersTest(self):
        #def makeAnswers(self, items):
        pass

    def makeDemographicsTest(self):
        #def makeDemographics(self, items):
        pass

    def makeAllTest(self):
        #def makeAll(self, demographics, tasks, answers):
        pass

    # functions with a lot of side effects that can only
    # be tested to throw assertions
    def writeTest(self):
        #def write(self, data, outfile):
        pass

    def loadJsonTest(self):
        #def loadJson(self, name, results):
        pass


if __name__ == '__main__':
    unittest.main()

