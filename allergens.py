# Import dependencies
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import AllergenForm

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
allergens = Blueprint("allergens", __name__, static_folder="static",
                 template_folder="templates")


@allergens.route("/allergen_add", methods=["GET", "POST"])
def allergen_add():
    """
    Route for allergen add
    """
    # request Form data
    form = AllergenForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    if request.method == "POST" and form.validate():
        # Set new allergen name variable
        allergen_name = form.name.data.lower()
        # Check if new allergen name exists in database
        if mongo.db.allergens.find_one({"name": allergen_name}):
            # Display flash message
            flash("Allergen already exists in database", "warning")
            return render_template("allergen_add.html", form=form)
        else:
            # Add new allergen to the database
            mongo.db.allergens.insert_one({"name":allergen_name})
            # Display flash message
            flash("Allergen succesfully added to the database", "success")
        return render_template("home.html", categories=categories, allergens=allergens, form=form)
    return render_template("allergen_add.html", form=form)

@allergens.route("/allergen_edit", methods=["GET", "POST"])
def allergen_edit():
    """
    Route for allergen edit
    """
    # request Form data
    form = AllergenForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    if request.method == "POST" and form.validate():
        # Get existing allergen name
        existing_allergen_name = request.form.get("allergenSelector").lower()
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
                flash("Allergen already exists in database", "warning")
                proceed = False
        if proceed:
            # Get allergen id
            allergen_id = mongo.db.allergens.find_one({"name": existing_allergen_name})["_id"]
            # Update allergen in the database
            allergen_update = {"name": allergen_name}
            mongo.db.allergens.update({"_id": ObjectId(allergen_id)}, allergen_update)
            # Display flash message
            flash("Allergen succesfully updated in the database", "success")
            return render_template("home.html", categories=categories, allergens=allergens, form=form)
        else:
            return render_template("allergen_edit.html", allergens=allergens, form=form)
        
    return render_template("allergen_edit.html", allergens=allergens, form=form)


@allergens.route("/allergen_delete", methods=["GET", "POST"])
def allergen_delete():
    """
    Route for allergen delete
    """
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    # Get categories collection from database
    categories = mongo.db.categories.find()
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
            # Get allergen id
            allergen_id = mongo.db.allergens.find_one({"name": existing_allergen_name})["_id"]
            # Delete allergen from the database
            mongo.db.allergens.remove({"_id": ObjectId(allergen_id)})
            # Display flash message
            flash("Allergen succesfully deleted from the database", "success")
            return render_template("home.html", categories=categories, allergens=allergens)
        else:
            return render_template("allergen_delete.html", allergens=allergens)
        
    return render_template("allergen_delete.html", allergens=allergens)