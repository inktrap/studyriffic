% rebase('base.tpl', title=name + ": Done")

<h1>Thank you!</h1>

<div>
    <span class="glyphicon glyphicon-thumbs-up"></span> You successfully completed the {{name}} study!
</div>
<div>
<span class="glyphicon glyphicon-hand-right"></span> <a href="{{link}}">Click here to get paid</a>.
</div>

% include('progress.tpl')

</div>
