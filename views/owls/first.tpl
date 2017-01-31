% rebase('base.tpl', title=name + ": Instructions", js=['first.js'], css=['first.css'])

<div class="next is_visible">
    <h1>
    Hello and thank you for your participation.
    </h1>

    Your task will be to answer questions. For each question,

    <ol>
        <li> you are going to see a description of a <mark>scenario</mark>, </li>
        <li> and you will be presented with a <mark>sentence</mark>. </li>
    </ol>

    Your task will be to tell us how certain you are that the sentence is
    <mark>true or false</mark> given the information provided by the scenario.

    % include('first-button-next.tpl', study=study)
</div>

<div class="next is_hidden topspace">
    Let us see an example:

    <hr class=""/>
    <div class="description">
            <span class="glyphicon glyphicon-hand-right"></span>
            {{situation}}
    </div>
    <div class="situation text-primary">
    An owl is a bird that eats mice.
    </div>
    <!--
    <h1 class="sentence "> Sentence </h1>
    -->
    <div class="description ">
        <span class="glyphicon glyphicon-hand-right"></span>
        {{question}}
    </div>
    <div class="sentence text-primary "> All owls are carnivores. </div>
    <hr class=""/>

    <div class="answer text-center topspace">
        <form class="scale disabled inline">
            % include('scale.tpl', min_scale=min_scale, max_scale=max_scale, max_scale_desc=max_scale_desc)
        </form>
    </div>
    <hr class=""/>

    In this case, you would probably select <!-- span class="text-bold">{{max_scale}}</span -->
    <span class="scaledescription">{{max_scale_desc}}</span>.
    % include('first-button-next.tpl', study=study)
</div>

<div class="next is_hidden topspace">
    Let us take another example:

    <hr class=""/>
    <div class="description">
            <span class="glyphicon glyphicon-hand-right"></span>
            {{situation}}
    </div>
    <div class="situation text-primary">
    An owl is a bird that eats mice.
    </div>
    <div class="description ">
        <span class="glyphicon glyphicon-hand-right"></span>
        {{question}}
    </div>
    <div class="sentence text-primary "> All owls are good at math. </div>
    <hr class=""/>

    <div class="answer text-center ">
        <form class="scale disabled inline">
            % include('scale.tpl', min_scale=min_scale, max_scale=max_scale, max_scale_desc=max_scale_desc)
        </form>
    </div>
    <hr class=""/>

    <p>
    In this case, you would probably select <!-- span class="text-bold">{{min_scale}}</span -->
    <span class="scaledescription">{{min_scale_desc}}</span>.
    However, the examples will not
    all be so clear and you may select any value between
    <!--span class="text-bold">{{min_scale}}</span -->
    <span class="scaledescription">{{min_scale_desc}}</span> and
    <!-- span class="text-bold">{{max_scale}}</span -->
    <span class="scaledescription">{{max_scale_desc}}</span>
    to reflect how certain you are of the truth or falsity of the sentence.
    </p>

    % include('first-button-next.tpl', study=study)
</div>


<div class="next is_hidden">
    <h2>
    Important!
    </h2>
    <p>
    There are no right or wrong answers. We are asking you for your <mark>own
    intuitive judgement</mark>. Do not let previous trials or your own earlier
    responses influence you. You should forget previous examples as the study goes
    on and provide your intuition only on the basis of the example at hand.
    </p>

    % include('first-button-submit.tpl', study=study)
</div>

