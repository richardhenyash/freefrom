# Import dependencies
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import ProductForm, ProductEditForm, ProductViewForm

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
products = Blueprint("products", __name__, static_folder="static",
                 template_folder="templates")


@products.route("/search", methods=["GET", "POST"])
def search():
    """
    Route for products search
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


@products.route("/add", methods=["GET", "POST"])
def add():
    """
    Route for products add
    """
    # request Form data
    form = ProductForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    # Validate form
    if request.method == "POST" and form.validate():
        # Get product name, manufacturer and category
        product_name = form.name.data.lower()
        product_manufacturer = form.manufacturer.data.lower()
        product_category = request.form.get("categorySelector").lower()
        # Check if category has been selected from drop down
        if product_category:
            if product_category == "category...":
                # Display flash message
                flash("Please select Product Category. If you would like to add a product category, please contact the site Administrator", "warning")
                proceed = False
            else:
                proceed = True
        else:
            # Display flash message
            flash("Please select Product Category. If you would like to add a product category, please contact the site Administrator", "warning")
            proceed = False
        if proceed:
            # Get category id
            product_category_id = mongo.db.categories.find_one({"name": product_category})["_id"]
            # Get selected allergens
            allergen_list = get_selected_allergen_list(allergens)
            # Check if any allergens are selected
            if allergen_list:
                proceed = True
            else:
                # Display flash message
                flash("Please select allergens that the product is Free From. If you would like to add an Allergen, please contact the site Administrator", "warning")
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
            flash("Product succesfully added", "success")
            form.name.data = None
            form.manufacturer.data = None
            form.rating.data = None
            form.review.data = None

        return render_template(
            "product_add.html", categories=categories.rewind(), allergens=allergens.rewind(), form=form)
    
    form.rating.data = None
    return render_template("product_add.html", categories=categories.rewind(), allergens=allergens.rewind(), form=form)


@products.route("/view/<product_id>", methods=["GET", "POST"])
def view(product_id):
    """
    Route for product view
    """
    # request Form data
    form = ProductViewForm(request.form)#
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    # Validate form
    #if request.method == "POST" and form.validate():
    # Get product from product_id
    product = mongo.db.products.find_one({"_id": (ObjectId(product_id))})
    print(product)
    form.name.data = product["name"]
    category_id = product["category_id"]
    category_name = mongo.db.categories.find_one({"_id": category_id})["name"]
    form.category.data = category_name
    form.manufacturer.data = product["manufacturer"]
    product_allergen_id_list = product["free_from_allergens"]
    product_free_from_allergens_list = []
    for allergen_id in product_allergen_id_list:
        allergen_name = mongo.db.allergens.find_one({"_id": allergen_id})["name"]
        product_free_from_allergens_list.append(allergen_name)
    form.freefrom.data = ', '.join(map(str, product_free_from_allergens_list)).title()
        
    # Get user name
    user_review = None
    if session:
        # Get user name
        user_name = session["user"]
        # Get user id from user name
        user_id = mongo.db.users.find_one({"username": user_name})["_id"]
        product_reviews = product["reviews"]
        for review in product_reviews:
            print(review["user_id"])
            print(ObjectId(user_id))
            if review["user_id"] == (ObjectId(user_id)):
                user_review = review
                form.rating.data = user_review["rating"]
                form.review.data = user_review["review"]
    return render_template("product_view.html", product=product, product_id=product_id, form=form)

@products.route("/edit<product_id>", methods=["GET", "POST"])
def edit(product_id):
    """
    Route for product edit
    """
    # request Form data
    form = ProductEditForm(request.form)
    # Get categories collection from database
    categories = mongo.db.categories.find()
    # Get allergens collection from database
    allergens = mongo.db.allergens.find()
    # Get products collection from database
    products = mongo.db.products.find()
    # Get product from product_id
    product = mongo.db.products.find_one({"_id": (ObjectId(product_id))})
    if request.method == "POST" and form.validate():
        # Get product name from form
        product_name = form.name.data
        # Get product manufacturer from form
        product_manufacturer = form.manufacturer.data
        # Get product category
        product_category = request.form.get("categorySelector").lower()
        # Check if category has been selected from drop down
        if product_category:
            if product_category == "category...":
                # Display flash message
                flash("Please select Product Category. If you would like to add a product category, please contact the site Administrator", "warning")
                proceed = False
            else:
                proceed = True
        else:
            # Display flash message
            flash("Please select Product Category. If you would like to add a product category, please contact the site Administrator", "warning")
            proceed = False
        if proceed:
            # Get category id
            product_category_id = mongo.db.categories.find_one({"name": product_category})["_id"]
            # Get selected allergens
            allergen_list = get_selected_allergen_list(allergens)
            # Check if any allergens are selected
            if allergen_list:
                proceed = True
            else:
                # Display flash message
                flash("Please select allergens that the product is Free From. If you would like to add an Allergen, please contact the site Administrator", "warning")
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
            print(product_update)
            # Update product in database
            mongo.db.products.update({"_id": ObjectId(product_id)}, product_update)
            # Display flash message
            flash("Product succesfully updated", "success")
            product_view_form = ProductViewForm(request.form)
            return render_template("product_view.html", product=product_update, product_id=product_id, form=product_view_form)
    
    # Update product name in form
    form.name.data = product["name"]
    # Update product manufcaturer in form
    form.manufacturer.data = product["manufacturer"]
    # Get product category id
    product_category_id = product["category_id"]
    # Get product category
    product_category = mongo.db.categories.find_one({"_id": product_category_id})["name"]
    # Get Selected allergens
    selected_allergens = product["free_from_allergens"]
    return render_template("product_edit.html", categories=categories.rewind(), allergens=allergens.rewind(), product_id=product_id, product_category=product_category, selected_allergens=selected_allergens, form=form)

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
    # If allergen list is empty, set to None
    if len(allergen_list) == 0:
        allergen_list = None
    return(allergen_list)
    
