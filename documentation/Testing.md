# Testing Documentation

### Contents
- [Lighthouse Testing](#lighthouse-testing)   
- [Browser Compatability](#browser-compatability)
- [Device Compatability](#device-compatability)
- [Accessibility](#accessibility)
- [Defensive Programming](#defensive-programming)
- [Known Bugs](#known-bugs)

___


### Lighthouse Testing
As a benchmark for site performance, the EventProf Search site has had a number of Lighthouse reports performed 
against it, using Chrome Devtools. For the most part, the four key results; Performance, Accessibility, 
Best Practices and SEO scored highly between 90 - 100 for desktop and 50 - 89 for mobile. 

Following a number of reports during testing, the demo user images and homepage image sizes have been scaled down 
to reduce load time.

At this stage, the remainder of improvement areas are predominantly due to the following reasons: 
- Heroku requires a valid SSL certificate to ensure that server requests are completed over HTTPS not HTTP.
- Third party JS and CSS files should be removed or reduced to improve the first contentful paint.

In further releases of this website, the above issues would be addressed, however this would require removing the 
styling codebase from Materialize to either a more lightweight library, or creating a custom library.

You can see the Lighthouse report results below:
#### Homepage (Desktop/Mobile):
<img src="./documentation/screenshots/lh-homepage-desktop.png" alt="lighthouse homepage desktop" width="300">
<img src="./documentation/screenshots/lh-homepage-mobile.png" alt="lighthouse homepage mobile" width="300">
<br>

#### Freelancers Page (Desktop/Mobile):
<img src="./documentation/screenshots/lh-freelancers-desktop.png" alt="lighthouse freelancers desktop" width="300">
<img src="./documentation/screenshots/lh-freelancers-mobile.png" alt="lighthouse freelancers mobile" width="300">
<br>

#### Projects Page (Desktop/Mobile):
<img src="./documentation/screenshots/lh-projects-desktop.png" alt="lighthouse projects desktop" width="300">
<img src="./documentation/screenshots/lh-projects-mobile.png" alt="lighthouse projects mobile" width="300">
<br><br>

### Browser Compatability
The application has been tested across Safari, Chrome and Firefox as the three most popular browsers. After refactoring a 
small number of incompatible styling bugs, the three browsers respond to the application almost identically with regards to style, performance and functionality.  

Whilst the experience remains unimpacted, one bug is evident on Firefox only, whereby the input field does not expand to the full-width of its parent, as it does on Chrome / Safari.

See the screenshots below to demonstrate this: 

#### Chrome

<img src="./documentation/screenshots/browsers/chrome-1.png" alt="chrome 1" width="300">
<img src="./documentation/screenshots/browsers/chrome-2.png" alt="chrome 2" width="300">
<img src="./documentation/screenshots/browsers/chrome-3.png" alt="chrome 3" width="300">

#### Safari

<img src="./documentation/screenshots/browsers/safari-1.png" alt="safari 1" width="300">
<img src="./documentation/screenshots/browsers/safari-2.png" alt="safari 2" width="300">
<img src="./documentation/screenshots/browsers/safari-3.png" alt="safari 3" width="300">

#### Firefox

<img src="./documentation/screenshots/browsers/moz-1.png" alt="moz 1" width="300">
<img src="./documentation/screenshots/browsers/moz-2.png" alt="moz 2" width="300">
<img src="./documentation/screenshots/browsers/moz-3.png" alt="moz 3" width="300">


### Device Compatability
EventProf Search has been tested across device breakpoints within Chrome Devtools, alongside a Samsung S9 and Iphone Xr. 
The application is fully responsive with minimal impact on performance or functionality degradation whichever device is used.

As with browsers, a small number of styling adjustments were required, but the user experience across devices remains equal and unimpacted across devices. 

As an example, see the below screenshots across Desktop, Tablet and Mobile which outline the key differences between cards, 
contact modals and profile or project pages: 

#### Desktop
<img src="./documentation/screenshots/devices/desktop-3.png" alt="desktop device 1" width="300">
<img src="./documentation/screenshots/devices/desktop-2.png" alt="desktop device 2" width="300">
<img src="./documentation/screenshots/devices/desktop-4.png" alt="desktop device 3" width="300">

#### Tablet

<img src="./documentation/screenshots/devices/ipad-2-ls.png" alt="ipad device 1" width="200">
<img src="./documentation/screenshots/devices/ipad-3.png" alt="ipad device 2" width="200">
<img src="./documentation/screenshots/devices/ipad-5.png" alt="ipad device 3" width="200">
<img src="./documentation/screenshots/devices/ipad-1-ls.png" alt="ipad alt device 1" width="300">
<img src="./documentation/screenshots/devices/ipad-2.png" alt="ipad alt device 2" width="300">
<img src="./documentation/screenshots/devices/ipad-5-ls.png" alt="ipad alt device 3" width="300">

#### Mobile

<img src="./documentation/screenshots/devices/mob-1.png" alt="mobile 1" width="200">
<img src="./documentation/screenshots/devices/mob-2.png" alt="mobile 2" width="200">
<img src="./documentation/screenshots/devices/mob-3.png" alt="mobile 3" width="200">
<img src="./documentation/screenshots/devices/mob-4.png" alt="mobile 4" width="200">
<img src="./documentation/screenshots/devices/mob-6.png" alt="mobile 6" width="200">
<img src="./documentation/screenshots/devices/mob-7.png" alt="mobile 7" width="200">

### Accessibility
Since the application is restricted to logged in users only, the [WAVE Evaluation Tool](https://chrome.google.com/webstore/detail/wave-evaluation-tool/jbbplnpkjmmeebjpijfedlgcdilocofh/related)
browser extension has been used to test accessibility. 

A few common errors were identified and rectified sitewide, such as contrast errors, missing aria-labels and incorrect headings levels.

Despite removing many of these errors, the Materialize CSS library introduces a 'missing label' error on any form that has a dropdown. This cause of this is that the input itself is hidden within the HTML dropdown and generated by Javascript, so it is not possible to assign a label when the ID is unknown.
This also produces an 'empty button' error within that element that is not accessible until the page is rendered in the DOM.

To avoid any accessibility issues caused by this, a custom label has been added to these fields, however the WAVE accessibility tool still generates the error. See below for an example of this:

<img src="./documentation/screenshots/testing/aria-2.png" alt="aria error">


### Defensive Programming

To ensure the site continues to function when unexpected user input or action occurs, a number of defensive programming meausures have been put in place: 
- User login check - this has been implemented to detect if the current user has a session active. 
    - If there is no session active, Flask will by default return an 'undefined key error' if a page looks for and requires this. 
    - To avoid this, each page route will determine if the session exists. If not, it will redirect the user to the login page, versus return the internal error.
- 404 page
    - This has been implemented using the Python 'errorhandler()' method. If a URL is inputted that returns a 404, the 404 HTML template is rendered, directing users back to the homepage. This response ensures that users experience a page similar to others they are used to, and not deterred from continuing to navigate the site.

   <img src="./documentation/screenshots/testing/404.png" alt="404 error" width="450">

- Route / URL manipulation
    - To prevent users from altering the URL string to edit other projects or users, the current session user 'id' must match that of the user / or the project 'submitter_slug' they are trying to edit or delete. If these do not match, the user is directed back to the project listing page, with a flash message notifying them that they must own the project to make edits to it.
    - Similarly, if a user attempts to edit a profile which does not match their session 'slug' then they are directed back to the freelancer listing page and flash message is shown to warn the user that they can only edit their own profile.

- Accidental user error
    - To prevent users inadvertantly overwriting their profile information or project details, an additional modal popup has been created on the 'edit profile' and 'edit project' pages. When a user clicks the 'update' button, a modal appears requiring secondary confirmation.
    - The secondary confirmation will help to avoid accidental user mistakes which will in turn, allow for a better user experience. 

    <img src="./documentation/screenshots/testing/confirmation.png" alt="confirmation" width="450">


### Known Bugs
- Firefox input textbox width not responding as per Chrome / Safari - currently width is smaller.
- Where form validation is used on a page that also has a confirmation modal, the validation prompt appears through the modal. This is a browser default response and the intention is to create an alternative validation method in future releases

___

### **[Return to the main README](/README.md)**