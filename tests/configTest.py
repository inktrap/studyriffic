#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
from modules.config import baseConfig
import os

import logging
logger = logging.getLogger('configTest.py')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


class TestConfigMethods(unittest.TestCase):

    def test_init(self):
        logger.info("Starting test")
        thisConfig = baseConfig()
        logger.debug(thisConfig.project_root)

if __name__ == '__main__':
    unittest.main()
