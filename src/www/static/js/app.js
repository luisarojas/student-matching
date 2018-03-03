var SUCCESS_CODE = 1;
var FAILURE_CODE = -1;

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

                res_data = JSON.parse(res)

                if (res_data.code == SUCCESS_CODE) {
                    // Load step 2
                    console.log(res_data.message)
                    $("#content").html(res_data.html)
                } else {
                    // Display error message.
                    $("#step1-errmsg").html(res_data.message)
                }

                //Download the file
                // $.get("/download/matched.xlsx");
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
});
