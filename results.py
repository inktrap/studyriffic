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
        u''' build paths, make assertions. sets self.result_paths and self.study_paths'''

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
        for result in results:
            csvResults.writeSettings(self, result)
            csvResults.writeDemographics(self, result)
            csvResults.writeTasks(self, result)
            csvResults.writeResults(self, result)

    def loadJson(self, name, results):
        #logger.debug(results[name])
        assert isinstance(name, str)
        assert isinstance(results, dict)
        with open(results[name], 'r') as fh:
            content = json.load(fh)
            assert len(content) > 0
        return content

    def writeSettings(self, results):
        u''' a generic method that simply dumps the contents as csv'''
        content = self.loadJson('settings', results)
        # remove unncessary keys:
        # - that ensures that studyriffic works the way it should (templates, categories, aso.)
        # - studyriffic configuration data (labels, active, aso.)
        # - study metadata (investigator or affiliation, or contact, aso.)
        # - study configuration data (time, question, questions, situation, aso.)
        unnecessary_keys = ['time', 'templates', 'university', 'question',
                            'situation', 'restrictions', 'actions', 'categories', 'types',
                            'active', 'labels', 'investigator', 'contact', 'link']
        for key in unnecessary_keys:
            try:
                del(content[key])
            except KeyError:
                pass
        header = content.keys()
        rows = []
        # settings are a dictionary so this table only has one row
        for item in header:
            rows.append(content[item])
        data = [header, rows]
        assert self.write(data, os.path.join(results['csv'], 'settings.csv')) is True
        return True

    def _joinList(self, this_list):
        assert isinstance(this_list, list)
        # do not modify strings that were entered by the user
        #return ' '.join([l.lower().strip() for l in this_list]).strip()
        return ' '.join([l.strip() for l in this_list]).strip()

    def writeTasks(self, results):
        # maybe later: get the categories and types from settings, create one column per category and type
        items = self.loadJson('tasks', results)
        logger.debug(items[0].keys())
        item_keys = items[0].keys()
        listKeys = ['type']
        data = [list(item_keys)]
        for item in items:
            row = []
            for key in item_keys:
                if key in listKeys:
                    row.append(self._joinList(item[key]))
                else:
                    row.append(item[key])
            data.append(row)
        assert self.write(data, os.path.join(results['csv'], 'tasks.csv')) is True
        return True

    def writeResults(self, results):
        items = self.loadJson('db', results)
        result_keys = items[0]['results'][0].keys()
        header = [['pid'] + list(result_keys)]
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
        assert self.write(data, os.path.join(results['csv'], 'results.csv')) is True
        return True

    def writeDemographics(self, results):
        listKeys = ['languages']
        items = self.loadJson('db', results)
        demographics_keys = items[0]['demographics'].keys()
        header = [['pid'] + list(demographics_keys)]
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
        assert self.write(data, os.path.join(results['csv'], 'demographics.csv')) is True
        return True

    def write(self, data, outfile):
        u''' write the rows to a file called name'''
        #logger.debug(data)
        with open(outfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        logger.info("Wrote %s" % outfile)
        return True

def main():
    thisConfig = baseConfig()
    csvResults(thisConfig.results)
    # print(thisConfig.results)
    # demographics
    # settings
    # tasks
    # results

if __name__ == "__main__":
    main()
