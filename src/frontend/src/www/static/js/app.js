var SUCCESS_CODE = 1;
var FAILURE_CODE = -1;

var numStudentsToMatch = 0
var rangeRelevancyValues = {"0": "Not Used", "1": "Low", "2": "Medium", "3": "High"}

$('document').ready(function() {

    // ------------------------------------------
    // INITIAL POST FOR HOMEPAGE
    // ------------------------------------------

    $.post('/newMatchStep1').done(function(res) {
        $("#content").html(res)
    });

    // ------------------------------------------
    // SIDE MENU EVENT LISTENERS
    // ------------------------------------------

    // set buttons as active upon click
    $(".btn-sidebar").click(function(){
        $(".btn-sidebar").removeClass("btn-sidebar-active");
        $(this).addClass("btn-sidebar-active");
    });

    $("#newmatch-btn").click(function() {
        $.post('/newMatchStep1').done(function(res) {
            $("#content").html(res)
        });
    });

    $("#lastmatch-btn").click(function() {
        $.post('/lastMatch', function(res) {
            $("#content").html(res)
        })
        .done(function() {

            // get all the students from the database
            $.post("/students").done(function(res){

		resJSON = JSON.parse(res)
		if (resJSON.code == SUCCESS_CODE) {
		    students = resJSON.students.data
		    $("#last-match-table").bootstrapTable('load', students)
                    // select the first row on default.
                    $("#last-match-table tr[data-index='0'] td")[0].click()

            // update the progress bar for the faculties at the bottom
            $.post("/facultypercent").done(function(res) {
                var data = JSON.parse(res).percentages.data;
                data.forEach(function(faculty) {
                    faculty_name = faculty.faculty;
                    css_selector = faculty_name.split(" ")[0].toLowerCase();
                    percent = faculty.percent;
                    //console.log(faculty_name, percent, css_selector);
                            $(".progress-bar."+css_selector).css("width", percent+"%");
                            $(".progress-bar."+css_selector).attr("data-original-title", faculty_name + " (" + Math.floor(percent) + "%)");
                });
            });

        		} else {
        			console.log(resJSON.message);
        			console.log(resJSON.exception);
        		}
            })
            .done(function () {

                // get all checked rows
                $("#test-btn").click(function () {
                    console.log(JSON.stringify($("#last-match-table").bootstrapTable('getSelections')));
                    $("#last-match-table").bootstrapTable('uncheckAll').find("tr").removeClass('selected');
                })

                // row click listener
                var months = ["Sept", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
                $("#last-match-table").on('click-row.bs.table', function(e, row, trElem) {

                    // create randomly generated line graph for tracked engagement
                    $("#content #engagement-chart-wrapper").html("<canvas id=\"engagement-chart\"></canvas>")
                    var ctx = $("#content").find("#engagement-chart")
                    var myChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: months,
                            datasets: [{
                                data: getRandomArr(months.length, 0, 6),
                                label: "Group",
                                borderColor: "#3e95cd",
                                fill: false,
                                borderWidth: 2,
                                pointBorderWidth: 2,
                                pointRadius: 2
                            }, {
                                data: getRandomArr(months.length, 0, 6),
                                label: "Faculty",
                                borderColor: "#c45850",
                                fill: false,
                                borderWidth: 2,
                                pointBorderWidth: 2,
                                pointRadius: 2
                            }]
                        },
                        options: { layout: { padding: { left: 0, right: 0, top: -9, bottom: -5 }},
                                    title: { display: false, text: 'Mentor & Mentee Engagement' },
                                    scales: { yAxes: [{ scaleLabel: { display: false,
                                                                        labelString: 'Engagement' }}],
                                            xAxes: [{ scaleLabel: { display: false,
                                                                    labelString: 'Month' }}]},
                                    tooltips: { enabled: false },
                                    legend: { display: true, labels: { boxWidth: 15}},
                                    responsive: true,
                                    maintainAspectRatio: false }
                    });

                    // get group for the selected student
        			$.ajax({
        				type: "POST",
        				url: "/get_group",
        				data: JSON.stringify({"student_id": row.student_id}),
        				contentType: 'application/json; charset=utf-8',
        				success: function(res) {
        					resData = JSON.parse(res);
        					console.log(resData.group.data);
                            numMentees = resData.group.data.length - 1; // subtract the mentor

                            // reset the content for the different tables
                            $(".mentors-table").empty();
                            $(".mentees-table").empty();
                            $(".faculty-table").empty();

                			// update faculty name for this group
                			var facultyName = resData.group.data[0]["faculty"]
                			$(".faculty-table").append("<tr><td colspan=\"3\">" + facultyName + "</td></tr>");

                			// update number of mentees in the current group
                			$("div.current-group div.group-mentor table.group-table thead#mentees-header p.mentees-num").html("(" + numMentees + ")")

                            for (i = 0; i < resData.group.data.length; ++i) {

                                current_data = resData.group.data[i];

                                student_id = current_data["student_id"];
                                first_name = current_data["name"];
                                last_name = current_data["surname"];
                                class_n = "";

    				            // highlight the student clicked
                                if (row.student_id == student_id) { class_n += "highlight-row"; }

                                line = "<tr class=\""+class_n+"\"><td>"+student_id+"</td><td>"+first_name+"</td><td>"+last_name+"</td></tr>";

                                if (current_data["is_mentor"]) { $(".mentors-table").append(line); } // add mentor to the table
    				            else { $(".mentees-table").append(line); } // add mentees to the table
                            }

                            $(".current-group").show();
        				}
        			});

                    // highlight selected row
                    $('.row-selected').removeClass('row-selected');
                    $(trElem).addClass('row-selected');
                });

                // remove row background setting on checkbox checked
                $("#last-match-table").on('check.bs.table', function(e, row, trElem) {
                    $(this).find("tr").removeClass('selected')
                });

                // remove row background setting on checkbox unchecked
                $("#last-match-table").on('uncheck.bs.table	', function(e, row, trElem) {
                    $(this).find("tr").removeClass('selected')
                });

                // add functionality to Faculty participation distribution bar
                var templateString = "<div class=\"tooltip\" role=\"tooltip\"><div class=\"arrow\"></div><div style=\"font-size:0.8em\" class=\"tooltip-inner\"></div></div>"
                $('[data-toggle="tooltip"]').tooltip({placement: "bottom", template: templateString})

                // add three-dot menu to table
                var menuElem = "<div class=\"dropdown\">" +
    				"<img id=\"three-dot-menu-btn\" class=\"float-right\" src=\"../static/img/three-dot-menu.png\" style=\"height: 28px; padding: 5px 5px 5px 10px; cursor: pointer;\">" +
    				"<div class=\"dropdown-content\">" +
    					"<ul>" +
    						"<li class=\"dropdown-list-el\" id=\"dropdown-email-btn\"><p>E-mail group</p</li>" +
    						"<li class=\"dropdown-list-el\" id=\"dropdown-manual-assignation-btn\"><p>Manual Assignation</p></li>" +
    					"</ul>" +
    				"</div>" +
    			"</div>";
                $("#content").find("div#table-wrapper").find("div.left-panel").prepend(menuElem);
        		$("#three-dot-menu-btn").click(function() {
        			console.log("menu clicked!");
        			$(".dropdown-content").toggle()
        		});
            });
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

			// ------------------------------------------
    			// NEW MATCH - STEP 2
    			// ------------------------------------------
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

	// hide button elements
	$("#checkmark-icon").css("display","none")
	$("#loading-icon").css("display","inline-block")
	$("#step2-buttons").css("display", "none");
	$("#match-success-msg n").html("");
	$("#match-success-msg").css("display", "none");

	// scroll to the top of the page
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
                // $("#step2-edit-matches").attr('disabled','disabled').addClass("mmm-btn-disabled");
		$("#step2-edit-matches").click(function() {
			 $("#lastmatch-btn").click();
		});

                // re-enable matching button (clicking it again causes issues... will leave it disabled for now)
                // $("#match-btn a").removeAttr("href")
		$("#match-btn").removeClass("mmm-btn-disabled").removeAttr("disabled")
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
function getRandomArr(n, min, max) {
    var a = []
    for (var i = 0; i < n; i++) {
        var randomNum = Math.random() * (max - min) + min;
        a.push(randomNum)
    }
    return a;
}

function rowStyle(row, index) {
    if (row.is_mentor == true) {
        return {
            css: {"background-color": "#F0F0F0"}
        };
    }
    return {};
}
