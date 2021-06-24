#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom User Authorisation Python module
Version 1.1.1
"""
# Import dependencies
from flask import (
    Blueprint, flash, render_template,
    redirect, request, session, url_for)
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, SignInForm

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
userauth = Blueprint(
    "userauth", __name__,
    static_folder="static", template_folder="templates")


# Route for user Registration
@userauth.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for user registration
    """
    # request form data
    form = RegistrationForm(request.form)
    # validate form
    if request.method == "POST" and form.validate():

        # check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # flash message to warn if username already exists in database
            flash("Username already exists", "warning")
            # return to register page
            return redirect(url_for(
                "userauth.register",
                _external=True, _scheme='https'))

        # gather form data
        register = {
            "admin": False,
            "username": form.username.data.lower(),
            "email": form.email.data.lower(),
            "password": generate_password_hash(form.password.data)
        }
        mongo.db.users.insert_one(register)

        # put the new user into "session" cookie
        session["user"] = request.form.get("username").lower()
        # set user admin
        session["admin"] = False
        flash("Registration successful", "success")
        # return to home page
        return redirect(
            url_for("home", username=session["user"]))

    return render_template("register.html", form=form)


# SignIn function
@userauth.route("/signin", methods=["GET", "POST"])
def signin():
    """
    Route for user SignIn
    """
    # request form data
    form = SignInForm(request.form)
    # validate form
    if request.method == "POST" and form.validate():
        # check if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], form.password.data):
                session["user"] = form.username.data.lower()
                session["admin"] = existing_user["admin"]
                flash(
                    "Welcome, {}"
                    .format(form.username.data.lower()),
                    "success")
                return redirect(url_for("home"))
            else:
                # invalid password match
                flash("Incorrect username and/or password", "warning")
                return redirect(url_for("userauth.signin"))
        else:
            # username doesn't exist
            flash("Incorrect username and/or password", "warning")
            return redirect(url_for("userauth.signin"))

    return render_template("signin.html", form=form)


# SignOut function
@userauth.route("/signout")
def signout():
    # remove user from session cookies
    flash("You have been signed out", "success")
    session.pop("user")
    session.pop("admin")
    return redirect(url_for("home"))


"""
User Class
=============
Contains the User Class to enable create, read, update and delete of
users stored in the MongoDB and preparaton of data
Classes: User
"""


class User():
    """
    A class that represents a User.
    Performs the relevant database CRUD functionality
    along with data preparation.
    """
    # This is called whenever a class is instantiated
    def __init__(self, admin, username, email, password, _id=None):
        """
        Product initialisation
        """
        self._id = _id
        self.admin = admin
        self.username = username
        self.email = email
        self.password = password

    def get_info(self):
        """
        Formats and returns the current User object attributes as a.
        dictionary. The format of the dictionary allows the return
        of this method to be written directly to the Database.
        """
        info = {"admin": self.admin, "username": self.username,
                "email": self.email, "password": self.password}

    # Can be called without instantiating a class
    @staticmethod
    def get_id(user_name):
        """
        Gets a user name from a user ID
        """
        user_id = mongo.db.users.find_one({"username": user_name})["_id"]
        return(user_id)
    
    @staticmethod
    def get_name(user_id):
        """
        Gets a user ID from a user name
        """
        user_name = mongo.db.users.find_one({"_id": user_id})["username"]
        return(user_name)

