# Import dependencies
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
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
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
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
        return render_template(
            "home.html", categories=categories,
            allergens=allergens, form=form)
    return render_template("category_add.html", form=form)


@categories.route("/categories_edit", methods=["GET", "POST"])
def category_edit():
    """
    Route for category edit
    """
    # request Form data
    form = CategoryForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
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
            category_id = mongo.db.categories.find_one(
                {"name": existing_category_name})["_id"]
            # Update category in the database
            category_update = {"name": category_name}
            mongo.db.categories.update(
                {"_id": ObjectId(category_id)}, category_update)
            # Display flash message
            flash(
                "Category " + category_name +
                " succesfully updated", "success")
            return render_template(
                "home.html", categories=categories,
                allergens=allergens)
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
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    # Get categories collection from database
    categories = mongo.db.categories.find()
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
            category_id = category["_id"]
            return render_template(
                "category_delete_confirm.html",
                category_id=category_id, category=category)
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
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    # Get categories collection from database
    categories = mongo.db.categories.find()
    if request.method == "POST":
        # Get category name from database
        category_name = mongo.db.categories.find_one(
            {"_id": (ObjectId(category_id))})["name"]
        # Delete category from the database
        mongo.db.categories.delete_one({"_id": (ObjectId(category_id))})
        # Display flash message
        flash(
            "Category " + category_name +
            " succesfully deleted", "success")
        return render_template(
                "home.html",
                categories=categories, allergens=allergens)

    category = mongo.db.categories.find_one(
        {"_id": (ObjectId(category_id))})
    return render_template(
        "category_delete_confirm.html",
        category_id=category_id, category=category)
