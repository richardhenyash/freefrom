# Import dependencies
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, TextField, TextAreaField, 
                     IntegerField, Form, validators)
import wtforms_validators

# SignIn form
class SignInForm(Form):
    """
    Sign In Form
    """
    username = StringField('User Name', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, max=25, message="User Name must be between 5 and 25 characters long"),
        validators.Regexp("\w+$", message="Username must contain only letters, numbers or underscore")
    ])
    password = StringField('Password', [
        validators.DataRequired(message="Input required"),
        validators.Length(min=5, max=25, message="Password must be between 5 and 25 characters long"), 
    ])


# Registration form, inherits from SignInForm 
class RegistrationForm(SignInForm):
    """
    Registration Form
    """
    email = StringField('Email', [
        validators.DataRequired(message="Input required"),
        validators.Email(message="Please enter a valid email address"),
        validators.Length(min=5, message="Email address must be 5 or more characters long")
    ])

# Product form
class ProductForm(Form):
    """
    Product Form
    """
    name = StringField('Product Name', [
        validators.DataRequired(message="Product name required in order to add product"),
        validators.Length(min=5, max=50, message="Product name must be between 5 and 50 characters long"),
        wtforms_validators.AlphaSpace(message="Product name must contain only letters, numbers or spaces")
    ])
    manufacturer = StringField('Manufacturer Name', [
        validators.DataRequired(message="Manufacturer name required in order to add product"),
        validators.Length(min=5, max=50, message="Manufacturer name must be between 5 and 50 characters long"),
        wtforms_validators.AlphaSpace(message="Manufacturer name must contain only letters, numbers or spaces")
    ])
    review = TextAreaField('Product Review', [
        validators.DataRequired(message="Product review required in order to add product"),
        validators.Length(min=5, max=250, message="Product review must be between 5 and 250 characters long")
    ])
    rating = IntegerField('Product Rating', [
        validators.DataRequired(message="Product rating required in order to add product"),
        validators.NumberRange(min=1, max=5, message="product rating must be an integer between 1 and 5"),
    ])
