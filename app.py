import os
from flask import (Flask, flash, redirect,
                   render_template, request, url_for, session)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
#from bson.object import ObjectId
#from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env

app = Flask(__name__)    

app.secret_key = os.environ.get("SECRET_KEY")

@app.route("/")
@app.route("/home")
def homepage():
    return render_template("home.html")


@app.route("/freelancers")
def get_freelancers():
    return render_template("freelancers.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
