import os
import json
import datetime
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
app.config['MAIL_USERNAME'] = 'eventprofsearch@gmail.com'
app.config['MAIL_PASSWORD'] = 'sycej66D!'
app.config['MAIL_DEFAULT_SENDER'] = 'bradleyh.cooney@gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def homepage():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
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
            "first_name").lower() + "_" + request.form.get("last_name").lower()

        # check if user name slug exists, if yes append incrementing int to end
        name_slug_exists = mongo.db.users.count_documents(
            {"first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name")})

        if name_slug_exists:
            full_name += str(name_slug_exists+1)

        register = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "name_slug": full_name,
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "user_type": user_type,
            "profile_image": "default_avatar.png",
            "is_hidden": True,
            "is_admin": False
        }

        mongo.db.users.insert_one(register)

        # put user info into session
        session['user'] = {"slug": full_name, "u_type": user_type}
        flash("Reg successful", name_slug_exists)
        return redirect(url_for("edit_profile", name=full_name))

    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # check if user exists
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email_lg")})

        if existing_user:
            if check_password_hash(
                existing_user["password"],
                    request.form.get("password_lg")):
                session["user"] = {
                    "slug": existing_user["name_slug"],
                    "u-type": existing_user["user_type"]}

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
    flash("You've been successfully logged out!")
    session.pop("user")
    return redirect("/")


@app.route("/edit_profile/<name>", methods=["GET", "POST"])
def edit_profile(name):

    # get user slug
    u_slug = session["user"]["slug"]

    # get user profile from DB
    profile_data = list(
        mongo.db.users.find({"name_slug": u_slug}))

    skills = list(mongo.db.skills.find())
    roles = list(mongo.db.roles.find())

    if request.method == "POST":
        image = request.files["profile_img"]
        filename = secure_filename(image.filename)

        if filename == "":
            filename = profile_data[0]["profile_image"]
        else:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mongo.save_file(image.filename, image)

        update = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "rate": request.form.get("rate"),
            "location": request.form.get("location"),
            "role": request.form.get("role"),
            "skills": request.form.getlist("skills[]"),
            "profile_image": filename,
            "about": request.form.get("about_textarea"),
            "is_hidden": False
        }

        mongo.db.users.update_one(
            {"name_slug": u_slug}, {"$set": update})

        return redirect(url_for(
            "profile", name=u_slug))

    return render_template(
        "edit_profile.html", name=u_slug,
        data=profile_data, skills=skills, roles=roles)


@app.route("/profile/<name>", methods=["GET", "POST"])
def profile(name):

    # create full name string for profile page
    names = mongo.db.users.find_one({"name_slug": session["user"]["slug"]})

    # get single user profile data
    profile_data = list(
        mongo.db.users.find({"name_slug": session["user"]["slug"]}))

    # get all freelancers and projects for sidebar widget
    all_freelancers = mongo.db.users.find(
        {"user_type": "freelancer", "is_hidden": False})
    all_projects = mongo.db.projects.find()

    if session["user"]:
        return render_template(
            "profile.html", name=names, data=profile_data,
            projects=all_projects, freelancers=all_freelancers)
    else:
        return render_template("home.html")


""" Project CRUD functions """


@app.route("/add_project", methods=["GET", "POST"])
def add_project():

    skills = list(mongo.db.skills.find())
    roles = list(mongo.db.roles.find())

    if request.method == "POST":

        submitter_slug = session["user"]["slug"]
        submitter = mongo.db.users.find_one(
            {"name_slug": submitter_slug})
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
        return redirect(url_for("profile", name=submitter_slug))

    return render_template("add_project.html", skills=skills, roles=roles)


@app.route("/opportunities", methods=["GET"])
def get_projects():

    projects = mongo.db.projects.find()

    return render_template("all_projects.html", projects=projects)


@app.route("/view_project/<project_id>", methods=["GET", "POST"])
def view_project(project_id):

    # get single project information
    project_data = list(mongo.db.projects.find({"slug": project_id}))

    # get all freelancers and projects for sidebar widget
    all_freelancers = mongo.db.users.find(
        {"user_type": "freelancer", "is_hidden": False})
    all_projects = mongo.db.projects.find()

    return render_template(
        "view_project.html", project_id=project_id,
        data=project_data, freelancers=all_freelancers, projects=all_projects)


@app.route("/edit_project/<project_id>", methods=["GET", "POST"])
def edit_project(project_id):

    # get all skills and roles from DB
    skills = list(mongo.db.skills.find())
    roles = list(mongo.db.roles.find())

    # get existing project data
    project_data = list(mongo.db.projects.find({"slug": project_id}))

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


""" Freelancer Loop """


@app.route("/freelancers", methods=["GET", "POST"])
def get_freelancers():

    current_user = session["user"]["slug"]

    freelancers = mongo.db.users.find(
        {"user_type": "freelancer", "is_hidden": False})

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
    query = request.form.get("query")
    freelancers = list(mongo.db.users.find({"$text": {"$search": query},
                       "user_type": "freelancer", "is_hidden": False}))

    results = len(freelancers)

    return render_template("all_freelancers.html",
                           freelancers=freelancers, query=query,
                           results=results)


@app.route("/search_projects", methods=["GET", "POST"])
def search_projects():
    query = request.form.get("query")
    projects = list(mongo.db.projects.find({"$text": {"$search": query}}))

    results = len(projects)

    return render_template("all_projects.html", projects=projects,
                           query=query, results=results)


@app.route("/send_email/<slug>", methods=["GET", "POST"])
def send_mail(slug):

    recipient = mongo.db.users.find_one({"name_slug": slug})
    sender = mongo.db.users.find_one({"name_slug": session['user']['slug']})
    to_email = recipient["email"]
    reply_to = sender["email"]
    testing_email = "bradleyh.cooney@gmail.com"
    sender_name = sender["first_name"] + " " + sender["last_name"]
    from_email = "eventprofsearch@gmail.com"
    subject = f"You have a message from {sender_name}"
    user_msg = request.form.get("body")
    body = render_template("contact_email.html",
                           name=sender_name, to_name=recipient['first_name'],
                           message=user_msg, u_link=session['user']['slug'])
    msg = Message(subject, reply_to=testing_email, recipients=[testing_email])
    msg.html = body

    mail.send(msg)
    flash("You're message has been sent!")
    return redirect(url_for('get_freelancers'))


""" Admin functions """

# Admin dashboard
@app.route("/admin", methods=["GET", "POST"])
def admin_home():

    return render_template("admin/admin_dashboard.html")


# Get all users in admin view
@app.route("/admin/users", methods=["GET", "POST"])
def admin_users():

    users = mongo.db.users.find()

    return render_template("admin/admin_dashboard.html", users=users, uid=None)


# Get all skills & roles in admin view
@app.route("/admin/skills", methods=["GET", "POST"])
def admin_skills():

    skills = mongo.db.skills.find()

    return render_template("admin/admin_dashboard.html", skills=skills)


# Update skills from admin view
@app.route("/admin/update_skills", methods=["GET", "POST"])
def admin_update_skills():

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

    return redirect(url_for('admin_skills', _anchor='add_input'))


@app.route("/admin/delete_skill/<id>", methods=["GET", "POST"])
def delete_skill(id):
    mongo.db.skills.delete_one({"skill_name": id})
    flash("The skill was deleted successfully!")
    return redirect(url_for('admin_skills'))


# Get all roles in admin view
@app.route("/admin/roles", methods=["GET", "POST"])
def admin_roles():

    roles = mongo.db.roles.find()

    return render_template("admin/admin_dashboard.html", roles=roles)


# Update skills from admin view
@app.route("/admin/update_roles", methods=["GET", "POST"])
def admin_update_roles():

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

    return redirect(url_for('admin_roles', _anchor='add_input'))


@app.route("/admin/delete_role/<id>", methods=["GET", "POST"])
def delete_role(id):
    mongo.db.roles.delete_one({"role_name": id})
    flash("The role was deleted successfully!")
    return redirect(url_for('admin_roles'))


@app.route("/admin/users_update/<uid>", methods=["GET", "POST"])
def admin_update_user(uid):

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
    return render_template("admin/admin_dashboard.html")


# Debug delete user script
@app.route("/delete_user", methods=["GET", "POST"])
def delete_users():

    delete = {"skill_name": "sss"}
    delete_also = {"skill_name": "AutoCAD"}
    and_this = {"skill_name": "Adobe Illustrator"}

    mongo.db.users.delete_many(delete)
    return "done", delete


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
