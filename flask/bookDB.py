#!/usr/bin/python3
import flask
from flask import render_template, request
from flask_pymongo import PyMongo
import ndlapi

app = flask.Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)


def bookdb_update(query):
    res = ndlapi.searchNDL(query)

    if res is not None:
        title = res.find('dc:title').text
        author = res.find('dc:creator').text
        publisher = res.find('dc:publisher').text
        isbn = res.find('dc:identifier').text
        volume = res.find('dcndl:volume').text
        permalink = res.find('guid').text

        mongo.db.bookdb.find_one_and_update(
            {'isbn': isbn},
            {
                "$setOnInsert":
                {
                    "title": title,
                    "volume": volume,
                    "author": author,
                    "publisher": publisher,
                    "permalink": permalink,
                },
            },
            upsert=True
        )
        return True


@app.route('/book', methods=['GET'])
def bookdb():
    isbn = request.args.get('q')
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
        volume=mongo.db.bookdb.find_one({'isbn': isbn})['volume'],
        permalink=mongo.db.bookdb.find_one({'isbn': isbn})['permalink'],
    )


if __name__ == "__main__":
    app.run(debug=True)
