$(document).ready(function() {
    console.log("DOM Ready!")

    //test();
    initButtons();
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
            console.log('RETURNED DATA: \n' + data);
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
