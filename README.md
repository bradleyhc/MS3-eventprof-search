# EventProf Search

## About this site

The purpose of the EventProf Search site is for Freelancers in the Events Industry to find open Event Projects and for Project Owners, to find suitable Freelancers.

## Contents

lorem

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

#### Typography
sss

#### Imagery
ddi

#### Colour
ddd

### Wireframes
zz

### Data Schema
zz

---

## Features
sssssss
- Send email message to another user via Flask-mail

### Features to add in future releases
ssssss 

---

## Technologies Used

---

## Testing

### Code Validation

### User Story Testing

### Defensive Programming
- Email validation

### Security
- Hash passwords
- Emails not shown in DOM - all managed in back-end via Python / Flask-mail

### Access Restrictions


### Bugs
- Logged out users shown variable error - can't find session dict


## Deployment

### Setting up the Flask App
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

### Other
- Random name generator for users - https://www.behindthename.com/ 