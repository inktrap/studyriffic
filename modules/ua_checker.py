#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from ua_parser import user_agent_parser
import pprint
pp = pprint.PrettyPrinter(indent=4)


def parse_useragent(ua):
    try:
        result = user_agent_parser.Parse(ua)
        assert 'user_agent' in result.keys(
        ), '"user_agent" is not a key of the parsed result'
        assert 'major' in result[
            'user_agent'].keys(), '"major" is not a key of the parsed result'
        assert 'family' in result[
            'user_agent'].keys(), '"family" is not a key of the parsed result'
    except:
        return False
    return result['user_agent']


def main(user_agent):
    ''' return true if the ua is allowed, if not an error message'''

    req = {}
    req['opera'] = 15
    req['chrome'] = 24
    req['firefox'] = 15
    req['safari'] = 8
    req['ie'] = 10
    req['edge'] = 12
    default_error = "We could not determine the version of your browser. Please use a browser like: %s. " % ', '.join(
        [r.capitalize() for r in req.keys()])
    ua = parse_useragent(user_agent)
    if not ua:
        return default_error
    family = ua['family'].lower()
    if 'opera' in family:
        min_major = req['opera']
    elif 'chrome' in family:
        min_major = req['chrome']
    elif 'firefox' in family:
        min_major = req['firefox']
    elif 'safari' in family:
        min_major = req['safari']
    elif 'ie' in family:
        min_major = req['ie']
    elif 'edge' in family:
        min_major = req['edge']
    else:
        return default_error

    if int(ua['major']) < min_major:
        minimal = ', '.join([' '.join([k.capitalize(), str(v)]) for k, v in req.items()])
        return "We detected your browser to be %s version %s. Unfortunately, this version is too old to display this study. The minimal versions are: %s. " % (family.capitalize(), ua['major'], minimal)
    else:
        return True


