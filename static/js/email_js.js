// EmailJS API Script from https://dashboard.emailjs.com/admin/integration 

function sendContactEmail(contactForm) {
    console.log("this is working")
    emailjs.sendForm('service_fsjc9yj', 'EventProfSearch', contactForm)
        .then(function (response) {
            console.log('SUCCESS!', response.status, response.text);
        }, function (error) {
            console.log('FAILED...', error);
        });
}