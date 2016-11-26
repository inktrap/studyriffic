#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
import os

import tests.config
import logging
logger = logging.getLogger(__file__)

import results

import pprint
pp = pprint.PrettyPrinter(indent=4)

class TestCsvResults(unittest.TestCase):

    def setUp(self):
        '''
        mock_results = [{
            'settings': 'ROOT/studies/owls/settings.json',
            'db': 'ROOT/results/owls/db.json',
            'name': 'owls',
            'tasks': 'ROOT/studies/owls/tasks.json',
            'csv': 'ROOT/results/owls/csv'
        }]
        '''
        self.results = results.csvResults()
        self.outfile = "foobar"

    # helper functions

    def test__check_format(self):
        #def _check_format(self, outfile, data):
        self.assertTrue(self.results._check_format(self.outfile, [["", ""],["", ""]]))
        self.assertTrue(self.results._check_format(self.outfile, [["a", "bb"],["ccc", "dddd"]]))
        with self.assertRaises(AssertionError):
            self.assertTrue(self.results._check_format(self.outfile, [["", ""],["", "", 3]]))
        with self.assertRaises(AssertionError):
            self.assertTrue(self.results._check_format(self.outfile, [["", ""],["", "", ""]]))
        with self.assertRaises(AssertionError):
            self.assertTrue(self.results._check_format(self.outfile, [["", "", ""],["", "", 3]]))
        with self.assertRaises(AssertionError):
            self.assertTrue(self.results._check_format(self.outfile, [[],[]]))
        with self.assertRaises(AssertionError):
            self.assertTrue(self.results._check_format(self.outfile, [{"a":""}, [""]]))
        with self.assertRaises(AssertionError):
            self.assertTrue(self.results._check_format(self.outfile, [{}, {}]))
        with self.assertRaises(AssertionError):
            self.assertTrue(self.results._check_format(self.outfile, [1, 2]))

    def test__joinList(self):
        #def _joinList(self, this_list):
        self.assertEqual(self.results._joinList([1,2,3]), "1 2 3")
        self.assertEqual(self.results._joinList(["a","b",3]), "a b 3")
        self.assertEqual(self.results._joinList([""]), "")
        self.assertEqual(self.results._joinList([" ", " "]), "")
        self.assertEqual(self.results._joinList([" ", "-", " "]), "-")
        self.assertEqual(self.results._joinList([" ", " - ", " "]), "-")
        self.assertEqual(self.results._joinList([" det ", " adj ", "  noun "]), "det adj noun")
        self.assertEqual(self.results._joinList([" d et ", " adj ", "  noun "]), "d et adj noun")
        with self.assertRaises(AssertionError):
            self.results._joinList({" ":""})
        with self.assertRaises(AssertionError):
            self.results._joinList("abc")

    def test__mergeLists(self):
        #def _mergeLists(self, *args):
        self.assertEqual(self.results._mergeLists(), [])
        self.assertEqual(self.results._mergeLists([1,2]), [1,2])
        self.assertEqual(self.results._mergeLists([1,2], [3]), [1,2,3])
        self.assertEqual(self.results._mergeLists([1,2], [3], [4]), [1,2,3,4])
        self.assertEqual(self.results._mergeLists([1,"a"], ["b"], [4]), [1,"a","b",4])
        with self.assertRaises(AssertionError):
            self.results._mergeLists({1:"a"}, ["b"], [4])
        with self.assertRaises(AssertionError):
            self.results._mergeLists(1, ["b"], [4])

    # main functions (these should be tested first)

    def test_makeSettings(self):
        #def makeSettings(self, items):
        self.assertEqual(self.results.makeSettings({"a": "b"}), [["a"], ["b"]])
        self.assertEqual(self.results.makeSettings({"a": "b", "c": "d", "e": "f"}), [["a", "c", "e"], ["b", "d", "f"]])
        self.assertEqual(self.results.makeSettings({"a": 1, "c": "d", "e": 2}), [["a", "c", "e"], ["1", "d", "2"]])
        with self.assertRaises(AssertionError):
            self.results.makeSettings(["a"])

    def test_makeTasks(self):
        #def makeTasks(self, items, settings):
        items_check = [{'check': '[0]', 'value':'bar', 'type':['b']}]
        items = [{'value':'bar', 'type':['b']}]
        settings = {'types': ["b", "a"]}
        items_many = [{'value':'foo', 'type':['a']}, {'value':'bar', 'type':['b']}]
        items_less = [{'value':'foo', 'type':['a']}, {'type':['b']}]

        # self.assertEqual(self.results.makeTasks(items, settings), [])
        self.assertEqual(self.results.makeTasks(items_check, {'types': ["b"]}), [["value", "bType"], ["bar", "b"]])
        self.assertEqual(self.results.makeTasks(items_check, {'types': ["b"]}), self.results.makeTasks(items, {'types': ["b"]}))
        self.assertEqual(self.results.makeTasks(items_check, settings), [["value", "bType", "aType"], ["bar", "b", ""]])
        self.assertEqual(self.results.makeTasks(items_many, {'types': ["b", "a"]}), [["value", "bType", "aType"], ["foo", "", "a"], ["bar", "b", ""]])

        with self.assertRaises(AssertionError):
            self.results.makeTasks(items, {})
        with self.assertRaises(AssertionError):
            self.assertEqual(self.results.makeTasks(items_less, {'types': ["b", "a"]}), [["value", "bType", "aType"], ["foo", "", "a"], ["bar", "b", ""]])

    def test_makeAnswers(self):
        #def makeAnswers(self, items):
        items = [{'pid': 'example', 'results':[{"a":"afoo"}, {"a":"bfoo"}, {"a":"cfoo"}]}]
        self.assertEqual(self.results.makeAnswers(items), [['pid', 'a'], ['example', 'afoo'], ['example', 'bfoo'], ['example', 'cfoo']])

    def test_makeDemographics(self):
        #def makeDemographics(self, items):
        #self.assertTrue(True)
        languages = ["foo", "bar", "baz"]
        items = [{'pid': "example", 'demographics': {'languages': languages, 'age': 4, 'name': 'foobar'}}]
        self.assertEqual(self.results.makeDemographics(items), [['pid', 'age', 'languages', 'name'], ['example', '4', 'foo bar baz', 'foobar']])

    def test_makeAll(self):
        #def makeAll(self, demographics, tasks, answers):
        demographics = [['pid', 'age', 'languages', 'name'], ['example', '4', 'foo bar baz', 'foobar']]
        answers = [['pid', 'id'], ['example', 'aID'], ['example', 'bID'], ['example', 'cID']]
        tasks = [["value", "id", "aType", "sentence", "situation"], ["foo", "aID", "a", "sentence", "situation"], ["bar", "bID", "", "sentence", "situation"], ["baz", "cID", "", "sentence", "situation"]]
        self.assertEqual(self.results.makeAll(demographics, tasks, answers), [])

        # self.assertTrue(True)
        # self.assertEqual(self.results.makeAll(), )

    # functions with a lot of side effects that can only
    # be tested to throw the right assertions
    def test_write(self):
        #def write(self, data, outfile):
        with self.assertRaises(AssertionError):
            self.results.write([["a"],["b"]], 1)
        with self.assertRaises(AssertionError):
            self.results.write([["a"],["b"]], 3424.0)
        with self.assertRaises(AssertionError):
            self.results.write([["a"],["b"]], [])
        with self.assertRaises(AssertionError):
            self.results.write([["a"],["b"]], {})

    def test_loadJson(self):
        #def loadJson(self, name, results):
        # name has to be a string and
        # results has to be a dict
        # this test is a little bit … useless?
        with self.assertRaises(AssertionError):
            self.results.loadJson("foo", [])
        with self.assertRaises(AssertionError):
            self.results.loadJson(1, {})
        with self.assertRaises(AssertionError):
            self.results.loadJson("foo", 1)


if __name__ == '__main__':
    unittest.main()

