#!/usr/bin/python3
import requests as req
import types
import sys

def search(isbn):
    try:
        json = req.get('https://api.openbd.jp/v1/get?isbn=' + str(isbn)).json()
        Result = json[0].get('summary')
    except:    
        Result = "Error"
    return Result


if __name__ == '__main__':
    isbn = sys.argv[1]
    BookInfo = search(isbn)
    print(BookInfo)
