#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import re
import os
import json
from modules import get_tasks
from modules.logging import logger


class baseConfig():

    def __init__(self, project_root, template_path):
        # customize these
        self.cookie_scret = 'ajkbkjnkvnklrkvlkbgjknjkls'
        self.this_port = 63536
        # study directories have to match this regex
        self.study_regex = "[a-z,A-Z,0-9,-]+"
        # a list of customizable templates
        self.templates = ['first.tpl', 'last.tpl', 'consent.tpl', 'main.tpl']
        self.template_path = template_path
        # baseConfig.studies are configured by convention
        self.studies = self.configure(project_root)

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
            # settings['template_lookup'] = os.path.join(template_path, study)
        with open(study_tasks, 'r') as fh:
            this_tasks = json.load(fh)
        assert len(this_tasks) >= settings[
            'questions'], 'Study %s: There are not enough tasks (or questions is too high.)' % study

        # todo check tasks and restrictions here
        try:
            get_tasks.check_config(settings, this_tasks)
        except AssertionError as e:
            logger.error("There is an error in either settings.json or tasks.json for: %s" % study)
            raise e

        return {'settings': settings,
                'tasks': this_tasks,
                }

    def configure(self, project_root):
        studies_path = os.path.join(project_root, 'studies')
        studies = {}
        for study in os.listdir(studies_path):
            study_path = os.path.join(studies_path, study)
            #logger.debug(study_path)
            if os.path.isdir(study_path):
                this_study = self.configure_study(study, study_path)
                if this_study is False:
                    continue
                studies[study] = this_study
        assert len(studies.keys()) > 0, "No studies configured."
        return studies

