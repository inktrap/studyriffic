#!/usr/bin/env python3.5

from operator import eq
import random
import math

from functools import wraps
import errno
import os
import signal

import logging
logger = logging.getLogger('tasks_module')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

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
    assert isinstance(restriction, dict), "a restriction has to be a dictionary"
    assert 'action' in restriction.keys(), "a restriction has to have an action"
    assert (not('type' in restriction.keys() and 'category' in restriction.keys())), "a restriction operates on a type or a category, not both."
    assert 'argument' in restriction.keys(), "a restriction has to have an argument."
    assert len(restriction.keys()) == 3, "a restriction has to have 3 keys."
    assert restriction['action'] in settings['actions'], "the action of the restriction is not in the settings file."

    if 'type' in restriction.keys():
        assert isinstance(restriction['type'], str), "a type of a restriction has to be a string."
    elif 'category' in restriction.keys():
        assert isinstance(restriction['category'], str), "a category of a restriction has to be a string."
    # print(type(restriction['argument']))
    assert (isinstance(restriction['argument'], int) or
            isinstance(restriction['argument'], float)), "the argument of a restriction has to be an int or a float"

    if restriction['action'] == 'max_successors':
        assert isinstance(restriction['argument'], int)
        assert 'category' in restriction.keys() or 'type' in restriction.keys()
        assert restriction['argument'] >= 0
    elif restriction['action'] == 'select':
        assert isinstance(restriction['argument'], float)
        assert 'category' in restriction.keys()
        assert 0.0 < restriction['argument'] < 1.0
    else:
        raise ValueError("Unknown restriction action %s" % restriction['action'])
    return True


def check_task(settings, task):
    assert isinstance(task, dict), 'A task has to be a dictionary'
    assert len(task.keys()) == 5, 'A task has to have 5 keys.'
    assert 'category' in task.keys()
    assert 'type' in task.keys()
    assert 'situation' in task.keys()
    assert 'sentence' in task.keys()
    assert 'id' in task.keys()
    assert len(task.keys()) == 5
    assert task['category'] in settings['categories'], "The category %s has to be in settings" % task['category']
    assert len(task['category']) > 0, "A category can not be empty"
    assert isinstance(task['type'], list)
    for t in task['type']:
        assert isinstance(t, str), "A type is a list of strings. But the type %s is not a string." % t
        assert t in settings['types'], "The type %s has to be in settings." % t
        assert len(t) > 0, "A type, if given, can not be empty. (Id: %i)" % task['id']
    assert isinstance(task['situation'], str)
    assert isinstance(task['sentence'], str)
    assert isinstance(task['id'], int)
    assert len(task['sentence']) > 0, "A sentence can not be empty. (Id: %i)" % task['id']
    return True


def get_select_restrictions(restrictions):
    #logger.debug(restrictions)
    return list(filter(lambda x: x['action'] == 'select', restrictions))


def check_select(questions, select_restrictions):
    # semantic checks for select restrictions
    # check if the numbers of selects add up to 1
    assert sum([select_restriction['argument'] for select_restriction in select_restrictions]) == 1, "Select restrictions have to sum up to exactly 1"

    select_categories = []

    for select_restriction in select_restrictions:
        #print(math.modf(settings['questions'] * select_restriction['argument'])[0])
        assert (math.modf(questions * select_restriction['argument']))[0] == 0.0, "selection arguments can not produce items less than 1 (F.e.: You can not split a question in half)."
        assert 'category' in select_restriction.keys(), "Category key not present"
        assert select_restriction['argument'] > 0, "The argument of a select restriction must be greater 0 (it has to select something)"
        assert select_restriction['argument'] <= 1, "The argument of a select restriction must be <= 1 (you can't select more than 100%)"
        select_categories.append(select_restriction['category'])

    # check if select has been specified more than once with the same argument
    #select_categories = [select_restriction['category'] for select_restriction in select_restrictions]
    #logger.debug(select_categories)
    assert len(set(select_categories)) == len(select_categories), "A category can only be used once in a select statement, otherwise it contradicts the previous statements."

    return True


def apply_successor(sample, successor_restrictions):
    ''' apply the successors and return true or false if the sample is valid'''
    assert len(sample) > 0
    assert len(successor_restrictions) > 0
    logger.debug("applying successors")
    logger.debug(sample)
    logger.debug(successor_restrictions)
    # apply
    for index, item in enumerate(sample):
        # check every restriction
        for successor_restriction in successor_restrictions:
            # if there are not enough items, their order is not important
            # not enough means:
            #   the current item: index
            #   the number of allowed items: argument
            #   including the last one f.e. if argument = 3: we need [index, 1, 2, 3]
            #   but continue for [index, 1, 2]
            if (index + successor_restriction['argument'] + 1) > len(sample):
                logger.debug("continuing")
                continue

            if 'category' in successor_restriction.keys():
                # map and lambda: extract all the unique categories form the given range into a list
                # index
                    # the range includes the current item (index)
                    # and on top of that the items that are allowed (let's say we allow three items)
                    # [index, 1, 2, 3]
                    # so the slice should take [index, 1, 2, 3], including 3.
                # then make a set out of it to remove duplicates
                # create a list from the set
                # if there are other categories present, the length will be greater 1
                # if not, it fails
                successors = list(set(map(lambda x: x['category'], sample[index:index + successor_restriction['argument'] + 1])))
                # found a sequence that contradicts the requirements
                logger.debug("by category")
                logger.debug(successors)
                if len(successors) == 1 and (successors[0] == successor_restriction['category']):
                    logger.debug("false")
                    return False
            elif 'type' in successor_restriction.keys():
                successors = sample[index:index + successor_restriction['argument'] + 2]
                logger.debug("by type")
                logger.debug(successors)
                # we assume that the sequence contradicts the requirements
                contradicts = True
                for succ in successors:
                    # check the following tasks
                    if successor_restriction['type'] not in succ['type']:
                        # we found a sequence that does not contradict the requirements
                        # we are happy and can stop checking this part
                        logger.debug("false")
                        contradicts = False
                        break
                logger.debug("the sequence contradicts the requirements")
                # the sequence contradicts the requirements
                if contradicts is True:
                    return False
                # otherwise we keep looking
    logger.debug("the sequence is alright")
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
        # get number of entities the current restriction takes
        take_restrictions = questions * select_restriction['argument']
        # print(take_restrictions)
        # print(len(category_tasks))
        assert take_restrictions <= len(category_tasks), "You want to take more questions than there are questions"
        # create a list of the indices
        # we can use int here, because I checked this with math.modf before
        random_sample = random.sample(category_tasks, int(take_restrictions))
        # random.sample: Used for random sampling without replacement.
        result += random_sample

    # shuffle, because the *selections* were applied in order
    random.shuffle(result)
    return result


def main(settings, tasks):
    check_config(settings, tasks)
    # returns a random sample
    select_restrictions = get_select_restrictions(settings['restrictions'])
    check_select(settings['questions'], select_restrictions)
    random_sample = apply_select(settings['questions'], select_restrictions, tasks)
    successor_restrictions = list(filter(lambda x: x['action'] == 'max_successors', settings['restrictions']))
    if len(successor_restrictions) > 0:
        iterations = 0
        is_restricted = apply_successor(random_sample, successor_restrictions)
        while (is_restricted is False):
            iterations += 1
            random_sample = apply_select(settings['questions'], select_restrictions, tasks)
            is_restricted = apply_successor(random_sample, successor_restrictions)
            if iterations > 100000:
                random_sample = "Could not get a valid sample."
                break
        logger.info("Getting the tasks took %i iterations" % iterations)
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
    check_select(settings['questions'], get_select_restrictions(settings['restrictions']))

    for index, task in enumerate(tasks):
        assert index == task['id'], "A task needs an explicit numerical ID, but %s is not %i" % (str(task['id']), index)
        check_task(settings, task)
    return True

