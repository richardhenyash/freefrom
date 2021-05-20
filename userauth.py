# Import dependencies
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
userauth = Blueprint("userauth", __name__, static_folder="static",
                 template_folder="templates")

# Register function
@userauth.route("/register", methods=["GET", "POST"])
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

# SignIn function
@userauth.route("/signin", methods=["GET", "POST"])
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
                    session["admin"] = existing_user["admin"]
                    flash("Welcome, {}".format(request.form.get("username")), "success")
                    print(session)
                    return redirect(url_for("home"))
            else:
                # invalid password match
                flash("Incorrect username and/or password", "warning")
                return redirect(url_for("userauth.signin"))
        else:
            #username doesn't exist
            flash("Incorrect username and/or password", "warning")
            return redirect(url_for("userauth.signin"))

    return render_template("signin.html")

# SignOut function
@userauth.route("/signout")
def signout():
    # remove user from session cookies
    flash("You have been signed out", "success")
    session.pop("user")
    session.pop("admin")
    print(session)
    return redirect(url_for("home", _external=True, _scheme='https'))

