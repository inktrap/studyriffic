% rebase('base.tpl', title=name + ": " + str(error))

<h1>That did not go as planned!</h1>

<div class="alert alert-danger">{{error}}</div>

<p>We are sorry about that. Unfortunately, there is not a lot we can do.</p>
% if study:
<p>However, <a href="{{url('study', study=study)}}">you can start the study again</a>.</p>

