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
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
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
        assert isinstance(restriction['argument'], float)
        assert 'category' in restriction.keys()
        assert 0.0 < restriction['argument'] <= 1.0, "The argument for a select restriction x has to have the following property: 0 < x <= 1"
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
    # check if the numbers of selects add up to 1
    select_sum = sum([select_restriction['argument'] for select_restriction in select_restrictions])
    # TODO this is stupid for three thirds that are written as 0.33333333 each.
    #assert select_sum == 1, "Select restrictions have to sum up to (exactly?) 1, these sum up to: %s" % str(select_sum)
    assert 1 - select_sum < 0.00001, "Select restrictions have to sum up to (exactly?) 1, these sum up to: %s" % str(select_sum)

    select_categories = []

    for select_restriction in select_restrictions:
        logging.debug(math.modf(questions * select_restriction['argument'])[0])
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
    #assert len(successor_restrictions) > 0
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
        assert take_restrictions <= len(category_tasks), "You want to select %i task(s) of the category %s but there are only %i tasks of that category" % (take_restrictions, select_restriction["category"], len(category_tasks))
        # create a list of the indices
        # we can use int here, because I checked this with math.modf before
        random_sample = random.sample(category_tasks, int(take_restrictions))
        # random.sample: Used for random sampling without replacement.
        result += random_sample

    # shuffle, because the *selections* were applied in order
    random.shuffle(result)
    assert len(result) == questions, "The number of the sample does not equal the number of questions"
    return result

def _map_check(check, min_scale, max_scale):
    # TODO: test
    # map the check value to the scale (which means: the closest integer)
    logger.debug(check)
    assert isinstance(check, float)
    assert 0 <= check <= 1
    assert (max_scale - min_scale) > 0
    result = check * (max_scale - min_scale)
    result = int(round(result))
    logger.debug("mapped %f to %i" % (check, result))
    return result

def check_check(check, real, min_scale, max_scale):
    # TODO: test
    ''' check if the real value matches the check value (for a scale)'''
    # todo: check if the check value matches the real value
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
        # TODO: use check_range_interval, which specified one of: [] () [) (]
        # this is [] where both values are included
        return _map_check(check[0], min_scale, max_scale) <= real <= _map_check(check[1], min_scale, max_scale)
    # this code should never be reached:
    raise AssertionError("A check value has to be a list")
    return False

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
    assert "max_check_fail" in settings.keys()
    assert "questions" in settings.keys()
    assert "min_scale" in settings.keys()
    assert "max_scale" in settings.keys()
    assert "time" in settings.keys()

    assert isinstance(settings["active"], bool)
    assert isinstance(settings["labels"], bool)
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

    assert isinstance(settings["restrictions"], list)
    assert isinstance(settings["actions"], list)
    assert isinstance(settings["types"], list)
    assert isinstance(settings["categories"], list)
    assert isinstance(settings["templates"], list)

    for this_restriction in settings['restrictions']:
        check_restriction(settings, this_restriction)
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

