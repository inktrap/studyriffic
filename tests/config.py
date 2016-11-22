#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    # format = '%m-%d %H:%M:%S',
    datefmt='%m-%d %H:%M:%S',
)

logger = logging.getLogger(__file__)
