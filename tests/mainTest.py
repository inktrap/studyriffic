#!/usr/bin/env python3.5

import unittest
from modules import tasks_module
import main
import os

import tests.config
import logging
logger = logging.getLogger(__file__)

# check that tasks and restriction checks work
# they forbid a lot of things so it is easier to just check that they
# letting the good settings/tasks through
class TestMainAttention(unittest.TestCase):
    def setUp(self):
        self.max_check_fail = 5
        self.less_equal = range(0, self.max_check_fail + 1)
        self.greater = range(self.max_check_fail + 1, self.max_check_fail + 10 + 1)

    def test_pass_attention_check(self):

        # these are true
        for this_check in self.less_equal:
            self.assertTrue(main.pass_attention_check(this_check, self.max_check_fail))

        # these are false
        for this_check in self.greater:
            self.assertFalse(main.pass_attention_check(this_check, self.max_check_fail))

        # pass_attention check only checks the value given from the study_cookie
        # max_check_fail is a part of settings and checked on initialization
        # (and this is tested too)
        # fail if too small
        with self.assertRaises(AssertionError):
            self.assertTrue(main.pass_attention_check(-1, self.max_check_fail))
        # fail if string
        with self.assertRaises(AssertionError):
            self.assertTrue(main.pass_attention_check("1", self.max_check_fail))
        # fail if float
        with self.assertRaises(AssertionError):
            self.assertTrue(main.pass_attention_check(1.0, 1))


class TestMainExclusion(unittest.TestCase):
    def setUp(self):
        # def pass_exclusion_check(pid, excluded_pids):
        self.excluded_pids = set(map(str, list(range(1,10)) + list(range(5,20))))
        self.excluded = map(str, range(1,20))
        self.not_excluded_pids = set(map(str, list(range(20 + 1, 20 + 10 + 1))))

    def test_pass_exclusion_check(self):

        # these are false
        for this_excluded in self.excluded_pids:
            self.assertFalse(main.pass_exclusion_check(this_excluded, self.excluded_pids))

        # these are false
        for this_not_excluded in self.not_excluded_pids:
            self.assertTrue(main.pass_exclusion_check(this_not_excluded, self.excluded_pids))

        # every item is not in the empty set
        for this_item in self.excluded_pids.union(self.not_excluded_pids):
            self.assertTrue(main.pass_exclusion_check(this_item, set()))

        # pass_exclusion should not work on the wrong formats
        with self.assertRaises(AssertionError):
            main.pass_exclusion_check(434, self.excluded_pids)
        with self.assertRaises(AssertionError):
            main.pass_exclusion_check("434", [])


class TestMainDemographics(unittest.TestCase):

    def setUp(self):
        self.demographics_empty = [{}]
        self.demographics_empty_results = {'languages': [], 'age': '', 'gender': '', 'native': ''}
        self.demographics_language = [{'name':'languages', 'value':'Finnish'}]
        self.demographics_language_results = {'languages': ['Finnish'], 'age': '', 'gender': '', 'native': ''}
        self.demographics_languages = [{'name':'languages', 'value':'Finnish'}, {'name':'languages', 'value':'Korean'}]
        self.demographics_languages_results = {'languages': ['Finnish', 'Korean'], 'age': '', 'gender': '', 'native': ''}

        self.demographics_age = [{'name':'age', 'value':'20'}]
        self.demographics_age_results = {'languages': [], 'age': '20', 'gender': '', 'native': ''}
        self.demographics_gender = [{'name':'gender', 'value':'Male'}]
        self.demographics_gender_results = {'languages': [], 'age': '', 'gender': 'Male', 'native': ''}
        self.demographics_native = [{'name':'native', 'value':'Russian'}]
        self.demographics_native_results = {'languages': [], 'age': '', 'gender': '', 'native': 'Russian'}
        self.demographics_all = [{'name':'languages', 'value':'Korean'},{'name':'languages', 'value':'German'}, {'name':'age', 'value':'5'}, {'name':'gender', 'value': 'Female'}, {'name':'native', 'value':'Esperanto'}]
        self.demographics_all_results = {'languages': ['Korean', 'German'], 'age': '5', 'gender': 'Female', 'native': 'Esperanto'}

        # this is the default value that is returned if no info (empty)
        # has been provided or something went wrong
        self.demographics_default = {'languages': [], 'age': '', 'gender': '', 'native': ''}
        # check that limiting the result works
        self.demographics_100 = [{'name': 'age', 'value': 'a' * 111}]
        self.demographics_100_result = {'languages': [], 'age': 'a' * 100, 'gender': '', 'native': ''}
        self.demographics_language_100 = [{'name': 'languages', 'value': 'a' * 111}]
        self.demographics_language_100_result = {'languages': ['a' * 100], 'age': '', 'gender': '', 'native': ''}

        self.demographics_age_multi = [{'name':'age', 'value':'20'},{'name':'age', 'value':'20'}]
        self.demographics_age_multi_results = {'languages': [], 'age': '20', 'gender': '', 'native': ''}
        # if only one value is permitted the last value wins (and the user can only specify one value anyway
        self.demographics_age_multi_different = [{'name':'age', 'value':'10'},{'name':'age', 'value':'20'}]
        self.demographics_age_multi_different_results = {'languages': [], 'age': '20', 'gender': '', 'native': ''}

        # a value is empty too, if it only consists of spaces
        self.demographics_age_multi_empty = [{'name':'age', 'value':'20'},{'name':'age', 'value':' ' * 2}]
        self.demographics_age_multi_empty_results = {'languages': [], 'age': '20', 'gender': '', 'native': ''}

        self.demographics_age_multi_overwrite = [{'name':'age', 'value':'10'},{'name':'age', 'value':'20'}]
        self.demographics_age_multi_overwrite_results = {'languages': [], 'age': '20', 'gender': '', 'native': ''}

    def test_verify_demographics(self):
        # def main.verify_demographics(data):
        self.assertEqual(main.verify_demographics(self.demographics_empty), self.demographics_empty_results)
        self.assertEqual(main.verify_demographics(self.demographics_empty), self.demographics_empty_results)
        self.assertEqual(main.verify_demographics(self.demographics_language), self.demographics_language_results)
        self.assertEqual(main.verify_demographics(self.demographics_languages), self.demographics_languages_results)
        self.assertEqual(main.verify_demographics(self.demographics_age), self.demographics_age_results)
        self.assertEqual(main.verify_demographics(self.demographics_gender), self.demographics_gender_results)
        self.assertEqual(main.verify_demographics(self.demographics_native), self.demographics_native_results)
        self.assertEqual(main.verify_demographics(self.demographics_all), self.demographics_all_results)

        # limiting the lenght of results

        self.assertEqual(main.verify_demographics(self.demographics_100), self.demographics_100_result)
        self.assertEqual(main.verify_demographics(self.demographics_language_100), self.demographics_language_100_result)

        # stuff that fails silently
        # the type of input is wrong
        self.assertEqual(main.verify_demographics({}), self.demographics_default)
        # wrong key
        self.assertEqual(main.verify_demographics({'name':'foo', 'value':'bar'}), self.demographics_default)
        # no value key
        self.assertEqual(main.verify_demographics({'name':'age'}), self.demographics_default)
        # no name key
        self.assertEqual(main.verify_demographics({'value':'20'}), self.demographics_default)
        # empty value
        self.assertEqual(main.verify_demographics({'name':'language', 'value':''}), self.demographics_default)

        # these section checks how multiple values are handled
        # simple case:
        self.assertEqual(main.verify_demographics(self.demographics_age_multi), self.demographics_age_multi_results)
        # if only one value is permitted the last value wins (and the user can only specify one value anyway:
        self.assertEqual(main.verify_demographics(self.demographics_age_multi_different), self.demographics_age_multi_different_results)
        # a value is empty too, if it only consists of spaces
        self.assertEqual(main.verify_demographics(self.demographics_age_multi_empty), self.demographics_age_multi_empty_results)
        self.assertEqual(main.verify_demographics(self.demographics_age_multi_overwrite), self.demographics_age_multi_overwrite_results)
