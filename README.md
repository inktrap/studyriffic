# Surveyriffic

A simple beautiful rock solid survey tool to be used with prolific.

 - <http://127.0.0.1:8080/?prolific_pid=123&session_id=foobar>
 - <https://perigen.diphda.uberspace.de/fcgi-bin/surveyriffic.fcgi>

# Valentin Todo

 - put demo online with an example and send a link.
 - extra form demographic questions.
 - page with requirements
 - check if the prolific id already did the survey
 - write results to db and display link
 - get link from config
 - implement task selection
 - change format of tasks from latex to json

# Zsofia (?)

- write demographic questions.
- clear task selection criteria.
- prerequisite for task selection: label the tasks we have according to these major and minor categories first.
- rethink timing? Account for the time for consent form and introduction/examples and the demographic questions.
- come up with fillers for 2 & 3.
- write an introduction/example and write/modify the consent form.
- decide if RT is a factor for payment, if yes, which RTs?

# Maybe/Sometimes

 - separation into modules
 - tests
 - documentation
 - publish

# Deployment

 - enable error logging: ``uberspace-configure-webserver enable error_log``
 - upload with the upload script
 - remove ``pkg-resources==0.0.0`` from requirements.txt
 - install virtualenv with pip: ``[perigen@diphda surveyriffic]$ pip3.4 install virtualenv --user``
 - create the virtualenv and activate it: ``virtualenv .env && source ./.env/bin/activate``
 - install the requirements: ``[perigen@diphda surveyriffic]$ pip3.4 install -r requirements.txt``

 - change the script, use currently: ``/usr/local/bin/python3.4``
 - https://perigen.diphda.uberspace.de/fcgi-bin/surveyriffic.fcgi

 - check that the syntax of your wrapper works: ``python3.4 -m py_compile surveyriffic.fcgi``
 - check that the syntax of your script works: ``python3.4 -m py_compile surveyriffic.fcgi``
