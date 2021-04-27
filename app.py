import os
import random
import datetime
import csv
from flask import (Flask, flash, redirect,
                   render_template, request, url_for, session, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from flask_mail import Mail, Message
from bson import json_util
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


# Set user image upload config
UPLOAD_FOLDER = './static/images/user_uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


# Mail config credits http://pythonbasics.org/flask-mail/
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_DEFAULT_SENDER")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)
mongo = PyMongo(app)


# Global Functions
def check_login():
    flash("You need to be logged in to view that page!")
    return redirect(url_for('login'))


@app.route("/")
@app.route("/home")
def homepage():

    # Get latest 3 projects for the homepage
    projects = mongo.db.projects.find().sort("posted_date").limit(3)
    
    
    return render_template("home.html", projects=projects)


@app.errorhandler(404)
def not_found(err):
    return render_template("404.html")


@app.route("/privacy")
def privacy():

    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Redirect to profile if user logged in
    if not session.get("user") is None:
        return redirect(url_for("profile", name=session['user']['slug']))

    if request.method == "POST":

        # check for existing user email
        user_exists = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()}
        )

        if user_exists:
            flash("User with that email already exists, login instead")
            return redirect(url_for("register"))

        # check if user_type input switched to 'Project Owner'
        u_type_input = request.form.get("user_type")
        user_type = "freelancer" if u_type_input is None else "employer"

        # create full name string for profile page
        full_name = request.form.get(
            "first_name").strip().lower() + "_" + request.form.get(
            "last_name").strip().lower()

        # check if user name slug exists, if yes append incrementing int to end
        name_slug_exists = mongo.db.users.count_documents(
            {"first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name")})

        if name_slug_exists > 0:
            full_name += str(name_slug_exists+1)

        uid = random.randint(9999, 99999)

        register = {
            "first_name": request.form.get("first_name").strip(),
            "last_name": request.form.get("last_name").strip(),
            "name_slug": full_name,
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "user_type": user_type,
            "profile_image": "",
            "is_hidden": True,
            "is_complete": False,
            "is_admin": False,
            "uid": uid
        }

        mongo.db.users.insert_one(register)

        # put user info into session
        session['user'] = {"slug": full_name,
                           "u_type": user_type, "admin": False, "id": uid}
        session['logged_in'] = True
        flash("Registration successful")
        return redirect(url_for("edit_profile", name=full_name))

    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Redirect to profile if user logged in
    if not session.get("user") is None:
        return redirect(url_for("profile", name=session['user']['slug']))

    if request.method == "POST":

        # check if user exists

        if request.form.get("email_lg") is None:
            existing_user = mongo.db.users.find_one(
                {"email": request.form.get("email_lg_page")})
        else:
            existing_user = mongo.db.users.find_one(
                {"email": request.form.get("email_lg")})

        if existing_user:
            if check_password_hash(
                existing_user["password"],
                    request.form.get("password_lg")):
                session["user"] = {
                    "slug": existing_user["name_slug"],
                    "u_type": existing_user["user_type"],
                    "admin": existing_user["is_admin"],
                    "id": existing_user["uid"]}

                # if valid, redirect to profile page
                return redirect(url_for(
                    "profile", name=existing_user["name_slug"]))

            # invalid password
            else:
                flash("Incorrect user details, please try again")
                return redirect(url_for("login"))

        # user does not exist
        else:
            flash("Incorrect user details, please try again")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    print(session)
    flash("You've been successfully logged out!")
    session.pop("user")
    return redirect(url_for('homepage'))


@app.route("/edit_profile/<name>", methods=["GET", "POST"])
def edit_profile(name):

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    # get user slug
    u_slug = session["user"]["slug"]

    # Redirect if user tries to edit another user's profile
    if u_slug != name:
        flash("""Hang on now, that profile isn't yours!
               Edit your own profile by clicking 'My Profile'
               in the navigation bar.""")
        return redirect(url_for('get_freelancers'))

    # get user profile from DB
    profile_data = list(
        mongo.db.users.find({"name_slug": u_slug}))

    u_type_input = request.form.get("user_type")
    user_type = "freelancer" if u_type_input is None else "employer"

    skills = list(mongo.db.skills.find())
    roles = list(mongo.db.roles.find())

    if request.method == "POST":

        # create full name string for profile page
        full_name = request.form.get(
            "first_name").strip().lower() + "_" + request.form.get(
            "last_name").strip().lower()

        # check if user name slug exists, if yes append incrementing int to end
        name_slug_exists = mongo.db.users.count_documents(
            {"first_name": request.form.get("first_name"),
             "last_name": request.form.get("last_name")})

        if name_slug_exists:
            full_name += str(name_slug_exists+1)

        # Update DB with below dict on form submit
        update = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "rate": request.form.get("rate"),
            "location": request.form.get("location"),
            "role": request.form.get("role"),
            "skills": request.form.getlist("skills[]"),
            "profile_image": request.form.get("profile_img"),
            "about": request.form.get("about_textarea"),
            "is_hidden": False,
            "is_complete": True,
            "user_type": user_type,
            "name_slug": full_name
        }

        mongo.db.users.update_one(
            {"name_slug": u_slug}, {"$set": update})

        # Update session slug with new name
        session['user']['slug'] = full_name

        flash("Your profile has been updated!")
        return redirect(url_for(
            "profile", name=full_name))

    return render_template("edit_profile.html", data=profile_data,
                           skills=skills, roles=roles)


@app.route("/profile/<name>", methods=["GET", "POST"])
def profile(name):

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    # get single user profile data
    profile_data = list(
        mongo.db.users.find({"name_slug": name}))

    # get all freelancers and projects for sidebar widget
    all_freelancers = mongo.db.users.find(
        {"user_type": "freelancer", "is_hidden": False,
         "name_slug": {"$nin": [session['user']['slug']]}})
    all_projects = mongo.db.projects.find()

    # get current user email for reply_to
    current_user = mongo.db.users.find_one(
        {"name_slug": session["user"]["slug"]})

    # Redirect to 404 if user data not found
    if not profile_data:
        return not_found('404')

    # Make user edit profile if not yet completed
    elif (profile_data[0]['is_complete'] is False) and (
          profile_data[0] == current_user):
        flash("Please complete your profile before viewing.")
        return redirect(url_for("edit_profile", name=name))

    # Redirect if profile is hidden
    elif (profile_data[0]['is_hidden'] is True) or (
          profile_data[0]['is_complete'] is False):
        flash("This profile is hidden, please select another!")
        return redirect(url_for("get_freelancers"))

    # Redirect if profile is employer account and is not current user
    elif (profile_data[0]['user_type'] == 'employer') and (
          current_user['name_slug'] != name):
        flash("This profile isn't available, please select another!")
        return redirect(url_for("get_freelancers"))

    # Otherwise return profile page
    else:
        return render_template(
            "profile.html", data=profile_data,
            projects=all_projects, s_email=current_user["email"],
            s_name=current_user["first_name"], freelancers=all_freelancers)


""" Project CRUD functions """


@app.route("/add_project", methods=["GET", "POST"])
def add_project():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    skills = list(mongo.db.skills.find())
    roles = list(mongo.db.roles.find())

    if request.method == "POST":

        submitter_slug = session["user"]["id"]
        submitter = mongo.db.users.find_one(
            {"uid": submitter_slug})
        submitter_name = submitter["first_name"] + " " + submitter["last_name"]
        inc_slug = 0
        inc_slug += (mongo.db.projects.count() + 1)
        next_slug = str(inc_slug)

        project = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "role": request.form.get("role"),
            "skills": request.form.getlist("skills[]"),
            "location": request.form.get("location"),
            "posted_date": datetime.datetime.now(),
            "submitter_slug": submitter_slug,
            "submitted_name": submitter_name,
            "slug": str(next_slug)
        }

        mongo.db.projects.insert_one(project)

        flash("Project successfully added!")
        return redirect(url_for("get_projects"))

    return render_template("add_project.html", skills=skills, roles=roles)


@app.route("/opportunities", methods=["GET"])
def get_projects():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    projects = mongo.db.projects.find().sort("posted_date", -1)

    return render_template("all_projects.html", projects=projects)


@app.route("/view_project/<project_id>", methods=["GET", "POST"])
def view_project(project_id):

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    # get single project information
    project_data = list(mongo.db.projects.find({"slug": project_id}))

    # get all freelancers and projects for sidebar widget
    all_freelancers = mongo.db.users.find(
        {"user_type": "freelancer", "is_hidden": False})
    all_projects = mongo.db.projects.find()

    # Get user info for contact email
    user = mongo.db.users.find_one({"name_slug": session['user']['slug']})
    sender_email = user["email"]
    sender_name = user["first_name"]

    return render_template(
        "view_project.html", project_id=project_id, s_email=sender_email,
        s_name=sender_name, data=project_data,
        freelancers=all_freelancers, projects=all_projects)


@app.route("/edit_project/<project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    
    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    # get all skills and roles from DB
    skills = list(mongo.db.skills.find())
    roles = list(mongo.db.roles.find())

    # get existing project data
    project_data = list(mongo.db.projects.find({"slug": project_id}))

    # get user slug
    u_slug = session["user"]["id"]

    # Redirect if user tries to edit another user's profile
    if u_slug != project_data[0]['submitter_slug']:
        flash("""You can only edit your own projects!""")
        return redirect(url_for('get_projects'))

    if request.method == "POST":

        # add form data to dict
        project = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "role": request.form.get("role"),
            "skills": request.form.getlist("skills[]"),
            "location": request.form.get("location"),
            "posted_date": datetime.datetime.now()
        }

        mongo.db.projects.update_one(
            {"slug": project_id}, {"$set": project})

        flash("Your project has been updated!")
        return redirect(url_for(
            "view_project", project_id=project_id))

    return render_template(
        "edit_project.html", project_id=project_id,
        data=project_data, skills=skills, roles=roles)


@app.route("/delete/<project_id>")
def delete_project(project_id):

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    # get user slug
    u_slug = session["user"]["id"]

    project = mongo.db.projects.find_one({"slug": project_id})

    # Redirect if user tries to edit another user's profile
    if u_slug != project['submitter_slug']:
        flash("""You can only edit your own projects!""")
        return redirect(url_for('get_projects'))

    mongo.db.projects.delete_one({"slug": project_id})
    flash("The project was deleted successfully!")
    return redirect(url_for('get_projects'))


""" Freelancer Loop """


@app.route("/freelancers", methods=["GET", "POST"])
def get_freelancers():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    current_user = session["user"]["slug"]

    freelancers = mongo.db.users.find(
        {"user_type": "freelancer", "is_hidden": False, "is_complete": True})

    # get current user for email form data
    user = mongo.db.users.find_one({"name_slug": current_user})
    sender_email = user["email"]
    sender_name = user["first_name"]

    return render_template("all_freelancers.html", freelancers=freelancers,
                           s_email=sender_email, s_name=sender_name)


""" Sidebar widget for similar items """


@app.route("/sidebar_widget", methods=["GET", "POST"])
def sidebar_widget():

    get_freelancers = mongo.db.users.find(
        {"user_type": "freelancer", "is_hidden": False})

    get_projects = mongo.db.projects.find()

    return render_template(
        "similar_widget.html", w_projects=get_projects,
        w_freelancers=get_freelancers)


""" Search & Query handling """


@app.route("/search_freelancers", methods=["GET", "POST"])
def search_freelancers():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    # Create the query string
    query = request.form.get("query")

    # Get exact search match
    freelancers = list(mongo.db.users.find(
                       {"$text": {"$search": f"\"{query}\""},
                        "user_type": "freelancer", "is_hidden": False}))

    # Get partial match if exact not found
    if not freelancers:
        freelancers = list(mongo.db.users.find(
                       {"$text": {"$search": query},
                        "user_type": "freelancer", "is_hidden": False}))

    results = len(freelancers)

    return render_template("all_freelancers.html", freelancers=freelancers,
                           query=query, results=results)


@app.route("/search_projects", methods=["GET", "POST"])
def search_projects():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()

    query = request.form.get("query")

    # Search exact match from query
    projects = list(mongo.db.projects.find(
                    {"$text": {"$search": f"\"{query}\""}}))

    # Else find partial match
    if not projects:
        projects = list(mongo.db.projects.find({"$text": {"$search": query}}))

    results = len(projects)

    return render_template("all_projects.html", projects=projects,
                           query=query, results=results)


@app.route("/send_email/<slug>", methods=["GET", "POST"])
def send_mail(slug):

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    
    uid = int(slug)
    recipient = mongo.db.users.find_one({"uid": uid})
    print(recipient)
    sender = mongo.db.users.find_one({"uid": session['user']['id']})
    to_email = recipient["email"]
    reply_to = sender["email"]
    sender_name = sender["first_name"] + " " + sender["last_name"]
    subject = f"You have a message from {sender_name}"
    user_msg = request.form.get("body")
    body = render_template("contact_email.html",
                           name=sender_name, to_name=recipient['first_name'],
                           message=user_msg)
    msg = Message(subject, reply_to=reply_to,
                  recipients=[to_email])
    msg.html = body

    mail.send(msg)
    flash("You're message has been sent!")
    return redirect(url_for('get_freelancers'))


""" Admin functions """


# Get all users in admin view - default view
@app.route("/admin/users", methods=["GET", "POST"])
def admin_users():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] == False: 
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    users = mongo.db.users.find()

    return render_template("admin/admin_dashboard.html", users=users, uid=None)


# Search all users in admin
@app.route("/admin_search", methods=["GET", "POST"])
def admin_search_freelancers():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] is False:
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    query = request.form.get("query")
    users = list(mongo.db.users.find({"$text": {"$search": query}}))

    return render_template("admin/admin_dashboard.html", users=users, 
                            query=query)


@app.route("/admin/users_update/<uid>", methods=["GET", "POST"])
def admin_update_user(uid):

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] == False: 
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    user = mongo.db.users.find_one({"name_slug": uid})
    all_users = mongo.db.users.find()

    # Check current 'hidden' status of user
    if user["is_hidden"] is True:
        switch = False
    else:
        switch = True

    update = {
        "is_hidden": switch,
    }

    mongo.db.users.update_one({"name_slug": uid}, {"$set": update})

    flash("User updated successfully")
    return redirect(url_for('admin_users'))


# Get all skills & roles in admin view
@app.route("/admin/skills", methods=["GET", "POST"])
def admin_skills():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] == False: 
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    skills = mongo.db.skills.find()

    return render_template("admin/admin_dashboard.html", skills=skills)


# Update skills from admin view
@app.route("/admin/update_skills", methods=["GET", "POST"])
def admin_update_skills():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] == False: 
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    skill_count = mongo.db.skills.count()
    skills = mongo.db.skills.distinct("skill_name")
    submitted_skills = request.form.getlist("add_skill[]")

    if request.method == "POST":
        for skill in submitted_skills:
            skill_exists = mongo.db.skills.find_one({"skill_name": skill})

            if not skill_exists and skill != "":
                mongo.db.skills.insert_one({"skill_name": skill})

    new_skill_count = mongo.db.skills.count()

    if skill_count != new_skill_count:
        flash("Skills updated!")
    else:
        flash("There are no skills to update!")

    return redirect(url_for('admin_skills', _anchor='empty_skill_inputs'))


@app.route("/admin/delete_skill/<id>", methods=["GET", "POST"])
def delete_skill(id):

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] == False:
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    mongo.db.skills.delete_one({"skill_name": id})
    flash("The skill was deleted successfully!")
    return redirect(url_for('admin_skills'))


# Get all roles in admin view
@app.route("/admin/roles", methods=["GET", "POST"])
def admin_roles():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] == False: 
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    roles = mongo.db.roles.find()

    return render_template("admin/admin_dashboard.html", roles=roles)


# Update skills from admin view
@app.route("/admin/update_roles", methods=["GET", "POST"])
def admin_update_roles():

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] == False: 
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    role_count = mongo.db.roles.count()
    #skills = mongo.db.skills.distinct("skill_name")
    submitted_roles = request.form.getlist("add_role[]")

    if request.method == "POST":
        for role in submitted_roles:
            role_exists = mongo.db.roles.find_one({"role_name": role})

            if not role_exists and role != "":
                mongo.db.roles.insert_one({"role_name": role})

    new_role_count = mongo.db.roles.count()

    if role_count != new_role_count:
        flash("Roles updated!")
    else:
        flash("There are no roles to update!")

    return redirect(url_for('admin_roles', _anchor='empty_role_inputs'))


@app.route("/admin/delete_role/<id>", methods=["GET", "POST"])
def delete_role(id):

    # Redirect to login if user not logged in
    if session.get("user") is None:
        return check_login()
    elif session['user']['admin'] == False: 
        flash('You must be an admin to access this page')
        return redirect(url_for('get_freelancers'))

    mongo.db.roles.delete_one({"role_name": id})
    flash("The role was deleted successfully!")
    return redirect(url_for('admin_roles'))





# Debug delete user script
@app.route("/delete_user", methods=["GET", "POST"])
def delete_users():

    delete = ({"skill_name": { '$exists': 1 }})
    delete_also = {"skill_name": "AutoCAD"}
    and_this = {"skill_name": "Adobe Illustrator"}

    mongo.db.users.delete_many(delete)
    return "done", delete


# Import CSV of users credits by 'Perfect'
# in this thread:
# https://stackoverflow.com/questions/27416296/how-to-push-a-csv-data-to-mongodb-using-python/56241768
# encoding guidance: siebz0r https://stackoverflow.com/questions/17912307/u-ufeff-in-python-string/17912811
def view_csv(filename):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        keys = ['first_name', 'last_name', 'email', 'name_slug', 'password', 'user_type', 'about', 'location',
                'profile_image', 'rate', 'role', 'skills', 'is_hidden', 'is_admin', 'is_complete']
        reader = csv.DictReader(f, fieldnames=keys)
        print("this", reader)
        for row in reader:
            print("new row", row)
            mongo.db.users.insert_one(row)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
