# Import dependencies
import os
import smtplib
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from email.message import EmailMessage
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import ContactForm

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
mail = Blueprint("mail", __name__, static_folder="static",
                 template_folder="templates")


# Configure mail access variables
mail_username = os.environ.get("MAIL_USERNAME")
mail_password = os.environ.get("MAIL_PASSWORD")


# Route for Contact Developer
@mail.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Route for contact developer
    """
    # request form data
    form = ContactForm(request.form)
    # Get user name if logged in
    user_name = None
    if session:
        user_name = session["user"]
    # validate form
    if request.method == "POST" and form.validate():
        contact_name = form.name.data
        contact_email = form.email.data
        contact_message = form.message.data
        if user_name:
            message = "Message from FreeFrom \nName: " + contact_name + "\nUser name: " + user_name + "\nEmail Address: " + contact_email + "\nMessage: " + contact_message
        else:
            message = "Message from FreeFrom \nName: " + contact_name + "\nEmail Address: " + contact_email + "\nMessage: " + contact_message
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        try:
            server.login(mail_username, mail_password)
        except:
            flash("Could not log into email server, please check configuration variables", "warning")
            return render_template("contact.html", form=form)
        else:
            msg = EmailMessage()
            msg["Subject"] = "New contact message from FreeFrom"
            msg["From"] = mail_username
            msg["To"] = mail_username
            msg.set_content(message)
            try:
                server.send_message(msg)
            except:
                flash("Contact email has not been succesfully sent, please try again", "warning")
                return render_template("contact.html", form=form)
            else:
                flash("Contact email has been succesfully sent", "success")
            return render_template("home.html")      

    # If user is logged in, set email address field automatically
    if user_name:
        user_email = mongo.db.users.find_one({"username": user_name})["email"]
        form.email.data = user_email
    return render_template("contact.html", form=form)
