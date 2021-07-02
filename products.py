#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Products Python module
Version 1.1.1
"""
# Import dependencies
from flask import (
    Blueprint, flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from forms import ProductForm, ProductEditForm, ProductViewForm
from allergens import (allergen_get_id_list,
                       allergen_get_name_list_from_id_list,
                       allergen_get_selected_checkboxes)
from categories import (category_get_id, category_get_name,
                        category_get_selection)
from userauth import user_get

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
products = Blueprint(
    "products", __name__, static_folder="static",
    template_folder="templates")


@products.route("/search", methods=["GET", "POST"])
def search():
    """
    Route for products search
    """
    # Get categories collection from database
    categories = mongo.db.categories.find().sort("name", 1)
    # Get allergens collection from database
    allergens = mongo.db.allergens.find().sort("name", 1)
    if request.method == "POST":
        # Get search string from form
        search_str = request.form.get("search").lower()
        # Set search_str to None if not specified
        search_str = None if (search_str == "") else search_str
        # Get category from form
        category = request.form.get("categorySelector").lower()
        # Set category to None if not specified
        category = None if (category == "category...") else category
        # Get category_id if category is specified, oelse set category to None
        category_id = category_get_id(category) if category else None
        allergen_list = allergen_get_selected_checkboxes(allergens)
        allergen_id_list = allergen_get_id_list(allergen_list)
        # Build products search dictionary
        search_dict = product_get_search_dict(
            search_str, category_id, allergen_id_list)
        # Search the database based on the dictionary
        if search_dict:
            products = list(
                mongo.db.products.find(search_dict))
        else:
            products = list(mongo.db.products.find())
        products = product_process_search_results(products)
        return render_template(
            "home.html", categories=categories.rewind(),
            allergens=allergens.rewind(), products=products,
            selected_category=category, search_str=search_str,
            selected_allergens=allergen_list)
    return render_template(
        "home.html", categories=categories,
        allergens=allergens)


@products.route("/add", methods=["GET", "POST"])
def add():
    """
    Route for products add
    """
    # request Form data
    form = ProductForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find().sort("name", 1)
    # Get allergens collection from database
    allergens = mongo.db.allergens.find().sort("name", 1)
    # Validate form
    if request.method == "POST":
        # Get product name, manufacturer and category
        product_name = form.name.data.lower()
        product_manufacturer = form.manufacturer.data.lower()
        product_category = request.form.get("categorySelector").lower()
        allergen_list = allergen_get_selected_checkboxes(allergens)
        # Check if category has been selected from drop down
        cstr = ("add Product. " +
                "If you would like to add a product category, " +
                "please contact the site Administrator")
        proceed = False
        if product_check(product_name) and form.validate():
            product_category = category_get_selection(cstr)
            if product_category:
                proceed = True
        if proceed:
            product_category_id = category_get_id(product_category)
            # Check if any allergens are selected
            if allergen_list:
                proceed = True
            else:
                # Display flash message
                flash(
                    ("Please select allergens " +
                        "that the product is Free From. " +
                        "If you would like to add an Allergen, " +
                        "please contact the site Administrator"),
                    "warning")
                proceed = False
        if proceed:
            allergen_id_list = allergen_get_id_list(allergens)
        if proceed:
            # Get product rating
            product_rating = form.rating.data
            product_rating = None if product_rating == "" else int(
                product_rating)
            if product_rating:
                proceed = True
            else:
                # Display flash message
                flash("Please rate product", "warning")
                proceed = False
        if proceed:
            # Get product review
            product_review = form.review.data
            # Get user name
            user_name = session["user"]
            # Get user id from user name
            user_id = user_get(user_name)["_id"]
            # Set new product variable
            new_product = {
                "name": product_name,
                "manufacturer": product_manufacturer,
                "user_id": user_id,
                "category_id": product_category_id,
                "barcode": "",
                "free_from_allergens": allergen_id_list,
                "reviews": [{
                    "user_id": user_id,
                    "rating": product_rating,
                    "review": product_review
                }]
            }
            # Add new record to the database
            mongo.db.products.insert_one(new_product)
            # Display flash message
            flash(
                product_name + " succesfully added" +
                " to products", "success")
            form.name.data = None
            form.manufacturer.data = None
            form.rating.data = None
            form.review.data = None
            product_id = mongo.db.products.find_one(
                {"name": product_name})["_id"]
            return redirect(url_for('products.view', product_id=product_id))
        return render_template(
            "product_add.html", categories=categories.rewind(),
            allergens=allergens.rewind(),
            product_category=product_category,
            selected_allergens=allergen_list, form=form)

    form.rating.data = None
    return render_template(
        "product_add.html", categories=categories.rewind(),
        allergens=allergens.rewind(), form=form)


@products.route("/view/<product_id>", methods=["GET", "POST"])
def view(product_id):
    """
    Route for product view
    """
    # request Form data
    form = ProductViewForm(request.form)
    # Get product from product_id
    product = mongo.db.products.find_one({"_id": (ObjectId(product_id))})
    if product and request.method == "POST" and form.validate():
        # Get user name
        user_name = session["user"]
        # Get user id from user name
        user_id = mongo.db.users.find_one({"username": user_name})["_id"]
        # Set new review flag
        review_newflag = True
        # Get reviews
        reviews = product["reviews"]
        # Loop through reviews, find review that belongs to logged in user
        for review in reviews:
            # Update user review
            if review["user_id"] == user_id:
                review["rating"] = int(form.rating.data)
                review["review"] = form.review.data
                review_newflag = False
                user_review = {
                    "user_id": user_id,
                    "rating": int(form.rating.data),
                    "review": form.review.data
                }
        # If user has not reviewed product before
        if review_newflag:
            # Create new review object
            review_new = {
                "user_id": user_id,
                "rating": int(form.rating.data),
                "review": form.review.data
            }
            # Append new review to reviews
            reviews.append(review_new)
            # Update product object with new or edited review
            product["reviews"] = reviews

        # Update product in database
        mongo.db.products.update({"_id": ObjectId(product_id)}, product)
        # Display flash message
        flash(
            "Rating and review succesfully " +
            "updated for " + product["name"],
            "success")
        return redirect(url_for('products.view', product_id=product_id))
    elif product:
        # Set product name in form object
        form.name.data = product["name"]
        # Get category id from product object
        category_id = product["category_id"]
        # Get category name from categories collection
        category_name = mongo.db.categories.find_one(
            {"_id": category_id})["name"]
        # Set category name in form object
        form.category.data = category_name
        # Set manufacturer name in form object
        form.manufacturer.data = product["manufacturer"]
        # Get product allergen id list
        product_allergen_id_list = product["free_from_allergens"]
        # Get allergen names from allergen collection
        product_free_from_allergens_list = []
        for allergen_id in product_allergen_id_list:
            allergen_name = mongo.db.allergens.find_one(
                {"_id": allergen_id})["name"]
            product_free_from_allergens_list.append(allergen_name)
        # Set free from in form object
        form.freefrom.data = ', '.join(
            map(str, product_free_from_allergens_list))

        # Get user name
        user_review = None
        if session:
            # Get user name
            user_name = session["user"]
            # Get user id from user name
            user_id = mongo.db.users.find_one({"username": user_name})["_id"]
            # Cycle through product reviews
            for review in product["reviews"]:
                # If review belongs to logged in user
                if review["user_id"] == (ObjectId(user_id)):
                    user_review = review
                    # Set rating in form object
                    form.rating.data = user_review["rating"]
                    # Set review in form object
                    form.review.data = user_review["review"]
        reviews = product_get_reviews(product)

        return render_template(
            "product_view.html",
            product=product, product_id=product_id,
            user_review=user_review, reviews=reviews,
            form=form)
    else:
        flash("Ooops.... product not found :)", "danger")
        return redirect(url_for('products.search'))


@products.route("/edit/<product_id>", methods=["GET", "POST"])
def edit(product_id):
    """
    Route for product edit
    """
    # request Form data
    form = ProductEditForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find().sort("name", 1)
    # Get allergens collection from database
    allergens = mongo.db.allergens.find().sort("name", 1)
    # Get product from product_id
    product = mongo.db.products.find_one(
        {"_id": (ObjectId(product_id))})
    if request.method == "POST" and form.validate():
        # Get product name from form
        product_name = form.name.data
        # Get product manufacturer from form
        product_manufacturer = form.manufacturer.data
        # Get product category
        product_category = request.form.get(
            "categorySelector").lower()
        # Check if category has been selected from drop down
        if product_category:
            if product_category == "category...":
                # Display flash message
                flash(
                    ("Please select Product Category. " +
                        "If you would like to add a product category, " +
                        "please contact the site Administrator"),
                    "warning")
                proceed = False
            else:
                proceed = True
        else:
            # Display flash message
            flash(
                ("Please select Product Category. " +
                    "If you would like to add a product category, " +
                    "please contact the site Administrator"),
                "warning")
            proceed = False
        if proceed:
            # Get category id
            product_category_id = mongo.db.categories.find_one(
                {"name": product_category})["_id"]
            # Get selected allergens
            allergen_list = allergen_get_selected_checkboxes(allergens)
            # Check if any allergens are selected
            if allergen_list:
                proceed = True
            else:
                # Display flash message
                flash(
                    ("Please select allergens that the" +
                        "product is Free From. " +
                        "If you would like to add an Allergen, " +
                        "please contact the site Administrator"),
                    "warning")
                proceed = False
        # Get allergen id's and add to list
        if proceed:
            allergen_id_list = []
            for allergen in allergen_list:
                allergen_id = ObjectId(allergen["_id"])
                if allergen_id:
                    allergen_id_list.append(allergen_id)
        # Get user name
        user_name = session["user"]
        # Get user id from user name
        user_id = mongo.db.users.find_one({"username": user_name})["_id"]
        # Placeholder for barcode, may be added in the future
        barcode = ""
        if proceed:
            # Set product update variable
            product_update = {
                "name": product_name,
                "manufacturer": product_manufacturer,
                "user_id": user_id,
                "category_id": product_category_id,
                "barcode": barcode,
                "free_from_allergens": allergen_id_list,
                "reviews": product["reviews"]
            }
            # Update product in database
            mongo.db.products.update(
                {"_id": ObjectId(product_id)}, product_update)
            # Display flash message
            flash(product_name + " succesfully updated", "success")
            return redirect(url_for('products.view', product_id=product_id))

    # Update product name in form
    form.name.data = product["name"]
    # Update product manufcaturer in form
    form.manufacturer.data = product["manufacturer"]
    # Get product category id
    product_category_id = product["category_id"]
    # Get product category
    product_category = mongo.db.categories.find_one(
        {"_id": product_category_id})["name"]
    # Get Selected allergens
    selected_allergens = product["free_from_allergens"]
    # Get user name
    user_name = session["user"]
    # Get user id from user name
    user_id = mongo.db.users.find_one({"username": user_name})["_id"]
    if product["user_id"] == user_id:
        user_product = True
    else:
        user_product = False
    return render_template(
        "product_edit.html", categories=categories.rewind(),
        allergens=allergens.rewind(), product_id=product_id,
        product_category=product_category,
        selected_allergens=selected_allergens,
        user_product=user_product, form=form)


@products.route("/delete/<product_id>", methods=["GET", "POST"])
def delete(product_id):
    """
    Route for product delete
    """
    if request.method == "POST":
        # Get product name from database
        product_name = mongo.db.products.find_one(
            {"_id": (ObjectId(product_id))})["name"]
        # Delete product from database
        mongo.db.products.delete_one({"_id": (ObjectId(product_id))})
        flash(
            product_name +
            " succesfully deleted from products", "success")
        return redirect(url_for('products.search'))

    product = mongo.db.products.find_one(
        {"_id": (ObjectId(product_id))})
    return render_template(
        "product_delete_confirm.html", product_id=product_id, product=product)


def product_check(product_name):
    """
    Check if product name already exists in the database
    """
    if mongo.db.products.find_one({"name": product_name}):
        # Display flash message
        flash(product_name +
              " already exists in the database", "warning")
        product_check = False
    else:
        product_check = True
    return(product_check)


def product_get_reviews(product):
    """
    Return reviews for product, with username
    """
    # Initialise review list
    reviews = []
    # Cycle through product reviews
    for review in product["reviews"]:
        user = mongo.db.users.find_one(
            {"_id": (ObjectId(review["user_id"]))})
        if user:
            # Get user name
            user_name = user["username"]
            user_review = {
                "username": user_name,
                "rating": review["rating"],
                "review": review["review"]
            }
            reviews.append(user_review)
    return reviews


def product_get_search_dict(search_str, category_id, allergen_id_list):
    """
    Return product search dictionary
    """
    search_dict = {}
    if search_str:
        search_dict["$text"] = {"$search": search_str}
    if category_id:
        search_dict["category_id"] = ObjectId(category_id)
    if allergen_id_list:
        search_dict["free_from_allergens"] = {"$all": allergen_id_list}
    return search_dict


def product_process_search_results(products):
    """
    Process product search results, add category name, average rating and
    allergen names to product object
    """
    for product in products:
        # Add category name to product object
        product["category_name"] = category_get_name(product["category_id"])
        # Process reviews to get average rating and add to product object
        reviews = product["reviews"]
        # Initialise rating quantity counter
        rq = 0
        # Initialise totalrating counter
        totalrating = 0
        # Calculate average rating from reviews
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
        # Get allergen id's
        allergen_id_list = product["free_from_allergens"]
        # Get allergen names
        allergen_name_list = allergen_get_name_list_from_id_list(
            allergen_id_list)
        product["free_from_allergen_names"] = allergen_name_list
    return products
