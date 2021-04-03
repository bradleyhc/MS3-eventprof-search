// Initialize Materialize components
$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $('.modal').modal();
    $('select').formSelect();
    $('.datepicker').datepicker();
    // Hide flash messages on button click
    $("button.close-flash").click(function () {
        $("div.flash-msg").fadeOut();
    });
    $('.tabs').tabs();
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


// Submit form on change of input -Rory McCrossan https://stackoverflow.com/questions/38738034/submit-form-on-change-of-input-field 
$('.admin-hide-switch').change(function () {
    $(this).closest('.hide-user-form').submit()
})

$('.add-skill-input').change(function () {
    $(this).closest('form').submit()
})

$('#add_input_skill').click(function () {
    var prevInput = $('#empty_skill_inputs .add-skill-input:last-of-type');
    console.log("here",prevInput.val())
    if (prevInput.val() == "") {
        prevInput.addClass('input-missing-error')
    } else {
        prevInput.removeClass('input-missing-error')
        $('#empty_skill_inputs').append(
            '<input type="text" name="add_skill[]" class="add-skill-input"></input>'
        )
        // Credit to Y. Joy Ch. Singha -  https://stackoverflow.com/questions/19012495/smooth-scroll-to-div-id-jquery
        $('html, body').animate({
            scrollTop: $('#add_input_skill').offset().top
        }, 'slow');
    }
});

// Credits: https://api.jquery.com/jquery.getjson/ 
$.getJSON('../static/js/homepage_img.json', function(data){
    $.each(data, function (key, val) {
        let item = data[key]
        $('#hp_user_images').append(
            `<div class="hp-user-img">
                    <img src="./static/images/brand/${item.image}"
                        alt="Homepage user image five">
                        <div class="hp-user-img-overlay">
                            <p><span class="p-feat">${item.name}</span><br>${item.role}</p>
                        </div>
                </div>`
        )
    })   
});

// Add 'scroll' class to navbar on scroll
$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('nav').addClass("scrolled")
        console.log("we be scrolling")
    } else {
        $('nav').removeClass("scrolled")
    }
})