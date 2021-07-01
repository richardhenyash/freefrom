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
        existing_category_name = category_get_selection("Update")
        category_name = form.name.data.lower()
        if existing_category_name and category_check(category_name):
            category_id = category_get_id(existing_category_name)
            # Update category in the database
            if category_id:
                category_update(category_id, category_name)
                return redirect(url_for('products.search'))
            else:
                return redirect(url_for('categories.category_edit'))
        else:
            return render_template(
                "category_edit.html", categories=categories, form=form)

    return render_template(
        "category_edit.html", categories=categories, form=form)


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


def category_check(category_name):
    """
    Check if category name already exists in the database
    """
    category_check = True
    if mongo.db.categories.find_one({"name": category_name}):
        # Display flash message
        flash("Category already exists", "warning")
        category_check = False
    return category_check


def category_get_id(category_name):
    """
    Get category id from category name
    """
    category = mongo.db.categories.find_one({"name": category_name})
    category_id = None
    # Check if category exists in database
    if category:
        category_id = category["_id"]
    else:
        flash(
            "Ooops.... category " + category_name +
            " no longer exists in the database", "danger")
    return category_id


def category_get_selection(category_method):
    """
    Returns category name selected in Category Selector
    """
    # Get existing category name
    category_name = request.form.get("categorySelector").lower()
    # If category has not been selected
    if category_name == "category...":
        # Display flash message
        flash("Please select Category to " + category_method, "warning")
        category_name = None
    return category_name


def category_update(category_id, category_name):
    """
    Update category in the database given category id and new category name
    Returns category name
    """
    mongo.db.categories.update(
        {"_id": ObjectId(category_id)}, {"name": category_name})
    flash("Category " + category_name + " succesfully updated", "success")
    return category_name
