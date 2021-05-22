# Import dependencies
from flask import (
    Blueprint, Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Import PyMongo database instance
from database import mongo


# Initiate Blueprint
userauth = Blueprint("products", __name__, static_folder="static",
                 template_folder="templates")

# Route for search products