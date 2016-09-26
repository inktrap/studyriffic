#!/usr/bin/env python3.5

from operator import eq
import random
import math

from functools import wraps
import errno
import os
import signal

# restrictions
# this leads to the following grammar:
actions = ['max_successors', 'select']
# categories and the types that are defined in tasks.xml
categories = ['filler', 'target']
types = ['any'] + ['soft-presupposition', 'hard-presupposition', 'extra-soft-presupposition'] + ['bad', 'good', 'meh']

max_step = 4

# max_successor defines how many *successors* are *permitted*
# this allows 2 successors of type 'bad' to follow, so 3 in a sequence are allowed
# {'action':'max_successors', 'type':'bad', 'argument':2},
# this allows 0 sucessors of type bad.
# {'action':'max_successors', 'type':'bad', 'argument':0},
this_restrictions = [
    {'action':'max_successors', 'type':'bad', 'argument':0},
    {'action':'max_successors', 'type':'good', 'argument':0},
    {'action':'max_successors', 'type':'hard-presupposition', 'argument':0},
    {'action':'max_successors', 'type':'extra-soft-presupposition', 'argument':0},
    {'action':'max_successors', 'type':'soft-presupposition', 'argument':0},
    {'action':'select', 'type':'filler', 'argument':0.5},
    {'action':'select', 'type':'target', 'argument':0.5}
]

this_tasks = [
    {'category':'filler', 'type':'bad', 'situation':'1','sentence':'Barfoo'},
    {'category':'target', 'type':'hard-presupposition', 'situation':'2','sentence':'Barfoo'},
    {'category':'filler', 'type':'bad', 'situation':'3','sentence':'Barfoo'},
    {'category':'target', 'type':'extra-soft-presupposition', 'situation':'4','sentence':'Barfoo'}
]


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


def check_restriction(restriction):
    assert isinstance(restriction, dict)
    assert 'action' in restriction.keys()
    assert 'type' in restriction.keys()
    assert 'argument' in restriction.keys()
    assert len(restriction.keys()) == 3
    assert restriction['action'] in actions
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


def check_task(task):
    assert isinstance(task, dict)
    assert 'category' in task.keys()
    assert 'type' in task.keys()
    assert 'situation' in task.keys()
    assert 'sentence' in task.keys()
    assert len(task.keys()) == 4
    assert task['category'] in categories
    assert task['type'] in types
    assert isinstance(task['situation'], str)
    assert isinstance(task['sentence'], str)


def check_select(restrictions):

    # first apply the select restrictions
    # check if the numbers of selects add up to 1
    select_restrictions = list(filter(lambda x: x['action'] == 'select', restrictions))
    assert sum([select_restriction['argument'] for select_restriction in select_restrictions]) == 1

    # check if select has been specified more than once with the same argument
    select_types = [select_restriction['type'] for select_restriction in select_restrictions]
    assert len(set(select_types)) == len(select_types), "A type can only be used once in a select statement, otherwise it contradicts the previous statements."

    # check that all the arguments are dividable without a remainder
    for select_restriction in select_restrictions:
        #print(math.modf(max_step * select_restriction['argument'])[0])
        assert (math.modf(max_step * select_restriction['argument']))[0] == 0.0, "selection arguments can not produce items less than 1."
    return select_restrictions


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


def apply_select(select_restrictions):
    result = []
    # apply
    for select_restriction in select_restrictions:
        # get tasks by category
        # this works nicely because dictionary keys are **NOT** ordered
        # otherwise the first entries would be favored
        category_tasks = list(filter(lambda x: x['category'] == select_restriction['type'], this_tasks))

        assert len(category_tasks) > 0
        # get number of entities the current restriction takes
        take_restrictions = max_step * select_restriction['argument']
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
def apply_restrictions(restrictions):
    # apply the strictions and just to be save, do so with a timeout
    # (in the tests I did i never waited longer than 0.11s even with very strict
    # restrictions and a small number of tasks)
    select_restrictions = check_select(restrictions)
    random_sample = apply_select(select_restrictions)
    successor_restrictions = list(filter(lambda x: x['action'] == 'max_successors', restrictions))
    is_restricted = apply_successor(random_sample, successor_restrictions)
    while (is_restricted is False):
        random_sample = apply_select(select_restrictions)
        is_restricted = apply_successor(random_sample, successor_restrictions)
    return random_sample


def main():
    for this_restriction in this_restrictions:
        check_restriction(this_restriction)
    for this_task in this_tasks:
        check_task(this_task)
    print(apply_restrictions(this_restrictions))
    return True

if __name__ == '__main__':
    print(main())

