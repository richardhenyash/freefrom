# Import dependencies
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, TextField, TextAreaField, Form, validators)

# Registration form
class RegistrationForm(Form):
    username = StringField('User Name', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, message="User name must be 5 or more characters long")
    ])
    email = StringField('Email', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, message="Email address must be 5 or more characters long"), 
        validators.Email(message="Please enter a valid email address")
    ])
    password = StringField('Password', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, max=25, message="Password must be between 5 and 25 characters long"), 
        #check_password_format 
    ])
    
# SignIn form
class SignInForm(Form):
    username = StringField('User Name', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, message="User name must be 5 or more characters long")
    ])
    password = StringField('Password', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, max=25, message="Password must be between 5 and 25 characters long"), 
        #check_password_format 
    ])

# Check password format
def check_password_format(form, field):
    # Check that password contains at least one number and no special characters
    digitflag = False
    scflag = False
    res = False
    for char in field:
        if char.isdigit():
            digitflag = True
        if (not (char.isdigit())) and (not char.isalpha()):
            scflag = True
    if digitflag and (not scflag):
        res = True
    else:
        if not digitflag:
            raise ValidationError("Password must contain at least one number")
        if scflag:
            raise ValidationError("Password must contain only alphanumeric characters")
    return res
