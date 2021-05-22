# Import dependencies
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, TextField, TextAreaField, Form, validators)


# SignIn form
class SignInForm(Form):
    username = StringField('User Name', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, max=25, message="User Name must be between 5 and 25 characters long"),
        validators.Regexp("\w+$", message="Username must contain only letters, numbers or underscore")
    ])
    password = StringField('Password', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, max=25, message="Password must be between 5 and 25 characters long"), 
        #check_password_format 
    ])


# Registration form, inherits from SignInForm 
class RegistrationForm(SignInForm):
    email = StringField('Email', [
        validators.DataRequired(message="Input required"),
        validators.Email(message="Please enter a valid email address"),
        validators.Length(min=5, message="Email address must be 5 or more characters long")
    ])
