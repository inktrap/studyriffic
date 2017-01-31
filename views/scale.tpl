        <span class="scaledescription">{{min_scale_desc}}</span>
        % for i in range(min_scale, max_scale + 1):
            <div class="scaleitem">
                <input id="scale_{{i}}" class="uncheck" type="radio" value="{{i}}" name="answer"/>
                % if max_scale > 2 and labels:
                <label for="scale_{{i}}">{{i}}</label>
                % end
            </div>
        % end
        <span class="scaledescription">{{max_scale_desc}}</span>
