$(":button.task").on("click", function() {

    if (typeof sentence_start !== 'undefined') {
        sentence_end = performance.now();
        sentence_rt = sentence_end - sentence_start;
    } else {
        /* this might not be the best solution but the rt is supposed to never be 0 */
        sentence_rt = 0;
    }
    //console.log(sentence_rt);
    var result = {};
    result.value = $('input[name=answer]:checked', '.scale').val();
    result.sentence_rt = sentence_rt;
    result.situation_rt = situation_rt;
    $.when(
        $.ajax({
            url: task_url,
            type: "POST",
            data: JSON.stringify(result),
            contentType: "application/json",
            dataType: "json",
        })
    ).then(function(data, textStatus, jqXHR) {
        //console.log("post");
        //console.log(jqXHR.status); // Alerts 200
        //console.log(textStatus);
        //console.log(data);
        //console.log("---");
        if (textStatus == "success") {
            if (data.status === null) {
                alert(data.message);
            } else if (data.status === false) {
                alert(data.message);
            } else {
                getTask();
            }
        }
    });
});

$(":button.sentence").on("click", function() {
    /* this might not be the best solution but the rt is supposed to never be 0 */
    if (typeof situation_start !== 'undefined') {
        situation_end = performance.now();
        situation_rt = situation_end - situation_start;
    } else {
        situation_rt = 0;
    }

    //console.log(situation_rt);
    $(".is_visible").hide();
    $(".is_hidden").show();
    sentence_start = performance.now();
});

function getTask() {
    $.when(
        $.ajax({
            url: task_url,
            type: "GET",
            data: JSON.stringify($(".answer")),
            contentType: "application/json",
            dataType: "json",
        })
    ).then(function(data, textStatus, jqXHR) {
        //console.log("get");
        //console.log(jqXHR.status); // Alerts 200
        //console.log(textStatus);
        //console.log(data);
        //console.log("---");
        if (textStatus == "success") {
            if (data.status === false) {
                // show the error
                alert(data.message);
                //$("div.situation").html('An error occurred!');
                //$("div.sentence").html('An error occurred!');
            } else if (data.status === true) {
                // update progress bar
                //console.log(data['complete']);
                $(".progress-bar").css('width', data.complete + '%');
                $(".progress-bar").html(data.complete + '%');
                //console.log("Hiding");
                if ($('div.situation').length === 0) {
                    //console.log("empty situation");
                    $(".is_hidden").show();
                    $(".is_visible").hide();
                    situation_rt = 0;
                    sentence_start = performance.now();
                } else {
                    //console.log("non empty situation");
                    $(".is_hidden").hide();
                    $(".is_visible").show();
                }
                $(".uncheck").prop('checked', false);
                /* situation and sentence can contain newlines */
                $("div.situation").html(data.data.situation.replace(/(?:\r\n|\r|\n)/g, '<br/>'));
                $("div.sentence").html(data.data.sentence.replace(/(?:\r\n|\r|\n)/g, '<br/>'));
                situation_start = performance.now();
            } else if (data.status === null) {
                window.location.replace(demographics_url);
            }
        }
    });
}

$( document ).ready(function() {
    //console.log("getting task");
    getTask();
});
