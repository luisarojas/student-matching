$(document).ready(function() {
    console.log("DOM Ready!")

    test()
});

function test(){
    $.get(
        '/test'
    ).done(function(res) {
        console.log(res);
    });
}
