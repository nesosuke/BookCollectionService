#!/usr/bin/python3
from flask import Flask, render_template, request, session, jsonify, abort
import json
from flask_pymongo import PyMongo
import modules
app = Flask(__name__)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)

@app.route('/')
def toppage():
    return render_template('index.html')

@app.route('/book/<isbn>', methods=['GET'])
def show_bookinfo(isbn):
    if request.method == 'GET':
        bookinfo = modules.find_bookinfo_byisbn(isbn)
        del bookinfo['_id'] # json
        bookinfo = jsonify(bookinfo)
        return bookinfo


@app.route('/search', methods=['GET'])
def find_and_show_bookinfo():
    query = request.args.get('q')
    if query is None:
        return abort(404)
    else:
        bookinfo = modules.find_bookinfo_bytitle(query)  # list
        if len(bookinfo) == 0:
            return abort(404)
        else:
            return jsonify(bookinfo)


@app.route('/status', methods=['GET'])
def get_status():
    uid = str(request.args.get('uid'))  # flaskのログインセッションID からとる
    isbn = str(request.args.get('isbn'))
    reading_status = modules.get_reading_status(uid, isbn)
    if reading_status is None:
        return abort(404)
    else:
        del reading_status['_id']
        return reading_status


@app.route('/status', methods=['POST'])
def update_status():
    uid = str(request.args.get('uid'))  # flaskのログインセッションID からとる
    isbn = str(request.args.get('isbn'))
    status = str(request.args.get('status'))
    res = mongo.db.statusdb.find_one_and_update(
        {'uid': uid, 'isbn': isbn},
        {
            "$set":
                {
                    'status': status,
                },
        },
        upsert=True
    )
    res = mongo.db.statusdb.find_one({'uid': uid, 'isbn': isbn})
    del res['_id']  # json
    return res


if __name__ == "__main__":
    app.run(debug=True)
