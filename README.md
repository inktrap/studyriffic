# Surveyriffic

A simple beautiful rock solid survey tool to be used with prolific.

 - <http://127.0.0.1:8080/?prolific_pid=123&session_id=foobar>
 - <https://perigen.diphda.uberspace.de/fcgi-bin/surveyriffic.fcgi>

# Valentin Todo

 - put demo online with an example and send a link.

 - change template to use custom template if specified
     - extra form demographic questions.
 - check if the prolific id already did the survey
 - check that users can't skip to last
 - reenable session check
 - write results to db
 - change format of tasks from latex to json

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
