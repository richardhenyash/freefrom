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
from userauth import User
from categories import Category
from allergens import Allergen

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
        if search_str == "":
            search_str = None

        # Get category from form
        category = request.form.get("categorySelector")
        # Set category and category_id variables to None
        # if no category is selected
        if category == "Category...":
            category = None
            category_id = None
        # Otherwise get category_id from category collection
        else:
            category_id = mongo.db.categories.find_one(
                {"name": category})["_id"]

        # Initialise allergen list
        allergen_list = []
        allergen_id_list = []
        # Cycle through allergens in database
        for allergen in allergens:
            # Get checkbox name
            checkbox_name = allergen["name"] + "Checkbox"
            # Get checkbox value from form
            checkbox_value = request.form.get(checkbox_name)
            # If checkbox is set, add allergen_id to allergen_id_list
            if checkbox_value:
                # Get allergen id from allergen
                # collection based on name returned from checkbox
                allergen_id = mongo.db.allergens.find_one(
                    {"name": checkbox_value})["_id"]
                # Append allergen id to allergen_id_list
                allergen_id_list.append(allergen_id)
                # Append selected allergens to allergen_list
                allergen_list.append(allergen)

        # Build mongo db search dictionary
        search_dict = {}
        if search_str:
            search_dict["$text"] = {"$search": search_str}
        if category_id:
            search_dict["category_id"] = ObjectId(category_id)
        if allergen_id_list:
            search_dict["free_from_allergens"] = {"$all": allergen_id_list}

        # Search the database based on the dictionary
        if search_dict:
            products = list(
                mongo.db.products.find(search_dict))
        else:
            products = list(mongo.db.products.find())

        # Process the search results
        for product in products:

            # get category id from product object
            category_id = product["category_id"]
            category_name = mongo.db.categories.find_one(
                {"_id": category_id})["name"]
            # add category name to product object
            product["category_name"] = category_name

            # process reviews to get average rating
            reviews = product["reviews"]
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
            # initialise allergen list
            allergen_list = []
            # get allergen names from allergen object id's
            for allergen in allergen_id_list:
                allergen_name = mongo.db.allergens.find_one(
                    {"_id": allergen})["name"]
                allergen_list.append(allergen_name)
            # add allergen list to product object
            product["free_from_allergen_names"] = allergen_list
        return render_template(
            "home.html", categories=categories.rewind(),
            allergens=allergens.rewind(), products=products,
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
        # Get selected category
        product_category = request.form.get("categorySelector").lower()
        # Get selected allergens
        allergen_list = get_selected_allergen_list(allergens)
        # Add selected allergen names to selected_allergens list
        selected_allergens = []
        for allergen in allergen_list:
            selected_allergens.append(allergen["name"])
        # Check if category has been selected from drop down
        if form.validate():
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
            proceed = False
        if proceed:
            # Get category id
            product_category_id = mongo.db.categories.find_one(
                {"name": product_category})["_id"]
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
        # Get allergen id's and add to list
        if proceed:
            allergen_id_list = []
            for allergen in allergen_list:
                allergen_id = ObjectId(allergen["_id"])
                if allergen_id:
                    allergen_id_list.append(allergen_id)
        if proceed:
            # Get product rating
            product_rating = form.rating.data
            if product_rating == "":
                product_rating = None
            if product_rating:
                proceed = True
                product_rating = int(product_rating)
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
            user_id = mongo.db.users.find_one({"username": user_name})["_id"]
            # Create instance of product
            new_product = Product(
                product_name, product_manufacturer, user_id,
                product_category_id, "", allergen_id_list,
                [
                    {"user_id": user_id,
                     "rating": product_rating,
                     "review": product_review}])
            new_product.add_one()
            print(new_product.get_info())
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
            selected_allergens=selected_allergens, form=form)

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
    # Instantiate product object from product_id
    product = Product.set_one(product_id)
    if product and request.method == "POST" and form.validate():
        product.update_reviews(product_id, form)
        return redirect(url_for('products.view', product_id=product_id))
    elif product:
        # Set product view form
        product.set_view_form(form)        
        # Get all reviews
        reviews = product.get_reviews()
        # Get user review
        user_review = product.get_user_review(form)

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
    categories = Category.get_all()
    # Get allergens collection from database
    allergens = Allergen.get_all()
    # Get product from product_id
    product = Product.get_one(product_id)
    # Create an instance of the Product class from product_id
    productobj = Product.set_one(product_id)
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
            allergen_list = get_selected_allergen_list(allergens)
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

    # Set product edit form fields
    productobj.set_edit_form(form)
    # Get Category name
    product_category = Category.get_name(productobj.category_id)
    # Get Selected allergens list
    selected_allergens = productobj.free_from_allergens
    # Set user product flag
    user_product = productobj.user_product()
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
        Product.delete_one(product_id)
        return redirect(url_for('products.search'))

    product = Product.get_one(product_id)
    print(product)
    return render_template(
        "product_delete_confirm.html", product_id=product_id, product=product)


def get_selected_allergen_list(allergens):
    allergen_list = []
    for allergen in allergens.rewind():
        # Get checkbox name
        checkbox_name = allergen["name"] + "Checkbox"
        # Get checkbox value from form
        checkbox_value = request.form.get(checkbox_name)
        # If checkbox is set, add allergen to allergen_list
        if checkbox_value:
            # Append selected allergens to allergen_list
            allergen_list.append(allergen)
    return(allergen_list)


"""
Product Class
=============
Contains the Product Class to enable create, read, update and delete of
products stored in the MongoDB and preparaton of data
Classes: Product
"""


class Product():
    """
    A class that represents a Product.
    Performs the relevant database CRUD functionality
    along with data preparation.
    """
    def __init__(self, name, manufacturer, user_id, category_id, barcode,
                 free_from_allergens, reviews, _id=None):
        """
        Product initialisation
        """
        self._id = _id
        self.name = name
        self.manufacturer = manufacturer
        self.user_id = user_id
        self.category_id = category_id
        self.barcode = barcode
        self.free_from_allergens = free_from_allergens
        self.reviews = reviews

    def get_info(self):
        """
        Formats and returns the current Product object attributes as a.
        dictionary. The format of the dictionary allows the return
        of this method to be written directly to the Database.
        """
        info = {"name": self.name, "manufacturer": self.manufacturer,
                "user_id": self.user_id, "category_id": self.category_id,
                "barcode": self.barcode,
                "free_from_allergens": self.free_from_allergens,
                "reviews": self.reviews}
        return info

    def add_one(self):
        """
        Adds a Product to the Database.
        Writes the output of the get_info method directly to the database.
        """
        mongo.db.products.insert_one(self.get_info())

    def update_one(self, product_id):
        """
        Updates a Product in the Database.
        Writes the output of the get_info method directly to the database.
        """
        # Update product in database
        mongo.db.products.update(
            {"_id": ObjectId(product_id)}, self.get_info())

    def update_reviews(self, product_id, form):
        """
        Updates a Product review in the database for the signed in user
        from the Product view form input.
        """
        # Get user name
        user_name = session["user"]
        # Get user id from user name
        user_id = User.get_id(user_name)
        # Set new review flag
        review_newflag = True
        # Get reviews
        reviews = self.reviews
        # Loop through reviews, find review that belongs to logged in user
        for review in reviews:
            # Update user review if user has reviewed product before
            if review["user_id"] == user_id:
                review["rating"] = int(form.rating.data)
                review["review"] = form.review.data
                review_newflag = False
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
        self.reviews = reviews
        self.update_one(product_id)
        flash(
            "Rating and review succesfully " +
            "updated for " + self.name,
            "success")

    def get_reviews(self):
        """
        Gets all Product reviews and returns a list of reviews including user names.
        """
        # Get user name
        reviews_new = []
        for review in self.reviews:
            # Get user name
            username = User.get_name(review["user_id"])
            # Set new review object including user name
            review_new = {"username": username, "rating": review["rating"], "review": review["review"]}
            # Append to new reviews list
            reviews_new.append(review_new)
        return(reviews_new)

    def get_user_review(self, form):
        """
        Gets Product review belonging to the logged in user
        from the database and populates the product view form.
        """
        # Get user name
        user_review = None
        other_user_reviews = None
        if session:
            # Get user name
            user_name = session["user"]
            # Get user id from user name
            user_id = User.get_id(user_name)
            # Initialise other user review list
            other_user_reviews = []
            # Cycle through product reviews
            for review in self.reviews:
                # If review belongs to logged in user
                if review["user_id"] == (ObjectId(user_id)):
                    user_review = review
                    # Set rating in form object
                    form.rating.data = user_review["rating"]
                    # Set review in form object
                    form.review.data = user_review["review"]
            return(user_review)

    def set_view_form(self, form):
        """
        Sets product view form from the Product object.
        """
        form.name.data = self.name
        form.category.data = Category.get_name(self.category_id)
        form.manufacturer.data = self.manufacturer
        product_free_from_allergens_list = []
        # Get allergen names from allergen id's
        for allergen_id in self.free_from_allergens:
            product_free_from_allergens_list.append(Allergen.get_name(allergen_id))
        # Set free from field in form object
        form.freefrom.data = ', '.join(
            map(str, product_free_from_allergens_list))
        return(form)

    def set_edit_form(self, form):
        """
        Sets product edit form from the Product object.
        """
        form.name.data = self.name
        form.manufacturer.data = self.manufacturer
        return(form)

    def user_product(self):
        # Get user name
        user_name = session["user"]
        # Get user id from user name
        user_id = User.get_id(user_name)
        # Check if product is owned by user
        if self.user_id == user_id:
            user_product = True
        else:
            user_product = False
        return user_product

    @staticmethod
    def delete_one(product_id):
        """
        Removes a Product from the database
        """
        product_name = Product.get_name(product_id)
        mongo.db.products.delete_one({"_id": ObjectId(product_id)})
        flash(
            product_name +
            " succesfully deleted from products", "success")
        return(product_id)

    @staticmethod
    def get_name(product_id):
        """
        Gets a product name from a Product Object ID
        """
        product_name = mongo.db.products.find_one(
            {"_id": (ObjectId(product_id))})["name"]
        return(product_name)

    @staticmethod
    def get_one(product_id):
        """
        Gets a Product object from the database, given the ObjectID
        """
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        return (product)
    
    @staticmethod
    def get_user_id(product_id):
        """
        Gets a product user ID from a Product Object ID
        """
        user_id = mongo.db.products.find_one(
            {"_id": (ObjectId(product_id))})["user_id"]
        return(user_id)
    
    @classmethod
    def set_one(cls, product_id):
        """
        Returns a Product from the database and creates
        a Product instance with the returned data, given the ObjectID
        """
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        return cls(**product)

    
