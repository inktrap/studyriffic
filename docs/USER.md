# A user guide to Studyriffic

Studyriffic is a simple tool to create and host multiple studies, especially on
[prolific](https://prolific.ac). This is the [user
guide](https://github.com/inktrap/studyriffic/blob/master/docs/USER.md) (that
means: you want to setup your own instance of studyriffic), but
[developers](https://github.com/inktrap/studyriffic/blob/master/docs/DEVELOPER.md)
and [admins](https://github.com/inktrap/studyriffic/blob/master/docs/ADMIN.md)
should read it as well, because I am going to explain the ideas and concepts
while I create our first study and then we are going to collect the results. If
anything goes wrong during the setup, have a look at the errors. Let's start!

# Short Introduction

 - configure your database among other settings in ``ROOT/modules/config.py``
 - create your tasks in ``ROOT/studies/study/tasks.json``
 - create your settings in ``ROOT/studies/study/settings.json``
 - define an introduction in ``ROOT/views/study/first.tpl``

Run ``main.py`` and get a lot of ``AssertionError``s. Read more.


# Create a new study

Basicly what you are doing is always the same. Studyriffic is run by convention
over configuration and therefore some files are pretty important. You should
probably now what [json](https://en.wikipedia.org/wiki/JSON) is. Let's assume
you do. Let's assume further your are interested in [owls]() and you would like
to ask people questions about owls.

The first thing you have to do, is to create a folder, like this:
``ROOT/studies/owls``. This folder gives your study it's name and will contain
the settings and tasks files.


## Settings

Our settings are living in a file called ``settings.json`` in the folder we just created.

A settings file looks like the example below, and the keys that are described
below are mandatory. Studyriffic is checking this pretty strictly, so you
probably will get a lot of complaints (which is a good thing!) if you forget a key.

 - ``"active": true,``  if this setting is true, his study is active, if it is false, the study is not active.
 - ``"max_check_fail": 1``, the maximum number of attention checks a user is allowed to fail before the study will be aborted.
 - ``"labels": false,``  should we label the scale? scales will be labeled if this setting is active and the scale consists of 3 or more values.
 - ``"question":"Do you think the following sentence is “true” or “false” in the above situation?",`` this is the question you would like to ask the participant.
 - ``"situation":"Please consider the following situation:",``  This is an (optional) situation (or context) you would like to give. If it is empty, the task is displayed differently.
 - ``"questions": 20,``  the numbers of questions. Also depends on the criteria for select restrictions (or vice-versa, depends on you).
 - ``"min_scale": 0,``  minimal value of the scale (including value).
 - ``"max_scale": 4,``  maximal value of the scale (including value).
 - ``"min_scale_desc" : "Definitely false",``  description of the minimal value.
 - ``"max_scale_desc" : "Definitely true",`` description of the maximal value.
 - ``"university": "Great Owl University",``  the university or affiliation that is responsible. Will be displayed in the footer.
 - ``"investigator": "Dr. Owly Mc Owlface",``  the name of the person responsible for the study.
 - ``"contact" : "Owly.Owlface@owl-university.owl",``  the e-mail of the person responsible for the study.
 - ``"time" : 5,``  the time that you think is needed for the study. Used in the consent form, but not enforced (this is prolific's job).
 - ``"link" : "https://github.com/inktrap/studyriffic",`` the link that will appear in the end were participants are payed.
 - ``"types":["hunt", "fact", "jimmy", "owl"],`` a complete list of the types that appear in your tasks file.
 - ``"templates": ["first.tpl"],`` the custom templates you are going to use. By default this would be the template that shows the introductions and gives examples.
 - ``"restrictions":[]`` this is a list of restrictions. More on that later.

## Optional settings

 - ``excluded_pids`` is a list of excluded pids. If you want to exclude one or
 a few users from your study, you may list them here. If you want to
 exclude a lot of users, place a file called ``EXCLUDED_PIDS.txt`` in your
 study dir, it will be appended to this list.
 ``EXCLUDED_PIDS.txt`` has to contain one pid per line. In general it does not
 matter if you specify something as a number or a string or have duplicate
 values. In the end, every value will be turned into a string and then the whole list into a set.

## Restrictions

### Select


 - ``{"action":"select", "category":"filler", "argument":9},`` a select restriction that selects 9 tasks which are in the category ``filler``.
 - ``{"action":"select", "category":"target", "argument":9},`` same as above, with category ``target``.
 - ``{"action":"select", "category":"check", "argument":2},`` two tasks are attention ``check``s.

Note that the sum of all tasks  (here ``20``) has to be equal to the number of questions.


**PLEASE NOTE:** all select restrictions have to sum up to exactly 1 (100%) also you can only select tasks by category (that is what categories are for).

### Successor

 - ``{"action":"max_successors", "category":"check", "argument":0},`` a task with the category ``check`` is allowed to have ``0`` successors of the same category.
 - ``{"action":"max_successors", "category":"filler", "argument":3},``a task with the category ``filler`` is allowed to have ``3`` successors of the same category.
 - ``{"action":"max_successors", "category":"target", "argument":3},``a task with the category ``target`` is allowed to have ``3`` successors of the same category.
 - ``{"action":"max_successors", "type":"hunt", "argument":2},``a task with the type ``hunt`` is allowed to have ``2`` successors of the same type.
 - ``{"action":"max_successors", "type":"jimmy", "argument":2},``a task with the type ``jimmy`` is allowed to have ``2`` successors of the same type.

**PLEASE NOTE:** if a sequence that is not allowed is recognized the sample
will be drawn again that means that if you have a lot of restrictions and
a very small list of tasks it might be impossible or close to impossible to
find a sample that fits your requirements (and we can't realisticly find
a solution by random selection). In that case the user will recieve an error.

### Position

 - ``{"action":"not_positions", "category":"check", "argument":[0, 19]}`` an
 item of the category ``check`` is not allowed to occur at position ``0`` or
 position ``19`` (which are the head  and the tail of the list.


## Tasks

Your tasks are living in a file called ``tasks.json`` and it also has a pretty
strict format. Some values here affect ``settings.json``, so they have to fit
together.

### A single task

A ``tasks.json`` file consists of a list of tasks. A single task might look like this:

 - ``"situation": "",`` this is the situation. if it is non-empty (that means anything else than "") it will be displayed first, see: situation-sentence-example.
 - ``"category": "",`` the whole task has to have a category. typical categories are filler and target
 - ``"sentence": "",`` this is the sentence that the participant is going to rate/judge
 - ``"type": "",`` the whole task can have types which act as a fine-grained labeling that is not as broad as categories
 - ``"id":`` lastly a task has to have a sequential numerical id that is unique for this tasks file


### An example tasks file

And a very small ``tasks.json`` file might look like this:

~~~
[
{
    "category": "filler",
    "check": [0.0],
    "id": 0,
    "sentence": "It was surprising that the owl saw the mouse even if it was dark.",
    "situation": "Owls can hunt if it is dark.",
    "type": ["hunt"]
}, {
    "situation": "Owls are very good hunters.",
    "category": "target",
    "sentence": "The owl caught the mouse and ate it.",
    "type": ["hunt", "owl"],
    "id": 1
}, {
    "situation": "This is an attention check.",
    "category": "check",
    "sentence": "Please select MAX_SCALE_DESC",
    "type": [],
    "check": [1.0],
    "id": 2
}
]
~~~

So, we have two tasks, one is a filler and one a target and both are of the
type ``hunt`` and ``owl``. We also have two different situations and sentences.
The IDs don't have to be sequential, they only have to be unqiue integers.

#### Attention Checks

The last task is an attention check, because it is of the category ``check``.
Also it has an additional key ``check``, which specifies the value the
participant has to enter in order to pass the check.

 - The value of check, which is either ``0`` or ``1`` is mapped to the scale
 you specified in your ``settings.json`` file: ``0.0`` is mapped to the lowest
 possible value, or minimum of your scale, and ``1`` is mapped to the highest
 possible value, or maximum of your scale.
 - This is approach ensures that you can switch scales easily. The answer of an
 attention check that wants you to select the minimum always wants the lowest
 value on your scale.
 - You can use the placeholders ``MIN_SCALE``, ``MAX_SCALE``,
 ``MIN_SCALE_DESC`` and ``MAX_SCALE_DESC`` in the ``situation`` or ``sentence``
 texts and they will be replaced with the values you entered in the settings
 for ``min_scale`` aso.

If a participant fails ``max_check_fail`` checks for attention, the study is
aborted.

For fillers the category ``check`` is present, but currently unused.

### A tasks file that works

Please check the examples in the ``studies`` folder, set the ``active`` key in
``ROOT/studies/owls/settings.xml`` to ``true``. Then run ``./main.py``. The
debugging output tells you to go to ``http://127.0.0.1:63536/studies/owls/`` to
participate in the owls study.

**You should complete your study at least once yourself. Some errors
that way you can be sure everything looks like it should and you
get the results you like.**

## Views

Create a directory that is named like your study in the views directory. Then
put the template file you want to use in it. F.e.: to use a custom
``first.tpl`` in our owls-study, create we would have to create
``ROOT/views/owls/first.tpl``. **This is mandatory!!** But if you forget it,
don't worry, Studyriffic will remind you with an ``AssertionError`` (see
structural errors below).


### Inline HTML and newlines

The value of a ``"sentence"`` and ``"situation"``-key might contain a newline.
As per the JSON-standard, newlines have to be written as `\n`. The newline will
be transformed into an HTML-linebreak by JavaScript in the template
``main.tpl``.

Technical note: ``main.tpl`` uses Jquery's ``html``-method to display the content
-- and therefore is vulnerable to XSS-attacks and other shenanigans. I worked
with the assumption that you are creating your template (or are using mine) but
you are definitely creating your own tasks and settings files, so you can trust
them. That way you have the flexibility to include other inline markup, despite
that this is not the preferred way of doing this.


# Results

I am going to explain how you get your results and how you can interpret the
format. Then I'll show you how you can read them with R (which is basic R knowledge
but included for the sake of completeness).

## From Mongodb's JSON to CSV that R can read

Results are saved on your server in MongoDB. If you used the cronjob to backup
the data, you should get a json file with the results of your study. Let's
download it with scp and put it into the right results directory. For the owls
study this would be: ``ROOT/results/owls/db.json`` where I used the same
convention again: the folder is the name of the study and the results are in
a file with a fixed name: ``db.json``.

You **have** to use the same name that you used in ``ROOT/studies``.
You **have** to name your results ``db-foldername.json``. And you have to make
sure your study is well-configured, which means it has a ``tasks.json`` and
a ``settings.json`` and the assumption is that those are the files **that you
actually used during your study**.

If you are going to run ``results.py`` now, it will check for all of that,
except for the assumption mentioned above.


## The csv files

``results.py`` then will produce several csv files:

~~~
ROOT/results/owls/csv/settings.csv
ROOT/results/owls/csv/demographics.csv
ROOT/results/owls/csv/tasks.csv
ROOT/results/owls/csv/results.csv
~~~

What are they? ``RESULTS/owls/csv/demographics.csv`` is a file with the data
from the demographics form. ``RESULTS/owls/csv/settings.csv`` contains the
settings from the experiment. It might be important to interpret your results,
because it also lists the scale you used. Secondly ``university,
investigator``, and ``contact`` might be used to automatically publish your
data or results.

Your results file (``RESULTS/owls/csv/results.csv``) lists the results for each
participant (and their prolific id) together with a task-``id`` which is the
same as in ``RESULTS/owls/csv/tasks.csv``, the later telling you which result
originated from which task.


## R

That way you can simply copy the csv folder wherever you do your analysis.
There you can read the data into R with:

~~~
demographics = read.csv("./csv/demographics.csv")
settings = read.csv("./csv/settings.csv")
tasks = read.csv("./csv/tasks.csv")
results = read.csv("./csv/results.csv")
~~~

Then you'll get 4 dataframes and can easily connect the results with f.e. the
actual data used in the task. And you can check what your answers actually mean
by comparing ``results.csv`` with ``settings.csv``.


## Publish your data

My intention is to make the step from the database to the results transparent.
In addition I would reccomend using something like
[knitr](http://yihui.name/knitr/) and Rmarkdown to make the relationship
between the results and the published results transparent:

 - by using your ``settings.csv`` file which lists the authors of the study,
 you (or I) can write a script to export your ``csv``-files to a designated
 platform.

 - if you publish the ``task.json``, ``settings.json`` and ``db.json``, everyone
 can reproduce the csv files, because studyriffic and ``results.py`` is open
 source and (I hope) well documented. **TODO:** what about spam if the contact
 mail is included?

 - if you are using [knitr](http://yihui.name/knitr/) in
 your TeX-files or Rmarkdown, you can be sure that you are using the data from
 the csv files (and it is easy to check if two files are the same).

If you know a better and easier way, please leave some feedback, I would love
to hear about it! (TODO: [www.foastat.org](foastat)).


# Errors

When I am configuring a study I don't expect it to work immediately: “I will
get a lot of errors and that is a good thing.” It is like programming in
a statically typed language: The compiler will catch the biggest mistakes and
you have less headaches once your stuff works. (Yes, I used -- dynamically
typed -- Python here :)). This section is about common errors and what you have
to do to fix them.

It is easy to catch structural things and it is harder to get the
intentions right. So there are two broad categories of errors:

 - **logical errors:** mean you messed up a setting that conflicts with other
 settings or it might be that a setting/item/whatever has the wrong type or
 conflicts logically with the assumptions that I made for you and there are

 - **structural errors:** a file or a key or a value is missing -- it does not
 matter what -- something is missing or has not the structure that I expect.

If you think another error needs more explanations or is not justified, please
open a [GitHub issue]().


## Logical

There are a lot more assertions, but I think I should explain at least the
following ones (this might be slightly out of date).

### AssertionError: "Select restrictions have to sum up to …"

Selection restrictions have to sum up to one. Otherwise I don't know what
I should select for you to get 100% of the tasks.

### AssertionError: "You want to take more questions than there are questions"

The number of tasks you specified is too high. So either you should get more
tasks or reduce the number of tasks you want to display (this happens via the
``questions`` variable in your ``settings.json`` file.

### AssertionError: "A task needs an explicit numerical ID, but %s is not %i"

Honestly, giving each task an index it would had anyway seems like a burdon.
But the thing is: I don't want to rely on implicit ids. There are two reasons for that:

 - The tasks file might change: Maybe someone decides to update the tasks file
 and changes the order? That way every index would shift.

 - The second reason is that explicit indexes allow you to know immediately
 which task and which results are related.

And: you always can use the small script I put in the ``ROOT/studies``
directory, which does exactly that: ``add_sequential_id.py``.
It expects a list of dictionaries in json format (like a tasks list) and then
inserts a key with a numerical id into each dictionary. Voilá problem solved,
just check that everything worked as intended and move it into your studies folder
and rename it to ``tasks.json``.

## AssertionError: You want to select X tasks of the category C but there are only Y tasks of that category

The category has not enought tasks. So:

 - increase the number of tasks of category ``C`` or
 - change the selection or
 - use less questions

## Structural

### AssertionError: "Study %s needs the templates %s in %s"

You have to create a directory named like your study in the ``ROOT/views`` and
have to place the template file there. Which templates you have to place there
is defined in your ``settings.json`` file, for example for the owls study that
would be ``first.tpl``:

~~~
    "templates": ["first.tpl"],
~~~

