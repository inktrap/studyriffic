#!/usr/bin/env python3.5

from operator import eq
import random
import numbers
import math

from functools import wraps
import errno
import os
import signal
import re

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    # format = '%m-%d %H:%M:%S',
    datefmt='%m-%d %H:%M:%S',
)
logger = logging.getLogger(__file__)

#fh = logging.FileHandler('tasks_module.log')
#fh.setLevel(logging.INFO)
#fh.setFormatter(formatter)
#logger.addHandler(fh)


''' this modules
 - checks the config for the study, semantically, datatypes, missing stuff
 - selects the tasks for ONE study, according to the restrictions
 - checks that the order fits the requirements and will fail if a lot of tries are not enough
'''


def check_restriction(settings, restriction):
    # check any restriction
    assert isinstance(restriction, dict), "a restriction has to be a dictionary"
    assert 'action' in restriction.keys(), "a restriction has to have an action"
    assert (not('type' in restriction.keys() and 'category' in restriction.keys())), "a restriction operates on a type or a category, not both."
    assert 'argument' in restriction.keys(), "a restriction has to have an argument."
    assert len(restriction.keys()) == 3, "a restriction has to have 3 keys."
    assert restriction['action'] in settings['actions'], 'the action "%s" of a restriction is not in the settings file.' % restriction['action']

    if 'type' in restriction.keys():
        assert isinstance(restriction['type'], str), "a type of a restriction has to be a string."
    elif 'category' in restriction.keys():
        assert isinstance(restriction['category'], str), "a category of a restriction has to be a string."

    if restriction['action'] == 'max_successors':
        assert isinstance(restriction['argument'], int)
        assert 'category' in restriction.keys() or 'type' in restriction.keys(), "A max_successors restriction has to operate on either a type or a category"
        assert restriction['argument'] >= 0, "For the argument a of a max_successors restriction it has to hold that 0 <= a"
        # assert restriction['argument'] < settings['questions'], "For the argument a of a max_successors restriction it is probably a mistake if a >= the number of questions."
    elif restriction['action'] == 'select':
        assert isinstance(restriction['argument'], int), "A select restriction has to select a number of tasks"
        assert 'category' in restriction.keys()
        assert 0.0 < restriction['argument'] <= settings['questions'], "The argument for a select restriction x has to have the following property: 0 < x <= (number of tasks)"
    elif restriction['action'] == 'not_positions':
        assert isinstance(restriction['argument'], list)
        assert 'category' in restriction.keys(), "A not_positions restriction has to operate on a category"
        for a in restriction['argument']:
            assert isinstance(a, int), "A position in a list handed to not_positions has to be an integer"
        #print(settings['questions'])
        assert (max(restriction['argument']) < settings['questions']), "For a position p (starting with 0) it has to hold that p < N, where N is the number of the positions|questions available."
        assert (0 <= min(restriction['argument'])), "For a position p it has to hold that 0 <= p"
    else:
        raise ValueError("Unknown restriction action %s" % restriction['action'])
    return True


def _check_task_check(task):
    ''' check that the checks are correct '''
    assert 'check' in task.keys(), "A filler or a check has to check for an expected value"
    assert isinstance(task['check'], list), "A check has to be a list"
    for c in task['check']:
        assert isinstance(c, float), "A check has to specify a list of either one or two floating point numbers"
        assert (0 <= c <= 1), "The value c of a check has to be a floating point number 0.0 <= c <= 1"
    assert (1 <= len(task['check']) <= 2), "A check has to specify either one or two floating point numbers, not %i" % len(task['check'])
    if len(task['check']) == 2:
        assert task['check'][0] < task['check'][1], "If there are two floating point numbers c1 and c2 it has to hold that c1 < c2"
    return True


def check_task(settings, task):
    assert isinstance(task, dict), "A task has to be a dictionary"

    logger.debug(task)

    # check that all the keys are there
    assert 'category' in task.keys()
    assert 'type' in task.keys()
    assert 'situation' in task.keys()
    assert 'sentence' in task.keys()
    assert 'id' in task.keys()
    assert len(task['category']) > 0, "A category can not be empty."
    assert task['category'] in settings['categories'], "The category %s has to be in settings" % task['category']

    # if the task is a filler or a check, check the checks
    if (task['category'] == "check") or (task['category'] == "filler"):
        assert len(task.keys()) == 6, "A filler or a check has to have 6 keys."
        _check_task_check(task)
    else:
        assert len(task.keys()) == 5, 'A task that is not a filler or a check has to have 5 keys.'

    # check the types
    assert isinstance(task['type'], list)
    for t in task['type']:
        assert isinstance(t, str), "A type is a list of strings. But the type %s is not a string." % t
        assert t in settings['types'], "The type %s has to be in settings." % t
        assert len(t) > 0, "A type, if given, can not be empty. (Id: %i)" % task['id']

    # this is one of to checks for the ids (ids have to start with 0 and have to be ints 0,1,2,3 aso.)
    assert isinstance(task['id'], int)

    assert isinstance(task['situation'], str)
    assert isinstance(task['sentence'], str)
    assert len(task['sentence']) > 0, "A sentence can not be empty. (Id: %i)" % task['id']

    return True


def check_notpositions(notpos_restrictions):
    ''' check all the notpos-restrictions'''
    notpos_categories = []
    for notpos_restriction in notpos_restrictions:
        if 'category' in notpos_restriction.keys():
            notpos_categories.append(notpos_restriction['category'])
        else:
            raise AssertionError('''not_positions restrictions have to operate on
                    either a type or a category. This also means that sadly a
                    previous check failed, which should never happen.''')

    assert len(set(notpos_categories)) == len(notpos_categories), "A category can only be used once in a not_positions statement, please merge the restrictions."

    return True

def check_select(questions, select_restrictions):
    assert len(select_restrictions) > 0, "You have to specify at least one select restriction"

    # semantic checks for select restrictions
    # check if the numbers of selects add up to the number of tasks
    select_sum = sum([select_restriction['argument'] for select_restriction in select_restrictions])
    logger.debug(select_sum)
    assert select_sum == questions, "Select restrictions have to sum up to the number of tasks (%i), these sum up to: %i" % (questions, select_sum)

    select_categories = []

    for select_restriction in select_restrictions:
        logging.debug(math.modf(questions * select_restriction['argument'])[0])
        assert isinstance(select_restriction['argument'], int), "selection arguments have to be integers, you can not split a task"
        assert 'category' in select_restriction.keys(), "Category key not present"
        assert select_restriction['argument'] > 0, "The argument of a select restriction must be greater 0 (it has to select something)"
        assert select_restriction['argument'] <= questions, "The argument of a select restriction must be <= (number of tasks) (you can't select more than 100%)"
        select_categories.append(select_restriction['category'])

    # check if select has been specified more than once with the same argument
    #select_categories = [select_restriction['category'] for select_restriction in select_restrictions]
    #logger.debug(select_categories)
    assert len(set(select_categories)) == len(select_categories), "A category can only be used once in a select statement, otherwise it contradicts the previous statements."

    return True

def apply_not_positions(sample, notpos_restrictions):
    assert len(sample) > 0
    #assert len(notpos_restrictions) > 0
    for notpos_restriction in notpos_restrictions:
        # filter the positions that are forbidden
        restricted = [item for index, item in enumerate(sample) if index in notpos_restriction['argument']]
        #logger.debug("Going to check the following items")
        #logger.debug(restricted)
        for item in restricted:
            # logger.debug("Checking for equality: %s == %s?" % (item['category'], notpos_restriction['category']))
            if item['category'] == notpos_restriction['category']:
                return False
    return True

def apply_successor(sample, successor_restrictions):
    ''' apply the successors and return true or false if the sample is valid'''
    assert len(sample) > 0
    logger.debug("Entering function")
    logger.debug("Sample")
    logger.debug(sample)
    logger.debug("Restrictions are")
    logger.debug(successor_restrictions)

    # apply
    for index, item in enumerate(sample):
        # logger.debug("index %i" % index)
        logger.debug("item:")
        logger.debug(item)
        # check every restriction
        for successor_restriction in successor_restrictions:
            logger.debug(successor_restriction)
            lookahead = sample[index + 1: index + 1 + successor_restriction['argument'] + 1]
            # abort the check if there are less items anyway, so
            # [Foo, Foo, Foo, Foo] won't be checked if 3 of WHATEVER are allowed anyway.
            # or if they are 0
            # [Foo] if 0 is allowed
            if (0 == len(lookahead)) or (len(lookahead) < successor_restriction['argument']):
                continue
            if 'category' in successor_restriction.keys():
                logger.debug(item)
                logger.debug(successor_restriction)
                # check if the current item is affected by the restriction
                if item['category'] != successor_restriction['category']:
                    continue
                # check if the values in lookahead are successors
                lookahead = [successor_restriction['category'] == i['category'] for i in lookahead]
            elif 'type' in successor_restriction.keys():
                # check if the current item is affected by the restriction
                if successor_restriction['type'] not in item['type']:
                    continue
                # create a list of the type values (they are lists)
                lookahead = [successor_restriction['type'] in i['type'] for i in lookahead]
            else:
                # this should never happen
                raise ValueError
            logger.debug("Lookahead")
            logger.debug(lookahead)
            if all(lookahead):
                logger.debug("Returning False")
                return False
    logger.debug("Returning True")
    return True


def apply_select(questions, select_restrictions, tasks):
    result = []
    # apply
    for select_restriction in select_restrictions:
        # get tasks by category
        # this works nicely because dictionary keys are **NOT** ordered
        # otherwise the first entries would be favored
        category_tasks = list(filter(lambda x: x['category'] == select_restriction['category'], tasks))
        assert len(category_tasks) > 0, "There are no tasks for the category %s" % select_restriction['category']
        # print(len(category_tasks))
        assert isinstance(select_restriction['argument'], int)
        assert select_restriction['argument'] <= len(category_tasks), "You want to select %i task(s) of the category %s but there are only %i tasks of that category" % (select_restriction['argument'], select_restriction["category"], len(category_tasks))
        # create a list of the indices
        # we can use int here, because I checked this with math.modf before
        random_sample = random.sample(category_tasks, select_restriction['argument'])
        # random.sample: Used for random sampling without replacement.
        result += random_sample

    # shuffle, because the *selections* were applied in order
    random.shuffle(result)
    assert len(result) == questions, "The number of the sample does not equal the number of questions"
    return result

def _map_check(check, min_scale, max_scale):
    # map the percentage specified by check to the scale
    # (0.0: min_scale, 1.0: max_scale)
    logger.debug(check)
    assert isinstance(check, float)
    assert 0 <= check <= 1
    assert (max_scale - min_scale) > 0
    result = max([check * max_scale, min_scale])
    #result = check * max_scale
    result = int(round(result))
    logger.debug("mapped %f to %i" % (check, result))
    return result

def check_check(check, real, min_scale, max_scale):
    ''' check if the real value matches the check value (for a scale)'''
    assert isinstance(check, list)
    assert len(check) in [1,2]
    # unfortunately we have to do type juggling here :(
    # but let's do this the paranoid way and check that the value is an int as a string
    assert real in [str(i) for i in range(min_scale, max_scale + 1)]
    real = int(real)
    assert isinstance(real, int)
    logger.debug("Judging answer %i" % real)
    if len(check) == 1:
        # if there is one value check for equality
        return real == _map_check(check[0], min_scale, max_scale)
    elif len(check) == 2:
        # if we specified a range specify how should the check should be done?
        # TODO (feature): use check_range_interval, which specified one of: [] () [) (]
        # this is [] where both values are included
        return _map_check(check[0], min_scale, max_scale) <= real <= _map_check(check[1], min_scale, max_scale)
    # this code should never be reached:
    raise AssertionError("A check value has to be a list")
    return False

def _format_check(replacement_tuples, string):
    # apply all the replacements in the replacement tuple
    # so this function is testable
    assert isinstance(string, str)
    assert isinstance(replacement_tuples, list)
    for index, rt in enumerate(replacement_tuples):
        assert isinstance(rt, tuple)
        assert isinstance(rt[0], str) or isinstance(rt[0], numbers.Number)
        assert isinstance(rt[1], str) or isinstance(rt[1], numbers.Number)
        assert len(rt) == 2
    replacement_tuples = [(str(rt[0]), str(rt[1])) for rt in replacement_tuples]
    for index, rt in enumerate(replacement_tuples):
        # check for every tuple except the last tuple that the patterns don't overlap
        if index < len(replacement_tuples):
            # check the complete rest for overlaps and rematching
            for (rest_1, rest_2) in replacement_tuples[index + 1:]:
                assert rt[0] not in rest_1, "The pattern in (%s, %s) overlaps with (%s, %s)" % (rt[0], rt[1], rest_1, rest_2)
                assert rt[1] not in rest_1, "The result of (%s, %s) is matched by (%s, %s) again" % (rt[0], rt[1], rest_1, rest_2)
    for pattern, repl in replacement_tuples:
        string = re.sub(pattern, repl, string)
    return string

def format_checks(settings, tasks):
    ''' format the checks according to the following replacement_tuples'''
    # this could be realized through map but maybe on another day …
    # check that you don't rematch and that patterns don't overlap
    # TODO: unittest format_checks
    replacement_tuples = [('MIN_SCALE_DESC', settings['min_scale_desc']),
                          ('MAX_SCALE_DESC', settings['max_scale_desc']),
                          ('MIN_SCALE', settings['min_scale']),
                          ('MAX_SCALE', settings['max_scale'])
                          ]
    for this_check in tasks:
        # apply each replacement to each sentencen and situation of the task
        for this_key in ['sentence', 'situation']:
            this_check[this_key] = _format_check(replacement_tuples, this_check[this_key])
    return tasks

def filler_is_first(random_sample):
    # make the first element a filler
    if random_sample[0]['category'] == 'filler':
        return random_sample
    for index, sample in enumerate(random_sample):
        if sample['category'] == 'filler':
            original_first = random_sample[0]
            random_sample[0] = random_sample[index]
            random_sample[index] = original_first
            break
    return random_sample

def main(settings, tasks):
    check_config(settings, tasks)
    # returns a random sample
    select_restrictions = list(filter(lambda x: x['action'] == 'select', settings['restrictions']))
    # select restrictions have to be checked individually and together
    check_select(settings['questions'], select_restrictions)
    successor_restrictions = list(filter(lambda x: x['action'] == 'max_successors', settings['restrictions']))
    # notpos restrictions have to be checked individually and together
    notpos_restrictions = list(filter(lambda x: x['action'] == 'not_positions', settings['restrictions']))
    check_notpositions(notpos_restrictions)
    iterations = 0
    status = False
    while (status is False):
        iterations += 1
        if iterations > 100000:
            random_sample = "Could not get a valid sample despite trying desperately."
            break
        # get a sample
        random_sample = apply_select(settings['questions'], select_restrictions, tasks)
        # switch the first element with the first element that is a filler
        if settings['filler_is_first'] is True:
            logger.debug(random_sample)
            random_sample = filler_is_first(random_sample)
            logger.debug(random_sample)
        # check the sample
        status = apply_not_positions(random_sample, notpos_restrictions)
        if status is False:
            continue
        status = apply_successor(random_sample, successor_restrictions)
        if status is False:
            continue
        # everything went well and we can successfully leave the loop
        status = True
    logger.debug("Getting the tasks took %i iterations" % iterations)
    return random_sample

def check_settings(settings):
    assert "active" in settings.keys()
    assert "labels" in settings.keys()
    assert "filler_is_first" in settings.keys()
    assert "max_check_fail" in settings.keys()
    assert "questions" in settings.keys()
    assert "min_scale" in settings.keys()
    assert "max_scale" in settings.keys()
    assert "time" in settings.keys()

    assert isinstance(settings["active"], bool)
    assert isinstance(settings["labels"], bool)
    assert isinstance(settings["filler_is_first"], bool)
    assert isinstance(settings["questions"], int)
    assert isinstance(settings["min_scale"], int)
    assert isinstance(settings["max_scale"], int)
    assert isinstance(settings["time"], int)
    assert isinstance(settings["max_check_fail"], int)

    assert "situation" in settings.keys()
    assert "question" in settings.keys()
    assert "min_scale_desc" in settings.keys()
    assert "max_scale_desc" in settings.keys()
    assert "university" in settings.keys()
    assert "investigator" in settings.keys()
    assert "contact" in settings.keys()
    assert "link" in settings.keys()

    assert isinstance(settings["situation"], str)
    assert isinstance(settings["question"], str)
    assert len(settings["question"]) > 0, "The default question can't be empty, \
because a task has to have a question."

    assert isinstance(settings["min_scale_desc"], str)
    assert isinstance(settings["max_scale_desc"], str)
    assert isinstance(settings["university"], str)
    assert isinstance(settings["investigator"], str)
    assert isinstance(settings["contact"], str)
    assert isinstance(settings["link"], str)

    assert 'restrictions' in settings.keys()
    assert "actions" in settings.keys()
    assert "types" in settings.keys()
    assert "categories" in settings.keys()
    assert "templates" in settings.keys()
    assert "excluded_pids" in settings.keys(), "excluded_pids is optional but **has to be appended automatically** if it is not present"

    assert isinstance(settings["restrictions"], list)
    assert isinstance(settings["actions"], list)
    assert isinstance(settings["types"], list)
    assert isinstance(settings["categories"], list)
    assert isinstance(settings["templates"], list)
    assert isinstance(settings["excluded_pids"], set)

    for this_restriction in settings['restrictions']:
        check_restriction(settings, this_restriction)

    check_max_check_fail(settings)
    check_filler_is_first(settings)
    return True

def check_max_check_fail(settings):
    # assert that max_check_fail is configured correctly
    assert isinstance(settings['max_check_fail'], int), "max_check_fail has to be an integer"
    assert settings['max_check_fail'] >= 0, "max_check_fail has to be >= 0"
    return True

def check_filler_is_first(settings):
    # check that the minimal prerequisites for filler_is_first are met
    if settings['filler_is_first'] is True:
        select_restrictions = list(filter(lambda x: x['action'] == 'select', settings['restrictions']))
        filler = list(filter(lambda x: x['category'] == 'filler', select_restrictions))
        assert len(filler) > 0, "You have to have a select restriction"
        assert filler[0]['argument'] > 0, "You must select at least one filler so the first task can be a filler"
    return True

def check_tasks(settings, tasks):
    assert isinstance(tasks, list)
    # this is one of two checks for ids
    assert len(tasks) > 0
    for index, task in enumerate(tasks):
        assert index == task['id'], "A task needs an explicit numerical ID, but %s is not %i" % (str(task['id']), index)
        assert check_task(settings, task) is True
    return True

def check_config(settings, tasks):
    '''
    see if:
        the tasks implement the categories and types from settings
        selections have semantical contradictions
        restrictions have the allowed datatypes
    '''
    assert check_tasks(settings, tasks) is True
    assert check_settings(settings) is True

    return True

