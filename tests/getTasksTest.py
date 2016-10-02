#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
from modules import get_tasks
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


class TestGetTasks(unittest.TestCase):

    def test_init(self):
        # logger.debug(get_tasks.main())
        pass

    def test_main(self):
        logger.info("Starting test")

        '''
        settings = {}
        # restrictions
        # this leads to the following grammar:
        settings['actions'] = ['max_successors', 'select']
        # categories and the types that are defined in tasks.xml
        settings['categories'] = ['filler', 'target']
        settings['types'] = ['any'] + ['soft-presupposition', 'hard-presupposition', 'extra-soft-presupposition'] + ['bad', 'good', 'meh']
        settings['questions'] = 4

        # max_successor defines how many *successors* are *permitted*
        # this allows 2 successors of type 'bad' to follow, so 3 in a sequence are allowed
        # {'action':'max_successors', 'type':'bad', 'argument':2},
        # this allows 0 sucessors of type bad.
        # {'action':'max_successors', 'type':'bad', 'argument':0},
        settings['restrictions'] = [
            {'action':'max_successors', 'type':'bad', 'argument':0},
            {'action':'max_successors', 'type':'good', 'argument':0},
            {'action':'max_successors', 'type':'hard-presupposition', 'argument':0},
            {'action':'max_successors', 'type':'extra-soft-presupposition', 'argument':0},
            {'action':'max_successors', 'type':'soft-presupposition', 'argument':0},
            {'action':'select', 'type':'filler', 'argument':0.5},
            {'action':'select', 'type':'target', 'argument':0.5}
        ]

        tasks = [
            {'category':'filler', 'type':'bad', 'situation':'1','sentence':'Barfoo'},
            {'category':'target', 'type':'hard-presupposition', 'situation':'2','sentence':'Barfoo'},
            {'category':'filler', 'type':'bad', 'situation':'3','sentence':'Barfoo'},
            {'category':'target', 'type':'extra-soft-presupposition', 'situation':'4','sentence':'Barfoo'}
        ]
        '''

        print(get_tasks.main('binary'))

if __name__ == '__main__':
    unittest.main()
