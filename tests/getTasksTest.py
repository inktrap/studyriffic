#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
from modules.logging import logger
from modules import get_tasks
import os


class TestGetTasks(unittest.TestCase):

    def test_init(self):
        logger.info("Starting test")
        logger.debug()

if __name__ == '__main__':
    unittest.main()
