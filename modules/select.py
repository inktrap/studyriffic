#!/usr/bin/env python3.5

class ListSelector:
    def __init__(self, input_list, allowed_types):
        self.input_list = input_list
        self.allowed_types = allowed_types
        # the result
        self.result = []

    def main(self, item_number):
        # return <item_number> of items from input_list according to allowed_types
        self.item_number = item_number
        return self


if __name__ == "__main__":
    item_number = 3
    # a list with typed items:
    input_list = [{'id':0, 'type':['foo', 'bar']}, {'id':1, 'type':['bar']},
                  {'id':2, 'type':['foo', 'baz']}, {'id':3, 'type':['baz']}
                  ]
    # let's have a list with a list of allowed types for that position:
    allowed_types = [['foo', 'bar'], ['bar'], ['foo', 'baz'], ['baz']]

    select = ListSelector(input_list, allowed_types)
    select = select.main(item_number)

    # this should go in a test
    assert len(select.result) is item_number, \
        "There should be {} items, but there are {}.".format(item_number, len(select.result))

