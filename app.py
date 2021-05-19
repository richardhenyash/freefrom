import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    categories = mongo.db.categories.find()
    allergens = mongo.db.allergens.find()
    return render_template("home.html", categories=categories, allergens=allergens)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists", "warning")
            return redirect(url_for("register", _external=True, _scheme='https'))

        register = {
            "admin": False,
            "username": request.form.get("username").lower(), 
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into "session" cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful", "success")
        return redirect(url_for("home", username=session["user"], _external=True, _scheme='https'))

    return render_template("register.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # check if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")), "success")
                    return redirect(url_for("home"))
            else:
                # invalid password match
                flash("Incorrect username and/or password", "warning")
                return redirect(url_for("signin"))
        else:
            #username doesn't exist
            flash("Incorrect username and/or password", "warning")
            return redirect(url_for("signin"))

    return render_template("signin.html")


@app.route("/signout")
def signout():
    # remove user from session cookies
    flash("You have been signed out", "success")
    session.pop("user")
    return redirect(url_for("home", _external=True, _scheme='https'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Update to debug=False prior to deployment/submission
            debug=True)

