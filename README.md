# Surveyriffic

A simple beautiful rock solid survey tool to be used with prolific.

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

 - change template to use custom template if specified
     - extra form demographic questions.
 - check if the prolific id already did the survey
 - reenable session check
 - write results to db
 - change format of tasks from latex to json
 - I need to write the results of the study to the db. (Most important
   step!)
   (So the selection of new tasks could be based on previous selections …
   but I guess that random selection would be fine? Well, I could test how
   300 values in the interval [0,20] distribute …)
 - I need to incorporate and test the selection logic.
 - and I finally need to change the data to fit our needs.

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

- write demographic questions.
- clear task selection criteria.
- prerequisite for task selection: label the tasks we have according to these major and minor categories first.
- rethink timing? Account for the time for consent form and introduction/examples and the demographic questions.
- come up with fillers for 2 & 3.
- write an introduction/example and write/modify the consent form.
- decide if RT is a factor for payment, if yes, which RTs?

# Maybe/Sometimes

 - page with requirements
 - separation into modules
 - tests
 - documentation
 - autopep8
 - publish

# Deployment

 - enable error logging: ``uberspace-configure-webserver enable error_log``
 - upload with the upload script
 - remove ``pkg-resources==0.0.0`` from requirements.txt
 - install virtualenv with pip: ``[perigen@diphda surveyriffic]$ pip3.4 install virtualenv --user``
 - create the virtualenv and activate it: ``virtualenv .env && source ./.env/bin/activate``
 - install the requirements: ``[perigen@diphda surveyriffic]$ pip3.4 install -r requirements.txt``
 - use upload script to create service file and replace python path to virtualenv
 - check log: ``watch -n 1 "zcat -f ~/service/surveyriffic/log/main/* | tai64nlocal | tail -n 30"``
