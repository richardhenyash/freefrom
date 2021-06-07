# Import dependencies
from flask_pymongo import PyMongo

# Create an instance of PyMongo, assigned to the varable mongo
try:
    mongo = PyMongo()
except:
    print("Could not connect to the Mongo DB")
