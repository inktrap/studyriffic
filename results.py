#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import json
import os
import re
import csv
import sys

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
    def __init__(self, results):
        '''
        dump all the files as csv
        '''
        for result in results:
            settings = csvResults.makeSettings(self, result)
            assert self.write(settings, os.path.join(result['csv'], 'settings.csv')) is True
            demographics = csvResults.makeDemographics(self, result)
            assert self.write(demographics, os.path.join(result['csv'], 'demographics.csv')) is True
            tasks = csvResults.makeTasks(self, result)
            assert self.write(tasks, os.path.join(result['csv'], 'tasks.csv')) is True
            answers = csvResults.makeAnswers(self, result)
            assert self.write(answers, os.path.join(result['csv'], 'answers.csv')) is True
            all_results = csvResults.makeAll(self, settings, demographics, tasks, answers)
            assert self.write(all_results, os.path.join(result['csv'], 'all.csv')) is True

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

    def makeSettings(self, results):
        '''
        create the column and rows that form the settings table
        '''
        content = self.loadJson('settings', results)
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
                del(content[key])
            except KeyError:
                pass
        header = sorted(list(content.keys()))
        rows = []
        # settings are a dictionary so this table only has one row
        for item in header:
            rows.append(content[item])
        data = [header, rows]
        return data

    def _joinList(self, this_list):
        '''
        join a list with spaces and strip spaces on boundaries
        '''
        assert isinstance(this_list, list)
        # do not modify strings that were entered by the user
        #return ' '.join([l.lower().strip() for l in this_list]).strip()
        return ' '.join([l.strip() for l in this_list]).strip()

    def makeTasks(self, results):
        '''
        create the column and rows that form the tasks table
        '''
        # maybe later: get the categories and types from settings, create one column per category and type
        settings = self.loadJson('settings', results)
        type_keys = settings['types']
        items = self.loadJson('tasks', results)
        item_keys = list(items[0].keys())
        # exclude the check key because only fillers and checks have it
        if 'check' in item_keys:
            item_keys.remove('check')
        item_keys = sorted([item_key for item_key in item_keys if item_key != 'type'])
        # append the types after the end of the columns and rename each type (f.e. foobar becomes TypeFoobar)
        data = [list(item_keys) + [t + 'Type' for t in type_keys]]
        for item in items:
            row = []
            row_types = [''] * len(type_keys)
            for key in item_keys:
                row.append(item[key])
            for this_type in item['type']:
                # this is the most fragile step: setting 1 for each type that is true in the predefined list
                # redundant and duplicate behaviour would be
                row_types[type_keys.index(this_type)] = this_type
                #row_types[type_keys.index(this_type)] = 1
            row = row + row_types[:]
            data.append(row)
        return data

    def makeAnswers(self, results):
        '''
        create the column and rows that form the answers table
        '''
        items = self.loadJson('db', results)
        result_keys = sorted(list(items[0]['results'][0].keys()))
        header = [['pid'] + result_keys]
        data = header
        for item in items:
            for this_result in item['results']:
                row = []
                row.append(item['pid'])
                for key in result_keys:
                    try:
                        row.append(this_result[key])
                    except KeyError:
                        logger.error(this_result)
                        sys.exit(1)
                data.append(row)
        return data

    def makeDemographics(self, results):
        '''
        create the column and rows that form the demographics table
        '''
        listKeys = ['languages']
        items = self.loadJson('db', results)
        demographics_keys = sorted(list(items[0]['demographics'].keys()))
        header = [['pid'] + demographics_keys]
        data = header
        for item in items:
            row = []
            row.append(item['pid'])
            for key in demographics_keys:
                if key in listKeys:
                    row.append(self._joinList(item['demographics'][key]))
                else:
                    row.append(item['demographics'][key])
            data.append(row)
        return data

    def makeAll(self, settings, demographics, tasks, answers):
        '''
        combine all the different results into one huge redundant table
        that is convenient for statistical analysis
        - the unique value are the answers, for every answer a task must
          be selected
        '''
        # an answer has this format: ['pid', 'id', 'sent_rt', 'sit_rt', 'value']
        assert answers[0][0] == 'pid'
        #logger.debug(answers)
        for answer in answers[1:]:
            pass
        data = []
        return data

    def write(self, data, outfile):
        u'''
        data is expected to be a list of rows and the first row is the column.
        write the rows to a file called name.
        '''
        assert isinstance(data, list)
        assert isinstance(outfile, str)
        # all the rows have to have the same length
        for row in data:
            assert len(row) == len(data[0])
        #logger.debug(data)
        with open(outfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        logger.info("Wrote %s" % outfile)
        return True


def main():
    thisConfig = baseConfig()
    #logger.debug(thisConfig.results)
    csvResults(thisConfig.results)
    # print(thisConfig.results)
    # demographics
    # settings
    # tasks
    # results


if __name__ == "__main__":
    main()
