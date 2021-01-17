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


def isISBN(query):
    if str.isdecimal(query) is True and (len(query) == 10 or len(query) == 13):
        return True
    else:
        return False


def isnone_or_bs4(found_object, defalt_value=""):
    return defalt_value if found_object is None else found_object.text


def searchNDL(query, stringsearch=False, count=1):
    query = str(query)
    if isISBN(query) is False or stringsearch is True:
        url = 'https://iss.ndl.go.jp/api/opensearch?' \
            + 'cnt=' + str(count) + '&' \
            + 'title=' + str(query)
        res = req.get(url, verify=False)
        res = BeautifulSoup(res.content, 'lxml').channel.find_all('item')
        # tmp = []
        # for i in range(count):
        #     tmp.append(res.channel.find_all('item'))
        # res = tmp  # type(res) == list

    elif isISBN(query) is True:
        url = 'https://iss.ndl.go.jp/api/opensearch?' \
            + 'isbn=' + str(query)
        res = req.get(url, verify=False)
        # type(res) == dict
        res = BeautifulSoup(res.content, 'lxml',
                            from_encoding='uft-8').channel.find('item')
    else:
        res = None
    return res


def bookdb_update(query, skipsearch=False):
    res = searchNDL(query)
    if type(res) == list:
        return None

    if res is not None or skipsearch:
        title = isnone_or_bs4(res.find('dc:title'))
        author = isnone_or_bs4(res.find('dc:creator'))
        publisher = isnone_or_bs4(res.find('dc:publisher'))
        isbn = isnone_or_bs4(res.find('dc:identifier'))
        volume = isnone_or_bs4(res.find('dcndl:volume'),
                               defalt_value='1')  # 本により巻数記載の有無が異なる
        series = isnone_or_bs4(res.find('dcndl:seriestitle'))
        # ---
        permalink = isnone_or_bs4(res.find('guid'))

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


def bookdb(query):
    if query is None:
        # data = 'query is None'
        data = None
    elif isISBN(query) is not True:
        data = None
    else:  # 書籍情報があるか(MongoDB -> NDL)
        data = mongo.db.bookdb.find_one({'isbn': query})
        if data is None and bookdb_update(query) is None:
            data = None  # NDLでも見つからない場合
            # data = 'data is None'
        else:
            data = mongo.db.bookdb.find_one({'isbn': query})
    return data


if __name__ == "__main__":
    q = sys.argv[1]
    print(searchNDL(q)[0].find('dc:title').text)  # for debug
