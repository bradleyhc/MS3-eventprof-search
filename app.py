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

        register = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "user_type": user_type
        }

        # create full name string for profile page
        full_name = request.form.get(
            "first_name").lower() + "_" + request.form.get("last_name").lower()

        mongo.db.users.insert_one(register)

        # put user info into session
        session['user'] = request.form.get("email")
        print(session["user"])
        flash("Reg successful")
        return render_template("profile.html", name=full_name, data=register)

    return render_template("home.html")


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
    names = mongo.db.users.find_one({"email": session["user"]})

    full_name = names[
        "first_name"].lower() + "_" + names["last_name"].lower()

    profile_data = list(
        mongo.db.users.find({"email": session["user"]}))

    if session["user"]:
        return render_template(
            "profile.html", name=full_name, data=profile_data)


@app.route("/freelancers")
def get_freelancers():
    return render_template("freelancers.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
