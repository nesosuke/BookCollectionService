#!/usr/bin/python3
from flask import Flask, render_template, request, session
import json
from flask_pymongo import PyMongo
import modules
app = Flask(__name__)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)


@app.route('/book')
isbn = request.args.get('q')
bookinfo = modules.get_bookinfo_byISBN(isbn)
return render_template('result.html',
                       result=bookinfo)

# @app.route('search') # DBからElasticSearch叩くやつできてからにする
# query = request.args.get('q')
# bookinfo= modules.update_bookdb_bytitle(query)
# return render_template('result.html',
# result=bookinfo)