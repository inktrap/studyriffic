% rebase('base.tpl', title=name + ": Tasks", js=["main.js"])
      <div id="task" class="topspace">
        <!-- a situation might be empty. then the block is not displayed and js
        displayes the question immediately -->
        % if len(situation) > 0:
        <div class="description">
                <span class="glyphicon glyphicon-hand-right"></span>
                {{situation}}
        </div>
        <div class="situation text-primary"></div>
        <p class="text-center">
        <button type="submit" class="sentence is_visible btn btn-default" name="submit" value="true">Continue</button>
        </p>
        % end
        <!--
        <h1 class="sentence is_hidden"> Sentence </h1>
        -->
        <div class="description is_hidden">
            <span class="glyphicon glyphicon-hand-right"></span>
            {{question}}
        </div>
        <div class="sentence text-primary is_hidden"> </div>
        <hr class="is_hidden"/>
        <div class="answer text-center is_hidden">
            <form class="scale inline">
                % include('scale.tpl', min_scale=min_scale, max_scale=max_scale, max_scale_desc=max_scale_desc)
            </form>
        </div>
        <p class="text-center">
        <button type="submit" class="task is_hidden btn btn-default" name="submit" value="true">Continue</button>
        </p>
      </div>

      % include('progress.tpl', complete=complete)

