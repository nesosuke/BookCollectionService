#!/usr/bin/python3
import flask
from flask import render_template, request, abort
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
        if res.find('dcndl:volume') is not None:  # 本により巻数記載の有無が異なる
            volume = res.find('dcndl:volume').text
        else:
            volume = '1'
        if res.find('dcndl:seriestitle') is not None:
            series = res.find('dcndl:seriestitle').text
        else:
            series = 'None'
        permalink = res.find('guid').text

        mongo.db.bookdb.find_one_and_update(
            {'isbn': isbn},
            {
                "$set":
                {
                    "title": title,
                    "volume": volume,
                    "author": author,
                    "series": series,
                    "publisher": publisher,
                    "permalink": permalink,
                },
            },
            upsert=True
        )
    return res


@app.route('/book', methods=['GET'])
def bookdb():
    isbn = request.args.get('q')
    if isbn is None:
        return 'missing ISBN'
    else:  # 書籍情報があるか(MongoDB -> NDL)
        data = mongo.db.bookdb.find_one({'isbn': isbn})
        if data is None:
            if bookdb_update(isbn) is None:
                abort(404)  # NDLでも見つからない場合
        data = mongo.db.bookdb.find_one({'isbn': isbn})
        title = data['title']
        author = data['author']
        publisher = data['publisher']
        series = data['series']
        volume = data['volume']
        permalink = data['permalink']
        return render_template(
            'bookinfo.html',
            isbn=isbn,
            title=title,
            author=author,
            publisher=publisher,
            series=series,
            volume=volume,
            permalink=permalink,
        )


if __name__ == "__main__":
    app.run(debug=True)
