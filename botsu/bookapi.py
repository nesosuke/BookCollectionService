#!/usr/bin/python3
import requests as req
import sys

if __name__ == '__main__':
    ISBN = sys.argv[1]
    response = req.get('https://api.openbd.jp/v1/get?isbn=' + str(ISBN)).json()[0]
    BookInfo = response.get("summary")
    return BookInfo