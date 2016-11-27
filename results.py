#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import json
import os
import re
import csv
import sys

import pprint
pp = pprint.PrettyPrinter(indent=4)

import logging
logger = logging.getLogger('results.py')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


class baseConfig():
    def __init__(self):
        '''
        build paths, make assertions. sets self.result_paths and self.study_paths.
        the main purpose of this class is to build a list of result objects
        where a result object looks like this:
        {
            'settings': 'ROOT/studies/owls/settings.json',
            'db': 'ROOT/results/owls/db.json',
            'name': 'owls',
            'tasks': 'ROOT/studies/owls/tasks.json',
            'csv': 'ROOT/results/owls/csv'
        }
        '''

        # conventions
        studies_folder = 'studies'
        results_folder = 'results'
        self.results = []

        # build paths
        self.project_root = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        assert os.path.isdir(self.project_root) is True, "Project root %s is not a directory" % self.project_root
        self.studies_path = os.path.join(self.project_root, studies_folder)
        assert os.path.isdir(self.studies_path) is True, "Studies path %s is not a directory" % self.studies_path
        self.results_path = os.path.join(self.project_root, results_folder)
        assert os.path.isdir(self.results_path) is True, "Results path %s is not a directory" % self.results_path

        # required files for the configuration to work (only names, without ending)
        studies_files = ['settings', 'tasks']
        results_files = ['db']

        # read names
        study_names = self._get_names(studies_folder)

        # now that we have the studies, assert that the every result has one and get the paths
        result_names = self._get_names(results_folder)
        for result in result_names:
            assert result in study_names, "This results directory has no study: %s" % result
            result_path = self._get_dir_path(self.results_path, result)
            # now that we have the result path, assert that result directories are well configured
            # this happens via get_file_path
            [self._get_file_path(result_path, rf) for rf in [f + '.json' for f in results_files]]

            # it is important that study and result are named the same, that is why
            study = result
            # and the path to the study is:
            study_path = self._get_dir_path(self.studies_path, study)
            # same as with results: we check that the study is complete
            [self._get_file_path(study_path, rf) for rf in [f + '.json' for f in studies_files]]

            # then we create the result object
            current_result = {}
            current_result['name'] = study
            # the explicit list of files associated with this study
            for f in studies_files:
                current_result[f] = self._get_file_path(study_path, f + '.json')
            for f in results_files:
                current_result[f] = self._get_file_path(result_path, f + '.json')

            # if everything worked fine, create the csv dir if it does not exist
            if not os.path.isdir(os.path.join(result_path, 'csv')):
                os.mkdir(os.path.join(result_path, 'csv'))
            current_result['csv'] = self._get_dir_path(result_path, 'csv')

            # and save the complete result
            self.results.append(current_result)

    def _get_dir_path(self, path, name):
        u''' return a path and assert that it is a directory '''
        this_path = os.path.join(path, name)
        assert os.path.isdir(this_path), "%s is not a directory" % this_path
        return this_path

    def _get_file_path(self, path, name):
        u''' return a path and assert that it is a file '''
        this_path = os.path.join(path, name)
        assert os.path.isfile(this_path), "%s is not a file" % this_path
        return this_path

    def _get_names(self, path):
        u''' return a list of names of directories for a directory path'''
        names = []
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                names.append(name)
        return names

class csvResults():
    def __init__(self):
        pass

    def main(self, results):
        '''
        dump all the files as csv
        '''
        for result in results:
            items = self.loadJson('settings', result)
            settings = csvResults.makeSettings(self, items)
            assert self.write(settings, os.path.join(result['csv'], 'settings.csv')) is True

            items = self.loadJson('db', result)
            demographics = csvResults.makeDemographics(self, items)
            assert self.write(demographics, os.path.join(result['csv'], 'demographics.csv')) is True

            settings = self.loadJson('settings', result)
            items = self.loadJson('tasks', result)
            tasks = csvResults.makeTasks(self, items, settings)
            assert self.write(tasks, os.path.join(result['csv'], 'tasks.csv')) is True

            items = self.loadJson('db', result)
            answers = csvResults.makeAnswers(self, items)
            assert self.write(answers, os.path.join(result['csv'], 'answers.csv')) is True

            pids = csvResults.makePids(self, answers)
            logger.debug(pids)
            assert self.write(pids, os.path.join(result['csv'], 'pids.csv')) is True

            # create a combined results table
            all_results = csvResults.makeAll(self, demographics, tasks, answers)
            assert self.write(all_results, os.path.join(result['csv'], 'all.csv')) is True

    def _check_format(self, outfile, data):
        ''' check that this is a list of sublists of strings
            where all the sublists are of the same length'''
        # all the rows have to have the same length
        assert isinstance(data, list)
        for line, row in enumerate(data):
            assert isinstance(row, list)
            assert len(row) == len(data[0]), "Insonsistent lengths for %s at line %i (%i) and line 0 (%i)" % (outfile, line, len(row), len(data[0]))
            assert len(data[0]) > 0, "Empty data objects are probably a mistake"
            for item in row:
                assert isinstance(item, str), "In %s an entry is not a string (%s) at line %i" % (outfile, str(item), line)
        return True

    def loadJson(self, name, results):
        '''
        load json data given by
            name (the name you want)
            results (the result object that contains the file locations)
        '''
        #logger.debug(results[name])
        assert isinstance(name, str)
        assert isinstance(results, dict)
        with open(results[name], 'r') as fh:
            content = json.load(fh)
            assert len(content) > 0
        return content

    def makeSettings(self, items):
        '''
        create the column and rows that form the settings table
        this behaves a little bit like zip()
        '''

        assert isinstance(items, dict)
        # remove unncessary keys:
        # - that ensures that studyriffic works the way it should (templates, categories, aso.)
        # - studyriffic configuration data (labels, active, aso.)
        # - study metadata (investigator or affiliation, or contact, aso.)
        # - study configuration data (time, question, questions, situation, aso.)
        unnecessary_keys = ['time', 'templates', 'question',
                            'situation', 'restrictions', 'actions', 'categories', 'types',
                            'active', 'labels', 'max_check_fail', 'check_range_interval', 'link']
        # publishing_keys = ['university', 'investigator', 'contact']
        for key in unnecessary_keys:
            try:
                del(items[key])
            except KeyError:
                pass
        header = sorted(list(map(str, items.keys())))
        rows = []
        # settings are a dictionary so this table only has one row
        for item in header:
            rows.append(str(items[item]))
        data = [header, rows]
        return data

    def _joinList(self, this_list):
        '''
        join a list with spaces and strip spaces on boundaries
        '''
        assert isinstance(this_list, list)
        # do not modify strings that were entered by the user
        #return ' '.join([l.lower().strip() for l in this_list]).strip()
        return ' '.join([str(l).strip() for l in this_list]).strip()

    def _mergeLists(self, *args):
        result = []
        for arg in args:
            assert isinstance(arg, list)
            result += arg[:]
        return result

    def makeTasks(self, items, settings):
        '''
        create the column and rows that form the tasks table
        '''
        # maybe later: get the categories and types from settings, create one column per category and type
        assert 'types' in settings.keys()

        type_keys = settings['types']
        item_keys = list(items[0].keys())
        # exclude the check key because only fillers and checks have it
        if 'check' in item_keys:
            item_keys.remove('check')

        item_keys = sorted([str(item_key) for item_key in item_keys if item_key != 'type'])
        # append the types after the end of the columns and rename each type (f.e. foobar becomes TypeFoobar)
        data = [list(item_keys) + [t + 'Type' for t in type_keys]]
        for item in items:
            row = []
            row_types = [''] * len(type_keys)
            for key in item_keys:
                assert key in item.keys()
                row.append(str(item[key]))
            for this_type in item['type']:
                # this is the most fragile step: setting 1 for each type that is true in the predefined list
                # redundant and duplicate behaviour would be
                row_types[type_keys.index(this_type)] = str(this_type)
                #row_types[type_keys.index(this_type)] = 1
            row = row + row_types[:]
            data.append(row)
        return data

    def makeAnswers(self, items):
        '''
        create the column and rows that form the answers table
        '''
        assert isinstance(items, list)
        assert 'results' in items[0].keys()
        assert isinstance(items[0], dict)
        assert isinstance(items[0]['results'], list)
        assert len(items[0]['results']) > 0
        assert isinstance(items[0]['results'][0], dict)
        assert 'pid' in items[0]

        result_keys = sorted(list(items[0]['results'][0].keys()))
        header = [['pid'] + result_keys]
        data = header
        for item in items:
            for this_result in item['results']:
                row = []
                row.append(str(item['pid']))
                for key in result_keys:
                    try:
                        row.append(str(this_result[key]))
                    except KeyError:
                        logger.error(this_result)
                        sys.exit(1)
                data.append(row)
        return data

    def makeDemographics(self, items):
        '''
        create the column and rows that form the demographics table
        '''
        listKeys = ['languages']
        demographics_keys = sorted(list(items[0]['demographics'].keys()))
        header = [['pid'] + demographics_keys]
        data = header
        for item in items:
            row = []
            row.append(str(item['pid']))
            for key in demographics_keys:
                if key in listKeys:
                    row.append(self._joinList(item['demographics'][key]))
                else:
                    if isinstance(item['demographics'][key], list):
                        row.append(self._joinList(item['demographics'][key]))
                    else:
                        row.append(str(item['demographics'][key]))
            data.append(row)
        return data

    def _deleteFromTable(self, indices, table):
        assert isinstance(table, list)
        assert isinstance(indices, list)
        if len(table) == 0:
            return []
        for index in indices:
            assert isinstance(index, int)
            assert 0 <= index, "Index must be greater equal to 0"
            assert index < len(table[0]), "IndexError"
        if len(indices) == 0:
            return table
        # logger.debug(table[0])
        for task in table:
            # this is quite important: when deleting values from an array
            # the indices that are coming later are shifted.
            # so delete the indices from highest to lowest
            # otherwise this would be horribly wrong
            # (tbh: writing code that transforms tables feels horribly wrong, ugh)
            for d in sorted(indices, reverse=True):
                del task[d]
        return table

    def _duplicatesEqual(self, duplicates, table):
        assert isinstance(duplicates, list)
        assert isinstance(table, list)
        for indices in duplicates:
            for index in indices[1:]:
                for row in table:
                    if row[index] != row[indices[0]]:
                        return False
        return True

    def _deduplicateTable(self, table):
        assert isinstance(table, list)
        assert len(table) > 0
        assert isinstance(table[0], list)
        interim = {}
        # build a dictionary of occurrences
        # important assumptions: this is done for the header only and this is the first sublist
        for i, t in enumerate(table[0]):
            try:
                interim[t].append(i)
            except KeyError:
                interim[t] = [i]
        _, indices = zip(*list([(x,y) for x,y in interim.items() if len(y) > 1]))
        indices = list(indices)
        assert self._duplicatesEqual(indices, table) is True
        # exclude the first of every index (that way it won't be deleted)
        indices = list(map(lambda x: x[1:], indices))
        # unpack the lists and merge them, checking is already done
        return self._deleteFromTable(self._mergeLists(*indices), table)

    def _getPids(self, answers):
        assert isinstance(answers, list)
        assert len(answers) > 0
        assert isinstance(answers[0], list)
        assert len(answers[0][0]) > 0
        assert answers[0][0] == 'pid'
        # sorting is needed because otherwise testing might fail
        return sorted(list(set([x[0] for x in answers[1:]])))

    def makePids(self, answers):
        return [['pid']] + list(map(lambda x: [x], self._getPids(answers)))

    def makeAll(self, demographics, tasks, answers):
        '''
        combine all the different **results** into one huge redundant table
        that is convenient for statistical analysis.
        this includes: pid,id,sit_rt, sent_rt,value, category, type, age, languages

        - the unique value are the answers, for every answer a task must
          be selected
        '''
        # an answer has this format: ['pid', 'id', 'sent_rt', 'sit_rt', 'value']
        # the id joins the task and the answers value
        # a task looks like this ['category', 'id', 'sentence', 'situation', '*Type']
        # where *Type is one or more types, like fooType, barType, aso.
        # the pid joins the demographics and answers values
        assert answers[0][0] == 'pid'
        assert demographics[0][0] == 'pid'
        assert answers[0][1] == 'id'
        assert tasks[0][1] == 'id'

        indices = []
        try:
            indices.append(tasks[0].index('situation'))
        except ValueError:
            pass
        try:
            indices.append(tasks[0].index('sentence'))
        except ValueError:
            pass

        tasks = self._deleteFromTable(indices, tasks)
        data = []

        # get all the pids
        pids = self._getPids(answers)
        #logger.debug(pids)

        data = [self._mergeLists(demographics[0], tasks[0], answers[0])]
        #logger.debug(demographics[1])
        for pid in pids:
            # this_answers = [answer for answer in answers if answer[0] == pid]
            # get all the answers for the pid
            this_answers = list(filter(lambda x: x[0] == pid, answers))
            # get all the answer ids
            this_answer_ids = list(set([x[1] for x in this_answers]))
            # get all the tasks for this set of answers
            this_tasks = list(filter(lambda x: x[1] in this_answer_ids, tasks))
            # get all the demographic values for this pid (like originally done)
            this_demographics = list(filter(lambda x: x[0] == pid, demographics))
            assert len(this_demographics) == 1
            assert len(this_answers) == len(this_answer_ids) == len(this_tasks)
            for this_demographic in this_demographics:
                for this_answer in this_answers:
                    current_task = list(filter(lambda x: x[1] == this_answer[1], this_tasks))
                    assert len(current_task) == 1
                    current_task = current_task[0]
                    data.append(self._mergeLists(this_demographic, current_task, this_answer))
        data = self._deduplicateTable(data)
        return data

    def write(self, data, outfile):
        u'''
        data is expected to be a list of rows and the first row is the column.
        write the rows to a file called name.
        '''
        assert isinstance(outfile, str)
        assert self._check_format(outfile, data) is True
        #logger.debug(data)
        with open(outfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        logger.info("Wrote %s" % outfile)
        return True


def main():
    thisConfig = baseConfig()
    #logger.debug(thisConfig.results)
    thisResults = csvResults()
    thisResults.main(thisConfig.results)
    # print(thisConfig.results)
    # demographics
    # settings
    # tasks
    # results


if __name__ == "__main__":
    main()
