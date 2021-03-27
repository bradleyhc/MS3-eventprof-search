import os
from flask import (Flask, flash, redirect,
                   render_template, request, url_for, session)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

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

        mongo.db.users.insert_one(register)

        flash("Reg successful")

    return render_template("home.html")


@app.route("/freelancers")
def get_freelancers():
    return render_template("freelancers.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
