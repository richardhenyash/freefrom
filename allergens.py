# Import dependencies
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import AllergenAddForm

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
    form = AllergenAddForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    if request.method == "POST" and form.validate():
        # Set new allergen variable
        allergen_name = form.name.data.lower()
        print(allergen_name)
        # Check if allergen name exists in database
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