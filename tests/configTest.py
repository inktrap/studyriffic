#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
from modules.config import baseConfig
import os

import tests.config
import logging
logger = logging.getLogger(__file__)

import pprint
pp = pprint.PrettyPrinter(indent=4)

class TestConfigMethods(unittest.TestCase):
    def setUp(self):
        self.thisConfig = baseConfig()

    def test_existBasicKeys(self):
        ''' test that a config class has the basic keys'''
        # logger.info("Testing existence basic keys")
        assert hasattr(self.thisConfig, 'project_root')
        assert hasattr(self.thisConfig, 'cookie_secret')
        assert hasattr(self.thisConfig, 'this_port')
        assert hasattr(self.thisConfig, 'template_path')

    def test_typeBasicKeys(self):
        ''' test that a config class has the basic keys'''
        # logger.info("Testing types of basic keys")
        assert isinstance(self.thisConfig.project_root, str)
        assert isinstance(self.thisConfig.cookie_secret, str)
        assert isinstance(self.thisConfig.this_port, int)
        assert isinstance(self.thisConfig.template_path, str)

    def test_valueBasicKeys(self):
        ''' test that a config class has the basic keys'''
        # logger.info("Testing value of basic keys")
        assert len(self.thisConfig.project_root) > 0
        assert os.path.isdir(self.thisConfig.project_root)
        assert len(self.thisConfig.cookie_secret) > 0
        assert self.thisConfig.this_port > 0
        assert len(self.thisConfig.template_path) > 0
        assert os.path.isdir(self.thisConfig.template_path)


if __name__ == '__main__':
    unittest.main()
