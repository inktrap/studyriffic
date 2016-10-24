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


# check that tasks and restriction checks work
# they forbid a lot of things so it is easier to just check that they
# letting the good settings/tasks through
class TestChecks(unittest.TestCase):
    def setUp(self):
        self.settings = {
            "actions": ["select", "max_successors"],
            "types":["some", "types", "and", "more"],
            "categories":["filler", "target"]
        }
        # these should all work
        self.task_filler = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": ["some", "types"], "category": "filler"}
        self.task_target = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": ["some", "types"], "category": "target"}
        self.task_no_situation = {"id": 0, "sentence": "Foobar", "situation": "", "type": ["some", "types"], "category": "filler"}
        self.task_no_type = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": [], "category": "filler"}
        self.task_no_sentence = {"id": 0, "sentence": "", "situation": "Barfoo", "type": [], "category": "filler"}
        self.task_no_id = {"id": "", "sentence": "", "situation": "Barfoo", "type": [], "category": "filler"}
        self.task_no_category = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": [], "category": ""}

        # syntactically well formed restrictions
        self.restriction_successor_filler = {"action":"max_successors", "category":"filler", "argument":4}
        self.restriction_successor_target = {"action":"max_successors", "category":"target", "argument":4}
        self.restriction_successor_more = {"action":"max_successors", "type":"some", "argument":4}
        self.restriction_successor_some = {"action":"max_successors", "type":"more", "argument":4}
        self.restriction_successor_error = {"action":"max_successors", "type":"and", "argument":4}
        self.restriction_select_filler = {"action":"select", "category":"filler", "argument":0.5}
        self.restriction_select_target = {"action":"select", "category":"target", "argument":0.5}

    def test_check_restriction(self):
        #tests: def check_restriction(settings, restriction):
        self.assertEqual(tasks_module.check_restriction(self.settings, self.restriction_select_filler), True)
        self.assertEqual(tasks_module.check_restriction(self.settings, self.restriction_select_target), True)
        self.assertEqual(tasks_module.check_restriction(self.settings, self.restriction_successor_filler), True)
        self.assertEqual(tasks_module.check_restriction(self.settings, self.restriction_successor_target), True)
        self.assertEqual(tasks_module.check_restriction(self.settings, self.restriction_successor_more), True)
        self.assertEqual(tasks_module.check_restriction(self.settings, self.restriction_successor_some), True)
        self.assertEqual(tasks_module.check_restriction(self.settings, self.restriction_successor_error), True)

    def test_check_task(self):
        #tests: def check_task(settings, task):
        self.assertEqual(tasks_module.check_task(self.settings, self.task_filler), True)
        self.assertEqual(tasks_module.check_task(self.settings, self.task_target), True)
        self.assertEqual(tasks_module.check_task(self.settings, self.task_no_situation), True)
        self.assertEqual(tasks_module.check_task(self.settings, self.task_no_type), True)
        with self.assertRaises(AssertionError):
            tasks_module.check_task(self.settings, self.task_no_id)
        with self.assertRaises(AssertionError):
            tasks_module.check_task(self.settings, self.task_no_category)
        with self.assertRaises(AssertionError):
            tasks_module.check_task(self.settings, self.task_no_sentence)


class TestGetSelectRestrictions(unittest.TestCase):
    def setUp(self):
        self.select_pass = [{"action":"select", "category":"filler", "argument":0.5}, {"action":"select", "category":"target", "argument":0.5}]
        self.select_additional = [{"action":"max_successors", "type":"foobar", "argument":4}, {"action":"select", "category":"filler", "argument":0.5}, {"action":"select", "category":"target", "argument":0.5}]

    def test_get_select_restrictions(self):
        self.assertEqual(tasks_module.get_select_restrictions(self.select_pass), self.select_pass)
        self.assertEqual(tasks_module.get_select_restrictions(self.select_additional), self.select_pass)


class TestCheckSelect(unittest.TestCase):
    ''' these are semantic checks for select restrictions'''
    def setUp(self):
        self.select_pass = [{"action":"select", "category":"filler", "argument":0.5}, {"action":"select", "category":"target", "argument":0.5}]
        self.select_lesser = [{"action":"select", "category":"filler", "argument":-0.5}]
        self.select_zero = [{"action":"select", "category":"filler", "argument":0.0}]
        self.select_greater = [{"action":"select", "category":"filler", "argument":1.5}]
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
        # selections must be greater then 0
        with self.assertRaises(AssertionError):
            tasks_module.check_select(20, self.select_zero)
        # selections must be greater then 0
        with self.assertRaises(AssertionError):
            tasks_module.check_select(20, self.select_lesser)
        # selections must be smaller then 1
        with self.assertRaises(AssertionError):
            tasks_module.check_select(20, self.select_greater)
        # selections can't divide a question
        with self.assertRaises(AssertionError):
            tasks_module.check_select(1, self.select_pass)


class TestApplySuccessor(unittest.TestCase):
    def setUp(self):
        # restrictions by category
        self.successor_restrictions_category = [{"action":"max_successors", "category":"filler", "argument":3}]
        # samples with categories
        self.sample_category_filler = [{"category": "filler"}] * 5
        self.sample_category_filler_first = [{"category": "target"}] + [{"category": "filler"}] * 3
        self.sample_category_mixed = [{"category": "target"}] * 2 + [{"category": "filler"}] * 3 + [{"category": "target"}] * 2
        self.sample_category_filler_first_fail = [{"category": "target"}] + [{"category": "filler"}] * 4
        self.sample_category_filler_continue = [{"category": "filler"}] * 3

        # restrictions by type
        self.successor_restrictions_type = [{"action":"max_successors", "type":"foobar", "argument":3}]
        # samples with types
        self.sample_type_foobar = [{"type": ["foobar", "barfoo"]}] * 5
        self.sample_type_first = [{"type": ["barfoo"]}] + [{"type": ["foobar", "barfoo"]}] * 3
        self.sample_type_first_fail = [{"type": ["barfoo"]}] + [{"type": ["foobar", "barfoo"]}] * 4
        self.sample_type_continue = [{"type": ["foobar", "barfoo"]}] * 3
        self.sample_type_mixed = [{"type": ["barfoo"]}] * 2 + [{"type": ["foobar", "barfoo"]}] * 3 + [{"type": ["barfoo"]}] * 2

    def test_apply_successor_category(self):
        # tests: #def apply_successor(sample, successor_restrictions):
        # logger.info("Testing category restriction check")
        # will fail because there are too many fillers
        self.assertEqual(tasks_module.apply_successor(self.sample_category_filler, self.successor_restrictions_category), False)
        # will pass the first iteration and then fail because there are too many fillers
        self.assertEqual(tasks_module.apply_successor(self.sample_category_filler_first_fail, self.successor_restrictions_category), False)
        # will pass the first iteration and then continue
        self.assertEqual(tasks_module.apply_successor(self.sample_category_filler_first, self.successor_restrictions_category), True)
        # will continue
        self.assertEqual(tasks_module.apply_successor(self.sample_category_filler_continue, self.successor_restrictions_category), True)
        # will pass
        self.assertEqual(tasks_module.apply_successor(self.sample_category_mixed, self.successor_restrictions_category), True)

    def test_apply_successor_type(self):
        # tests: #def apply_successor(sample, successor_restrictions):
        # logger.info("Testing type restriction check")
        # will fail because there are too many items that include the type
        self.assertEqual(tasks_module.apply_successor(self.sample_type_foobar, self.successor_restrictions_type), False)
        # will pass at first then fail because there are too many items that include the type
        self.assertEqual(tasks_module.apply_successor(self.sample_type_first_fail, self.successor_restrictions_type), False)
        # will pass the first and then continue
        self.assertEqual(tasks_module.apply_successor(self.sample_type_first, self.successor_restrictions_type), True)
        # will continue
        self.assertEqual(tasks_module.apply_successor(self.sample_type_continue, self.successor_restrictions_type), True)


class TestApplySelect(unittest.TestCase):
    def setUp(self):
        self.select_50_50 = [{"action":"select", "category":"filler", "argument":0.5}, {"action":"select", "category":"target", "argument":0.5}]
        self.select_80_20 = [{"action":"select", "category":"filler", "argument":0.8}, {"action":"select", "category":"target", "argument":0.2}]
        self.select_20_80 = [{"action":"select", "category":"filler", "argument":0.2}, {"action":"select", "category":"target", "argument":0.8}]
        self.select_100 = [{"action":"select", "category":"filler", "argument":1}]
        self.select_category_fail = [{"action":"select", "category":"filler", "argument":0.2}, {"action":"select", "category":"foobar", "argument":0.8}]
        self.tasks = [{"category": "filler"}] * 50 + [{"category": "target"}] * 50
        self.questions_fail = len(self.tasks) + 1
        self.questions_pass = 10

    def test_apply_select(self):
        # tests: def apply_select(questions, select_restrictions, tasks):
        tasks_module.apply_select(self.questions_pass, self.select_50_50, self.tasks)
        with self.assertRaises(AssertionError):
            tasks_module.apply_select(self.questions_pass, self.select_category_fail, self.tasks)
        with self.assertRaises(AssertionError):
            tasks_module.apply_select(self.questions_fail, self.select_50_50, self.tasks)

        # subsequent calls should select different results:
        #logger.debug(tasks_module.apply_select(self.questions_pass, self.select_50_50, self.tasks))
        #logger.debug(tasks_module.apply_select(self.questions_pass, self.select_50_50, self.tasks))

        # it is improbable that two runs produce the exact same sequence
        self.assertNotEqual(tasks_module.apply_select(self.questions_pass, self.select_50_50, self.tasks),
                            tasks_module.apply_select(self.questions_pass, self.select_50_50, self.tasks))

        self.assertEqual(len(tasks_module.apply_select(self.questions_pass, self.select_50_50, self.tasks)), self.questions_pass)
        self.assertEqual(len(tasks_module.apply_select(self.questions_pass, self.select_80_20, self.tasks)), self.questions_pass)
        self.assertEqual(len(tasks_module.apply_select(self.questions_pass, self.select_20_80, self.tasks)), self.questions_pass)
        self.assertEqual(len(tasks_module.apply_select(self.questions_pass, self.select_100, self.tasks)), self.questions_pass)
        #logger.debug(tasks_module.apply_select(self.questions_pass, self.select_100, self.tasks))
        #logger.debug(tasks_module.apply_select(self.questions_pass, self.select_80_20, self.tasks))
        #logger.debug(tasks_module.apply_select(self.questions_pass, self.select_80_20, self.tasks))

        # lets count the result items for the 20_80 test
        result = tasks_module.apply_select(self.questions_pass, self.select_20_80, self.tasks)
        count_filler = 0
        count_target = 0
        for r in result:
            if r['category'] == 'filler':
                count_filler += 1
            elif r['category'] == 'target':
                count_target += 1
        # the checks make sure that a category can only occur once, so it has to be the first
        filler = [r for r in self.select_20_80 if r['category'] == 'filler'][0]
        target = [r for r in self.select_20_80 if r['category'] == 'target'][0]
        # now the counts have to match what's in that particular select restriction
        self.assertEqual(count_filler, int(filler['argument'] * self.questions_pass))
        self.assertEqual(count_target, int(target['argument'] * self.questions_pass))


