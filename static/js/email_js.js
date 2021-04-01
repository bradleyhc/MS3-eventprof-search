// EmailJS API Script from https://dashboard.emailjs.com/admin/integration 

function sendContactEmail(contactForm) {
var name = {{freelancer.name|safe}}

    console.log("this is working", name)
    /*emailjs.sendForm('service_fsjc9yj', 'EventProfSearch', contactForm)
        .then(function (response) {
            console.log('SUCCESS!', response.status, response.text);
        }, function (error) {
            console.log('FAILED...', error);
        });*/
}