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
        # process search results
        for product in products:

            # get category id from product object
            category_id = product["category_id"]
            category_name = mongo.db.categories.find_one({"_id": category_id})["name"]
            # add category name to product object
            product["category_name"] = category_name

            # process reviews to get average rating
            reviews=product["reviews"]
            # initialise rating quantity counter
            rq = 0
            # initialise totalrating counter
            totalrating = 0
            # calculate average rating from reviews
            for review in reviews:
                rating = review["rating"]
                if rating:
                    totalrating = totalrating + rating
                    rq = rq + 1
            # if product has been rated
            if totalrating > 0:
                avrating = round(((totalrating / rq) * 2)) / 2
                # avrating = round(totalrating / rq)
                # add average rating to product object
                product["average_rating"] = avrating

            # get allergens from product object
            allergen_id_list = product["free_from_allergens"]
            print(allergen_id_list)
            # initialise allergen list
            allergen_list = []
            # get allergen names from allergen object id's
            for allergen in allergen_id_list:
                allergen_name = mongo.db.allergens.find_one({"_id": allergen})["name"]
                allergen_list.append(allergen_name)
                print(allergen_name)
            # add allergen list to product object
            product["free_from_allergen_names"] = allergen_list
        print(products)
        return render_template("home.html", categories=categories.rewind(), allergens=allergens.rewind(), products=products, selected_allergens=allergen_list)
    return render_template("home.html", categories=categories, allergens=allergens)
