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


def isISBN(query):  # ISBN10/13かどうか判定する
    if len(str(query)) == 10 or len(str(query)) == 13:
        return str.isdecimal(query)
    else:
        return False


def isnone_or_bs4(found_object, defalt_value=""):  # None/bs4の判定
    return defalt_value if found_object is None else found_object.text


def get_bookinfo_byISBN(isbn):
    isbn = str(isbn)
    bookinfo = mongo.db.bookdb.find_one({'isbn': isbn})

    if bookinfo is None:
        res = update_bookdb_byisbn(isbn)
        bookinfo = mongo.db.bookdb.find_one({'isbn': isbn})
    return bookinfo


def 文献情報を自前DBから検索するして一覧にするやつ(タイトル):
    pass


def search_fromNDL_byisbn(isbn):
    url = 'https://iss.ndl.go.jp/api/opensearch?' + 'isbn=' + str(isbn)
    res = req.get(url, verify=False)
    bookinfo = BeautifulSoup(
        res.content, 'lxml', from_encoding='utf-8').channel.find('item')  # dict
    return bookinfo


def search_fromNDL_bytitle(title):
    url = 'https://iss.ndl.go.jp/api/opensearch?' \
        + 'cnt=' + str(10) + '&' \
        + 'title=' + str(title)
    res = req.get(url, verify=False)
    reslist = BeautifulSoup(
        res.content, 'lxml').channel.find_all('item')  # list

    bookinfolist = []
    for res in reslist:
        isbn = isnone_or_bs4(res.find('dc:identifier'))
        title = isnone_or_bs4(res.find('dc:title'))
        author = isnone_or_bs4(res.find('dc:creator'))
        publisher = isnone_or_bs4(res.find('dc:publisher'))
        volume = isnone_or_bs4(res.find('dcndl:volume'),
                               defalt_value='1')  # 本により巻数記載の有無が異なる
        series = isnone_or_bs4(res.find('dcndl:seriestitle'))
        permalink = isnone_or_bs4(res.find('guid'))

        bookinfolist.append({'isbn': isbn,
                             'title': title,
                             'author': author,
                             'publisher': publisher,
                             'volume': volume,
                             'series': series,
                             'permalink': permalink})
    return bookinfolist  # list


def update_bookdb_byisbn(isbn):
    bookinfo = search_fromNDL_byisbn(isbn)

    title = isnone_or_bs4(bookinfo.find('dc:title'))
    author = isnone_or_bs4(bookinfo.find('dc:creator'))
    publisher = isnone_or_bs4(bookinfo.find('dc:publisher'))
    volume = isnone_or_bs4(bookinfo.find('dcndl:volume'),
                           defalt_value='1')  # 本により巻数記載の有無が異なる
    series = isnone_or_bs4(bookinfo.find('dcndl:seriestitle'))
    permalink = isnone_or_bs4(bookinfo.find('guid'))

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
    return bookinfo


def update_bookdb_bytitle(title):
    bookinfolist = search_fromNDL_bytitle(str(title))
    for i in range(len(bookinfolist)):
        mongo.db.bookdb.find_one_and_update(
            {'isbn': bookinfolist[i]['isbn']},
            {
                "$set":
                {
                    "title": bookinfolist[i]['title'],
                    "volume": bookinfolist[i]['volume'],
                    "author": bookinfolist[i]['author'],
                    "series": bookinfolist[i]['series'],
                    "publisher": bookinfolist[i]['publisher'],
                    "permalink": bookinfolist[i]['permalink'],
                },
            },
            upsert=True
        )
    return bookinfolist


def 読了状態を格納する(uid, isbn, ステータス):
    pass


def 読了状態を持ってくる(uid, isbn):
    pass


def 読んだ一覧を持ってくる(uid):
    pass
