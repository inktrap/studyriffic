# A user guide to Studyriffic

“Or: I am getting ``AssertionError``s, how does this thing work?”

Studyriffic is a simple tool to create and host multiple studies, especially on
[prolific](). This is the [user guide]() (that means: you want to setup your
own instance of studyriffic), but [developers]() and [admins]() should read it
as well, because I am going to explain the ideas and concepts while I create
our first study and then we are going to collect the results. If anything goes
wrong during the setup, have a look at the errors. Let's start!


# Create a new study

Basicly what you are doing is always the same. Studyriffic is run by convention
over configuration and therefore some files are pretty important. You should
probably now what [json](https://en.wikipedia.org/wiki/JSON) is. Let's assume
you do. Let's assume further your are interested in [owls]() and you would like to
ask people questions about owls.

The first thing you have to do, is to create a folder, like this: ``ROOT/studies/owls``.
This folder gives your study it's name and will contain the settings and tasks files.


## Settings

Our settings are living in a file called ``settings.json`` in the folder we just created.

A settings file looks like the example below, and the keys that are described
below are mandatory. Studyriffic is checking this pretty strictly, so you
probably will get a lot of complaints (which is a good thing!).

Json does not allow comments, so you probably want to download the complete
[settings.json]() file without comments.

~~~
{
    "active" : true, /* if this setting is true, his study is active */
    "question":"Do you think the following sentence is “Owly” or “Not Owly” in the above situation?", /* this is the question you would like to ask the participant */
    "situation":"Please consider the following situation:", /* This is an (optional) situation (or context) you would like to give. If it is empty, the task is displayed differently */
    "questions": 4, /* the numbers of questions. Also depends on the criteria for select restrictions (or vice-versa, depends on you) */
    "min_scale": 1, /* minimal value of the scale (is included) */
    "max_scale": 5, /* maximal value of the scale (is included) */
    "min_scale_desc" : "Definitely Not Owly", /* description of the minimal value */
    "max_scale_desc" : "Definitely Owly", /* description of the maximal value */
    "university": "Great Owl University", /* the university or affiliation that is responsible. Will be displayed in the footer */
    "investigator": "Dr. Owly Mc Owlface", /* the name of the person responsible for the study */
    "contact" : "Owly.Owlface@owl-university.owl", /* the e-mail of the person responsible for the study */
    "time" : 5, /* the time that you think is needed for the study. Used in the consent form */
    "link" : "https://example.org", /* the link that will appear in the end were participants are payed */
    "actions": ["select", "max_successors"], /* a list of possible values for actions. If you are not adding new actions, you don't have to change this */
    "types":["hunt", "fact", "jimmy"], /* a complete list of the types that appear in your tasks file */
    "categories":["filler", "target"], /* a complete list of categories that appear in your tasks file */
    "templates": ["first.tpl"], /* the custom templates you are going to use. By default this would be the template that shows the introductions and gives examples */
    "restrictions":[ /* this is a list of restrictions */
        {"action":"select", "category":"filler", "argument":0.5}, /* a select restriction that selects 50% of the tasks to be of the type "filler" */
        {"action":"select", "category":"target", "argument":0.5}, /* a select restriction that selects 50% of the tasks to be of the type "target" */
                                                                  /* PLEASE NOTE:
                                                                     all select restrictions have to sum up to exactly 1 (100%) 
                                                                     also you can only select tasks by category (that is what categories are for
                                                                   */
        {"action":"max_successors", "category":"filler", "argument":3}, /* a sequence of three tasks of the category filler is allowed, more is forbidden */
        {"action":"max_successors", "category":"target", "argument":3}, /* a sequence of three tasks of the category target is allowed, more is forbidden */
        {"action":"max_successors", "type":"hunt", "argument":2},  /* a sequence of two tasks with the type hunt is allowed, more is forbidden */
        {"action":"max_successors", "type":"jimmy", "argument":2}  /* a sequence of two tasks of the type jimmy is allowed, more is forbidden */
                                                                  /* PLEASE NOTE:
                                                                     if a sequence that is not allowed is recognized the sample will be drawn again
                                                                     that means that if you have a lot of restrictions and a very small list of tasks
                                                                     it might be impossible or close to impossible to find a sample that fits your requirements
                                                                     (and we can't realisticly find a solution).
                                                                     In that case the user will be confronted with an error.
                                                                   */
    ]
}
~~~


## Tasks

Your tasks are living in a file called ``tasks.json`` and it also has a pretty
strict format. Some values here affect ``settings.json``, so they have to fit
together. Again, json does not allow comments, so download the whole
[tasks.json]() file (which is introduced at the bottom) without comments.

### A single task

A ``tasks.json`` file consists of a list of tasks. A single task looks like this:
~~~
{
    "situation": "", /* this is the situation. if it is non-empty (that means anything else than "") it will be displayed first, see: situation-sentence-example. */ TODO
    "category": "", /* the whole task has to have a category. typical categories are filler and target */
    "sentence": "", /* this is the sentence that the participant is going to rate/judge */
    "type": "", /* the whole task can have types which act as a fine-grained labeling that is not as broad as categories */
    "id": /* lastly a task has to have a sequential numerical id that is unique for this tasks file */
}
~~~

### An example tasks file

And a ``tasks.json`` file might look like this:

~~~
[
{
    "situation": "Owls can hunt if it is dark.",
    "category": "filler",
    "sentence": "It was surprising that the owl saw the mouse even if it was dark.",
    "type": ["hunt", "owl"],
    "id": 0
}, {
    "situation": "Owls are very good hunters.",
    "category": "target",
    "sentence": "The owl caught the mouse and ate it.",
    "type": ["hunt", "owl"],
    "id": 1
}
]
~~~

So, we have two tasks, one is a filler and one a target and both are of the
type ``hunt`` and ``owl``. We also have two different situations and sentences.
The ids are how they should be: unique, numerical and sequential.

### A tasks file that works

Typicly you have a lot of questions and this is pretty important, otherwise the
task selection algorithm might not be able to produce results according to your
requirements -- there simply might not be enough items in each category or
for each type. So, this is like the previous file, only with more tasks.

~~~
[{
    "situation": "Owls can hunt if it is dark.",
    "category": "filler",
    "sentence": "It was surprising that the owl saw the mouse even if it was dark.",
    "type": ["hunt"],
    "id": 0
}, {
    "situation": "Owls are very good hunters.",
    "category": "target",
    "sentence": "The owl caught the mouse and ate it.",
    "type": ["hunt"],
    "id": 1
}, {
    "situation": "Owls can eat a lot of mice.",
    "category": "filler",
    "sentence": "It was surprising that the owl did not eat the mouse.",
    "type": ["fact"],
    "id": 2
}, {
    "situation": "Owls are not very good listeners.",
    "category": "target",
    "sentence": "Jimmy called the owl but the owl did not listen.",
    "type": ["fact"],
    "id": 3
}, {
    "situation": "Owls are awesome.",
    "category": "filler",
    "sentence": "It was surprising that the owl saw the mouse even if it was dark.",
    "type": ["fact"],
    "id": 4
}, {
    "situation": "Owls have a lot of feathers.",
    "category": "target",
    "sentence": "The owl caught the mouse and ate it.",
    "type": ["hunt"],
    "id": 5
}, {
    "situation": "Owls have a lot of humor.",
    "category": "filler",
    "sentence": "It was surprising that the owl saw the mouse even if it was dark.",
    "type": ["fact"],
    "id": 6
}, {
    "situation": "Jimmy petted an owl once.",
    "category": "target",
    "sentence": "The owl caught the mouse and ate it.",
    "type": ["jimmy"],
    "id": 7
}, {
    "situation": "The owl caught a mouse and brought it to Jimmy.",
    "category": "filler",
    "sentence": "It was surprising that the owl saw the mouse even if it was dark.",
    "type": ["jimmy"],
    "id": 8
}, {
    "situation": "Jimmy is the best friend of an owl.",
    "category": "target",
    "sentence": "The owl caught the mouse and ate it.",
    "type": ["jimmy"],
    "id": 9
}]

~~~


Here we have ten tasks, two categories (``filler, target``) and three types
(``jimmy, hunt, fact``). This should be enough for a small study with
four questions.

So set the ``active`` key in ``ROOT/studies/owl/settings.xml`` to ``true``.
Then run ``./main.py``. The debugging output tells you to go to
``http://127.0.0.1:63536/studies/owl/`` to participate in the owl study.


### Inline HTML and newlines

The value of a ``"sentence"`` and ``"situation"``-key might contain a newline.
As per the JSON-standard, newlines have to be written as `\n`. The newline will
be transformed into an HTML-linebreak by JavaScript in the template
``main.tpl``.

(Please note: ``main.tpl`` uses Jquery's ``html``-method to display the content
-- and therefore is vulnerable to XSS-attacks and other shenanigans. I worked
with the assumption that you are creating your template (or are using mine) but
you are definitely creating your own tasks and settings files, so you can trust
them. That way you have the flexibility to include other inline markup, despite
that this is not the preferred way of doing this.)

(Additional note/reminder for mysel: I still have to find out if bottle's
cookie function is vulnerable to CSRF and if my endpoints should look out for
token. On the other hand: the prolifc id is stored in the cookie, which has
a signature.)


## Views

 - if you want to use a custom template, create a directory that is named like
 your study in the views directory. Then put the template file you want to use
 in it. F.e.: to use a custom ``first.tpl`` in our owls-study, create we would
 have to create ``ROOT/views/owls/first.tpl``. But if you forget it, don't
 worry, Studyriffic will remind you with an ``AssertionError`` (see structural
 errors below).


# Results

I am going to explain the format of the results now and I'll show you how you
can process them with R.


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
following ones.

### AssertionError: "Select restrictions have to sum up to exactly 1"

Selection restrictions have to sum up to one. Otherwise I don't know what
I should select for you to get 100% of the tasks.

### AssertionError: "selection arguments can not produce items less than 1 (F.e.: You can not split a question in half)."

This happens if your selection restrictions would split a question. The number
of tasks you want to use has to be divideable without a remainder by all the
select restrictions. Otherwise I would have to guess or to round and that is
not something I want to do.

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

## Structural

### AssertionError: "Study %s needs the templates %s in %s"

You have to create a directory named like your study in the ``ROOT/views`` and
have to place the template file there. Which templates you have to place there
is defined in your ``settings.json`` file, for example for the owl study that
would be ``first.tpl``:

~~~
    "templates": ["first.tpl"],
~~~


