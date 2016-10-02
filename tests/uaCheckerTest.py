#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import unittest
import pprint
from modules import ua_checker
pp = pprint.PrettyPrinter(indent=4)

import logging
logger = logging.getLogger('uaCheckerTest.py')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


class TestUaChecker(unittest.TestCase):

    def setUp(self):
        #logger.info("Starting test")

        opera = ['Opera', "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36 OPR/15.0.1147.100"]
        chrome = ['Chrome Mobile', "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"]
        firefox = ['Firefox', "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"]
        safari = ['Safari', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71"]
        ie = ['IE', "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"]
        edge = ['Edge', "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136"]
        self.uas = [opera, chrome, firefox, safari, ie, edge]
        self.this_keys = ['family', 'major', 'minor', 'patch']

    # possible testcase
    def test_parse_major(self):
        ''' check that the major version matches'''
        for ua in self.uas:
            ua_result = ua_checker.parse_useragent(ua[1])
            self.assertEqual(ua[0], ua_result['family'])

    def test_parse_keys(self):
        ''' check that all the keys are there'''
        for ua in self.uas:
            ua_result = ua_checker.parse_useragent(ua[1])
            for this_key in self.this_keys:
                self.assertEqual(True, this_key in ua_result.keys())

if __name__ == '__main__':
    unittest.main()
