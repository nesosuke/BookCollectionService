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
def show_bookinfo():
    isbn = request.args.get('q')
    bookinfo = modules.find_bookinfo_byisbn(isbn)  # dict
    return render_template('bookinfo.html',
                       bookinfo = bookinfo)


@ app.route('/search', methods = ['GET'])
def find_and_show_bookinfo():
    query=request.args.get('q')
    if query is None:
        return render_template('search.html')
    elif modules.isISBN13(query):
        bookinfo=[modules.find_bookinfo_byisbn(query)]  # list
    else:
        bookinfo=modules.find_bookinfo_bytitle(query)  # list

    return render_template('result.html',
                           bookinfo = bookinfo)


if __name__ == "__main__":
    app.run(debug = True)
