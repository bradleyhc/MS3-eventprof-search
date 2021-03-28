import os
import json
from flask import (Flask, flash, redirect,
                   render_template, request, url_for, session, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from bson import json_util
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Set user image upload config
UPLOAD_FOLDER = './static/images/user_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

        register = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "name_slug": full_name,
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "user_type": user_type
        }

        mongo.db.users.insert_one(register)

        # put user info into session
        session['user'] = request.form.get("email")
        flash("Reg successful")
        return render_template("profile.html", name=full_name, data=register)

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
                session["user"] = request.form.get("email_lg")

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
    # create full name string for profile page
    names = mongo.db.users.find_one({"email": session["user"]})

    full_name = names["first_name"].lower() + "_" + names["last_name"].lower()

    profile_data = list(
        mongo.db.users.find({"email": session["user"]}))

    skills = list(mongo.db.skills.find())
    roles = list(mongo.db.roles.find())

    if request.method == "POST":
        image = request.files["profile_img"]
        filename = secure_filename(image.filename)
        update = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "rate": request.form.get("rate"),
            "location": request.form.get("location"),
            "role": request.form.get("role"),
            "skills": request.form.getlist("skills[]"),
            "profile_image": filename,
        }

        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mongo.save_file(image.filename, image)
        mongo.db.users.update_one(
            {"email": session["user"]}, {"$set": update})

        return render_template(
            "edit_profile.html", name=full_name,
            data=profile_data, skills=skills, roles=roles)

    return render_template(
        "edit_profile.html", name=full_name,
        data=profile_data, skills=skills, roles=roles)


@app.route("/profile/<name>", methods=["GET", "POST"])
def profile(name):

    # create full name string for profile page
    names = mongo.db.users.find_one({"email": session["user"]})["name_slug"]

    profile_data = list(
        mongo.db.users.find({"email": session["user"]}))

    if session["user"]:
        return render_template(
            "profile.html", name=names, data=profile_data)
    else:
        return render_template("home.html")


@app.route("/freelancers")
def get_freelancers():
    return render_template("freelancers.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
