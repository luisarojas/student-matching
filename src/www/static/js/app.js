$(document).ready(function() {
    console.log("DOM Ready!")

    test();
    initButtons();
});

function initButtons(){

}

function test(){
    $.get(
        '/test'
    ).done(function(res) {
        console.log(res);
    });
}
