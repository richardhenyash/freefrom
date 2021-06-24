#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Categories Python module
Version 1.1.1
"""
# Import dependencies
from flask import (
    Blueprint, flash, render_template, redirect, request, url_for)
from bson.objectid import ObjectId
from forms import CategoryForm

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
categories = Blueprint(
    "categories", __name__, static_folder="static",
    template_folder="templates")


@categories.route("/category_add", methods=["GET", "POST"])
def category_add():
    """
    Route for category add
    """
    # request Form data
    form = CategoryForm(request.form)
    if request.method == "POST" and form.validate():
        # Set new category name variable
        category_name = form.name.data.lower()
        # Check if new category name exists in database
        if mongo.db.categories.find_one({"name": category_name}):
            # Display flash message
            flash("Category already exists", "warning")
            return render_template("category_add.html", form=form)
        else:
            # Add new category to the database
            mongo.db.categories.insert_one({"name": category_name})
            # Display flash message
            flash(
                "Category " + category_name +
                " succesfully added", "success")
        return redirect(url_for('products.search'))
    return render_template("category_add.html", form=form)


@categories.route("/categories_edit", methods=["GET", "POST"])
def category_edit():
    """
    Route for category edit
    """
    # request Form data
    form = CategoryForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find().sort("name", 1)
    if request.method == "POST" and form.validate():
        # Get existing category name
        existing_category_name = request.form.get(
            "categorySelector").lower()
        # Check if category has been selected from drop down
        if existing_category_name:
            if existing_category_name == "category...":
                # Display flash message
                flash("Please select Category to update", "warning")
                proceed = False
            else:
                proceed = True
        else:
            # Display flash message
            flash("Please select Category to update", "warning")
            proceed = False
        if proceed:
            # Set new category name variable
            category_name = form.name.data.lower()
            # Check if new category name exists in database
            if mongo.db.categories.find_one({"name": category_name}):
                # Display flash message
                flash("Category already exists", "warning")
                proceed = False
        if proceed:
            # Get category id
            category = mongo.db.categories.find_one(
                {"name": existing_category_name})
            # Check if category is still in database
            if category:
                category_id = category["_id"]
                # Update category in the database
                category_update = {"name": category_name}
                mongo.db.categories.update(
                    {"_id": ObjectId(category_id)}, category_update)
                # Display flash message
                flash(
                    "Category " + category_name +
                    " succesfully updated", "success")
                return redirect(url_for('products.search'))
            else:
                # Display flash message
                flash(
                    "Ooops.... category " + existing_category_name +
                    " no longer exists in the database", "danger")
                return redirect(url_for('categories.category_edit'))
        else:
            return render_template(
                "category_edit.html",
                categories=categories, form=form)

    return render_template(
        "category_edit.html",
        categories=categories, form=form)


@categories.route("/categories_delete", methods=["GET", "POST"])
def category_delete():
    """
    Route for category delete
    """
    # Get categories collection from database
    categories = mongo.db.categories.find().sort("name", 1)
    if request.method == "POST":
        # Get existing category name
        existing_category_name = request.form.get(
            "categorySelector").lower()
        # Check if category has been selected from drop down
        if existing_category_name:
            if existing_category_name == "category...":
                # Display flash message
                flash("Please select Category to delete", "warning")
                proceed = False
            else:
                proceed = True
        else:
            # Display flash message
            flash("Please select Category to delete", "warning")
            proceed = False
        if proceed:
            # Get category
            category = mongo.db.categories.find_one(
                {"name": existing_category_name})
            # Check if category is still in database
            if category:
                category_id = category["_id"]
                return render_template(
                    "category_delete_confirm.html",
                    category_id=category_id, category=category)
            else:
                # Display flash message
                flash(
                    "Ooops.... category " + existing_category_name +
                    " no longer exists in the database", "danger")
                return redirect(url_for('categories.category_delete'))
        else:
            return render_template(
                "category_delete.html", categories=categories)

    return render_template(
        "category_delete.html", categories=categories)


@categories.route(
    "/categories_delete_confirm/<category_id>",
    methods=["GET", "POST"])
def category_delete_confirm(category_id):
    """
    Route for category delete confirm
    """
    if request.method == "POST":
        # Get category from database
        category = mongo.db.categories.find_one(
            {"_id": (ObjectId(category_id))})
        # Check if category is still in database
        if category:
            # Get category name
            category_name = category["name"]
            # Delete category from the database
            mongo.db.categories.delete_one({"_id": (ObjectId(category_id))})
            # Display flash message
            flash(
                "Category " + category_name +
                " succesfully deleted", "success")
            return redirect(url_for('products.search'))
        else:
            # Display flash message
            flash(
                "Ooops.... selected category no longer " +
                "exists in the database", "danger")
            return redirect(url_for('categories.category_delete'))

    category = mongo.db.categories.find_one(
        {"_id": (ObjectId(category_id))})
    return render_template(
        "category_delete_confirm.html",
        category_id=category_id, category=category)


"""
Category Class
=============
Contains the Category Class to enable create, read, update and delete of
categories stored in the MongoDB and preparaton of data
Classes: Category
"""


class Category():
    """
    A class that represents an Category.
    Performs the relevant database CRUD functionality
    along with data preparation.
    """
    def __init__(self, name, _id=None):
        """
        Category initialisation
        """
        self._id = _id
        self.name = name

    def get_info(self):
        """
        Formats and returns the current Category object attributes as
        a dictionary. The format of the dictionary allows the return
        of this method to be written directly to the Database.
        """
        info = {"name": self.name}

    @staticmethod
    def get_all():
        categories = mongo.db.categories.find().sort("name", 1)
        return(categories)

    @staticmethod
    def get_all():
        categories = mongo.db.categories.find().sort("name", 1)
        return(categories)

    @staticmethod
    def get_id(category_name):
        """
        Gets an category ObjectId from an category name
        """
        category_id = mongo.db.categories.find_one({"name": category_name})["_id"]
        return(category_id)
    
    @staticmethod
    def get_name(category_id):
        """
        Gets a category name from an category ObjectId
        """
        category_name = mongo.db.categories.find_one({"_id": category_id})["name"]
        return(category_name)
    
