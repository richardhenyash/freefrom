#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Allergens Python module
Version 1.1.2
"""
# Import dependencies
from flask import (
    Blueprint, flash, render_template,
    redirect, request, url_for)
from bson.objectid import ObjectId
from forms import AllergenForm

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
allergens = Blueprint(
    "allergens", __name__, static_folder="static",
    template_folder="templates")


@allergens.route("/allergen_add", methods=["GET", "POST"])
def allergen_add():
    """
    Route for allergen add
    """
    # request Form data
    form = AllergenForm(request.form)
    if request.method == "POST" and form.validate():
        # Set new allergen name variable
        allergen_name = form.name.data.lower()
        # Check if new allergen name exists in database
        if mongo.db.allergens.find_one({"name": allergen_name}):
            # Display flash message
            flash("Allergen already exists", "warning")
            return render_template("allergen_add.html", form=form)
        else:
            # Add new allergen to the database
            mongo.db.allergens.insert_one(
                {"name": allergen_name})
            # Display flash message
            flash(
                "Allergen " + allergen_name +
                " succesfully added", "success")
        return redirect(url_for('products.search'))
    return render_template("allergen_add.html", form=form)


@allergens.route("/allergen_edit", methods=["GET", "POST"])
def allergen_edit():
    """
    Route for allergen edit
    """
    # request Form data
    form = AllergenForm(request.form)
    # Get allergens collection from database
    allergens = mongo.db.allergens.find().sort("name", 1)
    if request.method == "POST" and form.validate():
        existing_allergen_name = allergen_get_selection("Update")
        allergen_name = form.name.data.lower()
        if existing_allergen_name and allergen_check(allergen_name):
            allergen_id = allergen_get_id(existing_allergen_name)
            # Update allergen in the database
            if allergen_id:
                allergen_update(allergen_id, allergen_name)
                return redirect(url_for('products.search'))
            else:
                return redirect(url_for('allergens.allergen_edit'))
        else:
            return render_template(
                "allergen_edit.html",
                allergens=allergens, form=form)

    return render_template(
        "allergen_edit.html", allergens=allergens, form=form)


@allergens.route("/allergen_delete", methods=["GET", "POST"])
def allergen_delete():
    """
    Route for allergen delete
    """
    # Get allergens collection from database
    allergens = mongo.db.allergens.find().sort("name", 1)
    if request.method == "POST":
        # Get existing allergen name
        existing_allergen_name = allergen_get_selection("Delete")
        if existing_allergen_name:
            allergen_id = allergen_get_id(existing_allergen_name)
            allergen = mongo.db.allergens.find_one(
                {"_id": (ObjectId(allergen_id))})
            if allergen_id:
                return render_template(
                    "allergen_delete_confirm.html",
                    allergen_id=allergen_id, allergen=allergen)
            else:
                # Display flash message
                flash(
                    "Ooops.... allergen " + existing_allergen_name +
                    " no longer exists in the database", "danger")
                return redirect(url_for('allergens.allergen_delete'))
        else:
            return render_template(
                "allergen_delete.html", allergens=allergens)

    return render_template(
        "allergen_delete.html", allergens=allergens)


@allergens.route(
    "/allergen_delete_confirm/<allergen_id>",
    methods=["GET", "POST"])
def allergen_delete_confirm(allergen_id):
    """
    Route for allergen delete confirm
    """
    if request.method == "POST":
        # Get allergen from database
        allergen = mongo.db.allergens.find_one(
            {"_id": (ObjectId(allergen_id))})
        if allergen:
            # Get allergen name
            allergen_name = allergen["name"]
            # Delete allergen from the database
            mongo.db.allergens.delete_one(
                {"_id": (ObjectId(allergen_id))})
            # Display flash message
            flash(
                "Allergen " + allergen_name +
                " succesfully deleted", "success")
            return redirect(url_for('products.search'))
        else:
            # Display flash message
            flash(
                "Ooops.... selected allergen no longer " +
                "exists in the database", "danger")
            return redirect(url_for('allergens.allergen_delete'))

    allergen = mongo.db.allergens.find_one(
        {"_id": (ObjectId(allergen_id))})
    return render_template(
        "allergen_delete_confirm.html",
        allergen_id=allergen_id, allergen=allergen)


def allergen_check(allergen_name):
    """
    Check if allergen name already exists in the database
    """
    allergen_check = True
    if mongo.db.allergens.find_one({"name": allergen_name}):
        # Display flash message
        flash("Allergen already exists", "warning")
        allergen_check = False
    return allergen_check


def allergen_get_id(allergen_name):
    """
    Get allergen id from allergen name
    """
    allergen = mongo.db.allergens.find_one({"name": allergen_name})
    allergen_id = None
    # Check if allergen exists in database
    if allergen:
        allergen_id = allergen["_id"]
    else:
        flash(
            "Ooops.... allergen " + allergen_name +
            " no longer exists in the database", "danger")
    return allergen_id


def allergen_get_selection(allergen_method):
    """
    Returns allergen name selected in Allergen Selector
    """
    # Get existing allergen name
    allergen_name = request.form.get("allergenSelector").lower()
    # If allergen has not been selected
    if allergen_name == "allergen...":
        # Display flash message
        flash("Please select Allergen to " + allergen_method, "warning")
        allergen_name = None
    return allergen_name


def allergen_update(allergen_id, allergen_name):
    """
    Update allergen in the database given allergen id and new allergen name
    Returns allergen name
    """
    mongo.db.allergens.update(
        {"_id": ObjectId(allergen_id)}, {"name": allergen_name})
    flash("Allergen " + allergen_name + " succesfully updated", "success")
    return allergen_name
