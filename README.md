# EventProf Search

## About this site

The purpose of the EventProf Search site is for Freelancers in the Events Industry to find open Event Projects and for Project Owners, to find suitable Freelancers.

Users can contact each other as required via email message from within the site if they would like to discuss a role further.

___

## Contents

lorem

___

## User Experience (UX)
### User Stories
- Event Freelancer
    - As an Event Freelancer, I want to be able find suitable event projects that are looking for my skillset.
    - I want to be able to search the listings for projects openings at a specific location, or with keywords specific to my requirements i.e 'Producer'.
    - When I have found a suitable project, I want to be able to contact the owner of that project to inform them of my interest.
    - As the site allows for personalised profiles, I want the ability to update this information if necessary and publicly show this information to other users.

- Event Project Owner
    - As a Project Owner, I want to quickly find suitable Freelancers that could fill the position I have available.
    - I want the ability to check if Freelancers have the necessary skills for my project, without needing to read each profile bio.
    - If a suitable Freelancer is found, I want to be able to contact them easily to request more information from them. 
    - As a Project Owner, I want the ability to add further projects to the website, and edit those previously created.

- Event Recruiter
    - As a recruiter, I want to be able to find suitable candidates for contract projects based on a set list of skills and criteria. 
    - Since my knowledge of the specific project or role will be limited, I need to be able to quickly shortlist users based on easily identifiable skills.

- Site Admin
    - As a Site Admin, I want to be able to hide visibility of users on the freelancer listing page, if requested.
    - I want to have the ability to create new Skills and Roles for users to select when creating their profiles. 

### Design
The site design is simplistic in nature. To keep the user engaged, the UI is clean and not overly busy or complex, ensuring that the bold colour and call-to-action areas are easy to read and identify. 

EventProf Search uses a contemporary design with regards to UI buttons, cards, backgrounds and the colour scheme, which users expect with modern day sites focusing on social interaction.

#### Typography
The sans-serif font 'Lexend' has been selected for this site, as it helps to contribute to the clean, contemporary feel of the site, with sharp, easy to read characters. The font can be found at Google Fonts [here](https://fonts.google.com/specimen/Lexend).

#### Imagery
Similarly to the typography, the imagery used on this site is minimilistic, with only a single background image on the homepage, and then used throughout the page headers for continuity. 

Since the majority of the imagery will be user generated, site imagery is not required to improve the user experience. Instead the background chosed compliments the colour scheme of the site and ensure consistency between pages.

#### Colour
A vibrant, but slightly pastelled colour scheme has been selected for EventProf Search. Users are familiar with blue colour patterns from other popular social-based sites such as Facebook, Twitter and LinkedIn. As [CoSchedule](https://coschedule.com/blog/color-psychology-marketing#primary) suggest, blue is often associated with 'trust' or 'dependability'.

To compliment the blue shades, a brighter Teal and Pink colour have been used to help accent various features on the site and help them stand out, for example, under headers, the navbar, or call-to-action buttons.

### Wireframes
>TO BE UPDATED

### Data Schema
>TO BE UPDATED

---

## Features
### Sitewide
- User login and account creation.
- User profile type selection - freelancer or employer.
- User profile image (via URL) and information can be added and updated.
- Employer user type can add a project directly from the navbar.
- Project owners can see latest freelancers on their own profile via the sidebar widget. 
- Sidebar widget on freelancer / project page shows alternative recommendations based on 'role' of the current listing.

### Homepage
- Freelancer search functionality prominent on homepage.
- Latest projects are shown at the end of the page, prompting users to click-through.

### Freelancer listing page
- All freelancers that have completed profile information are shown in the listing.
- Users can search for freelancers based on location, name, skills or bio.
- Users can click to view more about the freelancer, or send an email.

### Project pages
- Projects can be searched using the search function at the top of the page.
- Projects show the location, type, dates and skills the project owner is looking for.
- All projects have individual page that can be viewed by clicking 'view more'.
- Project owners can edit or delete existing submissions by navigating to the project page.
- Freelancers can send project owners an email by clicking 'Email Project Owner' on the project page.

### Admin controls
- Admin users can switch user visibility on or off in the admin control (this hides the user from the freelancer page). 
- Admin users can add or delete roles or skills in the admin control.

### Features to add in future releases
- LinkedIn integration to pull API data into profile.
- Realtime chat between users using either Ajax or Web Socket.
- Social sharing of projects. 
- User connections, allowing users to 'refer a friend' for projects.

---

## Technologies Used

### Frontend languages & frameworks
- HTML5 - vanilla HTML for templates.
- Javascript - minimal vanilla Javascript alongside JQuery to allow for modals, input manipulation and validation. 
- Jquery
- CSS 
- Materialize - primary CSS & JS library for inputs and modals.
- Bootstrap - minimal as required where Materialize classes insufficient.

### Backend tools, languages & frameworks
- Python - primary backend language.
- Flask - used in conjunction with PyMongo and Flask-mail to create connection with database and mail server.
- Jinja2 - used for frontend templating using Flask connection.
- MongoDB - non-relational database used to store user and project data.
- Cloudinary - media storage for demo user profile images.

### Other
- Name Generator - for generating randomised names for demo users.

---

## Testing

### Code Validation
> To be added

### User Story Testing
The site has been tested against the initial user stories to ensure that it meets the minimum requirements of its users. Details of how the site fulfills these tests are outlined below:

#### Event Freelancer
- As an Event Freelancer, I want to be able find suitable event projects that are looking for my skillset.
    - Freelancers can view the skillset required for projects both on the project card and under the header on the 'view project' page.
    > insert s.shot
- I want to be able to search the listings for projects openings at a specific location, or with keywords specific to my requirements i.e 'Producer'.
    - Freelancers can use the searchbar at the top of the project listing page to search for their specific requirements.
    - If the search returns no results, then users can click the call-to-action button or 'clear' at the searchbar to view all projects.
- When I have found a suitable project, I want to be able to contact the owner of that project to inform them of my interest.
    - Users can send an email to the project owner when viewing the project page, by clicking the 'Email Project Owner' button. 
    - When this CTA button is clicked, a modal popup will appear prompting the user to input the message. 
    - The user has the opportunity to change their email in the 'Your Email' input field.
    - To send the message, the user must agree to provide their email to the recipient.
- As the site allows for personalised profiles, I want the ability to update this information if necessary and publicly show this information to other users.
    - Users must complete their profile upon initial registration before it will be shown to other users.
    - Once created, users can update their name, rate, location, role, skills and bio in the 'edit profile' page.
    - All freelancers, unless hidden by an Admin, will be visible to other users.

#### Event Project Owner & Event Recruiter
- As a Project Owner, I want to quickly find suitable Freelancers that could fill the position I have available.
    - Project owners can search for freelancers by name, location, skills or bio, on the 'freelancers' page.
    - If the search returns matching results, these users will be shown on the page, otherwise a 'no results' card is returned prompting the user to try another search.
    - If the user is currently on a 'Project View' page, then the sidebar widget will show up to three freelancers where the 'freelancer role' and the 'project role' are matched. 
- I want the ability to check if Freelancers have the necessary skills for my project, without needing to read each profile bio.
    - Users can quickly identify a freelancer's key skills by looking at the skill tags on each profile card on the 'freelancers' page.
    - The above functionality also satisfies the event recruiter's need to identify skills against a prepared set of criteria.
- If a suitable Freelancer is found, I want to be able to contact them easily to request more information from them. 
    - Users can send an email to freelancers directly from the 'freelancers' listing page, but clicking the 'send email' button on the profile card.
    - Upon clicking this CTA button, a modal form will appear, prompting the user to enter their message, and confirm they agree to provide their email to the recipient.
- As a Project Owner, I want the ability to add further projects to the website, and edit those previously created.
    - A user with the user type 'employer' will be able to add projects using the 'Add Project' link in the navbar.
    - Clicking this link will open the 'add project' form page, where users can input the key details before submitting.
    - Form validation is in place on this form to ensure users are entering sufficient and appropriate data, e.g only alphanumeric characters in text fields and minimum of 5 characters in length. 

#### Site Admin
- As a Site Admin, I want to be able to hide visibility of users on the freelancer listing page, if requested.
    - This can be achieved with the Admin user navigating to the 'admin' dashboard page on the navbar and selecting 'Update User Visibility'. 
    - Once selected, the Admin will see all users of the site, and will be able to switch visibility on or off.
    - If the switch input is switched, the page will refresh and implement the change, confirming that this has been done with a flash message appearing on screen.
- I want to have the ability to create new Skills and Roles for users to select when creating their profiles. 
    - This can be achieved by clicking either 'Update Skill Options' or 'Update Role Options' on the admin dashboard.
    - Once selected, the Admin will be presented with either the list of roles or skills that can be added to, or deleted.
    - To delete a role/skill, the Admin clicks the red 'X' next to the item. 
    - To add a role/skill, the Admin begins typing in the last input of the list and clicks the 'save' button. 
    - To add multiple roles/skills, the Admin clicks the blue '+' button to the right of the final input and clicks the 'save' button. 


### Defensive Programming
> To be added

To ensure the site continues to function when unexpected user input or action occurs, a number of defensive programming meausures have been put in place: 
- User login check - this has been implemented to detect if the current user has a session active. 
    - If there is no session active, Flask will by default return an 'undefined key error' if a page looks for and requires this. 
    - To avoid this, each page route will determine if the session exists. If not, it will redirect the user to the login page, versus return the internal error.
- 404 page
    - This has been implemented using the Python 'errorhandler()' method. If a URL is inputted that returns a 404, the 404 HTML template is rendered, directing users back to the homepage. This response ensures that users experience a page similar to others they are used to, and not deterred from continuing to navigate the site.

- Route / URL manipulation
    - To prevent users from altering the URL string to edit other projects or users, the current session user 'id' must match that of the user / or the project 'submitter_slug' they are trying to edit or delete. If these do not match, the user is directed back to the project listing page, with a flash message notifying them that they must own the project to make edits to it.
    - Similarly, if a user attempts to edit a profile which does not match their session 'slug' then they are directed back to the freelancer listing page and flash message is shown to warn the user that they can only edit their own profile.

- Accidental user error
    - To prevent users inadvertantly overwriting their profile information or project details, an additional modal popup has been created on the 'edit profile' and 'edit project' pages. When a user clicks the 'update' button, a modal appears requiring secondary confirmation.
    - The secondary confirmation will help to avoid accidental user mistakes which will in turn, allow for a better user experience. 

### Security
> To be added
- Hash passwords
- Emails not shown in DOM - all managed in back-end via Python / Flask-mail

### Access Restrictions
> To be added

### Bugs
- Logged out users shown variable error - can't find session dict


## Deployment
> To be added

### Setting up the Flask App
> To be added
- env.py
    - setup the environment variables such as IP, PORT and SECRET KEY for the app to run locally
    - Add env.py to .gitignore file to ensure variables are not published to production site or GitHub repo 

- requirements.txt
    pip freeze --local > requirements.txt



## Credits

### Images

- Avatar image - by <a href="https://pixabay.com/users/janjf93-3084263/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1699635">janjf93</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1699635">Pixabay</a>
- User image homepage - Photo by Joshua Mcknight from Pexels - https://www.pexels.com/photo/woman-sitting-on-a-chair-3290234/
- User image homepage - Photo by Italo Melo from Pexels - https://www.pexels.com/photo/portrait-photo-of-smiling-man-with-his-arms-crossed-standing-in-front-of-white-wall-2379004/
- User image homepage - Image by <a href="https://pixabay.com/users/pexels-2286921/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1868750">Pexels</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1868750">Pixabay</a>
- User image homepage - Image by <a href="https://pixabay.com/users/1866946-1866946/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1252995">Mihai Paraschiv</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1252995">Pixabay</a>

### Guides 

- Flexbox - https://css-tricks.com/dont-overthink-flexbox-grids/
- Submit on change of input for user hidden fields
- Get all values from specific key in PyMongo - https://stackoverflow.com/questions/40282812/get-all-the-values-of-a-particular-key
- Sorting and limited PyMongo - https://stackoverflow.com/questions/4421207/how-to-get-the-last-n-records-in-mongodb 
- Giudance on PyMongo $nin operator - https://stackoverflow.com/questions/18439612/mongodb-find-all-except-from-one-or-two-criteria
- Strip method to remove whitespaces on string - https://www.journaldev.com/23763/python-remove-spaces-from-string#:~:text=Python%20String%20strip()%20function%20will%20remove%20leading%20and%20trailing%20whitespaces.&text=If%20you%20want%20to%20remove,or%20rstrip()%20function%20instead. 
- Commit message descriptions - https://stackabuse.com/git-adding-a-commit-message/ 
- Error Handling - https://www.geeksforgeeks.org/python-404-error-handling-in-flask/ 
- Limit results in Jinja2 - Raju Sarkar https://stackoverflow.com/questions/12368475/jinja2-first-x-items-in-for-if-loop/30053006 

### Other
- Random name generator for users - https://www.behindthename.com/ 