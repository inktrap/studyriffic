#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import re
import os
import json
from modules import tasks_module
import socket
from pymongo import MongoClient
import urllib.parse

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    # format = '%m-%d %H:%M:%S',
    datefmt='%m-%d %H:%M:%S',
)

logger = logging.getLogger(__file__)

class baseConfig():

    def __init__(self):
        database = 'studyriffic'
        if socket.gethostname() == "box":
            client = MongoClient()
            mongodb_uri = 'mongodb://localhost:27017/%s' % database
        else:
            # configured uberspace
            # client = MongoClient('mongodb://username:password@localhost:27017/')
            username = 'perigen'
            password = 'zeishee3ue'
            this_username = urllib.parse.quote_plus(username)
            this_password = urllib.parse.quote_plus(password)
            this_port = 21205
            mongodb_uri = 'mongodb://%s:%s@localhost:%i/%s' % (this_username, this_password, this_port, database)

        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=1)
        db_test = client.server_info()
        assert(isinstance(db_test, dict))
        logger.debug(db_test)

        self.db = client[database]
        self.project_root = os.path.abspath(os.path.dirname(os.path.realpath(os.path.join(__file__, '..'))))
        # logger.debug(self.project_root)
        # customize these
        self.cookie_secret = 'WOkY1WWxxBECSlXIOemPzIXLt9UGpqfBsk19VwYRvPDeMlmWyKZQvFPNRdzplOj2UrbUaRozkuJLQuIjM7s07l31SGptnTzMXliR'
        self.this_port = 63536
        # study directories have to match this regex
        self.study_regex = "[a-z,A-Z,0-9,-]+"
        # a list of customizable templates (currently only first.tpl is customizable)
        self.templates = ['demographics.tpl', 'first.tpl', 'last.tpl', 'consent.tpl', 'main.tpl']
        self.template_path = os.path.join(self.project_root, 'views')
        self.required_settings_keys = ["question",
                                       "situation",
                                       "questions",
                                       "min_scale",
                                       "max_scale",
                                       "min_scale_desc",
                                       "max_scale_desc",
                                       "university",
                                       "investigator",
                                       "contact",
                                       "active",
                                       "labels",
                                       "time",
                                       "link",
                                       "actions",
                                       "types",
                                       "categories",
                                       "templates",
                                       "restrictions"
                                       ]
        # baseConfig.studies are configured by convention
        # studies dict contains settings for each study
        self.studies = self.configure()

    def configure_study(self, study, study_path):
        study_settings = os.path.join(study_path, "settings.json")
        study_tasks = os.path.join(study_path, "tasks.json")
        study_template_path = os.path.join(self.template_path, study)

        assert re.match(self.study_regex, study), "Rename your directory to match %s" % self.study_regex

        assert os.path.isfile(
            study_settings), "%s: Please create %s" % (study, study_settings)
        assert os.path.isfile(
            study_tasks), "%s: Please create %s" % (study, study_tasks)

        with open(study_settings, 'r') as fh:
            try:
                settings = json.load(fh)
            except json.decoder.JSONDecodeError as e:
                logger.error("There is an error in one of your settings.json files: %s" % study_settings)
                raise e
            for key in self.required_settings_keys:
                assert key in settings.keys(), "You have to specify the key '%s' in your settings file: %s" % (key, study_settings)
            if 'active' in settings.keys():
                # the active key is opional
                if settings['active'] is False:
                    # do not include inactive studies
                    return False
            if 'templates' in settings.keys():
                # assert that all templates that are specified by study exist
                assert all([template in self.templates for template in settings['templates']]), "Study %s uses a template that is not one of: %s" % (study, ', '.join(self.templates))
                assert all([os.path.isfile(os.path.join(study_template_path, template)) for template in settings['templates']]), "Study %s needs the templates %s in %s" % (study, ', '.join(settings['templates']), study_template_path)
            else:
                settings['templates'] = []
            # let the task selection module worry about restrictions
            #if 'restrictions' in settings.keys():
            #    assert all([restriction in restrictions for restriction in settings['restrictions']]), "Study %s uses a restriction that is not one of: %s" % (study, ', '.join(restrictions))
            settings['name'] = study.capitalize()
            settings['study'] = study
            if 'excluded_pids' not in settings.keys():
                settings['excluded_pids'] = []
            excluded_file = os.path.join(study_path, 'EXCLUDED_PIDS.txt')
            if os.path.isfile(excluded_file):
                with open(excluded_file, 'r') as fh:
                    excluded_pids = filter(lambda x: x != '', map(str.strip, fh.read().splitlines()))
                settings['excluded_pids'] += excluded_pids
            # turn into a set of strings
            settings['excluded_pids'] = set(map(str, settings['excluded_pids']))
        with open(study_tasks, 'r') as fh:
            try:
                this_tasks = json.load(fh)
            except json.decoder.JSONDecodeError as e:
                logger.error("There is an error in one of your tasks.json files: %s" % study_tasks)
                raise e
        assert len(this_tasks) >= settings[
            'questions'], 'Study %s: There are not enough tasks (or number of questions is greater.)' % study

        try:
            tasks_module.check_config(settings, this_tasks)
        except AssertionError as e:
            logger.error("There is an error in either settings.json or tasks.json for: %s" % study)
            raise e

        # this is just a check if it is possible to get tasks (this is done once per study!)
        assert isinstance(tasks_module.main(settings, this_tasks), list)

        return {'settings': settings,
                'tasks': this_tasks,
                }

    def configure(self):
        studies_path = os.path.join(self.project_root, 'studies')
        studies = {}
        for study in os.listdir(studies_path):
            study_path = os.path.join(studies_path, study)
            #logger.debug(study_path)
            if os.path.isdir(study_path):
                this_study = self.configure_study(study, study_path)
                if this_study is False:
                    continue
                studies[study] = this_study
        #logger.debug(studies.keys())
        assert len(studies.keys()) > 0, "No studies configured."
        return studies


thisConfig = baseConfig()
