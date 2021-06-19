#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Application Python module
Version 1.1.1
"""
# Import dependencies
import os
from bson import errors
from flask import (Flask, render_template)

# Import Blueprints
from userauth import userauth
from products import products
from allergens import allergens
from categories import categories
from mail import mail

# Import PyMongo database instance
from database import mongo

# Import environment variables, if running locally
if os.path.exists("env.py"):
    import env

# Initiate instance of Flask application
app = Flask(__name__)

# Blueprints
# Blueprint for user authentication
app.register_blueprint(userauth)
# Blueprint for products
app.register_blueprint(products)
# Blueprint for allergens
app.register_blueprint(allergens)
# Blueprint for categories
app.register_blueprint(categories)
# Blueprint for contact
app.register_blueprint(mail)

# Configure database access variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Initiate instance of PyMongo
mongo.init_app(app)


@app.route("/")
def home():
    """
    Route for home
    """
    categories = mongo.db.categories.find()
    allergens = mongo.db.allergens.find()
    if categories and allergens:
        return render_template(
            "home.html", categories=categories, allergens=allergens)
    else:
        print("Could not connect to the Mongo DB")


@app.errorhandler(Exception)
def error_generic(e):
    """
    Generic error handler
    """
    errstr = "something went wrong"
    return render_template('error.html', error=errstr), 500


@app.errorhandler(404)
def error_page_not_found(e):
    """
    Error handler for page not found
    """
    errstr = "looks like you've lost your way"
    return render_template('error.html', error=errstr), 404


@app.errorhandler(errors.InvalidId)
def error_invalid_id(e):
    """
    Error handler for invalid bson id
    """
    errstr = "product not found"
    return render_template('error.html', error=errstr), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Update to debug=False prior to deployment/submission
            debug=True)
