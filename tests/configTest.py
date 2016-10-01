#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
from modules.logging import logger


class TestConfigMethods(unittest.TestCase):

    def test_init(self):
        logger.info("Starting test")

if __name__ == '__main__':
    unittest.main()
