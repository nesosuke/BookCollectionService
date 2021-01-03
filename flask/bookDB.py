#!/usr/bin/python3
import flask
from flask import render_template, request
from flask_pymongo import PyMongo
import ndlapi

app = flask.Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)


def bookdb_update(isbn):
    res = ndlapi.searchByISBN(isbn)

    if res is None:
        return False

    else:
        title = res.find('dc:title').text
        author = res.find('dc:creator').text
        publisher = res.find('dc:publisher').text

        mongo.db.bookdb.find_one_and_update(
            {'isbn': isbn},
            {
                "$setOnInsert":
                {
                    "title": title,
                    "author": author,
                    "publisher": publisher,
                },
            },
            upsert=True
        )
        return True


@app.route('/book', methods=['GET'])
def bookdb():
    isbn = request.args.get('isbn')
    isExistinDB = mongo.db.bookdb.find_one({'isbn': isbn})

    if isExistinDB is None:
        if bookdb_update(isbn) is False:
            isFound = False
            return isFound
    else:
        isFound = True
    return render_template(
        'bookinfo.html',
        isFound=str(isFound),
        isbn=mongo.db.bookdb.find_one({'isbn': isbn})['isbn'],
        title=mongo.db.bookdb.find_one({'isbn': isbn})['title'],
        author=mongo.db.bookdb.find_one({'isbn': isbn})['author'],
        publisher=mongo.db.bookdb.find_one({'isbn': isbn})['publisher'],
    )


if __name__ == "__main__":
    app.run(debug=True)
