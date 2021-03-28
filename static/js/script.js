// Initialize Materialize components
$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $('.modal').modal();
    $('select').formSelect();
    // Hide flash messages on button click
    $("button.close-flash").click(function () {
        $("div.flash-msg").fadeOut();
    })
});

// Preview profile image before upload without page reload
// CREDITS: https://www.tutorialrepublic.com/faq/how-to-preview-an-image-before-it-is-uploaded-using-jquery.php
function previewImg() {
    let file = $("#profile_img").get(0).files[0];

    if (file) {
        let readFile = new FileReader()
        readFile.onload = function () {
            $(".profile-image").attr("src", readFile.result);
        }
        readFile.readAsDataURL(file);
    }

}