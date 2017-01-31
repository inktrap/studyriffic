% rebase('base.tpl', title=name + ": Demographics", js=["demographics.js"])

<h1>Additional Questions</h1>

<p>
Thank you for completing the experiment. We would only like to ask you to answer a few brief questions about yourself now.
If you don't want to do that, just click <code>Continue</code> at the <a href="#bottom">bottom</a>.
</p>

<form action="" id="demographics" class="demographics" method="post">
    <div class="form-group">
        <div class="form-content">
            <h2>Age</h2>
            <fieldset id="age">
                <div class="radio">
                    <label for="age-1"><input type="radio" id="age-1" name="age" value="18-29">18-29 years old</label>
                </div>
                <div class="radio">
                    <label for="age-2"><input type="radio" id="age-2" name="age" value="30-44">30-44 years old</label>
                </div>
                <div class="radio">
                    <label for="age-3"><input type="radio" id="age-3" name="age" value="45-59">45-59 years old</label>
                </div>
                <div class="radio">
                    <label for="age-4"><input type="radio" id="age-4" name="age" value="60">60 years or older</label>
                </div>
                <div class="radio">
                    <label for="age-5"><input class="checked" type="radio" id="age-5" name="age" value="">Prefer not to say</label>
                </div>
            </fieldset>

            <h2>Gender</h2>
            <fieldset id="gender">
                <div class="radio">
                    <label for="gender-1"><input type="radio" id="gender-1" name="gender" value="male">Male</label>
                </div>
                <div class="radio">
                    <label for="gender-2"><input type="radio" id="gender-2" name="gender" value="female">Female</label>
                </div>
                <div class="text">
                   <input class="input-medium" type="text" id="gender-3" name="gender" maxlength="100" placeholder="Other"> <label class="sr-only" for="gender-3">Other:</label>
                </div>
                <div class="radio">
                    <label for="gender-4"><input class="checked" type="radio" id="gender-4" name="gender" value="">Prefer not to say</label>
                </div>
            </fieldset>

            <h2>Native Language</h2>
            <fieldset id="native">
                <div class="radio">
                    <label for="native-1"><input type="radio" id="native-1" name="native" value="british">British English</label>
                </div>
                <div class="radio">
                    <label for="native-2"><input type="radio" id="native-2" name="native" value="american">American English</label>
                </div>
                <div class="text">
                   <input class="input-medium" type="text" id="native-3" name="native" maxlength="100" placeholder="Other"> <label class="sr-only" for="native-3">Other:</label>
                </div>
                <div class="radio">
                    <label for="native-4"><input class="checked" type="radio" id="native-4" name="native" value="">Prefer not to say</label>
                </div>
            </fieldset>

            <h2>Other Languages</h2>
            <fieldset id="languages">
                <div class="checkbox">
                    <label for="languages-1"><input type="checkbox" id="languages-1" name="languages" value="none">None</label>
                </div>
                <div class="checkbox">
                    <label for="languages-2"><input type="checkbox" id="languages-2" name="languages" value="german">German</label>
                </div>
                <div class="checkbox">
                    <label for="languages-3"><input type="checkbox" id="languages-3" name="languages" value="french">French</label>
                </div>
                <div class="checkbox">
                    <label for="languages-4"><input type="checkbox" id="languages-4" name="languages" value="spanish">Spanish</label>
                </div>
                <div class="text">
                   <input class="input-medium" type="text" id="languages-5" name="languages" maxlength="100" placeholder="Other"> <label class="sr-only" for="languages-5">Other:</label>
                </div>
            </fieldset>
        </div>

        <p class="text-center">
        <a name="bottom"></a>
        <button type="sumit" class="demographics btn-default btn" name="submit" value="true">Continue</button>
        </p>
    </div>
</form>

