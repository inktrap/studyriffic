#!/usr/bin/env python3.5

from operator import eq
import random
import math

from functools import wraps
import errno
import os
import signal

from modules.config import thisConfig

import logging
logger = logging.getLogger('get_tasks')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

''' this modules
 - checks the config for the study, semantically, datatypes, missing stuff
 - selects the tasks for ONE study, according to the restrictions
 - checks that the order fits the requirements and will fail with a
   TimeoutError if the requirements can't be met.
'''


class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    # source: <http://stackoverflow.com/a/2282656>
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def check_restriction(settings, restriction):
    assert isinstance(restriction, dict)
    assert 'action' in restriction.keys()
    assert 'type' in restriction.keys()
    assert 'argument' in restriction.keys()
    assert len(restriction.keys()) == 3
    assert restriction['action'] in settings['actions']
    assert isinstance(restriction['type'], str)
    # print(type(restriction['argument']))
    assert (isinstance(restriction['argument'], int) or
            eq('all', restriction['argument']) or
            isinstance(restriction['argument'], float))

    if restriction['action'] == 'max_successors':
        assert isinstance(restriction['argument'], int)
        assert restriction['argument'] >= 0
    elif restriction['action'] == 'select':
        assert isinstance(restriction['argument'], float)
        assert 0.0 < restriction['argument'] < 1.0
    else:
        raise ValueError("Unknown restriction action %s" % restriction['action'])


def check_task(settings, task):
    assert isinstance(task, dict)
    assert 'category' in task.keys()
    assert 'type' in task.keys()
    assert 'situation' in task.keys()
    assert 'sentence' in task.keys()
    assert len(task.keys()) == 4
    assert task['category'] in settings['categories']
    assert task['type'] in settings['types']
    assert isinstance(task['situation'], str)
    assert isinstance(task['sentence'], str)


def get_select_restrictions(restrictions):
    #logger.debug(restrictions)
    return list(filter(lambda x: x['action'] == 'select', restrictions))


def check_select(settings, select_restrictions):
    # semantic checks for select restrictions
    # check if the numbers of selects add up to 1
    assert sum([select_restriction['argument'] for select_restriction in select_restrictions]) == 1

    # check if select has been specified more than once with the same argument
    select_types = [select_restriction['type'] for select_restriction in select_restrictions]
    assert len(set(select_types)) == len(select_types), "A type can only be used once in a select statement, otherwise it contradicts the previous statements."

    # check that all the arguments are dividable without a remainder
    for select_restriction in select_restrictions:
        #print(math.modf(settings['questions'] * select_restriction['argument'])[0])
        assert (math.modf(settings['questions'] * select_restriction['argument']))[0] == 0.0, "selection arguments can not produce items less than 1 (F.e.: You can not split a question in half)."
    return True


def apply_successor(sample, successor_restrictions):
    ''' apply the successors and return true or false if the sample is valid'''
    assert len(sample) > 0
    assert len(successor_restrictions) > 0
    # apply
    for index, item in enumerate(sample):
        # check every restriction
        for successor_restriction in successor_restrictions:
            # if there are not enough items, their order is not important
            if (index + successor_restriction['argument'] + 2) >= len(sample):
                continue
            # extract all the unique types form the given range into a list
            # the range includes the current item (index)
            # and on top of that the items that are allowed
            # and on top of that the item that *might* be not allowed
            # and it is +2 because slices give an interval like [x,y)
            #print(successor_restriction)
            #print(list(map(lambda x: x['type'], sample[index:index + successor_restriction['argument'] + 2])))
            successors = list(set(map(lambda x: x['type'], sample[index:index + successor_restriction['argument'] + 2])))
            if len(successors) == 1 and (successors[0] == successor_restriction['type']):
                return False
    return True


def apply_select(settings, select_restrictions, tasks):
    result = []
    # apply
    for select_restriction in select_restrictions:
        # get tasks by category
        # this works nicely because dictionary keys are **NOT** ordered
        # otherwise the first entries would be favored
        category_tasks = list(filter(lambda x: x['category'] == select_restriction['type'], tasks))
        assert len(category_tasks) > 0
        # get number of entities the current restriction takes
        take_restrictions = settings['questions'] * select_restriction['argument']
        # print(take_restrictions)
        # print(len(category_tasks))
        assert take_restrictions <= len(category_tasks)
        # create a list of the indices
        # we can use int here, because I checked this with math.modf before
        random_sample = random.sample(category_tasks, int(take_restrictions))
        # random.sample: Used for random sampling without replacement.
        result += random_sample

    # shuffle, because the *selections* were applied in order
    random.shuffle(result)
    return result


@timeout(5)
def main(study):
    settings = thisConfig.studies[study]['settings']
    tasks = thisConfig.studies[study]['tasks']
    check_config(settings, tasks)
    # returns a random sample
    # apply the strictions and just to be save, do so with a timeout
    # (in the tests I did i never waited longer than 0.11s even with very strict
    # restrictions and a small number of tasks)
    select_restrictions = get_select_restrictions(settings['restrictions'])
    check_select(settings, select_restrictions)
    random_sample = apply_select(settings, select_restrictions, tasks)
    successor_restrictions = list(filter(lambda x: x['action'] == 'max_successors', settings['restrictions']))
    if len(successor_restrictions) > 0:
        is_restricted = apply_successor(random_sample, successor_restrictions)
        while (is_restricted is False):
            random_sample = apply_select(settings, select_restrictions, tasks)
            is_restricted = apply_successor(random_sample, successor_restrictions)
    return random_sample


def check_config(settings, tasks):
    '''
    see if:
        the tasks implement the categories and types from settings
        selections have semantical contradictions
        restrictions have the allowed datatypes
    '''
    assert 'restrictions' in settings.keys()
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    for this_restriction in settings['restrictions']:
        check_restriction(settings, this_restriction)
    check_select(settings, get_select_restrictions(settings['restrictions']))

    for task in tasks:
        check_task(settings, task)
    return True

