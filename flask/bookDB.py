#!/usr/bin/python3
import requests as req
from flask import Flask
from flask_pymongo import PyMongo
import sys
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)

req.packages.urllib3.disable_warnings()
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


def searchNDL(query):
    if str.isdecimal(query) is True and (len(query) == 10 or len(query) == 13):
        url = 'https://iss.ndl.go.jp/api/opensearch?' \
            + 'isbn=' + str(query)
    else:
        count = 3
        url = 'https://iss.ndl.go.jp/api/opensearch?' \
            + 'cnt=' + str(count) + '&' \
            + 'title=' + str(query)
    res = req.get(url, verify=False)
    res = BeautifulSoup(res.content, 'lxml', from_encoding='uft-8')
    res = res.channel.find('item')


def bookdb_update(query):
    res = searchNDL(query)
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


def bookdb(isbn):
    if isbn is None:
        data = 'None'
    else:  # 書籍情報があるか(MongoDB -> NDL)
        data = mongo.db.bookdb.find_one({'isbn': isbn})
        if data is None and bookdb_update(isbn) is None:
            data = 'None'  # NDLでも見つからない場合
        else:
            data = mongo.db.bookdb.find_one({'isbn': isbn})
    return data


if __name__ == "__main__":
    isbn = sys.argv[1]
    print(bookdb(isbn))
