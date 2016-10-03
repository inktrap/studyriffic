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
        # logger.info("Starting test")
        study = 'binary'
        settings = thisConfig.studies[study]['settings']
        tasks = thisConfig.studies[study]['tasks']
        print(get_tasks.main(settings, tasks))

if __name__ == '__main__':
    unittest.main()
