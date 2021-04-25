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
    $('textarea').characterCounter();
    // set timeout for flash if not closed by user
    setTimeout(function () {
        $("div.flash-msg").fadeOut();
    }, 5000);
    $(".preloader-overlay").delay(300).fadeOut();
});

// Edit profile image - preview image on input change
$('#profile_img').on('input', function () {
    value = this.value
    if (value == "") {
        $(".profile-image").attr("src", "../static/images/user_uploads/default_avatar.png");
    } else {
        $(".profile-image").attr("src", value);   
    }
});


// Add class 'wide' on horizontal images to fill wrapper
function resizeImage(img) {
    img_h = $(img).height();
    img_wrap_h = $(".profile-img-wrapper").height();
    img_card_wrap_h = $(".card-img-wrapper").height();
    if (img_h < img_wrap_h || img_h < img_card_wrap_h) {
        $(img).addClass('wide');
    } else {
        $(img).removeClass('wide');
    }
    console.log(img_h, img_wrap_h, img_card_wrap_h)
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

/*
$('.add-skill-input').change(function () {
    $(this).closest('form').submit()
})*/


// Provide user with additional form inputs when 'plus' button clicked in Admin 'skills' page
$('#add_input_skill').click(function () {
    var prevInput = $('#empty_skill_inputs .add-skill-input:last-of-type');
    if (prevInput.val() == "") {
        prevInput.addClass('input-missing-error');
        $('#empty_skill_inputs').append(
            '<span class="helper-text-error abs-bottom" id="error_msg">Please enter a skill to add another!</span>'
        )
        console.log("this one",prevInput)
    } else {
        prevInput.removeClass('input-missing-error')
        console.log("remove me")
        $('span#error_msg').remove();
        $('#empty_skill_inputs').append(
            '<input type="text" name="add_skill[]" class="add-skill-input"></input>'
        )
        // Credit to Y. Joy Ch. Singha -  https://stackoverflow.com/questions/19012495/smooth-scroll-to-div-id-jquery
        $('html, body').animate({
            scrollTop: $('#add_input_skill').offset().top
        }, 'slow');
    }
});

// Provide user with additional form inputs when 'plus' button clicked in Admin 'roles' page
$('#add_input_role').click(function () {
    var prevInput = $('#empty_role_inputs .add-skill-input:last-of-type');
    if (prevInput.val() == "") {
        prevInput.addClass('input-missing-error');
        $('#empty_role_inputs').append(
            '<span class="helper-text-error abs-bottom" id="error_msg">Please enter a role to add another!</span>'
        )
    } else {
        prevInput.removeClass('input-missing-error')
        $('span#error_msg').remove();
        $('#empty_role_inputs').append(
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
    } else {
        $('nav').removeClass("scrolled")
    }
});

// Flexbox cards - last in row handler 
(function () {
    parent_width = $('.flex-grid-thirds').width()
    child_width = $('.freelancer-card:last-of-type').width()
    if (child_width > (parent_width / 2) && parent_width > 520) {
        $('.freelancer-card:last-of-type').addClass('last-in-grid');
    } else {
        $('.freelancer-card:last-of-type').removeClass('last-in-grid')
    }
})();