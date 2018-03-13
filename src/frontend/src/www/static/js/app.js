var SUCCESS_CODE = 1;
var FAILURE_CODE = -1;

var numStudentsToMatch = 0
var rangeRelevancyValues = {"0": "Not Used", "1": "Low", "2": "Medium", "3": "High"}

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
        $.post('/lastMatch', function(res) {
            console.log("test1")
            $("#content").html(res)
        })
        .done(function() {

            console.log("test2")

            // not working :(
            // $("#content .bootstrap-table .fixed-table-container").css("padding-bottom", "0 !imporant")
            //                                                     .css("height", "calc(100% - 80px) !important")

            // var imgElem = "<img src=\"assets/three-dot-menu.png\" style=\"height: 28px; width:auto; padding-top:8px;\">"
            // var elem = "<div style=\"margin: 10px 5px 10px 10px;\" class=\"float-right\">" + imgElem + "</div>"
            // TODO: add three dot menu
            // $("#content .fixed-table-toolbar").prepend(elem)

            // var labels = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
            // new Chart($("#myChart"), {
            //     type: 'line',
            //     data: {
            //             labels: labels,
            //             datasets: [{
            //                             data: getRandomArr(labels.length, 0, 5),
            //                             label: "Group",
            //                             borderColor: "#3e95cd",
            //                             fill: false
            //                         }, {
            //                             data: getRandomArr(labels.length, 0, 5),
            //                             label: "Faculty",
            //                             borderColor: "#8e5ea2",
            //                             fill: false
            //                         }
            //                     ]
            //         },
            //             options: {
            //                 title: {
            //                     display: true,
            //                     text: "Mentor-Mentee Engagement"
            //                 }
            //             }
            // });
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
        if (typeof this.files[0] == "undefined") {
            $("#mentor-filename").html("No file selected.").css("color", "red").css("font-family", "'Poppins', sans-serif")
        } else {
            $("#mentor-filename").html(this.files[0].name).css("color", "black").css("font-family", "'Inconsolata', monospace")
        }
    });

    $("#content").on('change', '#student-file-input', function () {

        if (typeof this.files[0] == "undefined") {
            $("#student-filename").html("No file selected.").css("color", "red").css("font-family", "'Poppins', sans-serif")
        } else {
            $("#student-filename").html(this.files[0].name).css("color", "black").css("font-family", "'Inconsolata', monospace")
        }
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
                        $("#questions-table-wrapper").append(innerResData.htmltable);

                        $("#questions-table tr").each(function () {

                                var currVal = $(this).find("input[type=range]").val()
                                $(this).find("label").text(rangeRelevancyValues[currVal])

                                $(this).find("input[type=range]").on('input change', function () {

                                    var selectedVal = this.value
                                    $(this).parent().find("label").text(rangeRelevancyValues[selectedVal])

                                    if (selectedVal == 0) {
                                        $(this).parent().find("label").css("color","lightgrey");
                                    } else if (selectedVal == 1) {
                                        $(this).parent().find("label").css("color","forestgreen");
                                    } else if (selectedVal == 2) {
                                        $(this).parent().find("label").css("color","goldenrod");
                                    } else if (selectedVal == 3) {
                                        $(this).parent().find("label").css("color","red");
                                    }
                                })
                        })
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

    // "match" button is clicked
    $("#content").on('click', '#match-btn', function () {

        $('html, body').animate({scrollTop: $("#step2-title").offset().top}, 0);

        // disable matching button
        $("#match-btn").attr('disabled','disabled').addClass("mmm-btn-disabled")

        // display loading message
        $("#step2-right-wrapper").css("display", "inline-block");
        $("#match-loading-msg n").html(numStudentsToMatch)

        // store table information in a json object
        var questionWeights = {'questions': []};
        $("#questions-table tbody tr").each(function() {
            var questionHeader = $(this).find("td.qheader").html();
            var questionWeight = $(this).find("input[type=range]").val()
            questionWeights.questions.push({'header': questionHeader, 'weight': questionWeight});
        });

        $.ajax({
            type: 'POST',
            url: "/match",
            data: JSON.stringify(questionWeights),
            contentType: 'application/json; charset=utf-8',
            success: function (res) {
                resData = JSON.parse(res)

                // update ui upon match completion
                $("#match-success-msg").css("display", "block");
                $("#match-success-msg n").html(resData.numGroups);
                $("#step2-buttons").css("display", "block");
                $("#loading-icon").toggle()
                $("#checkmark-icon").toggle()

                // buttons temporarily disabled - functionality not available yet
                $("#step2-email-mentors").attr('disabled','disabled').addClass("mmm-btn-disabled");
                $("#step2-edit-matches").attr('disabled','disabled').addClass("mmm-btn-disabled");

                $("#match-btn a").removeAttr("href")

                // re-enable matching button (clicking it again causes issues... will leave it disabled for now)
                // $("#match-btn").removeAttr('disabled').css("background", "rgb(100,216,226)").css("cursor", "pointer");
            }
        });
    });

    $("#content").on('click', '#step2-download-btn', function() {
        $.get("/download");
    });

});

/**
 * Returns a random number between min (inclusive) and max (exclusive)
 */
// function getRandomArr(n, min, max) {
//     var a = []
//     for (var i = 0; i < n, i++) {
//         var randomNum = Math.random() * (max - min) + min;
//         a.push(randomNum)
//     }
//     return a;
// }