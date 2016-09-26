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
import re
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

# build paths
project_root = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
template_path = os.path.join(project_root, 'views')
bottle.TEMPLATE_PATH.insert(0, template_path)

# customize these
cookie_secret = 'ajkbkjnkvnklrkvlkbgjknjkls'
this_port = 63536

# a list of customizable templates
templates = ['first.tpl', 'last.tpl', 'consent.tpl', 'main.tpl']

# study directories have to match this regex
study_regex = "[a-z,A-Z,0-9,-]+"


def configure_study(study, study_path):
    study_settings = os.path.join(study_path, "settings.json")
    study_tasks = os.path.join(study_path, "tasks.json")
    study_template_path = os.path.join(template_path, study)

    assert re.match(study_regex, study), "Rename your directory to match %s" % study_regex

    assert os.path.isfile(
        study_settings), "%s: Please create %s" % (study, study_settings)
    assert os.path.isfile(
        study_tasks), "%s: Please create %s" % (study, study_tasks)

    with open(study_settings, 'r') as fh:
        settings = json.load(fh)
        if 'active' in settings.keys():
            # the active key is opional
            if settings['active'] is False:
                # do not include inactive studies
                return False
        if 'templates' in settings.keys():
            # assert that all templates that are specified by study exist
            assert all([template in templates for template in settings['templates']]), "Study %s uses a template that is not one of: %s" % (study, ', '.join(templates))
            assert all([os.path.isfile(os.path.join(study_template_path, template)) for template in settings['templates']]), "Study %s needs the templates %s in %s" % (study, ', '.join(settings['templates']), study_template_path)
        else:
            settings['templates'] = []
        # let the task selection module worry about restrictions
        #if 'restrictions' in settings.keys():
        #    assert all([restriction in restrictions for restriction in settings['restrictions']]), "Study %s uses a restriction that is not one of: %s" % (study, ', '.join(restrictions))
        settings['name'] = study.capitalize()
        settings['study'] = study
        # settings['template_lookup'] = os.path.join(template_path, study)
    with open(study_tasks, 'r') as fh:
        tasks = json.load(fh)
    assert len(tasks) >= settings[
        'max_step'], 'Study %s: There are not enough tasks (or max_step is too high.)' % study

    return {'settings': settings,
            'tasks': tasks,
            }


def configure():
    studies_path = os.path.join(project_root, 'studies')
    studies = {}
    for study in os.listdir(studies_path):
        study_path = os.path.join(studies_path, study)
        #logger.debug(study_path)
        if os.path.isdir(study_path):
            this_study = configure_study(study, study_path)
            if this_study is False:
                continue
            studies[study] = this_study
    assert len(studies.keys()) > 0, "No studies configured."
    return studies

# print("Please visit:
# <http://127.0.0.1:%i/?prolific_pid=123&session_id=foobar>" % this_port)

print('''Please visit:
      <http://localhost:%i/study/example?prolific_pid=123&session_id=foobar>'''
      % this_port)

# studies are configured by convention
studies = configure()
#logger.debug(list(studies.keys()))


def get_useragent():
    return request.environ.get('HTTP_USER_AGENT')


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
# uas = [opera, chrome, firefox, safari, ie]
# all_uas = ""
# for ua in uas:
# this_ua = get_useragent()
#    this_ua = user_agent_parser.Parse(ua)
#    pp.pprint(this_ua['user_agent']['family'])


def check_useragent(user_agent):
    req = {}
    req['opera'] = 15
    req['chrome'] = 24
    req['firefox'] = 15
    req['safari'] = 8
    req['ie'] = 10
    default_error = "We could not determine the version of your browser. Please use a browser like: %s. " % ', '.join(
        req.keys())
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
    else:
        return default_error

    if int(ua['major']) < min_major:
        minimal = ', '.join([': '.join([k, str(v)]) for k, v in req.items()])
        return "We detected your browser to be %s with the version %s. Unfortunately, it is too old to display this survey. The minimal versions are: %s. " % (family, ua['major'], minimal)
    else:
        return True


def make_error(err, markup=True):
    u''' format error messages'''
    logger.debug(err)
    if markup:
        return template('error.tpl', error=err, name='Error')
    else:
        return err


@error(404)
def error404(error):
    '''generic 404 error page'''
    return make_error("We know nothing about this page.")


@hook('before_request')
def strip_path():
    ''' strip slashes'''
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


def get_study(*args, **kwargs):
    logger.debug("get study")
    logger.debug("args")
    logger.debug(args)
    logger.debug("kwargs")
    logger.debug(kwargs)
    if 'study' in kwargs.keys():
        logger.debug(kwargs['study'])
        if kwargs['study'] in studies.keys():
            return kwargs['study']
    else:
        if len(args) == 1:
            if args[0] in studies.keys():
                return args[0]
    return False


def verified_cookie(f):
    def func_wrapper(*args, **kwargs):
        logger.debug("verified cookie")
        study = get_study(*args, **kwargs)
        logger.debug(study)
        study_cookie = get_study_cookie(study)
        if isinstance(study_cookie, str):
            return make_error(study_cookie)
        else:
            return f(*args, **kwargs)
    return func_wrapper


def verified_study(f):
    def func_wrapper(*args, **kwargs):
        logger.debug("valid study")
        study = get_study(*args, **kwargs)
        if study is False:
            #logger.debug("Study does not exist")
            return make_error("Not a valid study: %s" % study, False)
        else:
            #logger.debug("Study exists")
            return f(*args, **kwargs)
    return func_wrapper


@route('/study/<study>/first', method='GET')
@verified_cookie
@verified_study
def first(study):
    # return template('first.tpl', **studies[study]['settings'])
    return template(os.path.join(template_path, study, 'first.tpl'), **studies[study]['settings'])


@route('/study/<study>/last', method='GET', name='last')
@verified_cookie
@verified_study
def last(study):
    # save the results and check that the data matches up
    results_cookie = get_results_cookie()
    study_cookie = get_study_cookie(study)
    if len(results_cookie) != studies[study]['settings']['max_step'] != len(study_cookie['tasks']) != study_cookie['step']:
        return make_error("Your results don't match up. This is bad.")
    result_ids = [result['id'] for result in results_cookie]
    for task_id in study_cookie['tasks']:
        if task_id not in result_ids:
            return make_error("Could not find all of the tasks that were given you. This is bad.")
    print(get_results_cookie())
    # when should i pay people?
    # yes: display payment link
    # check response times?
    # return template(os.path.join(template_path, study, 'first.tpl'), complete=100, **studies[study]['settings'])
    return template('last.tpl', complete=100, **studies[study]['settings'])


@route('/study/<study>/first', method='POST')
@verified_cookie
@verified_study
def set_first(study):
    # get rt how long it took to read the description
    redirect("/study/%s/main" % study)


@route('/static/<filepath:path>', name='static')
def server_static(filepath):
    return static_file(filepath, root='static')

# todo save results and if it went well give back success message


@route('/study/<study>/task', method='POST', name='task')
@verified_cookie
def set_results(study):
    if 'value' not in request.json.keys():
        return {'message': "Please select a value.", 'status': False}
    if (int(request.json['value']) >= studies[study]['settings']['min_scale'] and
            int(request.json['value']) <= studies[study]['settings']['max_scale']):
        # the step counter is already incremented if a new task is fetched
        # and points to the current task
        # when saving a result it is necessary to get the id of the previous
        # task
        set_results_cookie(get_current_task_id(study), request.json[
                           'situation_rt'], request.json['sentence_rt'], request.json['value'])
        # iterate the step and save it
        study_cookie = get_study_cookie(study)
        study_cookie['step'] += 1
        logger.debug(study_cookie)
        set_study_cookie(study=study, **study_cookie)
        return {'status': True}
    else:
        return {'message': "Invalid choice", 'status': False}


def get_current_task_id(study):
    '''get the id of the current task'''
    study_cookie = get_study_cookie(study)
    return study_cookie['tasks'][study_cookie['step']]


def get_current_task(study):
    '''get the current task'''
    return studies[study]['tasks'][get_current_task_id(study)]


def select_tasks(study):
    # todo generate a list of tasks
    this_tasks = list(range(0, studies[study]['settings']['max_step']))
    #restrictions = studies[study]['settings']['restrictions']
    #logger.debug(restrictions)
    assert len(this_tasks) == studies[study]['settings'][
        'max_step'], 'The number of selected tasks does not match max_step'
    return this_tasks


@route('/study/<study>/task', method='GET', name='task')
@verified_cookie
def fetch_task(study):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        study_cookie = get_study_cookie(study)
        logger.debug("maxstep")
        logger.debug(studies[study]['settings']['max_step'])
        logger.debug("step")
        logger.debug(study_cookie['step'])
        logger.debug("tasks")
        logger.debug(study_cookie['tasks'])
        if study_cookie['step'] == studies[study]['settings']['max_step']:
            data = {'error': "No more steps.", 'status': None}
        elif study_cookie['step'] < studies[study]['settings']['max_step'] and \
                study_cookie['step'] < len(studies[study]['tasks']):
            data = get_current_task(study)
            data['status'] = True
            data['complete'] = get_progress(study_cookie['step'], study=study)
        else:
            data = {'error': "Unknown error.", 'status': False}
    else:
        data = {'error': "Method not allowed.", 'status': False}
    return data


@verified_study
def get_progress(step, study):
    return int(round(((step / float(studies[study]['settings']['max_step'])) * 100), 0))


@route('/study/<study>/main', method='GET')
@verified_cookie
def main(study):
    logger.debug("main")
    logger.debug("Study: %s" % study)
    logger.debug(studies[study]['settings'].keys())
    return template('main.tpl',
                    complete=get_progress(0, study=study),
                    **studies[study]['settings']
                    )


@route('/study/<study>/main', method='POST')
@verified_cookie
def completion(study):
    return ""


def set_study_cookie(pid, sid, step, tasks, study):
    assert step <= studies[study]['settings']['max_step'], 'the current step is greater than max_step'
    assert step <= len(tasks), 'the current step is greater than the number of tasks'
    assert pid is not None, 'pid is None'
    assert sid is not None, 'sid is None'
    #logger.debug("Setting cookie %s" % study)
    return response.set_cookie('surveyriffic-user-%s' % study, {'pid': pid, 'sid': sid, 'step': step, 'tasks': tasks}, secret=cookie_secret)


@verified_study
def get_study_cookie(study):
    this_cookie = request.get_cookie('surveyriffic-user-%s' % study, secret=cookie_secret)
    if this_cookie is None:
        return "Cookie is not set. Please enable cookies and start this survey again."
    assert isinstance(this_cookie, dict), 'the cookie is not a dictionary'
    assert len(this_cookie.keys()) == 4, 'the cookie does not have 4 keys'
    #logger.debug("Getting cookie %s" % study)
    return this_cookie


def set_results_cookie(identifier, sit_rt, sent_rt, value):
    this_list = request.get_cookie(
        'surveyriffic-results', secret=cookie_secret)
    current_result = {'id': identifier, 'sit_rt':
                      sit_rt, 'sent_rt': sent_rt, 'value': value}
    if this_list is None:
        this_list = []
    this_list.append(current_result)
    return response.set_cookie('surveyriffic-results', this_list, secret=cookie_secret)


def get_results_cookie():
    return request.get_cookie('surveyriffic-results', secret=cookie_secret)


@verified_study
def verify_consent(study):
    ''' verifies consent and returns the pid and the sid from the cookie'''
    if not request.forms.get('consent') == "true":
        return "You did not consent with the terms of this study."
    if not request.forms.get('cookie') == "true":
        return "You did not consent with the setting of cookies."

    pid = request.forms.get('prolific_pid')
    if pid == "":
        return "Empty prolific id."

    '''
    sid = request.forms.get('session_id')
    if sid == "":
        return "Empty session id."
    '''
    sid = "foobar"
    response = set_study_cookie(pid, sid, 0, select_tasks(study), study=study)
    return True


@route('/study/<study>/consent', method='POST')
@verified_study
def consent(study):
    consent_result = verify_consent(study)
    if isinstance(consent_result, str):
        return make_error(consent_result)
    elif (consent_result is True):
        redirect("/study/%s/first" % study)
    else:
        return make_error("An unknown error occurred")


@route('/favicon.ico', method='GET')
def favicon():
    return server_static('icons/favicon.ico')


@route('/study/')
@route('/study/<study>')
def index(study=None):

    if study is None:
        return make_error("Please choose a study.")
    if study not in studies.keys():
        return make_error("Please choose an existing study.")

    ua = get_useragent()
    ua_check = check_useragent(ua)
    if isinstance(ua_check, str):
        return make_error(ua_check)

    # You can pass the participant ID at the end of the URL as
    # "?prolific_pid={{%PROLIFIC_PID%}}&session_id={{%SESSION_ID%}}". We'll
    # replace the  {{%PROLIFIC_PID%}} and  {{%SESSION_ID%}} with the values of
    # the participants taking part.

    pid = request.query.prolific_pid
    sid = request.query.session_id

    logger.debug(studies[study]['settings'])
    return template('consent.tpl', session_id=sid, prolific_pid=pid, **studies[study]['settings'])
    # return template(os.path.join(template_path, study, 'consent.tpl'), session_id=sid, prolific_pid=pid, **studies[study]['settings'])


if __name__ == '__main__':
    # cherrypy.config.update({'server.socket_port': this_port-1})
    # cherrypy.quickstart(run(server='cherrypy', port=this_port))
    bottle.run(host='localhost', port=this_port)

