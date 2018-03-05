var SUCCESS_CODE = 1;
var FAILURE_CODE = -1;

var numStudentsToMatch = 0

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

    // set buttons as active upon click
    $(".btn-sidebar").click(function(){
        $(".btn-sidebar").removeClass("btn-sidebar-active");
        $(this).addClass("btn-sidebar-active");
    })

    $("#home-btn").click(function() {
        $.post('/home').done(function(res) {
            $("#content").html(res)
        });
    });

    $("#newmatch-btn").click(function() {
        $.post('/newMatchStep1').done(function(res) {
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

    $("#content").on('change', '#mentor-file-input', function () {
        $("#mentor-filename").html(this.files[0].name)
    });

    $("#content").on('change', '#student-file-input', function () {

        // TODO: Fix bug where an error is outputed if the upload is clicked again after the initial submission
        $("#student-filename").html(this.files[0].name)
    });

    $("#content").on('submit', '#file-upload-form', function (e) {
        e.preventDefault();

        console.log("Submitting form...");

        var formData = new FormData(this);

        $.ajax({
            url: "/upload",
            type: 'POST',
            data: formData,
            success: function (res) {

                resData = JSON.parse(res)

                if (resData.code == SUCCESS_CODE) {

                    console.log(resData.message)
                    numStudentsToMatch = resData.numStudents

                    // load step 2
                    $.post('/newMatchStep2').done(function(innerRes) {

                        innerResData = JSON.parse(innerRes)

                        // load main content for step 2
                        $("#content").html(innerResData.html)

                        // hide some contents
                        $("#step2-right-wrapper").css("display", "none");
                        $("#step2-buttons").css("display", "none");
                        $("#match-success-msg").css("display", "none");

                        // load questions' table
                        $("#questions-table-wrapper").append(innerResData.htmltable)
                    });

                } else {
                    // display error message.
                    $("#step1-errmsg").html(resData.message)
                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });

    // ------------------------------------------
    // NEW MATCH - STEP 2
    // ------------------------------------------

    $("#content").on('click', '#match-btn', function () {

        // disable matching button
        $("#match-btn").attr('disabled','disabled').css("background", "rgb(226, 226, 226)").css("cursor", "default");

        // display loading message
        $("#step2-right-wrapper").css("display", "inline-block");
        $("#match-loading-msg n").html(numStudentsToMatch)

        $.post("/match", function(res) {

            resData = JSON.parse(res)

            // update ui upon match completion
            $("#match-success-msg").css("display", "block");
            $("#match-success-msg n").html(resData.numGroups);
            $("#step2-buttons").css("display", "block");
            $("#loading-icon").toggle()
            $("#checkmark-icon").toggle()

            // re-enable matching button (clicking it again causes issues... will leave it disabled for now)
            // $("#match-btn").removeAttr('disabled').css("background", "rgb(100,216,226)").css("cursor", "pointer");

        });
    });

    $("#content").on('click', '#step2-download-btn', function() {

        console.log('Download clicked!')

        $.get("/download", function () {

        })
    });
});
