% rebase('base.tpl', title=name + ": Consent")

<h1>Consent form</h1>

<p>
Welcome and thank you for participating in this web-based linguistics
experiment. Before taking part in this study, please read this consent form.
</p>

<p>
To participate you must be 18 years of age and you must be a native speaker of
English. There are no known risks associated with participation in this study.
Participation is voluntary and you have the right to discontinue at any time
without loss of benefits to which you are otherwise entitled.
</p>

<h2> Duration </h2>
<p> Please complete this experiment in one go. The experiment takes about
{{time}} minutes on average and consists of {{questions}} questions. You will
be paid for your participation at the posted rate upon full completion of the
experiment, that is, upon having answered all questions of the experiment.
</p>

<p>
Please note that the experiment contains attention checks. Failure to answer
{{max_check_fail + 1}} attention check questions correctly results in the
termination of the experiment without payment.
</p>

<h2> Privacy </h2>
<p>
All data you provide are recorded anonymously; we only associate your prolific
ID with the data you provide. We use cookies for the session, which contain
your prolific ID as the sole identifying information. Your individual privacy
will be maintained in all published and written data resulting from the study.
</p>

<h2> Optional Questions </h2>
<p>
At the end of the experiment, we will ask you to answer a few questions about
your person (e.g., age, gender, languages spoken) to provide us with
sociological data, but answering any of these questions is optional and failure
to answer will not result in any penalization or reduction of payment.
</p>

<h2> Consent </h2>

    % include('contact.tpl')

<form action="/study/{{study}}/consent" method="post">
    <div class="form-group">
    <div class="checkbox">
    <label><input type="checkbox" name="consent" value="true">I have read and understood the above statements and freely consent to participate in this study.</label>
    </div>
    <div class="checkbox">
    <label><input type="checkbox" name="cookie" value="true">I permit this study to create and use session cookies.</label>
    </div>
    <p>
    <label>
    % if prolific_pid is "":
    Please enter your prolific id:
    % else:
    Please change your prolific id, if it is wrong:
    % end
    <input type="text" name="prolific_pid" value="{{prolific_pid}}">
    </label>

    <p class="text-center">
    <button type="sumit" class="btn btn-default" name="submit" value="true">Continue</button>
    </p>
    </div>
</form>

