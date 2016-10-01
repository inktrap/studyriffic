#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
from modules.logging import logger
from modules.config import baseConfig
import os


class TestConfigMethods(unittest.TestCase):

    def test_init(self):
        logger.info("Starting test")
        project_root = os.path.abspath(os.path.dirname(os.path.realpath(os.path.join(__file__, '..'))))
        template_path = os.path.join(project_root, 'views')
        thisConfig = baseConfig(project_root, template_path)
        logger.debug(thisConfig.studies)

if __name__ == '__main__':
    unittest.main()
