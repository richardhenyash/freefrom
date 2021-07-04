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
    Route for user Register
    """
    # request form data
    form = RegistrationForm(request.form)
    # validate form
    if request.method == "POST" and form.validate():
        user_name = form.username.data.lower()
        if user_check(user_name):
            return redirect(url_for("userauth.register"))
        else:
            user_register(user_name, form)
            return redirect(
                url_for("home", username=session["user"]))

    return render_template("register.html", form=form)


# SignIn function
@userauth.route("/signin", methods=["GET", "POST"])
def signin():
    """
    Route for user Sign In
    """
    # request form data
    form = SignInForm(request.form)
    # validate form
    if request.method == "POST" and form.validate():
        # check if username exists in database
        user_name = request.form.get("username").lower()
        existing_user = user_get(user_name)
        if existing_user:
            entered_password = form.password.data
            if user_password_check(user_name, entered_password, existing_user):
                return redirect(url_for("home"))
            else:
                return redirect(url_for("userauth.signin"))
        else:
            return redirect(url_for("userauth.signin"))

    return render_template("signin.html", form=form)


# SignOut function
@userauth.route("/signout")
def signout():
    """
    Route for user Sign Out
    """
    # remove user from session cookies
    session.pop("user")
    session.pop("admin")
    flash("You have been signed out", "success")
    return redirect(url_for("home"))


def user_check(user_name):
    """
    Check if user name exists in the database
    """
    if mongo.db.users.find_one({"username": user_name}):
        # Display flash message
        flash("Username already exists", "warning")
        user_check = True
    else:
        user_check = False
    return(user_check)


def user_get(user_name):
    """
    Return existing user from database
    """
    existing_user = mongo.db.users.find_one({"username": user_name})
    if not(existing_user):
        flash("Incorrect username and/or password", "warning")
    return(existing_user)


def user_password_check(user_name, entered_password, existing_user):
    """
    Check user password entered in form against database
    """
    print(check_password_hash(existing_user["password"], entered_password))
    if check_password_hash(existing_user["password"], entered_password):
        session["user"] = user_name
        session["admin"] = existing_user["admin"]
        flash("Welcome, " + user_name, "success")
        password_check = True
    else:
        flash("Incorrect username and/or password", "warning")
        password_check = False
    return(password_check)


def user_register(user_name, form):
    """
    Gather form data, register user in the database
    and add user to session cookie
    """
    # gather form data
    register = {
        "admin": False,
        "username": user_name,
        "email": form.email.data.lower(),
        "password": generate_password_hash(form.password.data)
    }
    mongo.db.users.insert_one(register)
    # put the new user into "session" cookie
    session["user"] = request.form.get("username").lower()
    # set user admin
    session["admin"] = False
    flash("Registration successful", "success")
    return(user_name)
