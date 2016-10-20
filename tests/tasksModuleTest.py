#!/usr/bin/env python3.5

import unittest
from modules import tasks_module
from modules.config import thisConfig
import os

import logging
logger = logging.getLogger('getTasksTest.py')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


class TestCheckRestriction(unittest.TestCase):
    def test_check_restriction(self):
        #def check_restriction(settings, restriction):
        self.assertFalse()


class TestCheckTask(unittest.TestCase):
    def test_check_task(self):
        #def check_task(settings, task):
        self.assertFalse()


class TestGetSelectRestrictions(unittest.TestCase):
    def test_get_select_restrictions(self):
        #def get_select_restrictions(restrictions):
        self.assertFalse()


class TestCheckSelect(unittest.TestCase):
    def test_check_select(self):
        #def check_select(settings, select_restrictions):
        self.assertFalse()


class TestApplySuccessor(unittest.TestCase):
    def test_apply_successor(self):
        #def apply_successor(sample, successor_restrictions):
        self.assertFalse()


class TestApplySelect(unittest.TestCase):
    def test_apply_select(self):
        #def apply_select(settings, select_restrictions, tasks):
        self.assertFalse()


class TestCheckConfig(unittest.TestCase):
    def test_check_config(self):
        #check_config(settings, tasks):
        self.assertFalse()

