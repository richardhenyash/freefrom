#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FreeFrom Environment Python module
Version 1.1.1
"""
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault(
    "SECRET_KEY", "<your_secret_key>")
os.environ.setdefault(
    "MONGO_URI", (
        "mongodb+srv://<username>:<password>@<database>" +
        ".z6xjx.mongodb.net/<database>?retryWrites=true&w=majority"))
os.environ.setdefault("MONGO_DBNAME", "<database>")
os.environ.setdefault("MAIL_USERNAME", "<email_address>")
os.environ.setdefault("MAIL_PASSWORD", "<email_password>")
