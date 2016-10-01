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

# possible testcase
# opera = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36 OPR/15.0.1147.100"
# chrome = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"
# firefox = "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
# safari = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71"
# ie = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
# edge = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136"
# uas = [opera, chrome, firefox, safari, ie, edge]
# all_uas = ""
# for ua in uas:
# this_ua = get_useragent()
#    this_ua = user_agent_parser.Parse(ua)
#    pp.pprint(this_ua['user_agent']['family'])


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


