// Initialize Materialize components
$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $('.modal').modal();
    $('select').formSelect();
    $('.datepicker').datepicker();
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


validateDropdown();
function validateDropdown() {
    let role = $('#role_dropdown > div > .dropdown-trigger').val()
    let skill = $('#skills_dropdown > div > .dropdown-trigger').val()
    $("#update_profile_button_init").click(function () {
        if (role == ("Choose your role" || "Select required role")) {
            $('#helper_error_role').removeClass("hide");
            $('#update_profile_button_init').removeClass("modal-trigger")
        }
        if (skill == ("Select your skills" || "Select required skills")) {
            $('#helper_error_skill').removeClass("hide");
            $('#update_profile_button_init').removeClass("modal-trigger")
        }
        else {
            $('#update_profile_button_init').addClass("modal-trigger")
        }
    })
}