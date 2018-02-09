$(document).ready(function() {
    console.log("DOM Ready!")

    //test();
    initButtons();
    // $.get("/download/matched.xlsx");
    $.post('/gotodownload').done(function(data){
        // console.log(data);
    });
});

function initButtons(){

}

$("form").submit(function(e) {
    console.log("Submitting ...");
    e.preventDefault();

    var formData = new FormData(this);

    $.ajax({
        url: "/uploader",
        type: 'POST',
        data: formData,
        success: function (data) {
            console.log(data);
            
            //Download the file
            $.get("/download/matched.xlsx");
        },
        cache: false,
        contentType: false,
        processData: false
    });
});

function test(){
    $.get(
        '/test'
    ).done(function(res) {
        console.log(res);
    });
}
