#!/usr/bin/python3
import requests as req
import flask
from flask import render_template, request, session
import flask_login
from flask_pymongo import PyMongo, ObjectId
from bs4 import BeautifulSoup


app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)

# memo: Noneを返すようにすること


def isISBN(query):  # ISBN10/13かどうか判定する
    query_length = len(str(query))
    if str.isdecimal(query) is True and query_length == 10 or query_length == 13:
        return True
    else:
        return False


def isnone_or_bs4(found_object, defalt_value=""):  # None/bs4の判定
    return defalt_value if found_object is None else found_object.text


def get_bookinfo_fromDB(isbn):  # 自前DBから書籍情報を検索
    if isbn is None or isISBN(isbn) is False:
        return None

    bookinfo = mongo.db.bookinfo.find_one({'isbn': isbn})
    return bookinfo


def search_fromNDL_byISBN(isbn):  # NDLから探す -> dict
    if isISBN(isbn) is False:
        return None

    url = 'https://iss.ndl.go.jp/api/opensearch?' + 'isbn=' + str(isbn)
    res = BeautifulSoup(res.content, 'lxml',
                        from_encoding='uft-8').channel.find('item')  # dict
    return res


def search_fromNDL_byTitle(query, stringsearch=False, count=1):  # NDLからタイトルで検索() -> list
    query = str(query)
    if isISBN(query) is False or stringsearch is True:
        url = 'https://iss.ndl.go.jp/api/opensearch?' \
            + 'cnt=' + str(count) + '&' \
            + 'title=' + str(query)
        res = req.get(url, verify=False)
        res = BeautifulSoup(
            res.content, 'lxml').channel.find_all('item')  # list


def update_bookinfoDB(isbn):  # 書籍情報DBを更新する
    bookinfo = search_fromNDL_byISBN(isbn)
    if bookinfo is None:
        return None
    title = isnone_or_bs4(res.find('dc:title'))
    author = isnone_or_bs4(res.find('dc:creator'))
    publisher = isnone_or_bs4(res.find('dc:publisher'))
    isbn = isnone_or_bs4(res.find('dc:identifier'))
    volume = isnone_or_bs4(res.find('dcndl:volume'),
                           defalt_value='1')  # 本により巻数記載の有無が異なる
    series = isnone_or_bs4(res.find('dcndl:seriestitle'))
    permalink = isnone_or_bs4(res.find('guid'))

    mongo.db.bookinfo.find_one_and_update(
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

    return True


def update_status(uid, isbn, status='unread'):  # ステータスを更新(unread/read/reading/wish)
   if status != 'unread' or 'read' or 'reading' or 'wish':
        return None

    mongo.db.statuses.find_one_and_update(
        {'uid': uid, 'isbn': isbn},
        {
            "$set":
                {
                    'uid': uid,
                    'isbn': isbn,
                    'status': status,
                },
        },
        upsert=True
    )


def get_status_fromDB(uid, isbn):  # 読了状態を探す
    res = mongo.db.statuses.find_one({'isbn': isbn, 'uid': uid})  # uidは仮
    if res is not None:
        res = res['status']
    return res
