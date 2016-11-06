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
            "questions": 10,
            "actions": ["select", "max_successors", "not_positions"],
            "types":["some", "types", "and", "more"],
            "categories":["filler", "target"]
        }
        self.complete_settings = {}
        self.complete_settings["active"] = True
        self.complete_settings["labels"] = False
        self.complete_settings["questions"] = 10
        self.complete_settings["min_scale"] = 0
        self.complete_settings["max_scale"] = 1
        self.complete_settings["time"] = 10
        self.complete_settings["situation"] = "Situation"
        self.complete_settings["question"] = "Question"
        self.complete_settings["min_scale_desc"] = "Min"
        self.complete_settings["max_scale_desc"] = "Max"
        self.complete_settings["university"] = "Uni"
        self.complete_settings["investigator"] = "Investigator"
        self.complete_settings["contact"] = "contact"
        self.complete_settings["link"] = "link"
        self.complete_settings["restrictions"] = [{"action":"select", "category":"filler", "argument":1.0}]
        self.complete_settings["actions"] = ["select"]
        self.complete_settings["types"] = []
        self.complete_settings["categories"] = []
        self.complete_settings["templates"] = []

        # these should all work
        self.task_filler = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": ["some", "types"], "category": "filler", "check": [0.0]}
        self.task_target = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": ["some", "types"], "category": "target"}
        self.task_no_situation = {"id": 0, "sentence": "Foobar", "situation": "", "type": ["some", "types"], "category": "filler", "check": [0.0]}
        self.task_no_type = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": [], "category": "filler", "check": [0.0]}
        self.task_no_sentence = {"id": 0, "sentence": "", "situation": "Barfoo", "type": [], "category": "filler", "check": [0.0]}

        # these should not work
        self.task_no_id = {"id": "", "sentence": "", "situation": "Barfoo", "type": [], "category": "filler", "check": [0.0]}
        self.task_no_category = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": [], "category": "", "check": [0.0]}
        self.task_no_check_check = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": [], "category": "check"}
        self.task_no_check_filler = {"id": 0, "sentence": "Foobar", "situation": "Barfoo", "type": [], "category": "filler"}

        # syntactically well formed restrictions
        self.restriction_successor_filler = {"action":"max_successors", "category":"filler", "argument":4}
        self.restriction_successor_target = {"action":"max_successors", "category":"target", "argument":4}
        self.restriction_successor_more = {"action":"max_successors", "type":"some", "argument":4}
        self.restriction_successor_some = {"action":"max_successors", "type":"more", "argument":4}
        self.restriction_successor_error = {"action":"max_successors", "type":"and", "argument":4}
        self.restriction_select_filler = {"action":"select", "category":"filler", "argument":0.5}
        self.restriction_select_target = {"action":"select", "category":"target", "argument":0.5}
        self.restriction_position_fine = {"action":"not_positions", "category":"check", "argument":[1, 3]}
        self.restriction_position_error_value = {"action":"not_positions", "category":"check", "argument":[0, "a"]}
        self.restriction_position_error_argument = {"action":"not_positions", "category":"check", "argument":"a"}

    def test_check_settings(self):
        self.assertTrue(tasks_module.check_settings(self.complete_settings))
        #with self.assertRaises(AssertionError):
        #    tasks_module.check_settings(self.complete_settings)

    def test_check_restriction(self):
        #tests: def check_restriction(settings, restriction):
        self.assertTrue(tasks_module.check_restriction(self.settings, self.restriction_select_filler))
        self.assertTrue(tasks_module.check_restriction(self.settings, self.restriction_select_target))
        self.assertTrue(tasks_module.check_restriction(self.settings, self.restriction_successor_filler))
        self.assertTrue(tasks_module.check_restriction(self.settings, self.restriction_successor_target))
        self.assertTrue(tasks_module.check_restriction(self.settings, self.restriction_successor_more))
        self.assertTrue(tasks_module.check_restriction(self.settings, self.restriction_successor_some))
        self.assertTrue(tasks_module.check_restriction(self.settings, self.restriction_position_fine))
        with self.assertRaises(AssertionError):
            tasks_module.check_restriction(self.settings, self.restriction_position_error_value)
        with self.assertRaises(AssertionError):
            tasks_module.check_restriction(self.settings, self.restriction_position_error_argument)

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
        with self.assertRaises(AssertionError):
            tasks_module.check_task(self.settings, self.task_no_check_check)
        with self.assertRaises(AssertionError):
            tasks_module.check_task(self.settings, self.task_no_check_filler)


class TestCheckNotPositions(unittest.TestCase):
    ''' test if not positions checks work '''
    def setUp(self):
        self.restriction_position_fine = [{"action":"not_positions", "category":"check", "argument":[1, 3]}]
        self.restriction_position_error = [{"action":"not_positions", "category":"check", "argument":[0]}] * 2
        self.restriction_position_error_later = [{"action":"not_positions", "category":"filler", "argument":[0]},
                                                 {"action":"not_positions", "category":"check", "argument":[0]},
                                                 {"action":"not_positions", "category":"filler", "argument":[2]}]

    def test_check_notpos(self):
        # def check_notpos(notpos_restrictions):
        self.assertEqual(tasks_module.check_notpos(self.restriction_position_fine), True)
        with self.assertRaises(AssertionError):
            tasks_module.check_notpos(self.restriction_position_error)
        with self.assertRaises(AssertionError):
            tasks_module.check_notpos(self.restriction_position_error_later)


class TestApplyNotPositions(unittest.TestCase):
    ''' test if not positions do what they should '''
    def setUp(self):
        self.restriction_position_fine = [{"action":"not_positions", "category":"check", "argument":[1, 3]}]
        self.restriction_position_error_0 = [{"action":"not_positions", "category":"check", "argument":[0]}]
        self.restriction_position_error_2 = [{"action":"not_positions", "category":"check", "argument":[2]}]
        self.restriction_position_error_later = self.restriction_position_fine + self.restriction_position_error_2
        self.task_check = [{"category": "check"}, {"category": "filler"},{"category": "check"}, {"category": "filler"}]

    def test_apply_not_positions(self):
        # def apply_not_positions(sample, notpos_restrictions):
        # this will work
        self.assertEqual(tasks_module.apply_not_positions(self.task_check, self.restriction_position_fine), True)
        # this will not work
        self.assertEqual(tasks_module.apply_not_positions(self.task_check, self.restriction_position_error_0), False)
        self.assertEqual(tasks_module.apply_not_positions(self.task_check, self.restriction_position_error_2), False)
        self.assertEqual(tasks_module.apply_not_positions(self.task_check, self.restriction_position_error_later), False)


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


