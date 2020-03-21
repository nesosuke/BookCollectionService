#!/usr/bin/python3
# #Google BooksでAPIを叩く
import requests as req
import sys

ISBN = sys.argv[1]
response = req.get('https://api.openbd.jp/v1/get?isbn=' + str(ISBN)).json()
BookInfo = response[0].get("onix")
BookTitle = BookInfo.get("DescriptiveDetail").get("TitleDetail").get("TitleElement").get("TitleText").get("content")
#BookAuthor = BookInfo["authors"][0]
print(BookTitle)