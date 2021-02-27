#!/usr/bin/python3
import requests as req
from flask import Flask
from bs4 import BeautifulSoup
from flask_pymongo import PyMongo

app = Flask(__name__)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)

req.packages.urllib3.disable_warnings()
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


def isISBN13(query):  # ISBN13かどうか判定する
    if len(str(query)) == 13:
        return str.isdecimal(query)
    else:
        return False


def check_none_or_bs4(found_object, default_value=""):  # None/bs4の判定
    return default_value if found_object is None else found_object.text


def 文献情報を自前DBから検索するして一覧にするやつ(タイトル):
    pass


def find_bookinfo_byisbn(isbn):  # Nonetype or dict
    # ISBNがユニークな値であると想定
    # bookDBからISBNで検索，無ければNDL叩く
    isbn = str(isbn)

    bookinfo_inbookDB = mongo.db.bookdb.find_one({'isbn': isbn})
    if bookinfo_inbookDB is not None:
        return bookinfo_inbookDB
    else:
        url = 'https://iss.ndl.go.jp/api/opensearch?' + 'isbn=' + isbn
        res = req.get(url, verify=False)
        bookinfo_fromNDL = BeautifulSoup(
            res.content, 'lxml', from_encoding='utf-8').channel.find('item')  # dict

        mongo.db.bookdb.find_one_and_update(
            {'isbn': isbn},
            {
                "$set":
                {
                    "title": check_none_or_bs4(bookinfo_fromNDL.find('dc:title')),
                    "author": check_none_or_bs4(bookinfo_fromNDL.find('dc:creator')),
                    "series":  check_none_or_bs4(bookinfo_fromNDL.find('dcndl:seriestitle')),
                    "volume":  check_none_or_bs4(bookinfo_fromNDL.find('dcndl:volume'), default_value='1'),
                    "publisher": check_none_or_bs4(bookinfo_fromNDL.find('dc:publisher')),
                    "permalink": check_none_or_bs4(bookinfo_fromNDL.find('guid')),
                },
            },
            upsert=True
        )
        return bookinfo_fromNDL


def find_bookinfo_bytitle(title):  # list
    # 現状bookDBから検索できないのでNDL APIでタイトル検索．
    # ｢bookDBで探して，無ければNDLを叩き直す｣挙動にしたい．

    url = 'https://iss.ndl.go.jp/api/opensearch?' \
        + 'cnt=' + str(20) + '&' \
        + 'title=' + str(title)
    res = req.get(url, verify=False)
    reslist = BeautifulSoup(
        res.content, 'lxml').channel.find_all('item')  # list

    bookinfolist_fromNDL = []
    for res in reslist:
        bookinfolist_fromNDL.append({'isbn': check_none_or_bs4(res.find('dc:identifier')),
                                     'title': check_none_or_bs4(res.find('dc:title')),
                                     'author': check_none_or_bs4(res.find('dc:creator')),
                                     'series': check_none_or_bs4(res.find('dcndl:seriestitle')),
                                     'volume': check_none_or_bs4(res.find('dcndl:volume')),
                                     'publisher': check_none_or_bs4(res.find('dc:publisher')),
                                     'permalink': check_none_or_bs4(res.find('guid'))
                                     })  # list

    # 検索結果をISBN検索時に再利用できるようにbookDBに格納
    for i in range(len(bookinfolist_fromNDL)):
        mongo.db.bookdb.find_one_and_update(
            {'isbn': bookinfolist_fromNDL[i]['isbn']},
            {
                "$set":
                {
                    "title": bookinfolist_fromNDL[i]['title'],
                    "author": bookinfolist_fromNDL[i]['author'],
                    "series": bookinfolist_fromNDL[i]['series'],
                    "volume": bookinfolist_fromNDL[i]['volume'],
                    "publisher": bookinfolist_fromNDL[i]['publisher'],
                    "permalink": bookinfolist_fromNDL[i]['permalink'],
                },
            },
            upsert=True
        )
    return bookinfolist_fromNDL


def update_reading_status(uid, isbn, status):
    tmp = mongo.db.statusdb.find_one_and_update(
        {'uid': uid, 'isbn': isbn},
        {
            "$set":
                {
                    'status': status,
                },
        },
        upsert=True
    )
    return tmp


def get_reading_status(uid, isbn): #get_status
    status_data=mongo.db.statusdb.find_one(
        {'uid':uid, 'isbn':isbn}
    )
    return status_data['status']

def 読んだ一覧を持ってくる(uid):
    pass
