#!/usr/bin/python3
from flask import Flask, render_template, request, session, jsonify
import json
from flask_pymongo import PyMongo
import modules
app = Flask(__name__)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)


@app.route('/')
def toppage():
    return render_template('index.html')


@app.route('/book', methods=['GET'])
def show_bookinfo():
    if request.method == 'GET':
        isbn = request.args.get('q')
        bookinfo = modules.find_bookinfo_byisbn(isbn)
        del bookinfo['_id'] # json
        bookinfo = jsonify(bookinfo)
        return render_template('bookinfo.html',
                               bookinfo=bookinfo)
        # return bookinfo

@app.route('/search', methods=['GET'])
def find_and_show_bookinfo():
    query = request.args.get('q')
    if query is None:
        return render_template('search.html')
    elif modules.isISBN13(query):
        bookinfo = [modules.find_bookinfo_byisbn(query)]  # list
    else:
        bookinfo = modules.find_bookinfo_bytitle(query)  # list

    return render_template('result.html',
                           bookinfo=bookinfo)
    # return str(bookinfo)

@app.route('/status', methods=['POST'])
def record_status():
    uid = 'test'  # flaskのログインセッションID からとる
    isbn = str(request.form.get('isbn'))
    status = str(request.form.get('status'))
    t = modules.update_reading_status(uid, isbn, status)
    del t['_id'] # json

    return t

@app.route('/status', methods=['GET'])
def get_status():
    uid = 'test'  # flaskのログインセッションID からとる
    isbn = str(request.args.get('isbn'))
    reading_status = modules.get_reading_status(uid, isbn)
    return reading_status


if __name__ == "__main__":
    app.run(debug=True)
