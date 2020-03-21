#!/usr/bin/python3
# #Google BooksでAPIを叩く
import requests as req
import sys

ISBN = sys.argv[1]
response = req.get('https://api.openbd.jp/v1/get?isbn=' + str(ISBN)).json()[0]
BookInfo = response.get("summary")
Title = BookInfo.get("title")
Author = BookInfo.get("author")
Publisher = BookInfo.get("publisher")
Published_at = BookInfo.get("pubdate")
Cover = BookInfo.get("cover")

print(Title)
print(Author)
print(Publisher)
print(Published_at)
print(Cover)