#!/usr/bin/python3
from flask import Flask
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)


def recordStatus(user_id, isbn, status):
    record = mongo.db.records.find_one_and_update(
        {'_id': ObjectId(oid=user_id), 'isbn': isbn},
        {"$set": {'status': status}},
        upsert=True
    )
    return record
