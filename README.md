# Studyriffic

A simple beautiful rock solid study tool to be used with prolific.

## Features

Some parts are still missing, but that is alright with my estimate.
Here is a quick overview of the framework I wrote. It features:

 - a responsive html5 layout with browser detection to meet the minimal
   requirements, also permissions checks.
 - customizable question/situation introductions per study, as is
   the scale (see the different examples)
 - a smart consent form that is automatically customized (see time and
   number of questions)
 - the first page that lists examples is ment to be created by
   experiment (the other pages could be too, but they are flexible
   enough)
 - timestamps for the time to read the situation and another timestamp
   to give an answer, per task.
 - a lot of other stuff, like a simple, flexible json configuration, aso.

## Demo

 - A longer study with the binary scale: <https://perigen.diphda.uberspace.de/study/binary?prolific_pid=123&session_id=foobar>
 - A longer study with the likert scale: <https://perigen.diphda.uberspace.de/study/likert?prolific_pid=123&session_id=foobar>
 - A small, silly study: <https://perigen.diphda.uberspace.de/study/silly?prolific_pid=123&session_id=foobar>

# Valentin Todo

 - major: write results to db
 - major: change format of tasks from latex to json (vim macros)
 - major: make the step before last rock solid!!!
     - check if the prolific id already did the study
     - reenable session check?
     - check for TODOs
 - deploy
    - separate uberspace with some money
    - daemontools
    - create cronjob file from settings.json
        - cronjob with mongoexport and timestamps, (so we get backups!)
        - to location accessible from pw protected dir
        - ``mongoexport --db test --collection traffic --out traffic.json``

 - at some point: results
    - json to r: jsonlite <https://www.opencpu.org/posts/jsonlite-a-smarter-json-encoder/>
 - optional: change all the view functions to use the custom template, if specified
 - optional/maybe: tests?
 - optional/maybe: documentation?
 - optional/maybe: autopep8?
 - optional/maybe: publish?? (blogpost, pr)
 - known limitation: no newlines in tasks.
 - info needed:
     - bug: ie (weird): skips back to 0% and first question, then after Continue, skips to the next new question after the last position before break-off (e.g., 50%).
     - bug: ie 11 (weird): does not work (endless loop after two questions)
     - bug: ie 11: default magnification too big

# Done

 x major: extra optional form for demographic questions.
 x optional/maybe: separation into modules?
 x optional/maybe: page with requirements? (no!)
 x minor: adjust task and content location on all devices
 x major: use selection logic (use as module)
 x optional: put user agent check in a module
 x added edge 12 to min versions
 x major bug: in general: status bar blocks the view, continue not visible (not reproducible)
 x bug: opera: progress bar not visible? more info needed, resizing issue? (not reproducible)
 x minor: bigger font size (change this via custom bootstrap file: <http://getbootstrap.com/customize/?id=c7d628a60824a5506ec07364dd3ce003>
 x major bug: in general: footer blocks the view, continue not visible
 x drop situation and sentence headings
 x include go back link in error page, if available
 x spacing between answers
 x include university placeholder
 x implement task selection
 x multiple experiments at the same time
     - traverse experiment folder
         - read all the settings
         - include active: true setting
         - log by experiment
         - have first template by experiment
     - change all the backends
         - create routes per experiment
         - set cookie by experiment, aso.

# Zsofia (?)

x write demographic questions.
x clear task selection criteria.
x prerequisite for task selection: label the tasks we have according to these major and minor categories first.
x come up with fillers for 2 & 3.
x write an introduction/example and write/modify the consent form.
- rethink timing? Account for the time for consent form and introduction/examples and the demographic questions.
- decide if RT is a factor for payment, if yes, which RTs?

# Deployment (automate uberspace deployment in general)

## Init Uberspace

 - manual step: create uberspace
 - automate?
     - use pwgen and symlink pw
     - use password file sheme
     - change ssh config
     - upload ssh key
     - rsync minimal config

## Init Code

 - (it would be best to write a script for this that automates this process via ssh.)
 - enable error logging: ``uberspace-configure-webserver enable error_log``
 - upload with the upload script
 - remove ``pkg-resources==0.0.0`` from requirements.txt
 - install virtualenv with pip: ``[perigen@diphda studyriffic]$ pip3.4 install virtualenv --user``
 - create the virtualenv and activate it: ``virtualenv .env && source ./.env/bin/activate``
 - install the requirements: ``[perigen@diphda studyriffic]$ pip3.4 install -r requirements.txt``
 - use upload script to create service file and replace python path to virtualenv

## Init DB

 - enable own mongodb instance, password protected
 - run mongodb instance via uberspace
 - change the webapp config so pymongo can access the db

## Run Code

 - use run script
 - check log: ``watch -n 1 "zcat -f ~/service/studyriffic/log/main/* | tai64nlocal | tail -n 30"``

## Reporting/Monitoring/Testing?

