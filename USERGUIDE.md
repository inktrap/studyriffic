# A user guide to Studyriffic

“Or: I am getting ``AssertionError``s, how does this thing work?”

Studyriffic is a simple tool to create and host multiple studies, especially on
[prolific](). This is the [user guide](), but [developers]() should read it as well,
because I am going to explain the ideas and concepts while I create our first
study. Let's start!


# Create a new study

Basicly what you are doing is always the same. Studyriffic is run by convention
over configuration and therefore some files are pretty important. You should
probably now what [json](https://en.wikipedia.org/wiki/JSON) is. Let's assume
you do. Let's assume further your are interested in [owls]() and you would like to
ask people questions about owls.

The first thing you have to do, is to create a folder, like this: ``ROOT/studies/owls``.
This folder gives your study it's name and will contain the settings and tasks files.


# Settings

Our settings are living in a file called ``settings.json`` in the folder we just created.

A settings file looks like the example below, and the keys that are described
below are mandatory. Studyriffic is checking this pretty strictly, so you
probably will get a lot of complaints (which is a good thing!).

Json does not allow comments, so you probably want to download the complete
[settings.json]() file without comments.

~~~
~~~


# Tasks

Your tasks are living in a file called ``tasks.json`` and it also has a pretty
strict format. Some values here affect ``settings.json``, so they have to fit
together. Again, json does not allow comments, so download the whole
[tasks.json]() file without comments.

## A single task

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

## An example tasks file

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

## A tasks file that works

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


## Inline HTML and newlines

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


# Views

 - if you want to use a custom template, create a directory that is named like
 your study in the views directory. Then put the template file you want to use
 in it. F.e.: to use a custom ``first.tpl`` in our owls-study, create
 we would have to create ``ROOT/views/owls/first.tpl``. But if you forget it,
 don't worry, Studyriffic will remind you with an ``AssertionError``.

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


## Logical

## Structural


