$(".checked").prop('checked', true);

/* uncheck radiobuttons if a user enters text into the text input field */
$('input[type=text]').click(function() {
    /* fields with multiple values are checkboxes so they won't be unselected by this */
    $('input[type=radio][name="' + $(this).attr("name").replace(/"/g, '\\"') + '"]').removeAttr("checked").prop('checked', false);

});

/* clear text input field if a user checks a radio button */
$('input[type=radio]').change(function() {
    /* fields with multiple values are checkboxes so they won't be unselected by this */
    $('input[type=text][name="' + $(this).attr("name").replace(/"/g, '\\"') + '"]').val("");

});

/* do not send post twice! */
$("#demographics").submit(function(event) {
    event.preventDefault();
});

$(":button.demographics").on("click", function() {
    result = $('form.demographics').serializeArray();
    //console.log(result);
    $.when(
        $.ajax({
            url: demographics_complete_url,
            type: "POST",
            data: JSON.stringify(result),
            contentType: "application/json",
            dataType: "json",
        })
    ).then(function(data, textStatus, jqXHR) {
        if (textStatus == "success") {
            if (data.status === false) {
                // show the error
                alert(data.message);
            } else if (data.status === true) {
                window.location.replace(last_url);
            }
        }
    });
});
