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
import json
import os
import re
from modules import tasks_module
from modules import ua_checker
from modules.config import baseConfig
# dev
import socket
import random

import logging

# get config
thisConfig = baseConfig()
# thisConfig contains self.db which is the mongo-db for this project

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

bottle.TEMPLATE_PATH.insert(0, thisConfig.template_path)


def get_useragent():
    return request.environ.get('HTTP_USER_AGENT')


all_local_studies = []
all_remote_studies = []
random_pid = random.randint(0,1000000)
attention_error = "You failed too many checks for attention."
excluded_error = "You are excluded from this study."
duplicate_error = "Someone with this prolific id already did this study."

for this_study in thisConfig.studies:
    all_local_studies.append('<http://localhost:%i/study/%s?prolific_pid=%i>' % (thisConfig.this_port, this_study, random_pid))
    logger.info("Excluded pids for %s are: %s" % (this_study, ", ".join(map(str, thisConfig.studies[this_study]['settings']['excluded_pids']))))

all_local_studies = '\n'.join(all_local_studies[::-1])
#all_remote_studies = '\n'.join(all_remote_studies[::-1])

logger.info("If running locally, please visit:\n%s" % all_local_studies)
#logger.info("If running remotely, please visit:\n%s" % all_remote_studies)
logger.info("All active studies are: %s" % ', '.join(thisConfig.studies.keys()))

def make_error(err, study=False, markup=True):
    u''' format error messages'''
    logger.error(err)
    if markup:
        return template('error.tpl', error=err, study=study, name='Error')
    else:
        return err


@error(404)
def error404(error):
    '''generic 404 error page'''
    return make_error("We know nothing about this page.")


@error(500)
def error500():
    '''generic 500 error page'''
    return make_error("Internal Server Error.")


@hook('before_request')
def strip_path():
    ''' strip slashes'''
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


def get_study(*args, **kwargs):
    #logger.debug("get study")
    #logger.debug("args")
    #logger.debug(args)
    #logger.debug("kwargs")
    #logger.debug(kwargs)
    if 'study' in kwargs.keys():
        #logger.debug(kwargs['study'])
        if kwargs['study'] in thisConfig.studies.keys():
            return kwargs['study']
    else:
        if len(args) == 1:
            if args[0] in thisConfig.studies.keys():
                return args[0]
    return False


def verified_cookie(f):
    def func_wrapper(*args, **kwargs):
        #logger.debug("verified cookie")
        study = get_study(*args, **kwargs)
        #logger.debug(study)
        study_cookie = get_study_cookie(study)
        if isinstance(study_cookie, str):
            return make_error(study_cookie, study=study)
        else:
            return f(*args, **kwargs)
    return func_wrapper


def verified_study(f):
    def func_wrapper(*args, **kwargs):
        # logger.debug("valid study")
        study = get_study(*args, **kwargs)
        if study is False:
            return make_error("Not a valid study: %s" % study, False)
        else:
            #logger.debug("Study exists")
            return f(*args, **kwargs)
    return func_wrapper

def pass_attention_check(check, max_check_fail):
    ''' return true if an attention check is passed, false otherwise'''
    assert isinstance(check, int)
    assert check >= 0
    return check <= max_check_fail

def pass_exclusion_check(pid, excluded_pids):
    ''' takes the set of excluded pids and checks
    membership for the given pid'''
    assert isinstance(pid, str)
    assert isinstance(excluded_pids, set)
    # if the set is empty it has no member
    # and the check is always passed which is fine
    return not (pid in excluded_pids)


def pass_duplicate_check(study, pid):
    #logger.debug(thisConfig.db[study].find_one({'pid': pid}))
    if thisConfig.db[study].find_one({'pid': pid}) is None:
        return True
    else:
        return False

@route('/study/<study>/first', method='GET')
@verified_cookie
@verified_study
def first(study):
    if "first.tpl" in thisConfig.studies[study]['settings']['templates']:
        return template(os.path.join(thisConfig.template_path, study, 'first.tpl'), **thisConfig.studies[study]['settings'])
    else:
        return template('first.tpl', **thisConfig.studies[study]['settings'])


@route('/study/<study>/demographics', method='GET', name='demographics')
@verified_cookie
@verified_study
def demographics(study):
    return template('demographics.tpl', complete=100, **thisConfig.studies[study]['settings'])


def verify_demographics(data):
    # this function is written to discard everything
    # that is not expected silently
    logger.debug("verifying result, data is:")
    logger.debug(data)
    # initialize empty dict
    result = {'age':'', 'gender':'', 'native':'', 'languages':[]}
    if not isinstance(data, list):
        return result
    logger.debug(data)
    for d in data:
        # check if the format is as expected
        if not isinstance(d, dict):
            logger.warning("Got something else than dict")
            continue
        if not ('name' in d.keys() and 'value' in d.keys()):
            logger.warning("Got not all of 'name' and 'value' keys")
            continue
        # do not save results we did not asked for
        if d['name'] not in result.keys():
            logger.warning("Got values we did not ask for")
            continue
        value = d['value'].strip()
        # skip if the value if it is empty
        if value == '':
            continue
        if len(value) > 100:
            value = value[:100]
        # a person can speak multiple languages
        if d['name'] == 'languages':
            result[d['name']].append(value)
        else:
            result[d['name']] = value
    logger.debug("this is the result:")
    logger.debug(result)
    return result


@route('/study/<study>/demographics', method='POST', name='demographics-complete')
@verified_cookie
@verified_study
def demographics_complete(study):
    # print(request.json)
    if request.json is not None:
        result = verify_demographics(request.json)
        set_demographics_cookie(result, study=study)
        data = {'status': True}
    else:
        data = {'error':'JSON is not set.', 'status':False}
    return data


@route('/study/<study>/last', method='GET', name='last')
@verified_cookie
@verified_study
def last(study):
    logger.debug("entering last")
    # save the results and check that the data matches up
    results_cookie = get_results_cookie(study=study)
    study_cookie = get_study_cookie(study)
    demographics_cookie = get_demographics_cookie(study)
    # better be save and do this without decorators again
    if study_cookie is None:
        return make_error("Could not find your cookie.", study=study)
    if results_cookie is None:
        return make_error("Could not find any of the tasks that were given to you. This is bad.", study=study)
    if not pass_attention_check(study_cookie['check'], thisConfig.studies[study]['settings']['max_check_fail']):
        return make_error(attention_error)
    # assert that saved step in study_cookie == maximal number of steps
    if not (len(results_cookie) == thisConfig.studies[study]['settings']['questions'] == len(study_cookie['tasks']) == study_cookie['step']):
        return make_error("Your results don't match up. This is bad.", study=study)
    # assert that all the tasks that were given out to the user are indeed in the results array
    for index, given_task in enumerate(study_cookie['tasks']):
        if given_task is None:
            return make_error("Your results don't match up. This is bad.", study=study)
        if index > len(results_cookie) - 1:
            return make_error("Your results don't match up. This is bad.", study=study)
        if given_task != results_cookie[index]['id']:
            return make_error("Your results don't match up. This is bad.", study=study)
    result_ids = [result['id'] for result in results_cookie]
    for task_id in study_cookie['tasks']:
        if task_id not in result_ids:
            return make_error("Could not find all of the tasks that were given to you. This is bad.", study=study)

    # logger.debug(study_cookie['pid'])
    # TODO
    if not pass_duplicate_check(study, study_cookie['pid']):
        # this contains the pure error message
        return duplicate_error
    else:
        results = {'results': results_cookie, 'pid': study_cookie['pid'], 'demographics': demographics_cookie}
        try:
            thisConfig.db[study].insert_one(results)
        except:
            return make_error("We could not write your results to the database. This is bad.")
        #logger.info("inserted " + str(thisConfig.db[study].find_one({'pid': study_cookie['pid']})))

    return template('last.tpl', complete=100, **thisConfig.studies[study]['settings'])


@route('/study/<study>/first', method='POST')
@verified_cookie
@verified_study
def set_first(study):
    # get rt how long it took to read the description
    redirect("/study/%s/main" % study)


@route('/static/<filepath:path>', name='static')
def server_static(filepath):
    return static_file(filepath, root=os.path.join(thisConfig.project_root, 'static'))

@route('/study/<study>/task', method='POST', name='task')
@verified_cookie
def set_results(study):
    if 'value' not in request.json.keys():
        return {'message': "Please select a value.", 'status': None}
    if (int(request.json['value']) >= thisConfig.studies[study]['settings']['min_scale'] and
            int(request.json['value']) <= thisConfig.studies[study]['settings']['max_scale']):
        # check if the task is of the type check
        this_task = get_current_task(study)
        study_cookie = get_study_cookie(study)
        # check if we have to check
        if this_task['category'] == 'check':
            # check if the check for attention was successful
            if tasks_module.check_check(check=this_task['check'],
                                        real=request.json['value'],
                                        min_scale=thisConfig.studies[study]['settings']['min_scale'],
                                        max_scale=thisConfig.studies[study]['settings']['max_scale']) is False:
                logger.debug("check_check is False")
                study_cookie['check'] += 1
                set_study_cookie(study=study, **study_cookie)
        # if it was not, check if this happened more than max_check_fail times
        if not pass_attention_check(study_cookie['check'], thisConfig.studies[study]['settings']['max_check_fail']):
            # if it did, return an error.
            return {'message': attention_error, 'status': False}
        # write the results we just got
        set_results_cookie(get_current_task_id(study), request.json[
                           'situation_rt'], request.json['sentence_rt'], request.json['value'], study=study)
        # iterate the step and save it
        study_cookie['step'] += 1
        logger.debug(study_cookie)
        set_study_cookie(study=study, **study_cookie)
        return {'status': True}
    else:
        return {'message': "You send us an invalid choice.", 'status': False}


def get_current_task_id(study):
    '''get the id of the current task'''
    study_cookie = get_study_cookie(study)
    return study_cookie['tasks'][study_cookie['step']]


def get_current_task(study):
    '''get the current task'''
    current_id = get_current_task_id(study)
    # the id is not equivalent to the index anymore
    logger.debug(current_id)
    current_task = list(filter(lambda x: x['id'] == current_id, thisConfig.studies[study]['tasks']))
    logger.debug(current_task)
    assert len(current_task) == 1
    return current_task[0]


def select_tasks(study):
    settings = thisConfig.studies[study]['settings']
    tasks = thisConfig.studies[study]['tasks']
    # logger.debug(tasks)
    random_sample = tasks_module.main(settings, tasks)
    logger.debug(random_sample)
    if isinstance(random_sample, str):
        return make_error(random_sample)
    assert len(random_sample) == thisConfig.studies[study]['settings'][
        'questions'], 'The number of selected tasks does not match the number of planned questions/tasks'
    return [r['id'] for r in random_sample]


@route('/study/<study>/task', method='GET', name='task')
@verified_cookie
def fetch_task(study):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        study_cookie = get_study_cookie(study)
        # do not allow the participant to get a task if max_check_fail is reached
        #if not pass_attention_check(study_cookie['check'], thisConfig.studies[study]['settings']['max_check_fail']):
        #    return make_error(attention_error)
        #logger.debug("maxstep")
        #logger.debug(thisConfig.studies[study]['settings']['questions'])
        #logger.debug("step")
        #logger.debug(study_cookie['step'])
        #logger.debug("tasks")
        #logger.debug(study_cookie['tasks'])
        if study_cookie['step'] == thisConfig.studies[study]['settings']['questions']:
            data = {'error': "No more steps.", 'status': None}
        elif study_cookie['step'] < thisConfig.studies[study]['settings']['questions'] and \
                study_cookie['step'] < len(thisConfig.studies[study]['tasks']):
            # important: get a copy of the current task, delete some of the keys and return it to the user.
            this_data = get_current_task(study).copy()
            # this is information that should not be exposed to the user
            del this_data['type']
            del this_data['category']
            # only checks and fillers have a check
            try:
                del this_data['check']
            except KeyError:
                pass
            data = {'data':this_data, 'status':True, 'complete': get_progress(study_cookie['step'], study=study)}
        else:
            data = {'error': "Unknown error.", 'status': False}
    else:
        data = {'error': "Method not allowed.", 'status': False}
    return data


@verified_study
def get_progress(step, study):
    return int(round(((step / float(thisConfig.studies[study]['settings']['questions'])) * 100), 0))


@route('/study/<study>/main', method='GET')
@verified_cookie
def main(study):
    #logger.debug("main")
    #logger.debug("Study: %s" % study)
    #logger.debug(thisConfig.studies[study]['settings'].keys())
    return template('main.tpl',
                    complete=get_progress(0, study=study),
                    **thisConfig.studies[study]['settings']
                    )


def set_study_cookie(pid, step, tasks, study, check):
    assert isinstance(check, int)
    assert check >= 0
    assert step <= thisConfig.studies[study]['settings']['questions'], 'the current step is greater than the number of questions'
    assert step <= len(tasks), 'the current step is greater than the number of tasks'
    assert pid is not None, 'pid is None'
    #logger.debug("Setting cookie %s" % study)
    return response.set_cookie('studyriffic-study-%s' % study, {'pid': pid, 'step': step, 'tasks': tasks, 'check': check}, secret=thisConfig.cookie_secret)


@verified_cookie
def set_demographics_cookie(results, study):
    return response.set_cookie('studyriffic-demographics-%s' % study, results, secret=thisConfig.cookie_secret)


@verified_cookie
def get_demographics_cookie(study):
    return request.get_cookie('studyriffic-demographics-%s' % study, secret=thisConfig.cookie_secret)


@verified_study
def get_study_cookie(study):
    this_cookie = request.get_cookie('studyriffic-study-%s' % study, secret=thisConfig.cookie_secret)
    if this_cookie is None:
        return "Cookie is not set. Please enable cookies and start this survey again."
    assert isinstance(this_cookie, dict), 'the cookie is not a dictionary'
    assert len(this_cookie.keys()) == 4, 'the cookie does not have 4 keys'
    #logger.debug("Getting cookie %s" % study)
    return this_cookie


def set_results_cookie(identifier, sit_rt, sent_rt, value, study):
    this_list = request.get_cookie(
        'studyriffic-results-%s' % study, secret=thisConfig.cookie_secret)
    current_result = {'id': identifier, 'sit_rt':
                      sit_rt, 'sent_rt': sent_rt, 'value': value}
    if this_list is None:
        this_list = []
    this_list.append(current_result)
    return response.set_cookie('studyriffic-results-%s' % study, this_list, secret=thisConfig.cookie_secret)


def get_results_cookie(study):
    return request.get_cookie('studyriffic-results-%s' % study, secret=thisConfig.cookie_secret)


@verified_study
def verify_consent(study):
    ''' verifies consent and returns the pid from the cookie'''
    if not request.forms.get('consent') == "true":
        return "You did not consent to the terms of this study."
    if not request.forms.get('cookie') == "true":
        return "You did not consent to the setting of cookies."

    pid = request.forms.get('prolific_pid')
    if pid == "":
        return "Empty prolific id."

    # now we have a pid. check if the study was done before
    if not pass_duplicate_check(study, pid):
        # this contains the pure error message
        return duplicate_error
    # check if the user is excluded from the study

    if not pass_exclusion_check(pid, thisConfig.studies[study]['settings']['excluded_pids']):
        return excluded_error

    # logger.debug(study)
    this_tasks = select_tasks(study)
    if isinstance(this_tasks, str):
        return this_tasks

    # we have the tasks and are ready to go!
    set_study_cookie(pid=pid, step=0, tasks=this_tasks, study=study, check=0)

    # reset results if the user cookie is set
    # that way a user cant enter a new id and skip to the last page
    # yes, a user could block this and then skip to the last page
    # but that is something that prolific should take care of (session id check)
    response.set_cookie('studyriffic-results-%s' % study, [], secret=thisConfig.cookie_secret)
    return True


@route('/study/<study>/consent', method='POST')
@verified_study
def consent(study):
    logger.debug(study)
    consent_result = verify_consent(study)
    if isinstance(consent_result, str):
        return make_error(consent_result, study=study)
    elif (consent_result is True):
        redirect("/study/%s/first" % study)
    else:
        return make_error("An unknown error occurred", study=study)


@route('/favicon.ico', method='GET')
def favicon():
    return server_static('icons/favicon.ico')


@route('/study/')
@route('/study/<study>', name='study')
@route('/study/<study>/consent', method='GET')
def index(study=None):

    if study is None:
        return make_error("Please choose a study.")
    if study not in thisConfig.studies.keys():
        return make_error("Please choose an existing study.")

    ua = get_useragent()
    ua_check = ua_checker.main(ua)
    if isinstance(ua_check, str):
        return make_error(ua_check, study=study)

    # You can pass the participant ID at the end of the URL as
    # "?prolific_pid={{%PROLIFIC_PID%}}&session_id={{%SESSION_ID%}}". We'll
    # replace the  {{%PROLIFIC_PID%}} and  {{%SESSION_ID%}} with the values of
    # the participants taking part.

    pid = request.query.prolific_pid

    if not pass_exclusion_check(pid, thisConfig.studies[study]['settings']['excluded_pids']):
        return make_error(excluded_error, study=study)

    # logger.debug(thisConfig.studies[study]['settings'])
    return template('consent.tpl', prolific_pid=pid, **thisConfig.studies[study]['settings'])


if __name__ == '__main__':
    if socket.gethostname() == "box":
        bottle.run(host='localhost', port=thisConfig.this_port)
    else:
        cherrypy.config.update(
            {'server.socket_port': thisConfig.this_port - 1,
             'engine.autoreload.on': False
             }
        )

        cherrypy.quickstart(run(reloader=True, server='cherrypy', port=thisConfig.this_port))

