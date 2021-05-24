# Import dependencies
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
products = Blueprint("products", __name__, static_folder="static",
                 template_folder="templates")


@products.route("/search", methods=["GET", "POST"])
def search():
    """
    Route for search
    """
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    if request.method == "POST":
        # Get search string from form
        searchstr = request.form.get("search").lower()
        # Set searchstr to None if not specified
        if searchstr == "":
            searchstr = None

        # Get category from form
        category = request.form.get("categorySelector")
        # Set category variable to None if no category selected
        if category == "Category...":
            category = None
            category_id = None
        # Otherwise get category_id from category collection
        else:
            category_id = mongo.db.categories.find_one({"name": category})["_id"]

        # Initialise allergen list
        allergen_list=[]
        allergen_id_list = []
        # Cycle through allergens in database
        for allergen in allergens:
            # Get checkbox name
            checkbox_name = allergen["name"] + "Checkbox"
            # Get checkbox value from form
            checkbox_value = request.form.get(checkbox_name)
            # If checkbox is set, add allergen_id to allergen_id_list
            if checkbox_value:
                # Get allergen id from allergen collection based on name returned from checkbox
                allergen_id = mongo.db.allergens.find_one({"name": checkbox_value})["_id"]
                # Append allergen id to allergen_id_list
                allergen_id_list.append(allergen_id)
                # Append selected allergens to allergen_list
                allergen_list.append(allergen)
        # If allergen id list is empty, set to None
        if len(allergen_id_list) == 0:
            allergen_id_list = None        
        # If allergen list is empty, set to None
        if len(allergen_list) == 0:
            allergen_list = None

        # Search the database conditionally based on the form inputs

        # If allergen list, category and search string are specified
        if allergen_id_list and category_id and searchstr:
            products = list(mongo.db.products.find({"$text": {"$search": searchstr}, "category_id": ObjectId(category_id), "free_from_allergens": { "$all": allergen_id_list }}))
        # else if allergen list and category are specified and search string is not specified
        elif  allergen_id_list and category_id and (not(searchstr)):
            products = list(mongo.db.products.find({"category_id": ObjectId(category_id), "free_from_allergens": { "$all": allergen_id_list }}))
        # else if allergen list is not specified, category is specified and search string is specified
        elif  (not (allergen_id_list)) and category_id and searchstr:
            products = list(mongo.db.products.find({"$text": {"$search": searchstr}, "category_id": ObjectId(category_id)}))
        # else if allergen list is not specified, category is specified and search string is not specified
        elif (not (allergen_id_list)) and category_id and (not(searchstr)):
            products = list(mongo.db.products.find({"category_id": ObjectId(category_id)}))
        # else if allergen list is specified, category is not specified and search string is specified
        elif allergen_id_list and (not (category_id)) and searchstr:
            products = list(mongo.db.products.find({"$text": {"$search": searchstr}, "free_from_allergens": { "$all": allergen_id_list }}))
        # else if allergen list is specified, category is not specified and search string is not specified
        elif allergen_id_list and (not (category_id)) and (not(searchstr)):
            products = list(mongo.db.products.find({"free_from_allergens": { "$all": allergen_id_list }}))
        # else if allergen list is not specified, category is not specified and search string is specified
        elif (not(allergen_id_list)) and (not (category_id)) and searchstr:
            products = list(mongo.db.products.find({"$text": {"$search": searchstr}}))
        elif (not(allergen_id_list)) and (not (category_id)) and (not(searchstr)):
            products = list(mongo.db.products.find())

        print(products)
        return render_template("home.html", categories=categories.rewind(), allergens=allergens.rewind(), products=products, selected_allergens=allergen_list)
    return render_template("home.html", categories=categories, allergens=allergens)
