# Import dependencies
import os
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Import Blueprints
from userauth import userauth
from products import products

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

# Configure database access variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Initiate instance of PyMongo
# mongo = PyMongo(app)
mongo.init_app(app)


@app.route("/")
def home():
    """
    Route for home
    """
    categories = mongo.db.categories.find()
    allergens = mongo.db.allergens.find()
    return render_template("home.html", categories=categories, allergens=allergens)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Update to debug=False prior to deployment/submission
            debug=True)

