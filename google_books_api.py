#!/usr/bin/python3
# #Google BooksでAPIを叩く
import requests as req
import sys

ISBN = sys.argv[1]
response = req.get(
    'https://www.googleapis.com/books/v1/volumes',
    params={
        "q": "isbn=" + str(ISBN)
    })
BookInfo = dict(response.json()).get("items")[0]
#BookTitle = BookInfo["title"]
#BookAuthor = BookInfo["authors"][0]
print(BookInfo)