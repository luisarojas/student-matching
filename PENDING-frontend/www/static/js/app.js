$('document').ready(function() {

    // ------------------------------------------
    // INITIAL POST FOR HOMEPAGE
    // ------------------------------------------

    $.post('/home').done(function(res) {
        $("#content").html(res)
    });

    // ------------------------------------------
    // SIDE MENU EVENT LISTENERS
    // ------------------------------------------

    $("#home-btn").click(function() {
        $.post('/home').done(function(res) {
            $("#content").html(res)
        });
    });

    $("#newmatch-btn").click(function() {
        $.post('/newMatch').done(function(res) {
            $("#content").html(res)
        });
    });

    $("#lastmatch-btn").click(function() {
        $.post('/lastMatch').done(function(res) {
            $("#content").html(res)
        });
    });

    $("#mentorlogs-btn").click(function() {
        $.post('/mentorLogs').done(function(res) {
            $("#content").html(res)
        });
    });

    $("#feedback-btn").click(function() {
        $.post('/feedback').done(function(res) {
            $("#content").html(res)
        });
    });

    // ------------------------------------------
    // NEW MATCH - STEP 1
    // ------------------------------------------

    $("#content").on('click', '#upload-mentors-btn', function () {

    });

    $("#content").on('click', '#upload-students-btn', function () {
        console.log('submit students button clicked');
    });

});
