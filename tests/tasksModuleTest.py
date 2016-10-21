#!/usr/bin/env python3.5

import unittest
from modules import tasks_module
from modules.config import thisConfig
import os

import logging
logger = logging.getLogger('getTasksTest.py')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


class TestCheckRestriction(unittest.TestCase):
    def test_check_restriction(self):
        #def check_restriction(settings, restriction):
        #self.assertFalse()
        pass


class TestCheckTask(unittest.TestCase):
    def test_check_task(self):
        #def check_task(settings, task):
        # self.assertFalse()
        pass


class TestGetSelectRestrictions(unittest.TestCase):
    def setUp(self):
        self.select_perfect = [{"action":"select", "category":"filler", "argument":0.5}, {"action":"select", "category":"target", "argument":0.5}]
        self.select_additional = [{"action":"max_successor", "type":"foobar", "argument":4}, {"action":"select", "category":"filler", "argument":0.5}, {"action":"select", "category":"target", "argument":0.5}]

    def test_get_select_restrictions(self):
        self.assertEqual(tasks_module.get_select_restrictions(self.select_perfect), self.select_perfect)
        self.assertEqual(tasks_module.get_select_restrictions(self.select_additional), self.select_perfect)


class TestCheckSelect(unittest.TestCase):
    def setUp(self):
        self.select_perfect = [{"action":"select", "category":"filler", "argument":0.5}, {"action":"select", "category":"target", "argument":0.5}]
        self.select_duplicate = [{"action":"select", "category":"filler", "argument":0.3}, {"action":"select", "category":"filler", "argument":0.2}, {"action":"select", "category":"target", "argument":0.5}]
        self.select_percentage_less = [{"action":"select", "category":"filler", "argument":0.3}, {"action":"select", "category":"target", "argument":0.5}]
        self.select_percentage_more = [{"action":"select", "category":"filler", "argument":0.8}, {"action":"select", "category":"target", "argument":0.5}]

    def test_check_select(self):
        # selections have to sum up to one
        with self.assertRaises(AssertionError):
            tasks_module.check_select(20, self.select_percentage_less)
        # selections have to sum up to one
        with self.assertRaises(AssertionError):
            tasks_module.check_select(20, self.select_percentage_more)
        # selections can not contain contradicting statements
        with self.assertRaises(AssertionError):
            tasks_module.check_select(20, self.select_duplicate)
        # selections can't divide a question
        with self.assertRaises(AssertionError):
            tasks_module.check_select(1, self.select_perfect)


class TestApplySuccessor(unittest.TestCase):
    def setUp(self):
        self.successor_restrictions_category = [{"action":"max_successors", "category":"filler", "argument":3}]
        self.sample_category_filler = [{"category": "filler"}] * 5
        self.sample_category_filler_first = [{"category": "target"}] + [{"category": "filler"}] * 4
        self.sample_category_filler_perfect = [{"category": "filler"}] * 3
        self.successor_restrictions_type = [{"action":"max_successors", "type":"foobar", "argument":3}]
        self.sample_type_foobar = [{"type": ["foobar", "barfoo"]}] * 5
        self.sample_type_first = [{"type": ["barfoo"]}] + [{"type": ["foobar", "barfoo"]}] * 3
        self.sample_type_perfect = [{"type": ["foobar", "barfoo"]}] * 3

    def test_apply_successor(self):
        logger.info("Testing category restriction check")
        self.assertEqual(tasks_module.apply_successor(self.sample_category_filler, self.successor_restrictions_category), False)
        self.assertEqual(tasks_module.apply_successor(self.sample_category_filler_first, self.successor_restrictions_category), False)
        self.assertEqual(tasks_module.apply_successor(self.sample_category_filler_perfect, self.successor_restrictions_category), True)
        logger.info("Testing type restriction check")
        self.assertEqual(tasks_module.apply_successor(self.sample_type_foobar, self.successor_restrictions_type), False)
        self.assertEqual(tasks_module.apply_successor(self.sample_type_perfect, self.successor_restrictions_type), True)
        self.assertEqual(tasks_module.apply_successor(self.sample_type_first, self.successor_restrictions_type), True)
        ##def apply_successor(sample, successor_restrictions):
        # self.assertFalse()


class TestApplySelect(unittest.TestCase):
    def test_apply_select(self):
        pass
        #def apply_select(settings, select_restrictions, tasks):
        # self.assertFalse()


class TestCheckConfig(unittest.TestCase):
    def test_check_config(self):
        pass
        #check_config(settings, tasks):
        # self.assertFalse()

