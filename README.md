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

 - A study with the likert scale: <https://perigen.diphda.uberspace.de/study/demo_likert?prolific_pid=123&session_id=foobar>
 - A study with the likert scale: <https://perigen.diphda.uberspace.de/study/demo_binary?prolific_pid=123&session_id=foobar>

# Valentin Todo

 - Problems:
    - experiment 1b) has a 50/50 split between filler and target-items, but 15 questions. This is not possible.
    - experiment 1b) will have the same taskorder than 1a), right?
    - a task can only have one label, since it is a string and not a list
        - conj/disj can only be implemented as extra labels, which is … annoying?


 - create more question types, f.e. question answer pair question types (how
 could this be done flexibly? currently this is … an inconvenience, but for
 studyriffic to be really useful this would be needed, c.f. experigen setup.
 generate main.tpl content from json?)
    - the thing is … the data that is saved in the cookies and so on is checked
    to be consistent … I have to rewrite a lot of stuff and generate it dynamically …
    this is not practical for now (should I just adapt it to fit the situation?)

 - clean up uberspace (no mysql db needed, delete unnecessary data …)
 - deploy
    - create cronjob file from settings.json
        - cronjob with mongoexport and timestamps, (so we get backups!)
        - study data  is accessible from pw protected dir (htaccess htuser, data.perigen …)
        - ``mongoexport --db test --collection traffic --out traffic.json``
 - major: after everything is set up, password protect the index for testing

 - meeting: share information (increase the bus factor). give zsophia:
    - the uberspace credentials
    - the study testing credentials
    - the study data access credentials
    - possibly documentation

 - run a small test experiment?
    - create a prolific account
    - transfer money to prolific
    - reset the db
    - do a very small test experiment (to get the selectors right and see how everything works 5€?)
 - run main experiment:
    - reset the db
    - do the main experiment

 - write documentation and maybe some more tests
    - a paper would be nice that could be cited by … zsophia? is that a good idea?

 - optional (load private settings from separate settings file, add it to gitignore)
 - at some point: results
    - json to r: jsonlite <https://www.opencpu.org/posts/jsonlite-a-smarter-json-encoder/>

 - optional: change all the view functions to use the custom template, if specified
 - optional/maybe: tests?
 - optional/maybe: documentation?
 - optional/maybe: autopep8?
 - optional/maybe: publish?? (blogpost, pr)
 - known limitation: no newlines in tasks.
 - info needed (if ie has this weird behaviour i am going to exclude it as well as edge):
     - bug: ie: skips back to 0% and first question, then after Continue, skips to the next new question after the last position before break-off (e.g., 50%).
     - bug: ie 11: does not work (endless loop after two questions)
     - bug: ie 11: default magnification too big (why?)

# Done

~~~
 x tasks have an extra id field
 x check if the prolific id already did the study (before saving and before the study loads)
 x separate hostname based db config for uberspace
 x check for TODOs
 x consent form styling
 x why is the method to insert the document into the db called twice?! (answer: js and redirect)
 x major: make the step before last rock solid!!!
     - check if the prolific id already did the study
 x major: write results to db
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
~~~

# Zsofia (?)

~~~
x write demographic questions.
x clear task selection criteria.
x prerequisite for task selection: label the tasks we have according to these major and minor categories first.
x come up with fillers for 2 & 3.
x write an introduction/example and write/modify the consent form.
- rethink timing? Account for the time for consent form and introduction/examples and the demographic questions.
- decide if RT is a factor for payment, if yes, which RTs?
~~~

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

