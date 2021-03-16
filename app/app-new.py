#!/usr/bin/python3
from flask import Flask, render_template, request, session, jsonify, abort
import json
import requests as req
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup
app = Flask(__name__)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)


req.packages.urllib3.disable_warnings()
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

def bs4totext(bs4object, default_value=""):
    if bs4object is None:
        return default_value
    else:
        return bs4object.text


def find_bookinfo(isbn, update=False):  # json
    bookinfo = mongo.db.bookdb.find_one({'isbn': isbn})
    if bookinfo is None or update:  # NDLから更新する
        url = 'https://iss.ndl.go.jp/api/opensearch?' + 'isbn=' + isbn
        res = BeautifulSoup(req.get(url, verify=False).content,
                            'lxml', from_encoding='utf-8').channel.find('item')
        # if res is None:  # NDLにも無い
        #     return None
        # else:
            # res = res.find('item')

        title = bs4totext(res.find('dc:title'))
        author = bs4totext(res.find('dc:creator'))
        series = bs4totext(res.find('dcndl:seriestitle'))
        volume = bs4totext(res.find('dcndl:volume'))
        publisher = bs4totext(res.find('dc:publisher'))
        permalink = bs4totext(res.find('guid'))

        bookinfo = mongo.db.bookdb.find_one_and_update(
            {'isbn': isbn},
            {
                "$set":
                {
                    "title": title,
                    "author": author,
                    "series": series,
                    "volume": volume,
                    "publisher": publisher,
                    "permalink": permalink,
                },
            },
            upsert=True
        )

    del bookinfo['_id']
    return jsonify(bookinfo)


def find_bookinfo_bytitle(title):  # json(list)
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


@app.route('/book/<isbn>', methods=['GET'])
def show_bookinfo(isbn):
    return find_bookinfo(isbn, update=False)


@app.route('/book/<isbn>/update', methods=['GET'])
def update_bookinfo(isbn):
    return find_bookinfo(isbn, update=True)



if __name__ == "__main__":
    app.run(debug=True)
