#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import bottle
import cherrypy
from bottle import route, run, template
from bottle import request
from bottle import response
from bottle import redirect
from bottle import static_file, post, url
from bottle import error
from bottle import hook
from bottle import BaseRequest
from bottle import SimpleTemplate
SimpleTemplate.defaults["url"] = url
from ua_parser import user_agent_parser
import json
import os
# dev
import pprint
pp = pprint.PrettyPrinter(indent=4)

import logging
# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

cookie_secret = 'ajkbkjnkvnklrkvlkbgjknjkls'
this_port = 63536
project_root = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


@route('/study')
@route('/study/')
@route('/study/<this_study>')
def study(this_study='World'):
    return "Hello %s" % str(this_study)

if __name__ == '__main__':
    # cherrypy.config.update({'server.socket_port': this_port-1})
    # cherrypy.quickstart(run(server='cherrypy', port=this_port))
    bottle.run(host='localhost', port=this_port)
