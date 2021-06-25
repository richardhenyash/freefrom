#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Forms Python module
Version 1.1.1
"""
# Import dependencies
from wtforms import (
    StringField, PasswordField, TextAreaField, Form, validators)
import wtforms_validators


# SignIn form
class SignInForm(Form):
    """
    Sign In Form
    """
    username = StringField('User Name', [
        validators.DataRequired(message="Input required"),
        validators.Length(
            min=5, max=25,
            message="User Name must be between 5 and 25 characters long"),
        wtforms_validators.AlphaNumeric(
            message="User Name must contain only letters or numbers")
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message="Input required"),
        validators.Length(
            min=5, max=25,
            message="Password must be between 5 and 25 characters long")
    ])


# Registration form, inherits from SignInForm
class RegistrationForm(SignInForm):
    """
    Registration Form
    """
    email = StringField('Email', [
        validators.DataRequired(message="Input required"),
        validators.Email(message="Please enter a valid email address"),
        validators.Length(
            min=5,
            message="Email address must be 5 or more characters long")
    ])
    confirmpassword = PasswordField('Confirm Password', [
        validators.DataRequired(message="Input required"),
        validators.EqualTo("password", message='Passwords must match')
    ])


# Contact form
class ContactForm(Form):
    """
    Contact Form
    """
    name = StringField('Name', [
        validators.DataRequired(message="Input required"),
        validators.Length(
            min=3, max=100,
            message="User Name must be between 3 and 100 characters long"),
        wtforms_validators.AlphaSpace(
            message="Name must contain only letters or spaces")
    ])
    email = StringField('Email', [
        validators.DataRequired(message="Input required"),
        validators.Email(message="Please enter a valid email address"),
        validators.Length(
            min=5,
            message="Email address must be 5 or more characters long")
    ])
    message = TextAreaField('Message', [
        validators.DataRequired(message="Message required"),
        validators.Length(
            min=10, max=500,
            message="Message must be between 10 and 500 characters long")
    ])


# Product form
class ProductForm(Form):
    """
    Product Form
    """
    name = StringField('Product', [
        validators.DataRequired(
            message="Product name required in order to add product"),
        validators.Length(
            min=3, max=50,
            message="Product name must be between 3 and 50 characters long"),
    ])
    manufacturer = StringField('Manufacturer', [
        validators.DataRequired(
            message="Manufacturer name required in order to add product"),
        validators.Length(
            min=3, max=50,
            message="Manufacturer name must be between 3 " +
            "and 50 characters long"),
    ])
    freefrom = StringField('Free From', [
        validators.Optional(),
    ])
    review = TextAreaField('Your Review', [
        validators.DataRequired(
            message="Product review required in order to add product"),
        validators.Length(
            min=5, max=250,
            message="Product review must be between 5 and 250 characters long")
    ])
    rating = StringField('Your Rating', [
        validators.Length(
            min=1, max=1,
            message="Please rate product between 1 and 5 stars")
    ])


class ProductViewForm(Form):
    """
    Product View Form
    """
    name = StringField('Product', render_kw={'readonly': True})
    category = StringField('Category', render_kw={'readonly': True})
    manufacturer = StringField('Manufacturer', render_kw={'readonly': True})
    freefrom = StringField('Free From', render_kw={'readonly': True})
    review = TextAreaField('Your Review', [
        validators.DataRequired(
            message="Product review required in order to add product"),
        validators.Length(
            min=5, max=250,
            message="Product review must be between 5 and 250 characters long")
    ])
    rating = StringField('Your Rating', [
        validators.Length(
            min=1, max=1,
            message="Please rate product between 1 and 5 stars")
    ])


class ProductEditForm(Form):
    """
    Product Edit Form
    """
    name = StringField('Product', [
        validators.DataRequired(
            message="Product name required in order to edit product"),
        validators.Length(
            min=3, max=50,
            message="Product name must be between 3 and 50 characters long"),
    ])
    manufacturer = StringField('Manufacturer', [
        validators.DataRequired(
            message="Manufacturer name required in order to edit product"),
        validators.Length(
            min=3, max=50,
            message="Manufacturer name must be between " +
            "3 and 50 characters long"),
    ])
    freefrom = StringField('Free From', [
        validators.Optional(),
    ])


class AllergenForm(Form):
    """
    Allergen Form
    """
    name = StringField('New Allergen Name', [
        validators.DataRequired(
            message="Allergen name required in order to add allergen"),
        validators.Length(
            min=3, max=20,
            message="Allergen name must be between 5 and 20 characters long"),
        wtforms_validators.AlphaSpace(
            message="Allergen name must contain only letters or spaces")
    ])


class CategoryForm(Form):
    """
    Category Form
    """
    name = StringField('New Category Name', [
        validators.DataRequired(
            message="Category name required in order to add allergen"),
        validators.Length(
            min=3, max=30,
            message="Category name must be between 5 and 30 characters long"),
        wtforms_validators.AlphaSpace(
            message="Category name must contain only letters or spaces")
    ])
