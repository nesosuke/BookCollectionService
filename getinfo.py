#!/usr/bin/python3
import requests as req
import sys

def search(isbn):
    BookInfo = req.get('https://api.openbd.jp/v1/get?isbn=' + str(isbn)).json()[0].get('summary')
    return BookInfo

if __name__ == '__main__':
    isbn = sys.argv[1]
    BookInfo = search(isbn)
    print(BookInfo)
