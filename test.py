#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Test Python module
Version 1.1.1
"""
# Import dependencies
import os
import unittest
import mongomock
from unittest import mock
from products import (
    product_get_id, product_get_name,
    product_get_search_dict, product_process_search_results)
from bson.objectid import ObjectId


class MockedMongoClient(mongomock.MongoClient):
    """
    MockedMongoClient class
    """
    def init_app(self, app):
        pass


class AppTests(unittest.TestCase):
    """
    AppTests class
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up class prior to each test
        """
        # Replace flask_pymongo.PyMongo with a fake client
        cls.patcher = mock.patch(
            'flask_pymongo.PyMongo', return_value=MockedMongoClient())
        cls.patcher.start()

        # This will instantiate Mongo, so mongomock is required before
        os.environ['SECRET_KEY'] = 'test'

        from app import app

        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Runs at the end of each test
        """
        cls.patcher.stop()

    def test_signout_before_signin(self):
        """
        Test signout before sign in
        """
        response = self.app.get("/signout")
        self.assertEqual(response.status_code, 500)
        self.assertIn('Oops.... something went wrong', str(response.data))

    def test_successful_register_post(self):
        """
        Test succesful user registration
        """
        username = "testuser"
        response = self.app.post("/register", data={
            "username": username,
            "email": "test@gmail.com",
            "password": "test123",
            "confirmpassword": "test123",
        })
        self.assertEqual(response.status_code, 302)
        from database import mongo
        user = mongo.db.users.find_one({"username": username})
        self.assertIsNotNone(user)

    def test_successful_signin_post(self):
        """
        Test successful user signin
        """
        username = "testadmin1"
        password = "testadmin1"
        response = self.app.post("/signin", data={
            "username": username,
            "password": password
        })
        self.assertEqual(response.status_code, 302)
        # Test the session cookie has been created
        self.assertIn("session", (response.headers["Set-Cookie"]))

    def test_successful_product_search_post(self):
        """
        Test successful product search
        """
        response = self.app.post("/search", data={
            "search": "digestives",
            "categorySelector": "biscuits"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("digestives", str(response.data))

    def test_successful_product_view_post(self):
        """
        Test successful product view
        """
        response = self.app.post("/view/60c30bdc8c137a1d611addaf")
        self.assertEqual(response.status_code, 200)
        self.assertIn("digestives", str(response.data))

    def test_get_product_id(self):
        """
        Test get product id
        """
        result = product_get_id("digestives")
        self.assertIsNotNone(result)
        self.assertEqual(result, ObjectId("60c30bdc8c137a1d611addaf"))

    def test_get_product_name(self):
        """
        Test get product name
        """
        result = product_get_name(ObjectId("60c30bdc8c137a1d611addaf"))
        self.assertIsNotNone(result)
        self.assertEqual(result, "digestives")

    def test_product_get_search_dict(self):
        """
        Test product process get search dictionary
        """
        result = product_get_search_dict(
            "digestives", ObjectId("609e4a13011739b2627fd835"),
            [ObjectId("609e499b011739b2627fd82e")])
        print(result)
        self.assertIsNotNone(result)
        self.assertEqual(result, {
            "$text": {"$search": "digestives"},
            "category_id": ObjectId("609e4a13011739b2627fd835"),
            "free_from_allergens": {
                "$all": [ObjectId("609e499b011739b2627fd82e")]}})

    def test_product_process_search_results(self):
        """
        Test product process search results
        """
        from database import mongo
        search_dict = product_get_search_dict(
            "digestives", ObjectId("609e4a13011739b2627fd835"),
            [ObjectId("609e499b011739b2627fd82e")])
        products = mongo.db.products.find(search_dict)
        result = product_process_search_results(products)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
