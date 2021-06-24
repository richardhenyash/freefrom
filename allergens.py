#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Allergens Python module
Version 1.1.1
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
        # Get existing allergen name
        existing_allergen_name = request.form.get(
            "allergenSelector").lower()
        # Check if allergen has been selected from drop down
        if existing_allergen_name:
            if existing_allergen_name == "allergen...":
                # Display flash message
                flash("Please select Allergen to update", "warning")
                proceed = False
            else:
                proceed = True
        else:
            # Display flash message
            flash("Please select Allergen to update", "warning")
            proceed = False
        if proceed:
            # Set new allergen name variable
            allergen_name = form.name.data.lower()
            # Check if new allergen name exists in database
            if mongo.db.allergens.find_one({"name": allergen_name}):
                # Display flash message
                flash("Allergen already exists", "warning")
                proceed = False
        if proceed:
            # Get allergen id
            allergen = mongo.db.allergens.find_one(
                {"name": existing_allergen_name})
            # Check if allergen is still in database
            if allergen:
                allergen_id = allergen["_id"]
                # Update allergen in the database
                allergen_update = {"name": allergen_name}
                mongo.db.allergens.update(
                    {"_id": ObjectId(allergen_id)}, allergen_update)
                # Display flash message
                flash(
                    "Allergen " + allergen_name +
                    " succesfully updated", "success")
                return redirect(url_for('products.search'))
            else:
                # Display flash message
                flash(
                    "Ooops.... allergen " + existing_allergen_name +
                    " no longer exists in the database", "danger")
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
        existing_allergen_name = request.form.get("allergenSelector").lower()
        # Check if allergen has been selected from drop down
        if existing_allergen_name:
            if existing_allergen_name == "allergen...":
                # Display flash message
                flash("Please select Allergen to delete", "warning")
                proceed = False
            else:
                proceed = True
        else:
            # Display flash message
            flash("Please select Allergen to delete", "warning")
            proceed = False
        if proceed:
            # Get allergen
            allergen = mongo.db.allergens.find_one(
                {"name": existing_allergen_name})
            # Check if allergen is still in database
            if allergen:
                allergen_id = allergen["_id"]
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

    
"""
Allergen Class
=============
Contains the Allergen Class to enable create, read, update and delete of
allergens stored in the MongoDB and preparaton of data
Classes: Allergen
"""


class Allergen():
    """
    A class that represents an Allergen.
    Performs the relevant database CRUD functionality
    along with data preparation.
    """
    def __init__(self, name, _id=None):
        """
        Allergen initialisation
        """
        self._id = _id
        self.name = name

    def get_info(self):
        """
        Formats and returns the current Allergen object attributes as
        a dictionary. The format of the dictionary allows the return
        of this method to be written directly to the Database.
        """
        info = {"name": self.name}

    @staticmethod
    def get_all():
        allergens = mongo.db.allergens.find().sort("name", 1)
        return(allergens)

    @staticmethod
    def get_id(allergen_name):
        """
        Gets an allergen ObjectId from an allergen name
        """
        allergen_id = mongo.db.allergens.find_one({"name": allergen_name})["_id"]
        return(allergen_id)
    
    @staticmethod
    def get_name(allergen_id):
        """
        Gets an allergen name from an allergen ObjectId
        """
        allergen_name = mongo.db.allergens.find_one({"_id": allergen_id})["name"]
        return(allergen_name)

