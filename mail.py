#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Mail Python module
Version 1.1.1
"""
# Import dependencies
import os
import smtplib
from flask import (Blueprint, flash, render_template, request, session)
from email.message import EmailMessage
from forms import ContactForm
from userauth import user_get


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
        message = contact_get_message_string(
            user_name, contact_name, contact_email, contact_message)
        # Set server variable
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # Put the SMTP connection in TLS (Transport Layer Security) mode
        server.starttls()
        # Attempt to log in to email server
        try:
            server.login(mail_username, mail_password)
        # Display flash message if there is is an exception
        except smtplib.SMTPException:
            flash(
                "Could not log into email server, " +
                "please check configuration variables",
                "danger")
            return render_template("contact.html", form=form)
        else:
            # Set message variable
            msg = EmailMessage()
            msg["Subject"] = "New contact message from FreeFrom"
            msg["From"] = mail_username
            msg["To"] = mail_username
            msg.set_content(message)
            # Attempt to send message
            try:
                server.send_message(msg)
            # Display flash message if there is is an exception
            except smtplib.SMTPException:
                flash(
                    "Contact email has not been succesfully sent, " +
                    "please try again",
                    "warning")
                return render_template("contact.html", form=form)
            # Display flash message if email is succesfully sent
            else:
                flash(
                    "Contact email has been succesfully sent",
                    "success")
            return render_template("home.html")

    # If user is logged in, set email address field automatically
    if user_name:
        form.email.data = user_get(user_name)["email"]
    return render_template("contact.html", form=form)


def contact_get_message_string(user_name, contact_name, contact_email,
                               contact_message):
    """
    Return message string, include user name if signed in
    """
    if user_name:
        message = (
            "Message from FreeFrom \nName: " +
            contact_name +
            "\nUser Name: " + user_name +
            "\nEmail Address: " + contact_email +
            "\nMessage: " + contact_message)
    else:
        message = (
            "Message from FreeFrom \nName: " +
            contact_name +
            "\nEmail Address: " + contact_email +
            "\nMessage: " + contact_message)
    return message
