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

 - owls


# Valentin Todo

 - test one huge results table
 - flexbox footer that is sticky and scales and simply works

### documentation:

 - before publishing, have another look at the documentation
 - describe different restrictions in detail
 - add a license or a way to quote the documentation


## maybe/sometimes:

 - flash message if the participant is going really fast (configurable)
 - how to display errors?
 - how to encapsulate js properly?
 - include expected values for fillers in data
 - include a setting to specify the type of interval for ranges in the check field
 - implement interval setting and rounding setting
 - refactoring
     - try out rope
     - rename (as NOUN_SPECIFIER, where noun is the type of thing):
        - min_scale -> scale_min
        - max_scale -> scale_max
        - min_scale_desc -> scale_min_desc
        - max_scale_desc -> scale_max_desc
        - max_check_fail -> check_max_fail
        - excluded_pids -> pids_excluded

        - link -> link_finish
        - investigator -> investigator_name
        - contact -> investigator_contact
        - labels -> scale_labels
        - question -> task_question
        - situation -> task_situation

## documentation

 - run main experiment
 - participant selection criteria
    - english speaking
    - > 18
    - for 1a) exclude 1b)
    - for all exclude: 57acfa4dbd4ee2000111d379

 - write documentation and a paper
    - a paper describing the workflow would be nice and would be cited by zsophia :)

# Optional

 - optional (load private settings from separate settings file, add it to gitignore)
 - at some point: results
    - json to r: jsonlite <https://www.opencpu.org/posts/jsonlite-a-smarter-json-encoder/>

 - optional: change all the view functions to use the custom template, if specified
 - optional/maybe: tests?
 - optional/maybe: documentation?
 - optional/maybe: autopep8?
 - optional/maybe: publish?? (blogpost, pr)
 - info needed (if ie has this weird behaviour i am going to exclude it as well as edge):
     - bug: ie: skips back to 0% and first question, then after Continue, skips to the next new question after the last position before break-off (e.g., 50%).
     - bug: ie 11: does not work (endless loop after two questions)
     - bug: ie 11: default magnification too big (why?)

 - create more question types, f.e. question answer pair question types (how
 could this be done flexibly? currently this is … an inconvenience, but for
 studyriffic to be really useful this would be needed, c.f. experigen setup.
 generate main.tpl content from json?)
    - the thing is … the data that is saved in the cookies and so on is checked
    to be consistent … I have to rewrite a lot of stuff and generate it dynamically …
    this is not practical for now (should I just adapt it to fit the situation?)

# Done

~~~
 x create one huge results table
 x change consent form
 x increase number of tasks to N + number of checks
 x select restrictions work with ints instead of floats now
 x test select restrictions
 x included attention checks in studies
 x changed selects in studies
 x moved category and action setting keys to config module (the user only has to change those if a new feature is needed).

 x check that PATTERNS in checks are replaced correctly
 x include nondeceptive simple checks in studies: 2 (short studies) 3 (longer studies)
 x wrote pattern replacement logic for checks
 x if too many attention checks failed the situation and sentence is there but empty. this could be improved.
 x abort if a participant fails 2 attention checks
 x fixed logging output, removed duplicates
 x check other pass_ … checks
 x feature to exclude participants
 x test feature to exclude participants
 x populate excluded_pids from a file if present (append to config value)
 x check that pass_exclusion check works
 x prolific attention checks
 x unittest prolific attention checks
 x add columns for all the types, like type1 type2 aso
 x include open interval behaviour notice in docs
 x include python rounding behaviour notice in docs
 x fixed demographic forms and made it skip empty values (this case should never happen but it is cleaner anyway)
 x check that all the values from demographics-form are processed correctly (unittest this assumption)
 x fixed a bug with check
 x fixed a bug with demographic-form values
 x wrote tests for map_check
 x tests for the new attributes and the new restriction
 x included not_positions restrictions (forbid a task of a certain category to occur at a list of positions)
 x included new attribute for fillers and checks: "check" (expected value between [0,1] that can be mapped to every scale)
 x kontierungsblatt uberspace
 x write message to participants
 x pay participants
 x run study 1b)
     x test everything one more time and wait for okay
     x clear the database and remove the backups that accumulated while testing
     x create the study on prolific
     x remove password protection from the studies
     x change the url so subjects get paid
     x study is live
 x major: IE problem (either fix it or forbid IE!) (comment: could not fix in reasonable time. IE and edge are forbidden for now, reopen if relevant)
 x Continue button in the middle of the scale
 x 1b) Charlie-David should be one sentence (2 times)
 x new fillers for 3)
 x increase task number (after other fixes, test timing again)
 x reworded error message
 x implemented settings unittest
 x introduce a setting if labels should be present
 x set setting if labels should be present to false
 x remove numerical labels from introductions
 x changed 2) 3) to 20 and 1b) to 12 questions
 x changed number of questions for 1b) to 20 (see: TESTREPORT 3)
 x changed demographic form text (see: TESTREPORT 3)
 x questions with 2 or less choices don't have a number (see: TESTREPORT 3)
 x change introduction texts (see: TESTREPORT 2)
 x fix wrong info output for available studies
 x scale description in quotes (or different styling?)
 x remove important! exclamation mark
 x remove numbers or change scale and include numbers
 x typo in Alex and Bill: "both of their ratings"
 x remove latex style quotes
 x test run for all studies to check timing assumptions
 x fix empty sentences
 x assert empty sentences are forbidden
 x test empty sentences assertion
 x deploy
    - create cronjob file from settings.json
        - cronjob with mongoexport and timestamps, (so we get backups!)
        - study data  is accessible from pw protected dir (htaccess htuser, data.perigen …)
        - ``mongoexport --db test --collection traffic --out traffic.json``
 x password protect the index for testing
 x clean up uberspace (no mysql db needed, delete unnecessary data …)
 x rewrote tasks so they can have multiple types
 x explicit types (restrictions, task labels) (conj, disj)
 x write some more tests
 x include heading for consent
 x use the correct introduction
 x highlight additional introduction parts
 x use introductions per experiment
 - share information (increase the bus factor). give zsophia:
     - the uberspace credentials
     - the study testing credentials
     - the study data access credentials
 - i gave all the experiments names that contain the number (and a random noun so it is harder to guess a study): z: alright!
 - experiment 1b) has a 50/50 split between filler and target-items, but 15 questions. This is not possible.: z: 16 works
 - clarification: experiment 1b) will have the same taskorder than 1a), right? (probably right)
 - limitation: a task can only have one label, since it is a string and not a list
    - implement conj/disj as explicit combined labels
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

